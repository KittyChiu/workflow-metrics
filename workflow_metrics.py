"""
workflow_metrics.py - Retrieve and evaluate GitHub Actions workflow runs for a repository.

The script uses the GitHub API to retrieve workflow runs for the specified repository or repositories inside an org, and
calculates metrics such as the average duration, median duration, success rate, and total number of runs for
each workflow. 

The following environment variables must be set:

- OWNER_NAME: The name of the repository owner (e.g. "myorg").
- START_DATE: The start date of the date range in ISO format (e.g. "2022-01-01").
- END_DATE: The end date of the date range in ISO format (e.g. "2022-01-31").
- REPO_NAME: Optional - The name of the repository (e.g. "myrepo").
- DELAY_BETWEEN_QUERY: Optional - The number of seconds to wait between queries to the GitHub API. 

The script uses the following external tools:

- `gh` (GitHub CLI): Used to authenticate with GitHub and retrieve workflow runs.
- `jq`: Used to extract workflow names from the workflow runs JSON.

The script outputs the following files:

- `runs.json`: Workflow runs in JSON, or `org-runs.json`: Workflow runs in JSON for every repo in the org.
- `workflow-stats.csv`: Workflow statistics in CSV, or `org-workflow-stats.csv`: Workflow statistics in CSV for every repo in the org.

Usage: python workflow_metrics.py
"""

import os
import subprocess
import time
import json

# Get environment variables
gh_token = os.getenv("GH_TOKEN")
if not gh_token:
    raise ValueError("GITHUB_TOKEN environment variable not set")

owner_name = os.getenv("OWNER_NAME")
if not owner_name:
    raise ValueError("OWNER_NAME environment variable not set")

start_date = os.getenv("START_DATE")
if not start_date:
    raise ValueError("START_DATE environment variable not set")

end_date = os.getenv("END_DATE")
if not end_date:
    raise ValueError("END_DATE environment variable not set")

repo_name = os.getenv("REPO_NAME")

sleep_time = os.getenv("DELAY_BETWEEN_QUERY")


# Authenticate with GitHub CLI
subprocess.run(['gh', 'auth', 'login', '--with-token'], input=gh_token.encode())

# Get list of repository names if no repository name is specified
if not repo_name:
    # Get list of repository names
    cmd = f'gh api orgs/{owner_name}/repos --jq \'.[] | .name\''
    query_output = subprocess.check_output(cmd, shell=True, text=True)
    repo_names = []
    for line in query_output.strip().split('\n'):
        repo_names.append(line)

    with open('org-workflow-stats.csv', 'w') as f:
        f.write('repository_name,workflow_name,average_duration,median_duration,success_rate,total_runs\n')
    # create a file for org-runs.json 
    with open('org-runs.json', 'w') as f:
        f.write('[\n')

    # Get workflow runs for each repository
    for repo in repo_names:

        # Get workflow runs
        subprocess.run(['python', 'get_workflow_runs.py', owner_name, repo, start_date, end_date])
        # Read every JSON record in runs.json, add repo name to each record, and append to org-runs.json
        with open('runs.json', 'r') as f1, open('org-runs.json', 'a') as f2:
            data = json.load(f1)
            for record in data:
                record['repository_name'] = str(repo)
            for i, record in enumerate(data):
                json.dump(record, f2)
                if i != len(data) - 1:
                    f2.write(',\n')
                else:
                    f2.write('\n]')

        # Evaluate workflow runs statistics
        subprocess.run(['python', 'evaluate_workflow_runs.py'])
        # Read every line of workflow-stats.csv skipping the header line, add repo name to the beginning of each line, and write to all-workflow-stats.csv
        with open('workflow-stats.csv', 'r') as f:
            lines = f.readlines()
            with open('org-workflow-stats.csv', 'a') as f2:
                for line in lines[1:]:
                    f2.write(f'{repo},{line}')
        if sleep_time:
            print(f'  Sleeping for {sleep_time} seconds to prevent rate limiting...')
            time.sleep(int(sleep_time))

else:
    # Get workflow runs
    subprocess.run(['python', 'get_workflow_runs.py', owner_name, repo_name, start_date, end_date])

    # Evaluate workflow runs statistics
    subprocess.run(['python', 'evaluate_workflow_runs.py'])
