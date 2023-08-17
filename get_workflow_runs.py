"""
Retrieves all workflow runs for a repository within the specified date range.

Usage:
    python get_workflow_runs.py <repo_owner> <repo_name> <start_date> <end_date>

Arguments:
    repo_owner (str): The owner of the repository.
    repo_name (str): The name of the repository.
    start_date (str): The start date of the date range in ISO 8601 format.
    end_date (str): The end date of the date range in ISO 8601 format.

Returns:
    A list of workflow runs with the following fields:
    - conclusion
    - created_at
    - display_title
    - event
    - head_branch
    - name
    - run_number
    - run_started_at
    - status
    - updated_at
    - url
    - duration

Requirements:
    - Python 3.x
    - jq
    - requests

Description:
    This script retrieves all workflow runs for a repository within the specified date range. The script takes four
    command-line arguments: the owner of the repository, the name of the repository, the start date of the date range,
    and the end date of the date range. The start and end dates should be in ISO 8601 format.

    The script uses the GitHub API to retrieve the workflow runs for the specified repository and date range. The
    script requires authentication with `repo` scope with the API.

    The script outputs a list of workflow runs in JSON format, with the following fields for each run:

        - conclusion
        - created_at
        - display_title
        - event
        - head_branch
        - name
        - run_number
        - run_started_at
        - status
        - updated_at
        - url
        - duration

    To run the script, you need to have a GitHub API token with the `repo` scope.

Output:
    - A list of workflow runs in JSON format

Example:
    python get_workflow_runs.py octocat hello-world 2022-01-01 2022-01-31
"""

import json
import sys
import requests
import os
import jq

from datetime import datetime

RUNS_FILE = 'runs.json'

# Parse the command-line arguments
if len(sys.argv) != 5:
    print('Usage: python get_workflow_runs.py <repo_owner> <repo_name> <start_date> <end_date>')
    sys.exit(1)

repo_owner = sys.argv[1]
repo_name = sys.argv[2]
start_date = sys.argv[3]
end_date = sys.argv[4]

# Validate the start_date and end_date arguments
try:
    start_date = datetime.fromisoformat(start_date).date()
    end_date = datetime.fromisoformat(end_date).date()
except ValueError:
    print('Error: Invalid date format. Please use ISO format (YYYY-MM-DD).')
    sys.exit(1)
    
# Define the jq query
jq_query = (
    f'.workflow_runs[] '
    f'| select(.run_started_at >= "{start_date}" and .run_started_at <= "{end_date}") '
    f'| {{conclusion,created_at,display_title,event,head_branch,name,run_number,run_started_at,run_attempt,status,updated_at,url}} '
    f'| select(length > 0)'
)
# Construct the GitHub API URL
url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/actions/runs?per_page=100&created={start_date}..{end_date}'

# Authenticate with the GitHub API using a personal access token
access_token = os.environ.get('GH_TOKEN')
if access_token is None:
    raise ValueError('GH_TOKEN environment variable is not set')
headers = {'Accept': 'application/vnd.github.v3+json', 'Authorization': f'token {access_token}'}

# Send the API request and retrieve the JSON response
response = requests.get(url, headers=headers)
response.raise_for_status()
data = response.json()
# Filter the data using the jq query
program = jq.compile(jq_query)
filtered_data = program.input(data).all()

# Calculate the duration for each workflow run
workflow_runs = []
for item in filtered_data:
    try:
        updated_at = datetime.fromisoformat(item['updated_at'].replace('Z', '+00:00'))
        run_started_at = datetime.fromisoformat(item['run_started_at'].replace('Z', '+00:00'))
        duration = (updated_at - run_started_at).total_seconds()
        item['duration'] = duration
        workflow_runs.append(item)
    except (KeyError, ValueError):
        pass

# Print the workflow runs as raw.json file
with open(RUNS_FILE, 'w') as f:
    json.dump(workflow_runs, f)

# Print the number of workflow runs 
print(f'[{repo_owner}/{repo_name}]: No. of workflow runs: {len(workflow_runs)}')
