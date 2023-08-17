"""
This file contains unit tests for the `get_workflow_runs.py` script.

Usage:
    python -m unittest test_get_workflow_runs.TestGetWorkflowRuns.test_get_workflow_runs

Requirements:
    - Python 3.x
    - `jq` command-line tool
    - `get_workflow_runs.py` script to test

Description:
    This script contains unit tests for the `get_workflow_runs.py` script. The tests verify that the script correctly
    retrieves workflow runs from the GitHub API within the specified date range, and outputs the runs to a JSON file.

    To run the tests, you need to have Python 3.x and the `jq` command-line tool installed on your system. You also
    need to be authenticated with the GitHub API with `repo` scope.

    The tests use the `unittest` module in Python to define test cases and assertions. Each test case corresponds to
    a specific function in the `get_workflow_runs.py` script, and tests the function's behavior under different
    conditions.

    To run the tests, you can use the following command:

        python -m unittest test_get_workflow_runs.TestGetWorkflowRuns.test_get_workflow_runs

    This command runs the `test_get_workflow_runs()` function in the `TestGetWorkflowRuns` class, which executes all
    the test cases defined in the class.

Output:
    - Test results for the `get_workflow_runs.py` script

Example:
    python -m unittest test_get_workflow_runs.py
"""
import unittest
import subprocess
import json
import os

from dotenv import load_dotenv

class TestGetWorkflowRuns(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        self.repo_owner = os.getenv("OWNER_NAME")
        self.repo_name = os.getenv("REPO_NAME")
        self.start_date = os.getenv("START_DATE")
        self.end_date = os.getenv("END_DATE")
        self.invalid_start_date = "abc"
        self.invalid_end_date = "xyz"

    def test_get_workflow_runs_with_valid_dates(self):
        # Run the script to retrieve workflow runs with valid dates
        subprocess.run(["python", "get_workflow_runs.py", self.repo_owner, self.repo_name, self.start_date, self.end_date])

        # Load the workflow runs from file
        with open("runs.json", "r") as f:
            workflow_runs = json.load(f)

        # Check that the workflow runs are not empty
        self.assertGreater(len(workflow_runs), 0)

        # Check that each workflow run has the expected fields
        for run in workflow_runs:
            self.assertIn("conclusion", run)
            self.assertIn("created_at", run)
            self.assertIn("display_title", run)
            self.assertIn("event", run)
            self.assertIn("head_branch", run)
            self.assertIn("name", run)
            self.assertIn("run_number", run)
            self.assertIn("run_started_at", run)
            self.assertIn("run_attempt", run)
            self.assertIn("status", run)
            self.assertIn("updated_at", run)
            self.assertIn("url", run)
            self.assertIn("duration", run)

        # Print the workflow runs
        with open("runs.json", "r") as f:
            raw_json = f.read()
            print("Number of characters in runs.json:", len(raw_json))

        # Clean up the temporary file
        os.remove("runs.json")

    def test_get_workflow_runs_with_invalid_dates(self):
        # Run the script to retrieve workflow runs with invalid dates
        subprocess.run(["python", "get_workflow_runs.py", self.repo_owner, self.repo_name, self.invalid_start_date, self.invalid_end_date])

        # Check that the runs.json file does not exist
        self.assertFalse(os.path.exists("runs.json"))

if __name__ == '__main__':
    unittest.main()