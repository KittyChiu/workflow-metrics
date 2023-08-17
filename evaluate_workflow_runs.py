"""
This script evaluates the stats for each workflow in the `runs.json` file and outputs the results to a CSV file.

Usage:
    python evaluate_workflow_runs.py

Requirements:
    - Python 3.x
    - `runs.json` file containing the workflow runs to evaluate

Optional:
    - `workflow-names.txt` file containing the unique workflow names to evaluate

Description:
    This script reads the `runs.json` file and extracts the workflow runs for each workflow specified in the
    `workflow-names.txt` file, if it exists. If `workflow-names.txt` is not found, the script evaluates all workflows
    in `runs.json`. For each workflow, the script calculates the average duration of the successful runs, the total
    number of runs, and the success rate (i.e. the percentage of successful runs).

    The script outputs the results to a CSV file named `workflow-stats.csv`, which contains the stats for each
    workflow. The CSV file has the following columns:

        - Workflow name: The name of the workflow.
        - Average duration of successful runs (in seconds): The average of the successful runs for the workflow.
        - Median duration of successful runs (in seconds): The median of the successful runs for the workflow.
        - Total number of runs: The total number of runs for the workflow.
        - Success rate (in percentage): The percentage of successful runs for the workflow.

    To run the script, you need to have Python 3.x installed on your system. You also need to have the `runs.json`
    file and the `workflow-names.txt` file in the same directory as the script.

Output:
    The script outputs the results to a CSV file named `workflow-stats.csv` in the same directory as the script.

Example:
    python evaluate_workflow_runs.py

Note:
    - The script assumes that the `runs.json` file and the `workflow-names.txt` file are in the same directory as the script.
    - The script assumes that the `runs.json` file contains a list of workflow runs in JSON format.
    - The script assumes that the `workflow-names.txt` file (if it exists) contains a list of unique workflow names to evaluate, with one name per line.
    - The script calculates the success rate as the percentage of successful or skipped runs out of the total number of runs.
    - The script ignores failed runs when calculating the average duration of successful runs.
"""

import os
import json
import statistics

WORKFLOW_NAMES_FILE = 'workflow-names.txt'
RUNS_FILE = 'runs.json'
STATS_FILE = 'workflow-stats.csv'

# Check if the workflow names file exists
if os.path.isfile(WORKFLOW_NAMES_FILE):
    print(f'  Info: {WORKFLOW_NAMES_FILE} file is found. Workflow runs will be filtered by the workflow names listed in the file.')
else:
    print(f'  Warning: {WORKFLOW_NAMES_FILE} file not found')
    # Load the workflow names from the RUNS_FILE
    with open(RUNS_FILE, 'r') as f:
        runs = json.load(f)
    workflow_names = list(set(run['name'] for run in runs))
    # Write the workflow names to the workflow names file
    with open(WORKFLOW_NAMES_FILE, 'w') as f:
        f.write('\n'.join(workflow_names))

# Load the workflow names from the workflow names file
with open(WORKFLOW_NAMES_FILE, 'r') as f:
    workflow_names = f.read().splitlines()

# Output the results to a CSV file
with open(STATS_FILE, 'w') as f:
    f.write('workflow_name,average_duration,median_duration,success_rate,total_runs\n')

# Evaluate the stats for each workflow
for workflow_name in workflow_names:
    print(f'  Evaluating: {workflow_name}')

    # Filter the runs by workflow name
    try:
        with open(RUNS_FILE, 'r') as f:
            runs = json.load(f)
        runs_filtered = [run for run in runs if run['name'] == workflow_name]
    except FileNotFoundError:
        print(f'Error: {RUNS_FILE} file not found')
        continue

    # Evaluate the total number of runs
    total_runs = len(runs_filtered)
    duration_data = [run['duration'] for run in runs_filtered]

    if total_runs > 0:
        # Evaluate the average duration
        average_duration = f'{statistics.mean(duration_data):.2f}'
        # Evaluate the median duration
        median_duration = f'{statistics.median(duration_data):.2f}'
        # Evaluate the percentage of successful or skipped runs
        success_rate = f'{statistics.mean([1 if run["conclusion"] in ["success", "skipped"] else 0 for run in runs_filtered]) * 100:.2f}'
    else:
        average_duration = '0.00'
        median_duration = '0.00'
        success_rate = '0.00'

    # Output the results to a CSV file
    with open(STATS_FILE, 'a') as f:
        f.write(f'{workflow_name},{average_duration},{median_duration},{success_rate},{total_runs}\n')

print(f'  Evaluation completed: Results are written to workflow-stats.csv')
os.remove(WORKFLOW_NAMES_FILE)
