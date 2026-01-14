# 0002-version-alignment-with-mnemosys-core

## Table of Contents
- [Status](#status)
- [Context](#context)
- [Decision](#decision)
- [Consequences](#consequences)

## Status
Accepted

## Context
This repository co-releases CLI utilities alongside mnemosys-core but does not
share all release cadence or changes. Full version lockstep would add
unnecessary coupling, while complete divergence would complicate cross-repo
coordination.

## Decision
Sync `MAJOR.MINOR` with mnemosys-core while keeping `PATCH.BUILD` independent
per repository, using the application versioning scheme.

## Consequences
- Cross-repo communication uses shared `MAJOR.MINOR` for compatibility framing.
- `PATCH.BUILD` increment independently based on this repo’s change cadence.
- Version alignment checks must compare only `MAJOR.MINOR` with mnemosys-core.
