"""
This script evaluates the stats for each workflow in the `runs.json` file and outputs the results to a CSV file.

Usage:
    python evaluate_workflow_runs.py

Requirements:
    - Python 3.x
    - `runs.json` file containing the workflow runs to evaluate
    - `workflow-names.txt` file containing the unique workflow names to evaluate

Description:
    This script reads the `runs.json` file and extracts the workflow runs for each workflow specified in the
    `workflow-names.txt` file. For each workflow, the script calculates the average duration of the successful runs,
    the total number of runs, and the success rate (i.e. the percentage of successful runs).

    The script outputs the results to a CSV file named `workflow-stats.csv`, which contains the stats for each
    workflow. The CSV file has the following columns:

        - Workflow name
        - Average duration of successful runs (in seconds)
        - Total number of runs
        - Success rate (in percentage)

    To run the script, you need to have Python 3.x installed on your system. You also need to have the `runs.json`
    file and the `workflow-names.txt` file in the same directory as the script.

Output:
    - `workflow-stats.csv` file containing the stats for each workflow

Example:
    python evaluate_workflow_runs.py
"""

import json
import statistics

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
        success_rate = '0.0'

    # Output the results to a CSV file
    with open('workflow-stats.csv', 'a') as f:
        # Add header row if file is empty
        if f.tell() == 0:
            f.write('workflow_name,average_duration,median_duration,success_rate,total_runs\n')
        f.write(f'{workflow_name},{average_duration},{median_duration},{success_rate},{total_runs}\n')