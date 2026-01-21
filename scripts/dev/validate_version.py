#!/usr/bin/env python3
"""
Validate version string rules for CI.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence

VERSION_PATTERN = re.compile(r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$")
VERSION_WITH_BUILD_PATTERN = re.compile(
    r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:\.(0|[1-9][0-9]*))?$"
)


@dataclass(frozen=True)
class Version:
    """Semantic version without a build component."""

    major: int
    minor: int
    patch: int

    def as_string(self) -> str:
        """Return the version formatted as MAJOR.MINOR.PATCH."""
        return f"{self.major}.{self.minor}.{self.patch}"

    def as_tuple(self) -> tuple[int, int, int]:
        """Return the version as a comparison tuple."""
        return (self.major, self.minor, self.patch)


def parse_arguments(argument_list: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Validate mnemosys-operations version string rules in CI.",
    )
    parser.add_argument(
        "--base-ref",
        default=None,
        help="Base branch reference for comparison (defaults to GITHUB_BASE_REF).",
    )
    parser.add_argument(
        "--event-name",
        default=None,
        help="Event name override (defaults to GITHUB_EVENT_NAME).",
    )
    return parser.parse_args(list(argument_list) if argument_list is not None else None)


def ensure_project_root() -> None:
    """Fail fast if invoked outside the repository root."""
    if not Path("pyproject.toml").is_file():
        raise SystemExit("Run from the repository root (pyproject.toml missing).")


def read_command_output(command: Sequence[str]) -> str:
    """Run a command and return its stripped standard output."""
    result = subprocess.run(command, check=True, text=True, capture_output=True)
    return result.stdout.strip()


def git_reference_exists(reference: str) -> bool:
    """Return True if the git reference exists."""
    result = subprocess.run(("git", "rev-parse", "--verify", "--quiet", reference))
    return result.returncode == 0


def resolve_base_reference(base_reference: str) -> str:
    """Resolve a base reference to an existing git ref."""
    if git_reference_exists(base_reference):
        return base_reference
    remote_reference = f"origin/{base_reference}"
    if git_reference_exists(remote_reference):
        return remote_reference
    raise SystemExit(
        "Base reference not found. Fetch the base branch before running version checks."
    )


def parse_version(version_value: str, allow_build: bool) -> Version:
    """Parse and validate a version string."""
    pattern = VERSION_WITH_BUILD_PATTERN if allow_build else VERSION_PATTERN
    match = pattern.match(version_value)
    if not match:
        raise SystemExit(f"Invalid version format: {version_value}")
    major, minor, patch = (int(match.group(index)) for index in range(1, 4))
    return Version(major=major, minor=minor, patch=patch)


def load_version_from_toml_text(toml_text: str, allow_build: bool) -> Version:
    """Load the version from a pyproject.toml text block."""
    data = tomllib.loads(toml_text)
    version_value = None
    project_section = data.get("project")
    if isinstance(project_section, dict):
        version_value = project_section.get("version")
    if version_value is None:
        raise SystemExit("Missing version in pyproject.toml (expected project.version).")
    if not isinstance(version_value, str):
        raise SystemExit("Version value in pyproject.toml must be a string.")
    return parse_version(version_value, allow_build)


def load_version_from_worktree() -> Version:
    """Load the version from the working tree."""
    pyproject_text = Path("pyproject.toml").read_text(encoding="utf-8")
    return load_version_from_toml_text(pyproject_text, allow_build=False)


def load_version_from_git(reference: str) -> Version:
    """Load the version from a git reference."""
    pyproject_text = read_command_output(("git", "show", f"{reference}:pyproject.toml"))
    return load_version_from_toml_text(pyproject_text, allow_build=True)


def find_base_version_commit(version: Version) -> str:
    """Return the commit that introduced the base version."""
    version_literal = f'version = "{version.as_string()}"'
    output = read_command_output(
        ("git", "log", "--format=%H", "-S", version_literal, "--", "pyproject.toml")
    )
    commits = [line for line in output.splitlines() if line]
    if not commits:
        raise SystemExit(
            "Unable to locate base version commit in history. "
            "Ensure full git history is available."
        )

    for commit in commits:
        try:
            pyproject_text = read_command_output(("git", "show", f"{commit}:pyproject.toml"))
        except subprocess.CalledProcessError:
            continue
        if load_version_from_toml_text(pyproject_text, allow_build=False).as_tuple() == version.as_tuple():
            return commit

    raise SystemExit(
        "Unable to verify base version commit in history. "
        "Ensure full git history is available."
    )


def derive_build_number(version: Version) -> int:
    """Derive the build number from git history."""
    base_commit = find_base_version_commit(version)
    count_text = read_command_output(("git", "rev-list", "--count", f"{base_commit}..HEAD"))
    try:
        return int(count_text)
    except ValueError as exc:
        raise SystemExit("Derived build number is not numeric.") from exc


def ensure_version_not_regressed(base_version: Version, head_version: Version) -> None:
    """Ensure the head version does not regress from the base."""
    if head_version.as_tuple() < base_version.as_tuple():
        raise SystemExit(
            "Base version regressed. "
            f"Base is {base_version.as_string()}, head is {head_version.as_string()}."
        )


def validate_develop_rules(base_version: Version, head_version: Version) -> None:
    """Validate develop-bound version rules."""
    if (head_version.major, head_version.minor) == (base_version.major, base_version.minor):
        if head_version.patch == base_version.patch:
            return
        if head_version.patch == base_version.patch + 1:
            return
        raise SystemExit(
            "PATCH must remain the same for feature work or increment by 1 for a new cycle. "
            f"Base is {base_version.as_string()}, head is {head_version.as_string()}."
        )

    if head_version.major == base_version.major and head_version.minor > base_version.minor:
        if head_version.patch != 0:
            raise SystemExit("PATCH must reset to 0 when MINOR changes.")
        return

    if head_version.major > base_version.major:
        if head_version.minor != 0 or head_version.patch != 0:
            raise SystemExit("MINOR and PATCH must reset to 0 when MAJOR changes.")
        return


def validate_promotion_rules(base_branch: str, base_version: Version, head_version: Version) -> None:
    """Validate promotion-bound version rules."""
    if base_branch in {"release", "main"} and head_version.as_tuple() != base_version.as_tuple():
        raise SystemExit(
            "Promotion pull requests must not change the base version. "
            f"Base is {base_version.as_string()}, head is {head_version.as_string()}."
        )


def main() -> int:
    arguments = parse_arguments()
    ensure_project_root()

    head_version = load_version_from_worktree()
    derive_build_number(head_version)

    base_reference = arguments.base_ref or os.environ.get("GITHUB_BASE_REF")
    event_name = arguments.event_name or os.environ.get("GITHUB_EVENT_NAME", "")
    if base_reference and (event_name == "pull_request" or arguments.base_ref is not None):
        resolved_base = resolve_base_reference(base_reference)
        base_version = load_version_from_git(resolved_base)
        ensure_version_not_regressed(base_version, head_version)

        base_branch = resolved_base.split("/")[-1]
        if base_branch == "develop":
            validate_develop_rules(base_version, head_version)
        else:
            validate_promotion_rules(base_branch, base_version, head_version)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
