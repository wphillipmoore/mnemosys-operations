# Mnemosys Operations Standards and Conventions

This repository follows the canonical standards at:
https://github.com/wphillipmoore/standards-and-conventions

## Table of Contents
- [Canonical references](#canonical-references)
  - [Core references (always required)](#core-references-always-required)
  - [Repository-type references (required for the declared type)](#repository-type-references-required-for-the-declared-type)
  - [Additional required references](#additional-required-references)
- [Project-specific overlay](#project-specific-overlay)
  - [Repository profile](#repository-profile)
  - [AI co-authors](#ai-co-authors)
  - [Versioning alignment](#versioning-alignment)
  - [Release environments](#release-environments)
  - [Local validation](#local-validation)
  - [Tooling requirement](#tooling-requirement)
  - [Local deviations](#local-deviations)

## Canonical references

### Core references (always required)
- https://github.com/wphillipmoore/standards-and-conventions/blob/develop/docs/foundation/markdown-standards.md
- https://github.com/wphillipmoore/standards-and-conventions/blob/develop/docs/code-management/repository-types-and-attributes.md
- https://github.com/wphillipmoore/standards-and-conventions/blob/develop/docs/code-management/commit-messages-and-authorship.md
- https://github.com/wphillipmoore/standards-and-conventions/blob/develop/docs/code-management/github-issues.md
- https://github.com/wphillipmoore/standards-and-conventions/blob/develop/docs/code-management/pull-request-workflow.md
- https://github.com/wphillipmoore/standards-and-conventions/blob/develop/docs/code-management/source-control-guidelines.md

### Repository-type references (required for the declared type)
- https://github.com/wphillipmoore/standards-and-conventions/blob/develop/docs/code-management/branching-and-deployment.md
- https://github.com/wphillipmoore/standards-and-conventions/blob/develop/docs/code-management/application-versioning-scheme.md

### Additional required references
- https://github.com/wphillipmoore/standards-and-conventions/blob/develop/docs/code-management/overview.md
- https://github.com/wphillipmoore/standards-and-conventions/blob/develop/docs/code-management/release-versioning.md
- https://github.com/wphillipmoore/standards-and-conventions/blob/develop/docs/code-management/hotfix-policy.md
- https://github.com/wphillipmoore/standards-and-conventions/blob/develop/docs/development/overview.md
- https://github.com/wphillipmoore/standards-and-conventions/blob/develop/docs/development/environment-and-tooling.md
- https://github.com/wphillipmoore/standards-and-conventions/blob/develop/docs/development/python/overview.md
- https://github.com/wphillipmoore/standards-and-conventions/blob/develop/docs/development/python/naming-conventions.md
- https://github.com/wphillipmoore/standards-and-conventions/blob/develop/docs/development/python/import-time-side-effects.md
- https://github.com/wphillipmoore/standards-and-conventions/blob/develop/docs/development/python/type-hints.md
- https://github.com/wphillipmoore/standards-and-conventions/blob/develop/docs/development/python/testing-and-coverage.md
- https://github.com/wphillipmoore/standards-and-conventions/blob/develop/docs/repository/overview.md
- https://github.com/wphillipmoore/standards-and-conventions/blob/develop/docs/repository/repository-structure.md
- https://github.com/wphillipmoore/standards-and-conventions/blob/develop/docs/foundation/architecture-standards.md
- https://github.com/wphillipmoore/standards-and-conventions/blob/develop/docs/foundation/ai-code-review-guidelines.md
- https://github.com/wphillipmoore/standards-and-conventions/blob/develop/docs/foundation/ai-assisted-development-loop.md

## Project-specific overlay

### Repository profile

- repository_type: application
- versioning_scheme: application
- branching_model: application-promotion
- release_model: environment-promotion
- supported_release_lines: single

### AI co-authors

None documented.

### Versioning alignment

MAJOR.MINOR synced with mnemosys-core; PATCH.BUILD are repo-specific.

### Release environments

Develop, test, production.

### Local validation

- `python3 scripts/dev/validate_local.py`
- Docs-only changes: `python3 scripts/dev/validate_docs.py`

### Tooling requirement

- `uv` `0.9.26` (install with `python3 -m pip install uv==0.9.26`).

### Local deviations

None.
