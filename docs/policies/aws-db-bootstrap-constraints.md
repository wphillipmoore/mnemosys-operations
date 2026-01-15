# AWS Database Bootstrap Constraints

## Table of Contents
- [Purpose](#purpose)
- [Scope](#scope)
- [Environment access model](#environment-access-model)
- [Credential and access rules](#credential-and-access-rules)
- [Bootstrap exit checklist](#bootstrap-exit-checklist)
- [References](#references)

## Purpose
Capture database access constraints and bootstrap rules for AWS-hosted MNEMOSYS
databases.

## Scope
Applies to RDS-backed environments and the credentials used by automation and
local development.

## Environment access model
- `mnemosys_dev` is API-only access and mirrors test/production constraints.
- `mnemosys_sandbox` is admin-accessible for schema testing and validation.
- `mnemosys_test` is API-only access and updated only by release automation.
- Local environments must not store test credentials.
- During bootstrap, `mnemosys_test` may share the non-production RDS instance
  with `mnemosys_dev` and `mnemosys_sandbox`.
- Before any external users access test, `mnemosys_test` must move to a
  dedicated RDS instance with separate network access controls.

## Credential and access rules
- Alembic tooling uses admin credentials via `MNEMOSYS_DB_ADMIN_*`; if unset,
  it falls back to `MNEMOSYS_DB_*`.
- The REST API uses non-admin credentials via `MNEMOSYS_DB_*` only.
- The development deployment database remains API-only; direct admin access is
  not assumed.
- Bootstrap public access exceptions are defined in
  `docs/policies/aws-bootstrap-exceptions.md`.

## Bootstrap exit checklist
- Disable public access on the development RDS instance.
- Remove temporary inbound rules (TCP 5432) from security groups.
- Rotate admin credentials and store them outside local `.env`.
- Ensure local environments only reference sandbox credentials.
- Verify `mnemosys_dev` accepts connections only from the REST API runtime role.

## References
- `docs/plans/in-progress/2026-01-03-alembic-schema-management-design.md` in
  https://github.com/wphillipmoore/mnemosys-core
