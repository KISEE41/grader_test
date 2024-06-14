from pathlib import Path

from loguru import logger
from nbconvert.exporters.exporter import ResourcesDict

from nbgrader.preprocessors import ClearOutput, Execute

from src.utils import read_notebook

from .preprocessors.cell_check import CellCheck
from .preprocessors.check_points import CheckPoint
from .preprocessors.autogrades import GetAutoGrades


class Grader:
    def check_instructor_file(self, instructor_file: str):
        # read notebook
        nb = read_notebook(instructor_file)
        
        # # notebook read is in the form of json format
        # logger.debug(nb)

        resources = ResourcesDict(
            None,
            {
                "scores": [],
                "total_obtained": 0,
                "total_marks": 0,
                "metadata": {"path": str(Path(instructor_file).parents[0])},
            },
        )

        # Clear Solutions
        nb, resources = ClearOutput().preprocess(nb=nb, resources=resources)

        # Execute notebook
        nb, resources = Execute().preprocess(nb=nb, resources=resources)
        # logger.debug(nb)
        
        # Checking if there is any error in the notebook
        _ = CellCheck().preprocess(nb=nb)

        # Autogrades the notebook
        nb, resources = GetAutoGrades().preprocess(nb=nb, resources=resources)

        # check the assignment if there are some issues
        # the grader must give full score for instructor file
        # checking if the grader has does so
        _ = CheckPoint().preprocess(resources=resources)

        # returning the notebook and the resources consisting of metadata
        return nb, dict(resources)

