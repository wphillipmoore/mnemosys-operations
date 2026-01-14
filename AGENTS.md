# MNEMOSYS Operations

## User Overrides (Optional)

If `~/AGENTS.md` exists and is readable, load it and apply it as a
user-specific overlay for this session. If it cannot be read, say so
briefly and continue.

Operations policy, procedures, and CLI utilities for the MNEMOSYS system.
This repository is treated as an application with co-released CLI utilities
aligned to mnemosys-core.

## Architecture Overview

This repository includes documentation and Python CLI utilities for operations
workflows. The guiding principle is long-term survivability without original
authorship: boring, explicit structure is preferred over cleverness.

### Core Principle

**No implicit state or side effects at import time.** CLI behavior and runtime
configuration must be explicit and invoked directly.

## Start Every Work Session: Create a Feature Branch

**CRITICAL FIRST STEP**: Before making ANY changes in a new session, you MUST:

1. **Check current branch**: `git branch --show-current`
2. **If on `develop`**: Create a feature branch immediately:
   ```bash
   git checkout -b feature/<descriptive-name>
   ```
3. **If already on a feature branch**: Continue working on that branch

**Guardrail**: Do not rely on earlier branch checks. Before any edit or commit (even mid-session or docs-only),
re-run `git branch --show-current`. If you are on `develop`, `release`, or `main`, stop and create a feature
branch before touching files.

**Why this matters**: Direct commits to `develop` violate the project's branching model. ALL changes to eternal branches (develop/main/release) must go through pull requests.

**Branch naming**:
- `feature/*` - New functionality, refactoring, documentation, dependencies (MOST COMMON)
- `bugfix/*` - Non-urgent defect fixes
- `hotfix/*` - Production-blocking issues ONLY

**Example workflow**:
```bash
# At start of session
git status
# If on develop:
git checkout -b feature/add-cli-command

# Do your work...
git add .
git commit -m "..."

# Push and submit PR
git push -u origin feature/add-cli-command
gh pr create --base develop --title "..." --body "..."
```

**If you forget**: You'll need to move commits from develop to a feature branch before pushing. Don't let this happen.

## CRITICAL: Heredoc Commands ALWAYS FAIL - Use Temp Files Instead

**This is a recurring failure pattern that happens every session.**

When creating git commits or GitHub PRs with multi-line messages, **HEREDOC syntax ALWAYS FAILS** in this environment. Avoid commands like:

```bash
# DO NOT USE
git commit -m "$(cat <<'EOF'
Multi-line commit message
EOF
)"
```

**Correct approach: use a temporary file**

```bash
cat > /tmp/commit-msg.txt << 'EOF'
Multi-line commit message
EOF

git commit -F /tmp/commit-msg.txt
rm /tmp/commit-msg.txt

cat > /tmp/pr-body.txt << 'EOF'
Multi-line PR body
EOF

gh pr create --base develop --title "..." --body-file /tmp/pr-body.txt
rm /tmp/pr-body.txt
```

## Before You Act: Consult Documentation First

**CRITICAL**: This project follows a documentation-first methodology. All knowledge required for any AI agent to work effectively is present in the repository and canonical standards. Always read the relevant documentation BEFORE taking action.

### Required Reading Before Common Operations

**Repository bootstrap and local overlays**
- `docs/standards-and-conventions.md`
- `docs/repository-bootstrap.md`

**Git Operations (commit, push, branch, merge)**
- https://github.com/wphillipmoore/standards-and-conventions/blob/main/docs/code-management/branching-and-deployment.md

**Pull Request Operations (creating, submitting, merging)**
- https://github.com/wphillipmoore/standards-and-conventions/blob/main/docs/code-management/pull-request-workflow.md#pre-submission-requirements
- https://github.com/wphillipmoore/standards-and-conventions/blob/main/docs/code-management/pull-request-workflow.md#pull-request-finalization

**Code Quality and Standards**
- https://github.com/wphillipmoore/standards-and-conventions/blob/main/docs/development/python/overview.md

### The RTFM Principle

If you find yourself:
- Using trial-and-error to discover workflow rules
- Guessing at conventions or standards

Stop and read the relevant documentation before proceeding.

### User Confirmation Checkpoints

Always pause and request user confirmation at these checkpoints. Never proceed automatically.

**Docs-Only Exception**: If the diff includes **only** documentation files (anything under `docs/` plus top-level
`README.md` or `CHANGELOG.md`), skip both confirmation checkpoints and proceed directly through PR creation
and finalization. Local validation is optional per the docs-only rule in
https://github.com/wphillipmoore/standards-and-conventions/blob/main/docs/code-management/pull-request-workflow.md.
If any non-documentation file changes, the checkpoints remain mandatory.

**Finalize Override**: If the user explicitly says **"Finalize PR"**, treat that as approval to submit and
finalize the PR for the current work without asking for "Submit PR?" or "Finalize PR?" again. This
permission expires as soon as new work is performed, defined as any new commit or any new file
modification after the approval is granted.

**Checkpoint: Before Submitting Pull Request**

After completing work and committing to your feature branch, validate locally before pushing.
If a local validation script exists, use it. Otherwise run:

```bash
poetry install
poetry run ruff check src tests
poetry run mypy src
poetry run pytest
```

After validation passes, STOP and ask:

```
Submit PR?
```

**Checkpoint: Before Finalizing Pull Request**

After submitting the PR, STOP and ask:

```
Finalize PR?
```

## Project Structure

```
mnemosys-operations/
├── docs/
│   ├── decisions/
│   │   ├── 0001-application-classification-and-co-release.md
│   │   └── 0002-version-alignment-with-mnemosys-core.md
│   ├── overview.md
│   ├── repository-bootstrap.md
│   └── standards-and-conventions.md
├── src/
│   └── mnemosys_operations/
│       ├── __init__.py
│       ├── __main__.py
│       └── cli.py
├── tests/
├── scripts/
├── LICENSE
├── README.md
└── pyproject.toml
```

## Technology Stack

- **Python**: 3.14+
- **Packaging**: Poetry with `src/` layout
- **CLI**: `mnemosys-ops` entrypoint (framework TBD)
- **Testing**: pytest

## Key Dependencies

Currently minimal; avoid adding heavy dependencies without justification.

## Development Workflow

### Setting Up the Environment

```bash
poetry install
```

### Running the CLI

```bash
poetry run mnemosys-ops --help
```

### Running Tests

```bash
poetry run pytest
```

## Coding Conventions

- No global state or import-time side effects.
- No wildcard imports; be explicit.
- Keep modules small and focused.
- Ensure new CLI commands have tests mirroring `src/` layout.

## Architectural Decisions

See `docs/decisions/` for ADRs:

- `0001-application-classification-and-co-release.md`
- `0002-version-alignment-with-mnemosys-core.md`

## Important Notes

- MAJOR.MINOR versions must remain in sync with mnemosys-core; PATCH.BUILD are repo-specific.
- When in doubt, consult mnemosys-core for established patterns and conventions.
