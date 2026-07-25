"""Command-line entry point."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence

from {{ cookiecutter.package_name }}.diagnostics import run_diagnostics
from {{ cookiecutter.package_name }}.testing import FakeModelClient


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="{{ cookiecutter.repository_name }}")
    subcommands = parser.add_subparsers(dest="command", required=True)
    subcommands.add_parser("diagnostics", help="run deterministic local diagnostics")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = build_parser().parse_args(argv)
    if arguments.command == "diagnostics":
        client = FakeModelClient({"diagnostic probe": "diagnostic-ok"})
        print(json.dumps(run_diagnostics(client).as_dict(), sort_keys=True))
        return 0
    raise AssertionError(f"unhandled command: {arguments.command}")


if __name__ == "__main__":
    raise SystemExit(main())
