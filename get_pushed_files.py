import os
from git import Repo, GitCommandError

from loguru import logger

def get_committed_files_with_status(repo_path, commit='HEAD'):
    try:
        repo = Repo(repo_path)
    except GitCommandError as e:
        logger.error(f"Error initializing the repository: {e}")
        return []
    
    try:
        # Get the commit object
        commit_obj = repo.commit(commit)
        
        # Get the parent commit (if it exists)
        parent_commit = commit_obj.parents[0] if commit_obj.parents else None
        
        added_ipynb_files = []
        
        if parent_commit:
            diff = parent_commit.diff(commit_obj)
        else:
            # If there is no parent, this is the initial commit; compare to NULL_TREE
            diff = commit_obj.diff(NULL_TREE)
        
        for diff_item in diff:
            status = 'modified'
            if diff_item.new_file and diff_item.a_path.endswith('.ipynb'):
                added_ipynb_files.append(diff_item.a_path)
            # elif diff_item.deleted_file:
            #     status = 'deleted'
            # elif diff_item.renamed:
            #     status = 'renamed'
            
            # committed_files.append({
            #     'path': diff_item.a_path,
            #     'status': status
            # })
        
        return added_ipynb_files
    except GitCommandError as e:
        logger.error(f"Error processing the diff: {e}")
        return []

def main():
    # Path to the local Git repository
    repo_path = './'

    result = []
    
    # Ensure the path exists
    # Ensure the path exists
    if not os.path.exists(repo_path):
        logger.error(f"Repository path {repo_path} does not exist.")
        return
    
    # Get the committed files with their statuses
    files = get_committed_files_with_status(repo_path)
    
    # Output the files and their statuses
    logger.debug("Committed files:")
    if files:   
        for file in files:
            logger.debug(f"{file}")
            result.append((file.split("/")[-1], file))

    return result

if __name__ == "__main__":
    main()
