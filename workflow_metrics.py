"""
workflow_metrics.py - Retrieve and evaluate GitHub Actions workflow runs for a repository.

This script retrieves the workflow runs for a specified repository and date range, and evaluates statistics
for each workflow. The following environment variables must be set:

- OWNER_NAME: The name of the repository owner (e.g. "myorg").
- REPO_NAME: The name of the repository (e.g. "myrepo").
- START_DATE: The start date of the date range in ISO format (e.g. "2022-01-01").
- END_DATE: The end date of the date range in ISO format (e.g. "2022-01-31").

The script uses the following external tools:

- `gh` (GitHub CLI): Used to authenticate with GitHub and retrieve workflow runs.
- `jq`: Used to extract workflow names from the workflow runs JSON.

The script outputs the following files:

- `runs.json`: The raw workflow runs JSON.
- `workflow-names.txt`: A list of unique workflow names extracted from the workflow runs.
- `workflow-stats.csv`: A CSV file containing statistics for each workflow.

Usage: python workflow_metrics.py
"""

import os
import subprocess

# Get environment variables
gh_token = os.getenv("GH_TOKEN")
if not gh_token:
    raise ValueError("GITHUB_TOKEN environment variable not set")

owner_name = os.getenv("OWNER_NAME")
if not owner_name:
    raise ValueError("OWNER_NAME environment variable not set")

repo_name = os.getenv("REPO_NAME")
if not repo_name:
    raise ValueError("REPO_NAME environment variable not set")

start_date = os.getenv("START_DATE")
if not start_date:
    raise ValueError("START_DATE environment variable not set")

end_date = os.getenv("END_DATE")
if not end_date:
    raise ValueError("END_DATE environment variable not set")

# Authenticate with GitHub CLI
subprocess.run(['gh', 'auth', 'login', '--with-token', gh_token])

# Get workflow runs
subprocess.run(['python', 'get_workflow_runs.py', owner_name, repo_name, start_date, end_date])
with open('runs.json', 'r') as f:
    print(f.read())

# Get list of workflow names from runs.json
result1 = subprocess.run(['jq', '[.[] | .name ] | unique', 'runs.json'], stdout=subprocess.PIPE)
result2 = subprocess.run(['jq', '-r', '.[]'], input=result1.stdout, stdout=subprocess.PIPE)

# Write workflow names to workflow-names.txt
with open('workflow-names.txt', 'w') as f:
    f.write(result2.stdout.decode())

with open('workflow-names.txt', 'r') as f:
    print(f.read())

# Evaluate workflow runs statistics
print("Evaluating workflow runs statistics")
subprocess.run(['python', 'evaluate_workflow_runs.py'])
with open('workflow-stats.csv', 'r') as f:
    print(f.read())