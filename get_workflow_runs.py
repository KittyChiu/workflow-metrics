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
    - `jq` command-line tool

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

    To run the script, you need to have Python 3.x and the `jq` command-line tool installed on your system. You also
    need to have a GitHub API token with the `repo` scope.

Output:
    - A list of workflow runs in JSON format

Example:
    python get_workflow_runs.py octocat hello-world 2022-01-01 2022-01-31
"""

import subprocess
import json
import sys

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
    start_date = datetime.fromisoformat(start_date)
    end_date = datetime.fromisoformat(end_date)
except ValueError:
    print('Error: Invalid date format. Please use ISO format (YYYY-MM-DD).')
    sys.exit(1)
    
# Parse jq query for gh api command
jq_query = (
    f'[.workflow_runs[] '
    f'| select(.run_started_at >= "{start_date}" and .run_started_at <= "{end_date}") '
    f'| {{conclusion,created_at,display_title,event,head_branch,name,run_number,run_started_at,run_attempt,status,updated_at,url}}] '
    f'| select(length > 0)'
)

# Construct the gh api command
cmd = f'gh api repos/{repo_owner}/{repo_name}/actions/runs --paginate --jq \'{jq_query}\''

# Send the command and retrieve the output
output = subprocess.check_output(cmd, shell=True, text=True)

# Parse the output as JSON and return the workflow runs
workflow_runs = []
for line in output.strip().split('\n'):
    try:
        data = json.loads(line)
        if isinstance(data, list):
            workflow_runs.extend(data)
        else:
            workflow_runs.append(data)
    except json.JSONDecodeError:
        pass

# Add the duration field to each workflow run, calculated as the difference between the updated_at and run_started_at fields
for item in workflow_runs:
    updated_at = datetime.fromisoformat(item['updated_at'].replace('Z', '+00:00'))
    run_started_at = datetime.fromisoformat(item['run_started_at'].replace('Z', '+00:00'))
    duration = (updated_at - run_started_at).total_seconds()
    item['duration'] = duration

# Print the workflow runs as raw.json file
with open(RUNS_FILE, 'w') as f:
    json.dump(workflow_runs, f)

# Print the number of workflow runs 
print(f'[{repo_owner}/{repo_name}]: No. of workflow runs: {len(workflow_runs)}')
