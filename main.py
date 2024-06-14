import os

from loguru import logger

from src.grader.base import Grader
from src.exceptions.exceptions import NotebookExecutionFailed, ScoreNotMatch

from get_pushed_files import main
from create_logs import create_logs


if __name__ == "__main__":
    grader = Grader()
    # getting the unpushed files path
    try:
        files = main()

        if files:
            for filename, file_path in files:
                logger.debug(file_path, filename)
                if "Instructor" in filename.split(".")[0]: 
                    create_logs(filename=filename)
                   
                    nb, resources =  grader.check_instructor_file(instructor_file=file_path)
                    logger.debug(resources)
        else:
            create_logs("sdaffasf")
            logger.debug("files arenot pushed")           
                       
            # except FileNotFoundError as err:
            #     logger.debug(err)
            # except NotebookExecutionFailed as err:
            #     logger.debug(err)
            # except ScoreNotMatch as err:
            #     logger.debug(err)
    
    except Exception as err:
        logger.debug(err)