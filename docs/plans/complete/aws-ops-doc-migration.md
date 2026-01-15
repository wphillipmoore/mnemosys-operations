# AWS Operations Documentation Migration Plan

## Table of Contents
- [Purpose](#purpose)
- [Scope](#scope)
- [Source inventory](#source-inventory)
- [Target structure](#target-structure)
- [Migration map](#migration-map)
- [Plan](#plan)
  - [Phase 0: Decisions before execution](#phase-0-decisions-before-execution)
  - [Phase 1: Prepare target structure](#phase-1-prepare-target-structure)
  - [Phase 2: Migrate documents](#phase-2-migrate-documents)
  - [Phase 3: Update references](#phase-3-update-references)
  - [Phase 4: Validate and close](#phase-4-validate-and-close)
- [Validation checks](#validation-checks)
- [Risks and mitigations](#risks-and-mitigations)
- [Open questions](#open-questions)
- [Status](#status)

## Purpose
Define a concrete plan to migrate AWS operations documentation from
mnemosys-core into mnemosys-operations and record the executed steps.

## Scope
- AWS operations runbooks, bootstrap procedures, and operational logs.
- Operational exceptions embedded in architecture or schema design docs.
- Link and ownership updates after migration.

Out of scope:
- Non-AWS operational docs unrelated to infrastructure.
- Code or tooling changes.

## Source inventory
Target sources in mnemosys-core (read-only until execution):
- `docs/architecture/MNEMOSYS_Infrastructure_and_Platform_Decisions.md`
- `docs/project/final/Database_Environment_Setup.md`
- `docs/plans/complete/2026-01-04-aws-nonprod-rest-api-deploy-plan.md`
- `docs/plans/complete/2026-01-07-test-prod-db-parity-plan.md` (stub pointing to the consolidated plan)
- `docs/operations/2026-01-12-18-31-nonprod-parity-ops.md`
- `docs/operations/2026-01-13-13-50-deployment-validation.md`
- `docs/plans/in-progress/2026-01-03-alembic-schema-management-design.md` (operational constraints section)

## Target structure
Proposed mnemosys-operations layout:
- `docs/aws/`: AWS runbooks and bootstrap procedures.
- `docs/operations/`: operational execution logs and validation records.
- `docs/policies/`: operational policy constraints and exceptions.

## Migration map
- `docs/plans/complete/2026-01-04-aws-nonprod-rest-api-deploy-plan.md`
  -> `docs/aws/nonprod-rest-api-deploy-plan.md`
- `docs/project/final/Database_Environment_Setup.md`
  -> `docs/aws/database-environment-setup.md`
- `docs/operations/2026-01-12-18-31-nonprod-parity-ops.md`
  -> `docs/operations/2026-01-12-18-31-nonprod-parity-ops.md`
- `docs/operations/2026-01-13-13-50-deployment-validation.md`
  -> `docs/operations/2026-01-13-13-50-deployment-validation.md`
- Extract operational exceptions from
  `docs/architecture/MNEMOSYS_Infrastructure_and_Platform_Decisions.md`
  -> `docs/policies/aws-bootstrap-exceptions.md`
- Extract operational constraints from
  `docs/plans/in-progress/2026-01-03-alembic-schema-management-design.md`
  -> `docs/policies/aws-db-bootstrap-constraints.md`
- Keep `docs/plans/complete/2026-01-07-test-prod-db-parity-plan.md` as a stub in
  mnemosys-core or migrate the stub to mnemosys-operations (decision needed).

## Plan

### Phase 0: Decisions before execution
- Confirm the target directory structure (`docs/aws`, `docs/operations`,
  `docs/policies`) and naming.
- Confirm whether mnemosys-core should retain stubs that link to the new
  mnemosys-operations locations.
- Confirm whether any AWS identifiers must be redacted or moved to a separate
  private doc before migration.

### Phase 1: Prepare target structure
- Create the target directories in mnemosys-operations.
- Add placeholder README files if needed to explain each area.

### Phase 2: Migrate documents
- Copy the runbook and operations documents into the new locations.
- Extract operational exceptions and constraints into policy docs.
- Preserve history and timestamps in file names and content.

### Phase 3: Update references
- In mnemosys-core, replace moved content with links to the new locations.
- Ensure architecture and schema docs reference the new policy docs instead of
  embedding operational exceptions.
- Update any cross-links inside migrated docs to point to the new paths.

### Phase 4: Validate and close
- Verify all moved docs include Tables of Contents per standards.
- Confirm no broken links remain in either repository.
- Record the migration decision in a new ADR (if required).

## Validation checks
- `rg -n "docs/aws|docs/operations|docs/policies" docs` in mnemosys-operations.
- `rg -n "mnemosys-operations" docs` in mnemosys-core to confirm link updates.
- Manual spot-check of each migrated document for TOC and link accuracy.

## Risks and mitigations
- Drift between core and operations docs.
  Mitigation: replace core content with explicit links and a single source of
  truth.
- Sensitive identifiers embedded in runbooks.
  Mitigation: confirm redaction policy before migration.
- Over-splitting architecture vs operations.
  Mitigation: keep architecture decisions in core, move procedures to ops.

## Open questions
- Should mnemosys-core keep stubs for migrated docs or only link from a single
  index page?
- Do we need a dedicated "runbooks" section instead of `docs/aws`?
- Which AWS identifiers are safe to keep in public docs?
- Should the parity plan stub move with the consolidated deploy plan?

## Status
Completed. Migration executed and references updated.
