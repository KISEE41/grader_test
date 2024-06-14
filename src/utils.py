import os
import pathlib

import fileinput
import importlib
import itertools

import re

import nbformat


def read_notebook(path: str):
    filepath = pathlib.Path(path)
    status = os.path.isfile(filepath)
    
    if status and filepath.suffix == ".ipynb":
        nb = nbformat.read(path, as_version=nbformat.NO_CONVERT)
    else:
        raise FileNotFoundError({
            "status": "Execution Failed",
            "reason": f"{path} not found"
        })

    return nb 