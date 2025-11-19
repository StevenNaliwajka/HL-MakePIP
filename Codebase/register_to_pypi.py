#!/usr/bin/env python3
from __future__ import annotations

import os
import sys
import subprocess
from pathlib import Path
import getpass


def _detect_project_root() -> Path:
    # Adjust as needed; currently assumes this file lives in <project_root>/Codebase/...
    return Path(__file__).resolve().parent.parent


def _prompt_token(prompt: str) -> str:
    """
    Try to read a hidden token with getpass.
    If that fails (e.g. in some IDE consoles), fall back to visible input().
    """
    try:
        if sys.stdin.isatty():
            # Standard terminal – use getpass
            return getpass.getpass(prompt).strip()
    except Exception:
        # Any error, fall back to input
        pass

    # Fallback for environments where getpass doesn't work
    print("(getpass not available here – your input will be visible)", flush=True)
    return input(prompt).strip()


def register_to_pypi(project_root: str | Path | None = None) -> int:
    """
    Upload dist/* to the real PyPI using a token provided interactively.

    Equivalent to:
      Windows: py -m twine upload dist/*
      Linux:   python3 -m twine upload dist/*
    """
    if project_root is None:
        project_root = _detect_project_root()
    project_root = Path(project_root).resolve()

    dist_dir = project_root / "dist"
    if not dist_dir.exists():
        print(f"[ERROR] dist/ directory not found at: {dist_dir}", flush=True)
        print("        Build your package first, e.g. `python -m build`.", flush=True)
        return 1

    print("============================================================", flush=True)
    print(" PyPI Upload Helper (REAL PYPI)", flush=True)
    print("============================================================", flush=True)
    print("1) Open this URL in your browser:", flush=True)
    print("   https://pypi.org/manage/account/#api-tokens", flush=True)
    print("2) Create a new API token (or copy an existing one).", flush=True)
    print("3) Have the token ready in your clipboard.", flush=True)
    print("4) Then come back here and press ENTER to continue.", flush=True)
    print("------------------------------------------------------------", flush=True)
    input("Press ENTER once your PyPI API token is ready... ")

    token = _prompt_token(
        "Paste your PyPI API token here (input may be hidden): "
    )

    if not token:
        print("[ERROR] No token entered. Aborting.", flush=True)
        return 1

    files = sorted(dist_dir.glob("*"))
    if not files:
        print(f"[ERROR] No files found in dist/: {dist_dir}", flush=True)
        print("        Run `python -m build` first to create distributions.", flush=True)
        return 1

    if os.name == "nt":
        python_cmd = ["py", "-m", "twine", "upload"]
    else:
        python_cmd = ["python3", "-m", "twine", "upload"]

    cmd = python_cmd + [str(f) for f in files]

    print("------------------------------------------------------------", flush=True)
    print(f"Project root : {project_root}", flush=True)
    print(f"dist/ files  : {[f.name for f in files]}", flush=True)
    print(f"Running      : {' '.join(cmd)}", flush=True)
    print("------------------------------------------------------------", flush=True)
    print("NOTE: Using username '__token__' and your API token as password.", flush=True)
    print("============================================================", flush=True)

    env = os.environ.copy()
    env["TWINE_USERNAME"] = "__token__"
    env["TWINE_PASSWORD"] = token

    try:
        result = subprocess.run(
            cmd,
            cwd=project_root,
            env=env,
            check=False,
        )
    except FileNotFoundError as e:
        print("[ERROR] Failed to run twine command.", flush=True)
        print("       Make sure 'twine' is installed in your environment:", flush=True)
        print("         pip install twine", flush=True)
        print(f"Details: {e}", flush=True)
        return 1

    if result.returncode == 0:
        print("✅ Upload to PyPI completed successfully.", flush=True)
    else:
        print(f"❌ twine exited with code {result.returncode}.", flush=True)
    return result.returncode


def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]

    project_root = argv[0] if argv else None
    return register_to_pypi(project_root=project_root)


if __name__ == "__main__":
    raise SystemExit(main())
