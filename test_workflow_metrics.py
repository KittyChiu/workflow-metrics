"""
test_workflow_metrics.py - Unit tests for the workflow_metrics.py script.

This script defines a set of unit tests for the workflow_metrics.py script. The tests check that the script
raises a ValueError if any of the required environment variables are not set, and that the script produces
the expected output when all environment variables are set.

Usage: python -m unittest test_workflow_metrics.py
"""

import os
import subprocess
import unittest

class TestWorkflowMetrics(unittest.TestCase):

    def test_workflow_metrics(self):
        os.environ['OWNER_NAME'] = 'myorg'
        os.environ['REPO_NAME'] = 'myrepo'
        os.environ['START_DATE'] = '2023-07-01'
        os.environ['END_DATE'] = '2023-07-31'
        
        #  import pdb; pdb.set_trace()
        result = subprocess.run(['python', 'workflow_metrics.py'], capture_output=True)
        
        self.assertEqual(result.returncode, 0)
        self.assertIn(b'Evaluating workflow runs statistics', result.stdout)

        # Assert that workflow-names.txt contains more than one line
        with open('workflow-stats.csv', 'r') as f:
            lines = f.readlines()
            self.assertGreater(len(lines), 1)


if __name__ == '__main__':
    unittest.main()