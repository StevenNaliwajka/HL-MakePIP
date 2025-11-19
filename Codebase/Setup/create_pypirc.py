from pathlib import Path

PYPIRC_CONTENT = """\
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = pypi-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
"""


def create_pypirc(folder: Path, pypirc_path: Path, force: bool) -> None:
    # Ensure project root exists
    folder.mkdir(parents=True, exist_ok=True)

    # Ensure the directory for the .pypirc file exists (e.g. project_root/UserData)
    pypirc_path.parent.mkdir(parents=True, exist_ok=True)

    if pypirc_path.exists() and not force:
        print(f"[setup-project-env] {pypirc_path} already exists. "
              f"Use --force to overwrite.")
        return

    action = "Overwriting" if pypirc_path.exists() else "Creating"
    print(f"[setup-project-env] {action} {pypirc_path}")
    pypirc_path.write_text(PYPIRC_CONTENT, encoding="utf-8")
