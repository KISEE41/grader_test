import re

from typing import Tuple

from loguru import logger

from nbgrader import utils
from nbgrader.preprocessors import NbGraderPreprocessor

from nbconvert.exporters.exporter import ResourcesDict

from nbformat.notebooknode import NotebookNode


class GetAutoGrades(NbGraderPreprocessor):
    def preprocess(
        self,
        nb: NotebookNode,
        resources: ResourcesDict,
    ) -> Tuple[NotebookNode, ResourcesDict]:
        """
        Preprocessing to apply on each notebook.

        Must return modified nb, resources.

        Overriding the preprocess_cell method to preprocess the notbook
        using custom scripts.

        Parameters
        ----------
        nb : NotebookNode
            Notebook being converted

        resources : dictionary
            Additional resources used in the conversion process.  Allows
            preprocessors to pass variables into the Jinja engine.
        """
        # Preprocessing each cell of the notebook through preprocess_cell method
        nb, resources = super(GetAutoGrades, self).preprocess(nb, resources)

        return nb, resources
    

    def _add_score(self, cell: NotebookNode, resources: ResourcesDict) -> None:
        """
        Autogrades the cell, and add the points.

        Parameters
        ----------
        nb : NotebookNode
            Notebook being converted

        resources : dictionary
            Additional resources used in the conversion process.  Allows
            preprocessors to pass variables into the Jinja engine.
        """
        # Auto grade the cell, and returns the points either partial or full
        auto_score, max_points = utils.determine_grade(cell, self.log)

        # determine_grade returns None if the cell encounters some error
        if auto_score is None:
            auto_score = 0
        try:
            # To determine which exercise/sub-exercise it it
            tags = cell["metadata"]["tags"]
        except KeyError:
            tags = []
        # Choose the task id from the collection of tags
        # ['Ex-1-Task-1', 'traing block', 'tag1', 'tag2'] -> ['Ex-1-Task-1']
        # Exercise must be in the format of 'Ex-\d+-Task-\d+'
        task_name = re.compile(r"(Ex-\d+-Task-\d+)")

        # checking the task_id match or not
        task_id = [tag for tag in tags if task_name.match(tag)]
        
        if len(task_id) == 0:
            task_id = "No task id found"
        
        if len(task_id) == 1:
            task_id = task_id[0]

        # manually graded points
        manually_graded = utils.is_grade(cell) and utils.is_solution(cell)

        # After autograding store the meta data
        resources["scores"].append(
            {   
                # task_id of the exercise
                "taskId": task_id,
                # total point assigned to that particular exercise
                "total": cell["metadata"]["nbgrader"].get("points", 0),
                # obtained marks
                "obtainedMarks": auto_score,
                # marks if manually graded
                "manuallyGraded": manually_graded,
            },
        )

        # adding the obtained marks while itterating the cells
        resources["total_obtained"] += auto_score

        # adding the total marks while itterating the cells
        resources["total_marks"] += cell["metadata"]["nbgrader"].get("points", 0)


    def _add_comment(self, cell: NotebookNode, resources: ResourcesDict) -> None:
        """
        Add necessary comments.

        Parameters
        ----------
        cell : NotebookNode
            cell of a notebook

        resources : dictionary
            Additional resources used in the conversion process.  Allows
            preprocessors to pass variables into the Jinja engine.
        """
        if (
            cell.metadata.nbgrader.get("checksum", None)
            == utils.compute_checksum(
                cell,
            )
            and not utils.is_task(cell)
        ):
            pass
            # self.log("No Response")


    def preprocess_cell(
        self,
        cell: NotebookNode,
        resources: ResourcesDict,
        cell_index: int,
    ) -> Tuple[NotebookNode, ResourcesDict]:
        """
        Preprocess each cell.
        
        Must return modified cell and resource dictionary.

        Parameters
        ----------
        cell : NotebookNode cell
            Notebook cell being processed

        resources : dictionary
            Additional resources used in the conversion process.  Allows
            preprocessors to pass variables into the Jinja engine.

        index : int
            Index of the cell being processed
        """
        if utils.is_grade(cell):
            self._add_score(cell, resources)

        if utils.is_solution(cell):
            self._add_comment(cell, resources)

        if utils.is_task(cell):
            self._add_comment(cell, resources)


        return cell, resources