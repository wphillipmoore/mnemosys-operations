from __future__ import annotations

import argparse
import importlib.metadata
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Sequence


def _package_version() -> str:
    try:
        return importlib.metadata.version("mnemosys-operations")
    except importlib.metadata.PackageNotFoundError:
        return "unknown"


class VersionAction(argparse.Action):
    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: str | Sequence[Any] | None,
        option_string: str | None = None,
    ) -> None:
        parser.exit(message=f"{_package_version()}\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mnemosys-ops",
        description="Mnemosys operations CLI utilities.",
    )
    parser.register("action", "version", VersionAction)
    parser.add_argument(
        "--version",
        action="version",
        nargs=0,
        help="Show the application version and exit.",
    )
    parser.add_argument(
        "--env",
        choices=["develop", "test", "production"],
        default="develop",
        help="Target environment for operations (placeholder).",
    )
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("status", help="Show placeholder status.")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "status":
        print("mnemosys-ops: no operational commands implemented yet.")
        return 0

    parser.print_help()
    return 2
