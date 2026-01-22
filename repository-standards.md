# Mnemosys Operations Repository Standards

## Table of Contents
- [Repository profile](#repository-profile)
- [AI co-authors](#ai-co-authors)
- [Versioning alignment](#versioning-alignment)
- [Release environments](#release-environments)
- [Local validation](#local-validation)
- [Tooling requirement](#tooling-requirement)
- [Local deviations](#local-deviations)

## Repository profile
- repository_type: application
- versioning_scheme: application
- branching_model: application-promotion
- release_model: environment-promotion
- supported_release_lines: single

## AI co-authors
- Co-Authored-By: mnemosys-codex <252598091+mnemosys-codex@users.noreply.github.com>
- Co-Authored-By: mnemosys-claude <252602472+mnemosys-claude@users.noreply.github.com>

## Versioning alignment
MAJOR.MINOR synced with mnemosys-core; PATCH.BUILD are repo-specific.

## Release environments
Develop, test, production.

## Local validation
- `python3 scripts/dev/validate_local.py`
- Docs-only changes: `python3 scripts/dev/validate_docs.py`

## Tooling requirement
- `uv` `0.9.26` (install with `python3 -m pip install uv==0.9.26`).

## Local deviations
None.
