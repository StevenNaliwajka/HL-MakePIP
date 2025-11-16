#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from Codebase import scaffold_project, build_project


def cmd_init(args: argparse.Namespace) -> int:
    scaffold_project(
        project_root=Path(args.project_root),
        dist_name=args.name,
        src_dir_name=args.src_dir,
        shell_entry=args.shell_entry,
        version=args.version,
        description=args.description,
        author_name=args.author_name,
        author_email=args.author_email,
        console_script_name=args.console_script or args.name,
    )
    print("[piphelper] init complete.")
    return 0


def cmd_build(args: argparse.Namespace) -> int:
    rc = build_project(Path(args.project_root))
    return rc


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="piphelper")
    sub = p.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="Scaffold pyproject + CLI")
    p_init.add_argument("--project-root", default=".")
    p_init.add_argument("--name", required=True)
    p_init.add_argument("--src-dir", default="Codebase")
    p_init.add_argument("--shell-entry", default="run.sh")
    p_init.add_argument("--version", default="0.1.0")
    p_init.add_argument("--description", default="")
    p_init.add_argument("--author-name", default="")
    p_init.add_argument("--author-email", default="")
    p_init.add_argument("--console-script", default=None)
    p_init.set_defaults(func=cmd_init)

    p_build = sub.add_parser("build", help="Run python -m build in project root")
    p_build.add_argument("--project-root", default=".")
    p_build.set_defaults(func=cmd_build)

    return p


def main() -> None:
    parser = build_parser()

    # If no subcommand is provided (e.g. clicking Run in PyCharm),
    # just show help and exit cleanly instead of erroring.
    if len(sys.argv) == 1:
        parser.print_help()
        raise SystemExit(0)

    args = parser.parse_args()
    raise SystemExit(args.func(args))


if __name__ == "__main__":
    main()
