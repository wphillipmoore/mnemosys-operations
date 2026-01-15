# Test/Production Environment Parity Plan (RDS + REST API)

**Status:** Completed (merged into `docs/aws/nonprod-rest-api-deploy-plan.md`)

This plan is consolidated into the nonprod deployment plan. Do not execute it
independently; use the consolidated plan instead.

## Table of Contents
- [Context](#context)
- [Goals](#goals)
- [Non-Goals](#non-goals)
- [Invariants](#invariants)
- [Current State (Assumed)](#current-state-assumed)
- [Target State](#target-state)
- [Plan (Step-by-Step)](#plan-step-by-step)
- [Validation](#validation)
- [Risks](#risks)
- [Open Questions](#open-questions)

## Context

The test environment must be a near-identical proxy for production. That requires
both the database and the REST API to run on the same infrastructure tier with
minimal configuration drift. To achieve this, we will promote the managed Postgres
instance used for development into a production-tier configuration and use that
pattern for the test database (release branch deployments). In parallel, the test
REST API service must run with production-like resiliency settings so the API and
database are evaluated together as a matched pair.

This plan builds on:
- `docs/aws/nonprod-rest-api-deploy-plan.md`
- `docs/aws/database-environment-setup.md`

## Goals

- Align test and production database infrastructure tiers.
- Align test and production REST API infrastructure tiers and resiliency settings.
- Document the production-grade AWS RDS and REST API configuration by applying it to test.
- Keep dev/test updates strictly pipeline-driven (no local credentials).
- Preserve "rebuild from scratch" and migration gate behavior.

## Non-Goals

- Full production cutover (main branch) and public-facing rollout.
- Multi-account or multi-region database strategy.
- Database sharding, read replicas, or cross-region replication.

## Invariants

- Test and production use the same engine version, parameter group, instance class,
  storage type, encryption, and backup policies.
- Test and production REST API services use the same deployment topology,
  health checks, scaling configuration, and failure handling defaults.
- Release branch drives test deployments; developers do not hold test credentials.
- Migration gate remains the only automated schema change path.
- Any drift between test and production must be intentional, documented, and minimal.
- Test database data is disposable during this proof-of-concept phase.

## Current State (Assumed)

- Nonprod RDS exists and is used by development/test deployments.
- Development database is on a non-production tier configuration.
- Test REST API is deployed but not configured for production-grade resiliency.
- Test database credentials are stored only in AWS (SSM/Secrets), not locally.

## Target State

- Test database runs on production-tier RDS configuration.
- Test REST API runs with production-grade resiliency configuration.
- Configuration parity with production is explicit and enforced.
- Development remains isolated from test (no shared credentials; no direct access).

## Plan (Step-by-Step)

1. Inventory current RDS configuration used by development/test:
   - Engine version, instance class, storage type, IOPS, encryption.
   - Parameter group, maintenance window, backup retention.
   - Security groups, subnet group, VPC placement.
2. Inventory current REST API configuration used by development/test:
   - ECS service desired count, autoscaling rules, health checks.
   - Deployment strategy, circuit breaker settings, and timeouts.
   - Task sizing, CPU/memory, and networking configuration.
3. Define the production-tier baseline:
   - Instance class and storage class sized for production.
   - Multi-AZ, backup retention, deletion protection, performance insights.
   - Parameter group settings required for production parity.
4. Define the production-tier REST API baseline:
   - Desired count and autoscaling targets for resiliency.
   - Health check configuration (ALB + container) and timeouts.
   - Deployment settings (minimum healthy percent, max percent).
5. Destroy and recreate the test database as a clean production-tier instance:
   - No data preservation required in the current proof-of-concept phase.
   - Apply instance class, storage, and parameter group changes at creation time.
   - Enforce backups, encryption, monitoring, deletion protection.
6. Update AWS secrets/SSM parameters for the test environment:
   - `/mnemosys/test/db/host`, `/mnemosys/test/db/port`, etc.
   - Confirm admin credentials are present and rotate if required.
7. Update REST API service configuration for test to match production baseline:
   - Apply scaling, health check, deployment, and resiliency settings.
   - Confirm task definitions and runtime configuration are aligned with prod.
8. Validate pipeline behavior:
   - Merge `develop` -> `release` and confirm the migration gate runs against the
     updated test database and succeeds.
   - Confirm application health checks succeed post-deploy.
9. Document the production-grade RDS and REST API configuration and parity rules.

## Validation

- Release pipeline deploys to test without manual database access.
- Alembic migration gate applies cleanly and logs expected output.
- RDS configuration matches the production-tier baseline.
- REST API service configuration matches the production-tier baseline.

## Risks

- Misconfigured parameter group or storage settings can cause downtime.
- REST API resiliency drift can hide production-only failure modes.
- Drift between test and production if parity rules are not enforced in docs.
- Instance recreation changes endpoints and requires secrets updates.

## Open Questions

- Is Multi-AZ required for test (to mirror production) or optional for cost?
- What are the exact production-tier parameters (instance class, storage size, IOPS)?
- What are the target REST API resiliency parameters (desired count, autoscaling thresholds)?
