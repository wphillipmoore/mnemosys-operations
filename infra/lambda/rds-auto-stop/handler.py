"""Lambda function to auto-stop RDS instances restarted by AWS.

AWS automatically restarts stopped RDS instances after 7 days. This function
is triggered by EventBridge when an RDS instance enters the 'available' state,
and immediately stops it again if it matches one of the allowed instance
identifiers.
"""

import logging

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ALLOWED_INSTANCES = frozenset({
    "mnemosys-postgres",
    "mnemosys-test-postgres",
})

rds = boto3.client("rds")


def handler(event, context):
    detail = event.get("detail", {})
    instance_id = detail.get("SourceIdentifier") or detail.get("requestParameters", {}).get("dBInstanceIdentifier")

    if not instance_id:
        logger.warning("No instance identifier found in event: %s", event)
        return {"status": "skipped", "reason": "no instance identifier"}

    if instance_id not in ALLOWED_INSTANCES:
        logger.warning("Instance %s not in allowed list, skipping", instance_id)
        return {"status": "skipped", "reason": "not in allowed list"}

    logger.info("Stopping RDS instance: %s", instance_id)
    try:
        rds.stop_db_instance(DBInstanceIdentifier=instance_id)
        logger.info("Stop command sent for %s", instance_id)
        return {"status": "stopped", "instance": instance_id}
    except rds.exceptions.InvalidDBInstanceStateFault:
        logger.info("Instance %s is not in a stoppable state, skipping", instance_id)
        return {"status": "skipped", "reason": "not in stoppable state"}
