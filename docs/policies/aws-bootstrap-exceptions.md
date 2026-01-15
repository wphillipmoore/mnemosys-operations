# AWS Bootstrap Exceptions

## Table of Contents
- [Purpose](#purpose)
- [Scope](#scope)
- [Bootstrap exceptions](#bootstrap-exceptions)
- [Account model](#account-model)
- [Bootstrap end trigger](#bootstrap-end-trigger)
- [References](#references)

## Purpose
Document the operational exceptions and constraints that apply during the AWS
bootstrap phase.

## Scope
Applies to AWS infrastructure used for MNEMOSYS development, test, and
production environments during bootstrap.

## Bootstrap exceptions
- Temporary public database access is permitted only for controlled bootstrap
  or diagnostics and must be removed afterward.
- The development RDS instance may be made public with IP allowlisting to
  provision and use `mnemosys_sandbox`.
- Local environments must store only sandbox credentials.
- Sandbox roles must be denied `CONNECT` on `mnemosys_dev`.
- Development and test databases may share the existing non-production RDS
  instance during bootstrap, but test must move to a dedicated RDS instance
  before any external users are granted access.

## Account model
- All environments share a single AWS account during bootstrap.
- A single console/CLI IAM user (`mnemosys-admin`) is used for access.
- The account model may be split into non-prod and prod accounts later if
  scale or risk demands it.

## Bootstrap end trigger
Bootstrap ends when end-to-end automation updates `mnemosys_dev` and restarts
the REST API service. At that point, the development RDS instance must be fully
locked down.

## References
- `docs/architecture/MNEMOSYS_Infrastructure_and_Platform_Decisions.md` in
  https://github.com/wphillipmoore/mnemosys-core
