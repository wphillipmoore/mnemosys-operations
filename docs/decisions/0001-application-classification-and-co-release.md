# 0001-application-classification-and-co-release

## Table of Contents
- [Status](#status)
- [Context](#context)
- [Decision](#decision)
- [Consequences](#consequences)

## Status
Accepted

## Context
This repository includes both operational documentation and Python CLI
utilities used alongside mnemosys-core deployments. The original scope
classified it as a library, but release alignment and deployment usage require
application-style versioning and promotion.

## Decision
Treat `mnemosys-operations` as an application that ships co-released CLI
utilities. Versioning follows the application scheme and aligns with
mnemosys-core across develop, test, and production environments.

## Consequences
- The repository uses application versioning (`MAJOR.MINOR.PATCH.BUILD`).
- CLI utilities are packaged as part of the application release.
- Development workflows mirror mnemosys-core promotion across environments.
