# Repository Bootstrap

## Table of Contents
- [Purpose](#purpose)
- [Bootstrap results](#bootstrap-results)
- [Pre-bootstrap decisions](#pre-bootstrap-decisions)
- [Decisions recorded](#decisions-recorded)
- [Questions for next bootstrap](#questions-for-next-bootstrap)

## Purpose
Summarize the repository bootstrap outcomes, the decisions made before work
started, and the open questions to resolve in the next bootstrap pass.

## Bootstrap results
- Added the required standards reference at `docs/standards-and-conventions.md`.
- Created documentation structure under `docs/` and ADR scaffolding.
- Established Python application packaging with Poetry and a CLI entrypoint.
- Added baseline package structure under `src/` and placeholders for tests and
  scripts.

## Pre-bootstrap decisions
- The repository is an application with co-released CLI utilities.
- CLI entrypoint name is `mnemosys-ops`.
- CLI framework is undecided; default implementation uses the Python stdlib.
- Release environments are develop, test, production.
- Versioning uses the application scheme; `MAJOR.MINOR` synced to mnemosys-core
  and `PATCH.BUILD` are repo-specific.
- Python runtime version is 3.14.

## Decisions recorded
- `docs/decisions/0001-application-classification-and-co-release.md`
- `docs/decisions/0002-version-alignment-with-mnemosys-core.md`

## Questions for next bootstrap
- Which CLI framework is the standard (typer, click, or other), and what is the
  rationale?
- What operational commands and subcommands are in scope for the first release?
- Should we add a version alignment check against mnemosys-core in CI?
- What is the dependency and release workflow for CLI utilities?
- Do we need a shared runtime or containerized dev environment definition?
