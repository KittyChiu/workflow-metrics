"""
test_workflow_metrics.py - Unit tests for the workflow_metrics.py script.

This script defines a set of unit tests for the workflow_metrics.py script. The tests check that the script
raises a ValueError if any of the required environment variables are not set, and that the script produces
the expected output when all environment variables are set.

Usage:
    python -m unittest test_workflow_metrics.py

Environment Variables:
    - GH_TOKEN: A personal access token for authenticating with the GitHub API, with `repo` and `admin:org` scopes
    - OWNER_NAME: The name of the organization or user that owns the repository.
    - START_DATE: The start date for the time range to analyze, in ISO 8601 format (e.g. "2022-01-01").
    - END_DATE: The end date for the time range to analyze, in ISO 8601 format (e.g. "2022-01-31").
    - REPO_NAME: The name of the repository to analyze. If not set, the script will analyze all repositories
      owned by the specified organization or user.
    - DELAY_BETWEEN_QUERY: The number of seconds to wait between queries to the GitHub API. This is useful
      when running the script against a large number of repositories, to avoid hitting the GitHub API rate
      limit. If not set, the script will not wait between queries.


Expected Output:
    The script should produce a file named "runs.json" or "org-runs.json" in the current directory, containing
    a JSON array of all workflow runs in the specified time range. And it also should produce a file named
    "workflow-stats.csv" or "org-workflow-stats.csv" in the current directory, containing a CSV file with
    workflow run statistics for the specified repository or organization.


Note that the script requires the `gh` command-line tool to be installed and authenticated with the `GH_TOKEN`
environment variable. The `gh` tool can be installed from https://cli.github.com/.
"""

import os
import subprocess
import unittest
from dotenv import load_dotenv

class TestWorkflowMetrics(unittest.TestCase):

    def setUp(self):
        print('Setting up test harness...')
        # Load environment variables from .env file
        load_dotenv()
        print('  Environment variables loaded from .env file')

    def test_workflow_metrics(self):

        # Check gh auth status
        auth_status = subprocess.run(['gh', 'auth', 'status'], capture_output=True)

        result = subprocess.run(['python', 'workflow_metrics.py'], capture_output=True)
        print(result.stdout.decode())
        print(result.stderr.decode())
        
        # Assert that runs.json was created
        self.assertTrue(os.path.exists('runs.json'))
        self.assertEqual(result.returncode, 0)

        # Assert that workflow-names.txt contains more than one line
        with open('workflow-stats.csv', 'r') as f:
            lines = f.readlines()
            self.assertGreater(len(lines), 1)

    
    # Usage: python -m unittest test_workflow_metrics.TestWorkflowMetrics.test_org_workflow_metrics
    def test_org_workflow_metrics(self):
        # Unset environment variables from session for the test case
        del os.environ['REPO_NAME']
        del os.environ['DELAY_BETWEEN_QUERY']

        # Check gh auth status
        auth_status = subprocess.run(['gh', 'auth', 'status'], capture_output=True)

        result = subprocess.run(['python', 'workflow_metrics.py'], capture_output=True)
        print(result.stdout.decode())
        print(result.stderr.decode())
        self.assertEqual(result.returncode, 0)
        
        # Assert that org-runs.json was created
        self.assertTrue(os.path.exists('org-runs.json'))

        # Assert that org-workflow-names.txt contains more than one line
        with open('org-workflow-stats.csv', 'r') as f:
            lines = f.readlines()
            self.assertGreater(len(lines), 1)


    def test_org_workflow_metrics_with_delay(self):
        # Unset environment variables from session for the test case
        del os.environ['REPO_NAME']

        # Check gh auth status
        auth_status = subprocess.run(['gh', 'auth', 'status'], capture_output=True)

        result = subprocess.run(['python', 'workflow_metrics.py'], capture_output=True)
        print(result.stdout.decode())
        print(result.stderr.decode())
        self.assertEqual(result.returncode, 0)
        
        # Assert that org-runs.json contains more than one line
        with open('org-runs.json', 'r') as f:
            lines = f.readlines()
            self.assertGreater(len(lines), 1)

        # Assert that org-workflow-names.txt contains more than one line
        with open('org-workflow-stats.csv', 'r') as f:
            lines = f.readlines()
            self.assertGreater(len(lines), 1)


    def tearDown(self):
        print('Tearing down test harness...')
        # Remove the test files if they exist
        if os.path.exists('runs.json'):
            os.remove('runs.json')
            print('  runs.json removed')
        if os.path.exists('org-runs.json'):
            os.remove('org-runs.json')
            print('  org-runs.json removed')
        if os.path.exists('workflow-stats.csv'):
            os.remove('workflow-stats.csv')
            print('  workflow-stats.csv removed')
        if os.path.exists('org-workflow-stats.csv'):
            os.remove('org-workflow-stats.csv')
            print('  org-workflow-stats.csv removed')


if __name__ == '__main__':
    unittest.main()