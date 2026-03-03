# RDS Auto-Stop Lambda + EventBridge

**Status**: Active
**Date**: 2026-03-03
**Last verified**: 2026-03-03

## Table of Contents

- [Purpose](#purpose)
- [Problem](#problem)
- [Architecture](#architecture)
- [AWS Resources](#aws-resources)
- [Implementation](#implementation)
  - [1) IAM Role](#1-iam-role)
  - [2) CloudWatch Log Group](#2-cloudwatch-log-group)
  - [3) Lambda Function](#3-lambda-function)
  - [4) EventBridge Rule](#4-eventbridge-rule)
  - [5) Connect Rule to Lambda](#5-connect-rule-to-lambda)
- [Verification](#verification)
- [Teardown](#teardown)

## Purpose

Automatically re-stop RDS instances that AWS restarts after the 7-day stopped-instance
limit, preventing unexpected charges while the project is on hiatus.

## Problem

AWS automatically restarts any stopped RDS instance after 7 days.
Both MNEMOSYS RDS instances (`mnemosys-postgres` and
`mnemosys-test-postgres`) have been stopped to save
costs. Without monitoring, these instances would silently restart and accrue charges.

## Architecture

```text
RDS instance starts
  → EventBridge rule matches event
  → Lambda invoked
  → rds:StopDBInstance
```

- **EventBridge** watches for `RDS DB Instance Event` with message `DB instance started`
  scoped to the two specific instance identifiers.
- **Lambda** receives the event, validates the instance identifier against an allowlist,
  and calls `stop_db_instance`.
- **CloudWatch Logs** capture Lambda execution output for auditing.

## AWS Resources

| Resource | Name / ARN |
|----------|-----------|
| IAM Role | `mnemosys-rds-auto-stop` |
| Lambda Function | `mnemosys-rds-auto-stop` |
| EventBridge Rule | `mnemosys-rds-auto-start-trigger` |
| CloudWatch Log Group | `/mnemosys/lambda/rds-auto-stop` |
| Account | `959713283130` |
| Region | `us-east-2` |

## Implementation

All commands use `AWS_PROFILE=mnemosys-admin` and `AWS_REGION=us-east-2`.

### 1) IAM Role

Trust policy for `lambda.amazonaws.com`:

```bash
aws iam create-role \
  --role-name mnemosys-rds-auto-stop \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Principal": {"Service": "lambda.amazonaws.com"},
      "Action": "sts:AssumeRole"
    }]
  }' \
  --description "Allows Lambda to stop RDS instances that AWS auto-restarts"
```

Inline policy scoped to the two instances:

```bash
aws iam put-role-policy \
  --role-name mnemosys-rds-auto-stop \
  --policy-name rds-stop-instances \
  --policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Action": ["rds:StopDBInstance", "rds:DescribeDBInstances"],
      "Resource": [
        "arn:aws:rds:us-east-2:959713283130:db:mnemosys-postgres",
        "arn:aws:rds:us-east-2:959713283130:db:mnemosys-test-postgres"
      ]
    }]
  }'
```

Managed policy for CloudWatch Logs access:

```bash
aws iam attach-role-policy \
  --role-name mnemosys-rds-auto-stop \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
```

### 2) CloudWatch Log Group

```bash
aws logs create-log-group \
  --log-group-name /mnemosys/lambda/rds-auto-stop

aws logs put-retention-policy \
  --log-group-name /mnemosys/lambda/rds-auto-stop \
  --retention-in-days 30
```

### 3) Lambda Function

Source code: `infra/lambda/rds-auto-stop/handler.py`

Package and deploy:

```bash
cd infra/lambda/rds-auto-stop
zip -j /tmp/rds-auto-stop.zip handler.py

aws lambda create-function \
  --function-name mnemosys-rds-auto-stop \
  --runtime python3.13 \
  --role arn:aws:iam::959713283130:role/mnemosys-rds-auto-stop \
  --handler handler.handler \
  --zip-file fileb:///tmp/rds-auto-stop.zip \
  --timeout 30 \
  --memory-size 128 \
  --logging-config LogGroup=/mnemosys/lambda/rds-auto-stop,LogFormat=Text \
  --description "Auto-stop RDS instances that AWS restarts after 7-day stop limit"
```

### 4) EventBridge Rule

Event pattern matches RDS instance start events for the two specific instances:

```bash
aws events put-rule \
  --name mnemosys-rds-auto-start-trigger \
  --event-pattern '{
    "source": ["aws.rds"],
    "detail-type": ["RDS DB Instance Event"],
    "detail": {
      "SourceIdentifier": ["mnemosys-postgres", "mnemosys-test-postgres"],
      "EventCategories": ["notification"],
      "Message": ["DB instance started"]
    }
  }' \
  --state ENABLED \
  --description "Fires when mnemosys RDS instances start"
```

### 5) Connect Rule to Lambda

Grant EventBridge permission to invoke the Lambda:

```bash
aws lambda add-permission \
  --function-name mnemosys-rds-auto-stop \
  --statement-id eventbridge-rds-auto-start \
  --action lambda:InvokeFunction \
  --principal events.amazonaws.com \
  --source-arn arn:aws:events:us-east-2:959713283130:rule/mnemosys-rds-auto-start-trigger
```

Add Lambda as the rule target:

```bash
aws events put-targets \
  --rule mnemosys-rds-auto-start-trigger \
  --targets "Id=rds-auto-stop-lambda,Arn=arn:aws:lambda:us-east-2:959713283130:function:mnemosys-rds-auto-stop"
```

## Verification

Confirm the rule is enabled:

```bash
aws events describe-rule --name mnemosys-rds-auto-start-trigger
```

Confirm the Lambda exists and is active:

```bash
aws lambda get-function --function-name mnemosys-rds-auto-stop \
  --query 'Configuration.{FunctionName:FunctionName,Runtime:Runtime,State:State}'
```

Test invocation (instance is already stopped, so it returns "not in stoppable state"):

```bash
aws lambda invoke \
  --function-name mnemosys-rds-auto-stop \
  --payload '{
    "detail-type": "RDS DB Instance Event",
    "source": "aws.rds",
    "detail": {
      "SourceIdentifier": "mnemosys-postgres",
      "EventCategories": ["notification"],
      "Message": "DB instance started"
    }
  }' \
  --cli-binary-format raw-in-base64-out \
  /tmp/lambda-output.json && cat /tmp/lambda-output.json
```

Check CloudWatch logs:

```bash
aws logs describe-log-streams \
  --log-group-name /mnemosys/lambda/rds-auto-stop \
  --order-by LastEventTime --descending --limit 1
```

## Teardown

When the project resumes and RDS instances should remain running, remove all resources
in reverse order:

```bash
export AWS_PROFILE=mnemosys-admin
export AWS_REGION=us-east-2

# 1. Remove EventBridge target
aws events remove-targets \
  --rule mnemosys-rds-auto-start-trigger \
  --ids rds-auto-stop-lambda

# 2. Delete EventBridge rule
aws events delete-rule \
  --name mnemosys-rds-auto-start-trigger

# 3. Delete Lambda function
aws lambda delete-function \
  --function-name mnemosys-rds-auto-stop

# 4. Delete CloudWatch log group
aws logs delete-log-group \
  --log-group-name /mnemosys/lambda/rds-auto-stop

# 5. Detach managed policy and delete inline policy
aws iam detach-role-policy \
  --role-name mnemosys-rds-auto-stop \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

aws iam delete-role-policy \
  --role-name mnemosys-rds-auto-stop \
  --policy-name rds-stop-instances

# 6. Delete IAM role
aws iam delete-role \
  --role-name mnemosys-rds-auto-stop
```
