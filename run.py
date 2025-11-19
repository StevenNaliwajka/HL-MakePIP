#!/usr/bin/env python3
from pathlib import Path

from Codebase.register_to_pip import register_to_pip
from Codebase.setup_project_env import setup_project_env


def run():

    ## Register HL-MakePIP to project

    project_root = Path(__file__).parent
    print(project_root)
    register_to_pip(project_root)
    ##setup_project_env(project_root)

if __name__ == "__main__":
    run()
