import os
import json
import logging

# Create logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)

# Configure logging to save logs in a file
logging.basicConfig(
    filename='logs/track_ipynb_files.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def get_ipynb_files(commits):
    ipynb_files = {
        'added': [],
        'renamed': [],
        'modified': []
    }

    for commit in commits:
        # Added files
        for file in commit.get('added', []):
            if file.endswith('.ipynb'):
                ipynb_files['added'].append(file)
        
        # Modified files
        for file in commit.get('modified', []):
            if file.endswith('.ipynb'):
                ipynb_files['modified'].append(file)
        
        # Renamed files
        for file in commit.get('removed', []):
            if file.endswith('.ipynb'):
                ipynb_files['renamed'].append(file)

        for file in commit.get('added', []):
            if file.endswith('.ipynb') and file not in ipynb_files['added']:
                ipynb_files['renamed'].append(file)

    return ipynb_files

def main():
    # Get the GitHub event path from environment variables
    github_event_path = os.getenv('GITHUB_EVENT_PATH')
    logging.debug(f"GITHUB_EVENT_PATH: {github_event_path}")
    
    if not github_event_path or not os.path.exists(github_event_path):
        logging.error(f"GITHUB_EVENT_PATH {github_event_path} does not exist.")
        return
    
    # Load the event data
    with open(github_event_path, 'r') as f:
        event_data = json.load(f)
    
    # Log the event data path
    logging.info(f"Event data loaded from: {github_event_path}")

    # Log the event data path
    logging.info(f"Event data: {event_data}")
    
    # Extract the commits
    commits = event_data.get('commits', [])
    
    # Get the .ipynb files
    ipynb_files = get_ipynb_files(commits)
    
    # Output the files
    if ipynb_files['added']:
        logging.info("Added .ipynb files:")
        for file in ipynb_files['added']:
            logging.info(file)
    
    if ipynb_files['renamed']:
        logging.info("Renamed .ipynb files:")
        for file in ipynb_files['renamed']:
            logging.info(file)
    
    if ipynb_files['modified']:
        logging.info("Modified .ipynb files:")
        for file in ipynb_files['modified']:
            logging.info(file)

if __name__ == "__main__":
    main()

