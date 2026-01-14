# Mnemosys Operations

Policy, procedures, and tooling for Mnemosys operations.

## Table of Contents
- [Purpose](#purpose)
- [Scope](#scope)
- [Repository layout](#repository-layout)
- [CLI utilities](#cli-utilities)
- [Standards and conventions](#standards-and-conventions)
- [Status](#status)

## Purpose
Define durable operational policy and procedures for Mnemosys and provide
supporting CLI utilities for operational workflows.

## Scope
- Operational policies, procedures, and checklists.
- Python CLI utilities used alongside mnemosys-core deployments.
- Application release workflow aligned to mnemosys-core.

## Repository layout
- `docs/`: documentation and standards references.
- `docs/decisions/`: architecture decision records (ADRs).
- `src/`: Python package source.
- `tests/`: test suite for CLI utilities.
- `scripts/`: developer tooling and automation.

## CLI utilities
- Entry point: `mnemosys-ops`
- CLI framework: TBD (placeholder implementation uses the stdlib)
- Target environments: develop, test, production

## Standards and conventions
See `docs/standards-and-conventions.md` for canonical standards and local
overlays.

## Status
Bootstrapping; content and tooling will be expanded as operations practices are
formalized.
