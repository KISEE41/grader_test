import os
import json
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def get_ipynb_files(commits):
    ipynb_files = {
        'added': [],
        'renamed': [],
        'modified': []
    }

    for commit in commits:
        for file in commit.get('added', []):
            if file.endswith('.ipynb'):
                ipynb_files['added'].append(file)
        
        for file in commit.get('modified', []):
            if file.endswith('.ipynb'):
                ipynb_files['modified'].append(file)
        
        for rename in commit.get('renamed', []):
            if rename['previous_filename'].endswith('.ipynb') or rename['filename'].endswith('.ipynb'):
                ipynb_files['renamed'].append(rename)

    return ipynb_files

def main():
    # Get the GitHub event path from environment variables
    github_event_path = os.getenv('GITHUB_EVENT_PATH')
    
    if not github_event_path or not os.path.exists(github_event_path):
        logging.error(f"GITHUB_EVENT_PATH {github_event_path} does not exist.")
        return
    
    # Load the event data
    with open(github_event_path, 'r') as f:
        event_data = json.load(f)
        logging.debug(event_data)
    
    # Extract the commits
    commits = event_data.get('commits', [])
    
    # Get the .ipynb files
    ipynb_files = get_ipynb_files(commits)
    
    # Output the files
    if ipynb_files['added']:
        logging.info("Added .ipynb files:")
        for file in ipynb_files['added']:
            logging.info(file)
    else:
        logging.info("No files")
    
    if ipynb_files['renamed']:
        logging.info("Renamed .ipynb files:")
        for rename in ipynb_files['renamed']:
            logging.info(f"{rename['previous_filename']} -> {rename['filename']}")
    else:
        logging.info("No files")
    
    if ipynb_files['modified']:
        logging.info("Modified .ipynb files:")
        for file in ipynb_files['modified']:
            logging.info(file)
    else:
        logging.info("No files")

if __name__ == "__main__":
    main()
