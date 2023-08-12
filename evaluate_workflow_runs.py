"""
This script evaluates the stats for each workflow in the `runs.json` file and outputs the results to a CSV file.

Usage:
    python evaluate_workflow_runs.py

Requirements:
    - Python 3.x
    - `runs.json` file containing the workflow runs to evaluate
    - `workflow-names.txt` file containing the unique workflow names to evaluate

Output:
    - `workflow-stats.csv` file containing the stats for each workflow

Example:
    python evaluate_workflow_runs.py
"""

import json

# Load the workflow names from the workflow-names.txt file
with open('workflow-names.txt', 'r') as f:
    workflow_names = f.read().splitlines()

# Evaluate the stats for each workflow
for workflow_name in workflow_names:
    print(f'Evaluating: {workflow_name}')

    # Filter the runs by workflow name
    with open('runs.json', 'r') as f:
        runs = json.load(f)
    runs_filtered = [run for run in runs if run['name'] == workflow_name]

    # Evaluate the total number of runs
    total_runs = len(runs_filtered)
    # print(f'...Total runs: {total_runs}')

    # Evaluate the average duration
    if total_runs > 0:
        raw_average_duration = sum(run['duration'] for run in runs_filtered) / total_runs
        average_duration = f'{raw_average_duration:.2f}s'
    else:
        average_duration = '0.00s'
    # print(f'...Average duration: {average_duration}')

    # Evaluate the number of successful or skipped runs
    total_success = len([run for run in runs_filtered if run['conclusion'] in ['success', 'skipped']])
    # print(f'...Total success or skipped runs: {total_success}')

    # Evaluate the percentage of successful or skipped runs
    if total_runs > 0:
        percentage_success = f'{total_success / total_runs * 100:.1f}%'
    else:
        percentage_success = '0.0%'
    # print(f'...Percentage success or skipped runs: {percentage_success}')

    # Output the results to a CSV file
    with open('workflow-stats.csv', 'a') as f:
        f.write(f'{workflow_name},{average_duration},{percentage_success},{total_runs}\n')