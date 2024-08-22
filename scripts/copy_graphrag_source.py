##
# This script copies the GraphRAG source code to the graphfleet/libs/graphrag directory.
# Run this script from the root of the graphfleet project.
# python scripts/copy_graphrag_source.py


import os
import shutil
import graphrag


def copy_graphrag_source():
    # Get the location of the installed graphrag package in .venv
    venv_path = os.path.join(".venv", "lib", "python3.10", "site-packages")
    graphrag_path = os.path.join(venv_path, "graphrag")

    # Define the destination path in your project
    dest_path = os.path.join("graphfleet", "libs", "graphrag")

    # Create the destination directory if it doesn't exist
    os.makedirs(dest_path, exist_ok=True)

    # Copy the contents of the graphrag package to the destination
    for item in os.listdir(graphrag_path):
        s = os.path.join(graphrag_path, item)
        d = os.path.join(dest_path, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)

    print(f"GraphRAG source copied to {dest_path}")


if __name__ == "__main__":
    copy_graphrag_source()