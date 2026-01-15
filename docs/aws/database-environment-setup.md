# MNEMOSYS Database Environment Setup (Bootstrap)

## Table of Contents
- [Purpose](#purpose)
- [Environment Model](#environment-model)
- [Infrastructure Model (Bootstrap)](#infrastructure-model-bootstrap)
- [Naming Conventions](#naming-conventions)
- [Bootstrap Setup Steps (Non-Production RDS)](#bootstrap-setup-steps-non-production-rds)
  - [1) Allow local access (bootstrap only)](#1-allow-local-access-bootstrap-only)
  - [2) Connect as the RDS master user](#2-connect-as-the-rds-master-user)
  - [3) Create roles and set passwords](#3-create-roles-and-set-passwords)
  - [4) Create databases and isolate access](#4-create-databases-and-isolate-access)
  - [5) Grant schema access (sandbox/dev/test)](#5-grant-schema-access-sandboxdevtest)
  - [6) Local environment configuration (sandbox only)](#6-local-environment-configuration-sandbox-only)
- [Production Setup (Dedicated RDS)](#production-setup-dedicated-rds)
- [Bootstrap Exit (Lockdown)](#bootstrap-exit-lockdown)

## Purpose

This document captures the concrete, repeatable steps to provision the MNEMOSYS
databases and roles during the bootstrap phase. It is intended as an operational
record and as a future reference.

## Environment Model

There are four environments:

- **sandbox**: pre-PR testing for feature/bugfix/hotfix work
- **development**: API-only deployment of `develop`
- **test**: API-only deployment of `release`
- **production**: API-only deployment of `main`

## Infrastructure Model (Bootstrap)

- Single AWS account.
- One non-production RDS instance hosting `sandbox`, `development`, and `test`.
- A separate RDS instance for `production` (created before real user access).
- The non-prod RDS instance may be public during bootstrap with IP allowlisting.
- Only the `mnemosys-admin` IAM user is used for console/CLI access.

## Naming Conventions

Database names:

- `mnemosys_sandbox`
- `mnemosys_dev`
- `mnemosys_test`
- `mnemosys_prod`

Postgres roles (underscores only):

- `mnemosys_sandbox_admin`, `mnemosys_sandbox_user`
- `mnemosys_dev_admin`, `mnemosys_dev_user`
- `mnemosys_test_admin`, `mnemosys_test_user`
- `mnemosys_prod_admin`, `mnemosys_prod_user`

## Bootstrap Setup Steps (Non-Production RDS)

### 1) Allow local access (bootstrap only)

Restrict inbound to your IP:

```bash
export AWS_PROFILE=mnemosys-admin
export AWS_REGION=us-east-2
MYIP=$(curl -fsSL https://checkip.amazonaws.com)
aws ec2 authorize-security-group-ingress \
  --group-id <non-prod-sg-id> \
  --protocol tcp \
  --port 5432 \
  --cidr ${MYIP}/32
```

### 2) Connect as the RDS master user

```bash
psql "host=<non-prod-endpoint> port=5432 user=<admin_user> dbname=postgres sslmode=require"
```

### 3) Create roles and set passwords

```sql
CREATE ROLE mnemosys_sandbox_admin LOGIN;
CREATE ROLE mnemosys_sandbox_user LOGIN;
CREATE ROLE mnemosys_dev_admin LOGIN;
CREATE ROLE mnemosys_dev_user LOGIN;
CREATE ROLE mnemosys_test_admin LOGIN;
CREATE ROLE mnemosys_test_user LOGIN;

\password mnemosys_sandbox_admin
\password mnemosys_sandbox_user
\password mnemosys_dev_admin
\password mnemosys_dev_user
\password mnemosys_test_admin
\password mnemosys_test_user
```

### 4) Create databases and isolate access

Run each `CREATE DATABASE` independently; if it already exists, skip it.

```sql
CREATE DATABASE mnemosys_sandbox OWNER mnemosys_sandbox_admin;
CREATE DATABASE mnemosys_dev OWNER mnemosys_dev_admin;
CREATE DATABASE mnemosys_test OWNER mnemosys_test_admin;

GRANT ALL PRIVILEGES ON DATABASE mnemosys_sandbox TO mnemosys_sandbox_admin;
GRANT CONNECT ON DATABASE mnemosys_sandbox TO mnemosys_sandbox_user;

GRANT ALL PRIVILEGES ON DATABASE mnemosys_dev TO mnemosys_dev_admin;
GRANT CONNECT ON DATABASE mnemosys_dev TO mnemosys_dev_user;

GRANT ALL PRIVILEGES ON DATABASE mnemosys_test TO mnemosys_test_admin;
GRANT CONNECT ON DATABASE mnemosys_test TO mnemosys_test_user;

REVOKE CONNECT ON DATABASE mnemosys_dev FROM mnemosys_sandbox_admin, mnemosys_sandbox_user, mnemosys_test_admin, mnemosys_test_user;
REVOKE CONNECT ON DATABASE mnemosys_sandbox FROM mnemosys_dev_admin, mnemosys_dev_user, mnemosys_test_admin, mnemosys_test_user;
REVOKE CONNECT ON DATABASE mnemosys_test FROM mnemosys_sandbox_admin, mnemosys_sandbox_user, mnemosys_dev_admin, mnemosys_dev_user;
```

### 5) Grant schema access (sandbox/dev/test)

Run each block while connected to the target database as its admin role.

Sandbox:

```sql
CREATE SCHEMA IF NOT EXISTS mnemosys AUTHORIZATION mnemosys_sandbox_admin;
GRANT USAGE ON SCHEMA mnemosys TO mnemosys_sandbox_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA mnemosys TO mnemosys_sandbox_user;
GRANT USAGE, SELECT, UPDATE ON ALL SEQUENCES IN SCHEMA mnemosys TO mnemosys_sandbox_user;
ALTER DEFAULT PRIVILEGES FOR ROLE mnemosys_sandbox_admin IN SCHEMA mnemosys
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO mnemosys_sandbox_user;
ALTER DEFAULT PRIVILEGES FOR ROLE mnemosys_sandbox_admin IN SCHEMA mnemosys
    GRANT USAGE, SELECT, UPDATE ON SEQUENCES TO mnemosys_sandbox_user;
```

Development:

```sql
CREATE SCHEMA IF NOT EXISTS mnemosys AUTHORIZATION mnemosys_dev_admin;
GRANT USAGE ON SCHEMA mnemosys TO mnemosys_dev_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA mnemosys TO mnemosys_dev_user;
GRANT USAGE, SELECT, UPDATE ON ALL SEQUENCES IN SCHEMA mnemosys TO mnemosys_dev_user;
ALTER DEFAULT PRIVILEGES FOR ROLE mnemosys_dev_admin IN SCHEMA mnemosys
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO mnemosys_dev_user;
ALTER DEFAULT PRIVILEGES FOR ROLE mnemosys_dev_admin IN SCHEMA mnemosys
    GRANT USAGE, SELECT, UPDATE ON SEQUENCES TO mnemosys_dev_user;
```

Test:

```sql
CREATE SCHEMA IF NOT EXISTS mnemosys AUTHORIZATION mnemosys_test_admin;
GRANT USAGE ON SCHEMA mnemosys TO mnemosys_test_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA mnemosys TO mnemosys_test_user;
GRANT USAGE, SELECT, UPDATE ON ALL SEQUENCES IN SCHEMA mnemosys TO mnemosys_test_user;
ALTER DEFAULT PRIVILEGES FOR ROLE mnemosys_test_admin IN SCHEMA mnemosys
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO mnemosys_test_user;
ALTER DEFAULT PRIVILEGES FOR ROLE mnemosys_test_admin IN SCHEMA mnemosys
    GRANT USAGE, SELECT, UPDATE ON SEQUENCES TO mnemosys_test_user;
```

### 6) Local environment configuration (sandbox only)

Local `.env` uses sandbox credentials only (no dev/test/prod secrets). Provide shared connection details plus both admin and user credentials:

```bash
MNEMOSYS_DB_HOST=<non-prod-endpoint>
MNEMOSYS_DB_PORT=5432
MNEMOSYS_DB_DRIVERNAME=postgresql
MNEMOSYS_DB_DATABASE=mnemosys_sandbox
MNEMOSYS_DB_SSLMODE=require
MNEMOSYS_DB_USERNAME=mnemosys_sandbox_user
MNEMOSYS_DB_PASSWORD=<sandbox-user-password>

MNEMOSYS_DB_ADMIN_USERNAME=mnemosys_sandbox_admin
MNEMOSYS_DB_ADMIN_PASSWORD=<sandbox-admin-password>

MNEMOSYS_ENV=sandbox
MNEMOSYS_DB_SCHEMA=mnemosys
```

Notes:
- `MNEMOSYS_DB_ADMIN_*` inherits host/port/driver/database/sslmode from `MNEMOSYS_DB_*` unless overridden.

## Production Setup (Dedicated RDS)

Repeat the same steps on the production RDS instance using:

- `mnemosys_prod` database
- `mnemosys_prod_admin` and `mnemosys_prod_user` roles

Local environments must never store production credentials.

## Bootstrap Exit (Lockdown)

When automated deployment updates `mnemosys_dev` and restarts the REST API,
bootstrap ends and the non-prod RDS instance must be locked down. See the
bootstrap exit checklist in `docs/policies/aws-db-bootstrap-constraints.md`.
