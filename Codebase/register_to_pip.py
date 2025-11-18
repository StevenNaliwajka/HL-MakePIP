#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Optional


def _run_cmd(cmd: list[str], cwd: Path, verbose: bool = True) -> None:
    """
    Run a subprocess command, raising a nice error if it fails.
    """
    if verbose:
        print(f"[register_to_pip] Running: {' '.join(cmd)} (cwd={cwd})")

    proc = subprocess.run(
        cmd,
        cwd=str(cwd),
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    if verbose and proc.stdout:
        print(proc.stdout.rstrip())

    if proc.returncode != 0:
        raise RuntimeError(
            f"Command {' '.join(cmd)!r} failed with exit code {proc.returncode}"
        )


def register_to_pip(
    project_root: Path,
    *,
    upload: bool = False,
    repository: Optional[str] = None,
    verbose: bool = True,
) -> None:
    """
    Build a Python project (using `python -m build`) and optionally upload it
    to PyPI/TestPyPI using `python -m twine`.

    Parameters
    ----------
    project_root:
        Path to the project you want to build / upload. Must contain pyproject.toml.
    upload:
        If True, will attempt to upload the artifacts in `dist/` using twine.
        If False (default), only builds the project.
    repository:
        Optional repository name or URL that will be passed to twine:

          * None (default) -> use twine's default repository (usually PyPI)
          * "testpypi"     -> use the 'testpypi' repository configured in ~/.pypirc
          * A full URL     -> passed as --repository-url=<URL>

    verbose:
        If True, prints progress and command output.
    """
    project_root = project_root.resolve()
    print(f"HERE {project_root}")


    if verbose:
        print(f"[register_to_pip] Project root: {project_root}")

    pyproject = project_root / "pyproject.toml"
    if not pyproject.is_file():
        raise FileNotFoundError(
            f"pyproject.toml not found at {pyproject}. "
            "The target project must be a pyproject-based package."
        )

    # 1) Build the project (wheel + sdist)
    if verbose:
        print("[register_to_pip] Step 1/2: Building project with `python -m build`")

    _run_cmd(
        [sys.executable, "-m", "build", "--wheel", "--sdist"],
        cwd=project_root,
        verbose=verbose,
    )

    dist_dir = project_root / "dist"
    if not dist_dir.is_dir():
        raise FileNotFoundError(
            f"Build completed but no 'dist' directory was found at {dist_dir}"
        )

    if not upload:
        if verbose:
            print("[register_to_pip] Build complete. Skipping upload (no --upload).")
            print(f"[register_to_pip] Artifacts are in: {dist_dir}")
        return

    # 2) Upload using twine
    if verbose:
        print("[register_to_pip] Step 2/2: Uploading with `python -m twine`")

    # Check twine is available
    try:
        import twine  # noqa: F401  # type: ignore
    except ImportError as exc:  # pragma: no cover - simple guard
        raise RuntimeError(
            "Twine is not installed. Install it with:\n\n"
            "    python -m pip install twine\n"
        ) from exc

    dist_glob = str(dist_dir / "*")

    cmd = [sys.executable, "-m", "twine", "upload", dist_glob]

    # If repository is given, interpret it
    if repository:
        if repository.startswith("http://") or repository.startswith("https://"):
            cmd.insert(3, f"--repository-url={repository}")
        else:
            # Named repository (pypi/testpypi/etc) configured in ~/.pypirc
            cmd.insert(3, f"--repository={repository}")

    _run_cmd(cmd, cwd=project_root, verbose=verbose)

    if verbose:
        print("[register_to_pip] Upload complete.")


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Build a Python project (wheel + sdist) and optionally upload it "
            "to PyPI/TestPyPI using twine."
        )
    )
    parser.add_argument(
        "project_root",
        nargs="?",
        default=".",
        help="Path to the project root (default: current directory).",
    )
    parser.add_argument(
        "--upload",
        action="store_true",
        help="After building, upload the artifacts in dist/ using twine.",
    )
    parser.add_argument(
        "--repository",
        metavar="NAME_OR_URL",
        default=None,
        help=(
            "Optional twine repository name or URL. "
            "Examples: 'pypi', 'testpypi', or "
            "'https://test.pypi.org/legacy/'. "
            "If omitted, twine's default is used."
        ),
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Reduce output (still shows errors).",
    )
    return parser


def main(argv: Optional[list[str]] = None) -> None:
    parser = _build_arg_parser()
    args = parser.parse_args(argv)

    project_root = Path(args.project_root)
    verbose = not args.quiet

    try:
        register_to_pip(
            project_root=project_root,
            upload=args.upload,
            repository=args.repository,
            verbose=verbose,
        )
    except Exception as exc:  # pragma: no cover
        # Nice one-line error for CLI usage
        print(f"[register_to_pip] ERROR: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
