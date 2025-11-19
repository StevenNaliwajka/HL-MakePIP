# HL-MakePIP
Makes a project pip project


pip install "git+https://github.com/USERNAME/REPO_NAME.git@BRANCH_OR_TAG"


ENTRY POINTS:
setup_project_env() - Sets up the project env. (pyproject.toml) User customizes.
register_to_test_pypi() - Registers to test PYPI. Requires API Key.
register_to_pypi() - Registers to PYPI. Requires API Key.


Future experimentation w/ github workflows. 
- Workflow creation automated. (.github/workflows/publish.yml) already.
- Exact workflow to compile succuessfully w/ "Trusted Publisher" automatically not figured out.

RQS NOT Automated.



register_to_test_pypi():
Test:
https://test.pypi.org/manage/account/#api-tokens
windows:
py -m twine upload --repository testpypi dist/*
Linux:
python3 -m twine upload --repository testpypi dist/*

register_to_pypi()
Real
https://pypi.org/manage/account/#api-tokens
Windows:
py -m twine upload dist/*
Linux:
python3 -m twine upload dist/*