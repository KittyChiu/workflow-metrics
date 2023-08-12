"""
This file contains unit tests for the `evaluate_workflow_runs.py` script.

Usage:
    python -m unittest test_evaluate_workflow_runs.TestEvaluateWorkflowRuns.test_evaluate_workflow_runs

Requirements:
    - Python 3.x
    - `jq` command-line tool
    - `evaluate_workflow_runs.py` script to test

Output:
    - Test results for the `evaluate_workflow_runs.py` script

Example:
    python -m unittest test_evaluate_workflow_runs.TestEvaluateWorkflowRuns.test_evaluate_workflow_runs
"""

import unittest
import json
import subprocess
import os

class TestEvaluateWorkflowRuns(unittest.TestCase):
    def test_evaluate_workflow_runs(self):
        # For debug: Print the contents of the runs.json file
        # with open('runs.json', 'r') as f:
        #     runs_contents = f.read()
        # print(runs_contents)

        # For debug: Print the contents of the workflow-names.txt file
        # with open('workflow-names.txt', 'r') as f:
        #     names_contents = f.read()
        # print(names_contents)

        # Run the evaluate-workflow-runs.py script
        subprocess.run(['python', 'evaluate_workflow_runs.py'])

        # Check the contents of the workflow-stats.csv file
        with open('workflow-stats.csv', 'r') as f:
            csv_contents = f.read()

        expected_csv_contents = 'workflow_1,12.33s,100.0%,3\nworkflow_2,15.50s,50.0%,2\nworkflow_3,25.12s,20.9%,43\n'
        self.assertEqual(csv_contents, expected_csv_contents)
        #print(csv_contents)

    def tearDown(self):
        # Remove the test files
        os.remove('workflow-names.txt')
        os.remove('runs.json')
        os.remove('workflow-stats.csv')

    def setUp(self):
        # Create a test workflow-names.txt file
        with open('workflow-names.txt', 'w') as f:
            f.write('workflow_1\nworkflow_2\nworkflow_3\n')

        # Create a test runs.json file
        runs = [
          {
            "conclusion": "success",
            "created_at": "2023-08-05T01:50:57Z",
            "display_title": "workflow_1",
            "event": "schedule",
            "head_branch": "main",
            "name": "workflow_1",
            "run_attempt": 1,
            "run_number": 109,
            "run_started_at": "2023-08-05T01:50:57Z",
            "status": "completed",
            "updated_at": "2023-08-05T01:51:09Z",
            "url": "https://repo-url/actions/runs/5768112009",
            "duration": 12
          },
          {
            "conclusion": "success",
            "created_at": "2023-08-04T01:52:27Z",
            "display_title": "workflow_1",
            "event": "schedule",
            "head_branch": "main",
            "name": "workflow_1",
            "run_attempt": 1,
            "run_number": 108,
            "run_started_at": "2023-08-04T01:52:27Z",
            "status": "completed",
            "updated_at": "2023-08-04T01:52:39Z",
            "url": "https://repo-url/actions/runs/5757521092",
            "duration": 12
          },
          {
            "conclusion": "success",
            "created_at": "2023-08-03T01:51:55Z",
            "display_title": "workflow_1",
            "event": "schedule",
            "head_branch": "main",
            "name": "workflow_1",
            "run_attempt": 1,
            "run_number": 107,
            "run_started_at": "2023-08-03T01:51:55Z",
            "status": "completed",
            "updated_at": "2023-08-03T01:52:08Z",
            "url": "https://repo-url/actions/runs/5745695002",
            "duration": 13
          },
          {
            "conclusion": "success",
            "created_at": "2023-08-02T22:40:38Z",
            "display_title": "workflow_3",
            "event": "workflow_dispatch",
            "head_branch": "main",
            "name": "workflow_3",
            "run_attempt": 1,
            "run_number": 43,
            "run_started_at": "2023-08-02T22:40:38Z",
            "status": "completed",
            "updated_at": "2023-08-02T22:41:05Z",
            "url": "https://repo-url/actions/runs/5744498681",
            "duration": 27
          },
          {
            "conclusion": "success",
            "created_at": "2023-08-02T17:25:51Z",
            "display_title": "workflow_3",
            "event": "workflow_dispatch",
            "head_branch": "main",
            "name": "workflow_3",
            "run_attempt": 1,
            "run_number": 42,
            "run_started_at": "2023-08-02T17:25:51Z",
            "status": "completed",
            "updated_at": "2023-08-02T17:26:20Z",
            "url": "https://repo-url/actions/runs/5741918816",
            "duration": 29
          },
          {
            "conclusion": "failure",
            "created_at": "2023-08-02T17:23:56Z",
            "display_title": "workflow_3",
            "event": "workflow_dispatch",
            "head_branch": "main",
            "name": "workflow_3",
            "run_attempt": 1,
            "run_number": 41,
            "run_started_at": "2023-08-02T17:23:56Z",
            "status": "completed",
            "updated_at": "2023-08-02T17:24:15Z",
            "url": "https://repo-url/actions/runs/5741899384",
            "duration": 19
          },
          {
            "conclusion": "success",
            "created_at": "2023-08-02T17:12:03Z",
            "display_title": "workflow_3",
            "event": "workflow_dispatch",
            "head_branch": "main",
            "name": "workflow_3",
            "run_attempt": 1,
            "run_number": 40,
            "run_started_at": "2023-08-02T17:12:03Z",
            "status": "completed",
            "updated_at": "2023-08-02T17:12:33Z",
            "url": "https://repo-url/actions/runs/5741780688",
            "duration": 30
          },
          {
            "conclusion": "failure",
            "created_at": "2023-08-02T17:09:03Z",
            "display_title": "workflow_3",
            "event": "workflow_dispatch",
            "head_branch": "main",
            "name": "workflow_3",
            "run_attempt": 1,
            "run_number": 39,
            "run_started_at": "2023-08-02T17:09:03Z",
            "status": "completed",
            "updated_at": "2023-08-02T17:09:21Z",
            "url": "https://repo-url/actions/runs/5741751563",
            "duration": 18
          },
          {
            "conclusion": "success",
            "created_at": "2023-08-02T16:59:53Z",
            "display_title": "workflow_3",
            "event": "workflow_dispatch",
            "head_branch": "main",
            "name": "workflow_3",
            "run_attempt": 1,
            "run_number": 38,
            "run_started_at": "2023-08-02T16:59:53Z",
            "status": "completed",
            "updated_at": "2023-08-02T17:00:17Z",
            "url": "https://repo-url/actions/runs/5741655896",
            "duration": 24
          },
          {
            "conclusion": "success",
            "created_at": "2023-08-02T16:52:58Z",
            "display_title": "workflow_3",
            "event": "workflow_dispatch",
            "head_branch": "main",
            "name": "workflow_3",
            "run_attempt": 1,
            "run_number": 37,
            "run_started_at": "2023-08-02T16:52:58Z",
            "status": "completed",
            "updated_at": "2023-08-02T16:53:27Z",
            "url": "https://repo-url/actions/runs/5741599662",
            "duration": 29
          },
          {
            "conclusion": "success",
            "created_at": "2023-08-02T16:40:46Z",
            "display_title": "workflow_3",
            "event": "workflow_dispatch",
            "head_branch": "main",
            "name": "workflow_3",
            "run_attempt": 1,
            "run_number": 36,
            "run_started_at": "2023-08-02T16:40:46Z",
            "status": "completed",
            "updated_at": "2023-08-02T16:41:14Z",
            "url": "https://repo-url/actions/runs/5741498070",
            "duration": 28
          },
          {
            "conclusion": "success",
            "created_at": "2023-08-02T16:38:05Z",
            "display_title": "workflow_3",
            "event": "workflow_dispatch",
            "head_branch": "main",
            "name": "workflow_3",
            "run_attempt": 1,
            "run_number": 35,
            "run_started_at": "2023-08-02T16:38:05Z",
            "status": "completed",
            "updated_at": "2023-08-02T16:38:23Z",
            "url": "https://repo-url/actions/runs/5741468129",
            "duration": 18
          },
          {
            "conclusion": "success",
            "created_at": "2023-08-02T16:18:55Z",
            "display_title": "workflow_3",
            "event": "workflow_dispatch",
            "head_branch": "main",
            "name": "workflow_3",
            "run_attempt": 1,
            "run_number": 34,
            "run_started_at": "2023-08-02T16:18:55Z",
            "status": "completed",
            "updated_at": "2023-08-02T16:19:15Z",
            "url": "https://repo-url/actions/runs/5741287077",
            "duration": 20
          },
          {
            "conclusion": "failure",
            "created_at": "2023-08-02T16:17:36Z",
            "display_title": "workflow_3",
            "event": "workflow_dispatch",
            "head_branch": "main",
            "name": "workflow_3",
            "run_attempt": 1,
            "run_number": 33,
            "run_started_at": "2023-08-02T16:17:36Z",
            "status": "completed",
            "updated_at": "2023-08-02T16:17:53Z",
            "url": "https://repo-url/actions/runs/5741274712",
            "duration": 17
          },
          {
            "conclusion": "failure",
            "created_at": "2023-08-02T16:15:30Z",
            "display_title": "workflow_3",
            "event": "workflow_dispatch",
            "head_branch": "main",
            "name": "workflow_3",
            "run_attempt": 1,
            "run_number": 32,
            "run_started_at": "2023-08-02T16:15:30Z",
            "status": "completed",
            "updated_at": "2023-08-02T16:15:58Z",
            "url": "https://repo-url/actions/runs/5741254037",
            "duration": 28
          },
          {
            "conclusion": "failure",
            "created_at": "2023-08-02T16:12:24Z",
            "display_title": "workflow_3",
            "event": "workflow_dispatch",
            "head_branch": "main",
            "name": "workflow_3",
            "run_attempt": 1,
            "run_number": 31,
            "run_started_at": "2023-08-02T16:12:24Z",
            "status": "completed",
            "updated_at": "2023-08-02T16:15:00Z",
            "url": "https://repo-url/actions/runs/5741224684",
            "duration": 156
          },
          {
            "conclusion": "failure",
            "created_at": "2023-08-02T16:10:25Z",
            "display_title": "workflow_3",
            "event": "workflow_dispatch",
            "head_branch": "main",
            "name": "workflow_3",
            "run_attempt": 1,
            "run_number": 30,
            "run_started_at": "2023-08-02T16:10:25Z",
            "status": "completed",
            "updated_at": "2023-08-02T16:10:50Z",
            "url": "https://repo-url/actions/runs/5741206030",
            "duration": 25
          },
          {
            "conclusion": "failure",
            "created_at": "2023-08-02T16:08:44Z",
            "display_title": "workflow_3",
            "event": "workflow_dispatch",
            "head_branch": "main",
            "name": "workflow_3",
            "run_attempt": 1,
            "run_number": 29,
            "run_started_at": "2023-08-02T16:08:44Z",
            "status": "completed",
            "updated_at": "2023-08-02T16:09:10Z",
            "url": "https://repo-url/actions/runs/5741189545",
            "duration": 26
          },
          {
            "conclusion": "failure",
            "created_at": "2023-08-02T16:03:20Z",
            "display_title": "workflow_3",
            "event": "workflow_dispatch",
            "head_branch": "main",
            "name": "workflow_3",
            "run_attempt": 1,
            "run_number": 28,
            "run_started_at": "2023-08-02T16:03:20Z",
            "status": "completed",
            "updated_at": "2023-08-02T16:03:58Z",
            "url": "https://repo-url/actions/runs/5741131614",
            "duration": 38
          },
          {
            "conclusion": "failure",
            "created_at": "2023-08-02T16:00:53Z",
            "display_title": "workflow_3",
            "event": "workflow_dispatch",
            "head_branch": "main",
            "name": "workflow_3",
            "run_attempt": 1,
            "run_number": 27,
            "run_started_at": "2023-08-02T16:00:53Z",
            "status": "completed",
            "updated_at": "2023-08-02T16:01:19Z",
            "url": "https://repo-url/actions/runs/5741103822",
            "duration": 26
          },
          {
            "conclusion": "failure",
            "created_at": "2023-08-02T15:55:36Z",
            "display_title": "workflow_3",
            "event": "workflow_dispatch",
            "head_branch": "main",
            "name": "workflow_3",
            "run_attempt": 1,
            "run_number": 26,
            "run_started_at": "2023-08-02T15:55:36Z",
            "status": "completed",
            "updated_at": "2023-08-02T15:56:01Z",
            "url": "https://repo-url/actions/runs/5741051958",
            "duration": 25
          },
          {
            "conclusion": "failure",
            "created_at": "2023-08-02T15:48:58Z",
            "display_title": "workflow_3",
            "event": "workflow_dispatch",
            "head_branch": "main",
            "name": "workflow_3",
            "run_attempt": 1,
            "run_number": 25,
            "run_started_at": "2023-08-02T15:48:58Z",
            "status": "completed",
            "updated_at": "2023-08-02T15:49:20Z",
            "url": "https://repo-url/actions/runs/5740992508",
            "duration": 22
          },
          {
            "conclusion": "failure",
            "created_at": "2023-08-02T15:44:42Z",
            "display_title": "workflow_3",
            "event": "workflow_dispatch",
            "head_branch": "main",
            "name": "workflow_3",
            "run_attempt": 1,
            "run_number": 24,
            "run_started_at": "2023-08-02T15:44:42Z",
            "status": "completed",
            "updated_at": "2023-08-02T15:45:08Z",
            "url": "https://repo-url/actions/runs/5740952125",
            "duration": 26
          },
          {
            "conclusion": "failure",
            "created_at": "2023-08-02T15:33:09Z",
            "display_title": "workflow_3",
            "event": "workflow_dispatch",
            "head_branch": "main",
            "name": "workflow_3",
            "run_attempt": 1,
            "run_number": 23,
            "run_started_at": "2023-08-02T15:33:09Z",
            "status": "completed",
            "updated_at": "2023-08-02T15:33:32Z",
            "url": "https://repo-url/actions/runs/5740835844",
            "duration": 23
          },
          {
            "conclusion": "failure",
            "created_at": "2023-08-02T15:30:03Z",
            "display_title": "workflow_3",
            "event": "workflow_dispatch",
            "head_branch": "main",
            "name": "workflow_3",
            "run_attempt": 1,
            "run_number": 22,
            "run_started_at": "2023-08-02T15:30:03Z",
            "status": "completed",
            "updated_at": "2023-08-02T15:30:21Z",
            "url": "https://repo-url/actions/runs/5740799895",
            "duration": 18
          },
          {
            "conclusion": "failure",
            "created_at": "2023-08-02T15:26:29Z",
            "display_title": "workflow_3",
            "event": "workflow_dispatch",
            "head_branch": "main",
            "name": "workflow_3",
            "run_attempt": 1,
            "run_number": 21,
            "run_started_at": "2023-08-02T15:26:29Z",
            "status": "completed",
            "updated_at": "2023-08-02T15:26:45Z",
            "url": "https://repo-url/actions/runs/5740766666",
            "duration": 16
          },
          {
            "conclusion": "failure",
            "created_at": "2023-08-02T15:23:25Z",
            "display_title": "workflow_3",
            "event": "workflow_dispatch",
            "head_branch": "main",
            "name": "workflow_3",
            "run_attempt": 1,
            "run_number": 20,
            "run_started_at": "2023-08-02T15:23:25Z",
            "status": "completed",
            "updated_at": "2023-08-02T15:24:00Z",
            "url": "https://repo-url/actions/runs/5740733967",
            "duration": 35
          },
          {
            "conclusion": "failure",
            "created_at": "2023-08-02T15:16:36Z",
            "display_title": "workflow_3",
            "event": "workflow_dispatch",
            "head_branch": "main",
            "name": "workflow_3",
            "run_attempt": 1,
            "run_number": 19,
            "run_started_at": "2023-08-02T15:16:36Z",
            "status": "completed",
            "updated_at": "2023-08-02T15:17:02Z",
            "url": "https://repo-url/actions/runs/5740658965",
            "duration": 26
          },
          {
            "conclusion": "failure",
            "created_at": "2023-08-02T15:11:40Z",
            "display_title": "workflow_3",
            "event": "workflow_dispatch",
            "head_branch": "main",
            "name": "workflow_3",
            "run_attempt": 1,
            "run_number": 18,
            "run_started_at": "2023-08-02T15:11:40Z",
            "status": "completed",
            "updated_at": "2023-08-02T15:12:06Z",
            "url": "https://repo-url/actions/runs/5740603562",
            "duration": 26
          },
          {
            "conclusion": "failure",
            "created_at": "2023-08-02T15:04:40Z",
            "display_title": "workflow_3",
            "event": "workflow_dispatch",
            "head_branch": "main",
            "name": "workflow_3",
            "run_attempt": 1,
            "run_number": 17,
            "run_started_at": "2023-08-02T15:04:40Z",
            "status": "completed",
            "updated_at": "2023-08-02T15:04:56Z",
            "url": "https://repo-url/actions/runs/5740519101",
            "duration": 16
          },
          {
            "conclusion": "success",
            "created_at": "2023-08-02T14:49:55Z",
            "display_title": "workflow_3",
            "event": "workflow_dispatch",
            "head_branch": "main",
            "name": "workflow_3",
            "run_attempt": 1,
            "run_number": 16,
            "run_started_at": "2023-08-02T14:49:55Z",
            "status": "completed",
            "updated_at": "2023-08-02T14:50:22Z",
            "url": "https://repo-url/actions/runs/5740361667",
            "duration": 27
          },
          {
            "conclusion": "failure",
            "created_at": "2023-08-02T14:48:53Z",
            "display_title": "workflow_3",
            "event": "workflow_dispatch",
            "head_branch": "main",
            "name": "workflow_3",
            "run_attempt": 1,
            "run_number": 15,
            "run_started_at": "2023-08-02T14:48:53Z",
            "status": "completed",
            "updated_at": "2023-08-02T14:49:15Z",
            "url": "https://repo-url/actions/runs/5740350689",
            "duration": 22
          },
          {
            "conclusion": "success",
            "created_at": "2023-08-02T14:10:32Z",
            "display_title": "workflow_2",
            "event": "workflow_dispatch",
            "head_branch": "main",
            "name": "workflow_2",
            "run_attempt": 1,
            "run_number": 48,
            "run_started_at": "2023-08-02T14:10:32Z",
            "status": "completed",
            "updated_at": "2023-08-02T14:10:49Z",
            "url": "https://repo-url/actions/runs/5739906808",
            "duration": 17
          },
          {
            "conclusion": "failure",
            "created_at": "2023-08-02T14:09:34Z",
            "display_title": "workflow_2",
            "event": "workflow_dispatch",
            "head_branch": "main",
            "name": "workflow_2",
            "run_attempt": 1,
            "run_number": 47,
            "run_started_at": "2023-08-02T14:09:34Z",
            "status": "completed",
            "updated_at": "2023-08-02T14:09:48Z",
            "url": "https://repo-url/actions/runs/5739895314",
            "duration": 14
          },
          {
            "conclusion": "failure",
            "created_at": "2023-08-02T12:33:24Z",
            "display_title": "workflow_3",
            "event": "workflow_dispatch",
            "head_branch": "main",
            "name": "workflow_3",
            "run_attempt": 1,
            "run_number": 14,
            "run_started_at": "2023-08-02T12:33:24Z",
            "status": "completed",
            "updated_at": "2023-08-02T12:33:39Z",
            "url": "https://repo-url/actions/runs/5738850142",
            "duration": 15
          },
          {
            "conclusion": "failure",
            "created_at": "2023-08-02T12:27:40Z",
            "display_title": "workflow_3",
            "event": "workflow_dispatch",
            "head_branch": "main",
            "name": "workflow_3",
            "run_attempt": 1,
            "run_number": 13,
            "run_started_at": "2023-08-02T12:27:40Z",
            "status": "completed",
            "updated_at": "2023-08-02T12:27:57Z",
            "url": "https://repo-url/actions/runs/5738789750",
            "duration": 17
          },
          {
            "conclusion": "failure",
            "created_at": "2023-08-02T12:26:26Z",
            "display_title": "workflow_3",
            "event": "workflow_dispatch",
            "head_branch": "main",
            "name": "workflow_3",
            "run_attempt": 1,
            "run_number": 12,
            "run_started_at": "2023-08-02T12:26:26Z",
            "status": "completed",
            "updated_at": "2023-08-02T12:26:42Z",
            "url": "https://repo-url/actions/runs/5738777757",
            "duration": 16
          },
          {
            "conclusion": "failure",
            "created_at": "2023-08-02T12:25:56Z",
            "display_title": "workflow_3",
            "event": "workflow_dispatch",
            "head_branch": "main",
            "name": "workflow_3",
            "run_attempt": 1,
            "run_number": 11,
            "run_started_at": "2023-08-02T12:25:56Z",
            "status": "completed",
            "updated_at": "2023-08-02T12:26:11Z",
            "url": "https://repo-url/actions/runs/5738773319",
            "duration": 15
          },
          {
            "conclusion": "failure",
            "created_at": "2023-08-02T12:23:15Z",
            "display_title": "workflow_3",
            "event": "workflow_dispatch",
            "head_branch": "main",
            "name": "workflow_3",
            "run_attempt": 1,
            "run_number": 10,
            "run_started_at": "2023-08-02T12:23:15Z",
            "status": "completed",
            "updated_at": "2023-08-02T12:23:32Z",
            "url": "https://repo-url/actions/runs/5738746190",
            "duration": 17
          },
          {
            "conclusion": "failure",
            "created_at": "2023-08-02T12:18:37Z",
            "display_title": "workflow_3",
            "event": "workflow_dispatch",
            "head_branch": "main",
            "name": "workflow_3",
            "run_attempt": 2,
            "run_number": 9,
            "run_started_at": "2023-08-02T12:19:39Z",
            "status": "completed",
            "updated_at": "2023-08-02T12:19:59Z",
            "url": "https://repo-url/actions/runs/5738698092",
            "duration": 20
          },
          {
            "conclusion": "failure",
            "created_at": "2023-08-02T12:16:58Z",
            "display_title": "workflow_3",
            "event": "workflow_dispatch",
            "head_branch": "main",
            "name": "workflow_3",
            "run_attempt": 2,
            "run_number": 8,
            "run_started_at": "2023-08-02T12:17:58Z",
            "status": "completed",
            "updated_at": "2023-08-02T12:18:14Z",
            "url": "https://repo-url/actions/runs/5738681879",
            "duration": 16
          },
          {
            "conclusion": "failure",
            "created_at": "2023-08-02T12:15:27Z",
            "display_title": "workflow_3",
            "event": "workflow_dispatch",
            "head_branch": "main",
            "name": "workflow_3",
            "run_attempt": 1,
            "run_number": 7,
            "run_started_at": "2023-08-02T12:15:27Z",
            "status": "completed",
            "updated_at": "2023-08-02T12:15:45Z",
            "url": "https://repo-url/actions/runs/5738667301",
            "duration": 18
          },
          {
            "conclusion": "failure",
            "created_at": "2023-08-02T12:11:33Z",
            "display_title": "workflow_3",
            "event": "workflow_dispatch",
            "head_branch": "main",
            "name": "workflow_3",
            "run_attempt": 1,
            "run_number": 6,
            "run_started_at": "2023-08-02T12:11:33Z",
            "status": "completed",
            "updated_at": "2023-08-02T12:11:55Z",
            "url": "https://repo-url/actions/runs/5738629026",
            "duration": 22
          },
          {
            "conclusion": "failure",
            "created_at": "2023-08-02T11:42:10Z",
            "display_title": "workflow_3",
            "event": "workflow_dispatch",
            "head_branch": "main",
            "name": "workflow_3",
            "run_attempt": 1,
            "run_number": 5,
            "run_started_at": "2023-08-02T11:42:10Z",
            "status": "completed",
            "updated_at": "2023-08-02T11:42:27Z",
            "url": "https://repo-url/actions/runs/5738360713",
            "duration": 17
          },
          {
            "conclusion": "failure",
            "created_at": "2023-08-02T11:41:10Z",
            "display_title": "workflow_3",
            "event": "workflow_dispatch",
            "head_branch": "main",
            "name": "workflow_3",
            "run_attempt": 1,
            "run_number": 4,
            "run_started_at": "2023-08-02T11:41:10Z",
            "status": "completed",
            "updated_at": "2023-08-02T11:41:24Z",
            "url": "https://repo-url/actions/runs/5738352682",
            "duration": 14
          },
          {
            "conclusion": "failure",
            "created_at": "2023-08-02T11:39:14Z",
            "display_title": "workflow_3",
            "event": "workflow_dispatch",
            "head_branch": "main",
            "name": "workflow_3",
            "run_attempt": 1,
            "run_number": 3,
            "run_started_at": "2023-08-02T11:39:14Z",
            "status": "completed",
            "updated_at": "2023-08-02T11:39:32Z",
            "url": "https://repo-url/actions/runs/5738337268",
            "duration": 18
          },
          {
            "conclusion": "failure",
            "created_at": "2023-08-02T11:33:58Z",
            "display_title": "workflow_3",
            "event": "workflow_dispatch",
            "head_branch": "main",
            "name": "workflow_3",
            "run_attempt": 1,
            "run_number": 2,
            "run_started_at": "2023-08-02T11:33:58Z",
            "status": "completed",
            "updated_at": "2023-08-02T11:34:15Z",
            "url": "https://repo-url/actions/runs/5738292428",
            "duration": 17
          },
          {
            "conclusion": "failure",
            "created_at": "2023-08-02T11:31:14Z",
            "display_title": "workflow_3",
            "event": "workflow_dispatch",
            "head_branch": "main",
            "name": "workflow_3",
            "run_attempt": 1,
            "run_number": 1,
            "run_started_at": "2023-08-02T11:31:14Z",
            "status": "completed",
            "updated_at": "2023-08-02T11:31:32Z",
            "url": "https://repo-url/actions/runs/5738265376",
            "duration": 18
          }
        ]
        with open('runs.json', 'w') as f:
            json.dump(runs, f)

if __name__ == '__main__':
    unittest.main()