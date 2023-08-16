# Workflow Metrics Action

This GitHub Action provides a way to evaluate statistics for your GitHub Actions workflows. With this action, you can easily monitor the performance of your workflows and identify areas for improvement.

Metrics that are evaluated are:

| Metric | Unit of measure | Description |
| --- | --- | --- |
| Average duration | second | Average of the successful workflow runs, with conclusion status of either `successful` or `skipped`. |
| Median duration | second | Median of the successful workflow runs, with conclusion status of either `successful` or `skipped`. |
| Total number of runs | workflow run | Total number of workflow runs. |
| Success rate | percentage | Percentage of successful runs for the workflow, with conclusion status of either `successful` or `skipped`. |

## Example use cases

- As a product engineer, I want to identify areas of improvement for my process automation, so that I can improve delivery in next iteration.
- As an engineering manager, I want to identify waste and inefficiencies in my SDLC process, so that I can reduce cycle time and improve velocity.
- As a DevOps platform owner, I want to identify long running workflows, so that I can right-sizing the runners.

## Configurations

The following options are available for configuring the action:

| Configuration | Required | Default | Description |
| --- | --- | --- | --- |
| `GH_TOKEN` | Yes | N/A | A GitHub token with access to the repository. Minimal scope is `repo` |
| `OWNER_NAME` | Yes | N/A | Name of the repository owner. |
| `REPO_NAME` | No | N/A | Name of the repository. If `REPO_NAME` is not provide, the action will analyse all the workflow runs in the organisation. |
| `START_DATE` | Yes | N/A | Start date for the workflow runs data set. This should be in the format `YYYY-MM-DD`. |
| `END_DATE` | Yes | N/A | End date for the workflow runs data set. This should be in the format `YYYY-MM-DD`. |
| `DELAY_BETWEEN_QUERY` | No | N/A | No. of seconds to wait between queries to the GitHub API. This is to prevent errors from rate limiting when analysing the whole org. |

## Outputs

After the action has completed, two files will be created in the root of the runner workspace:

- `runs.json` or `org-runs.json` - a JSON array of all workflow runs in the specified time range for the specified repository or organization.
- `workflow-stats.csv` or `org-workflow-stats.csv` - a CSV file with workflow run statistics for the specified repository or organization.


## Example usages

To use this action, simply include it in your workflow file:

### 1. Basic usage

<details>

```yml
name: My Workflow
on: workflow_dispatch
jobs:
  evaluate-actions-consumption:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Call workflow-runs action
        uses: KittyChiu/workflow-metrics@v0.4.5
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          OWNER_NAME: "myOrg"
          REPO_NAME: "myRepo"
          START_DATE: "2023-07-01"
          END_DATE: "2023-08-01"

      - name: Upload all .txt .csv .md files to artifact
        uses: actions/upload-artifact@v3
        with:
          name: workflow-stats
          path: |
            workflow-stats.csv
            runs.json
```

Below is an example of the `workflow-stats.csv` file:

```csv
workflow_name,average_duration,median_duration,success_rate,total_runs
workflow_1,12.33,12.00,100.00,3
workflow_3,25.12,22.00,20.93,43
workflow_2,15.50,15.50,50.00,2
```

</details>

This will analyse workflow runs in the selected repository, including the durations and success rate of each workflow.

### 2. Weekly report on selected repository and post to a GitHub Issue

<details>

```yml
name: Weekly Retrospective Report

on: 
  schedule:
    - cron: '0 12 * * 5'
    
jobs:
  evaluate-actions-consumption:
    runs-on: ubuntu-latest
    env:
      GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      OWNER_NAME: ${{ github.repository_owner }}

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set dates and repo name
        run: |
          echo "START_DATE=$(date -d '-1 month' +%Y-%m-%d)" >> "$GITHUB_ENV"
          echo "END_DATE=$(date +%Y-%m-%d)" >> "$GITHUB_ENV"
          
          repo=$(echo "${{ github.repository }}" | cut -d'/' -f2)
          echo "REPO_NAME=${repo}" >> $GITHUB_ENV

      - name: Call workflow-runs action
        uses: KittyChiu/workflow-metrics@v0.4.5
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          REPO_NAME: ${{ env.REPO_NAME }}
          START_DATE: ${{ env.START_DATE }}
          END_DATE: ${{ env.END_DATE }}

      - name: Convert workflow-stats.CSV to stats-table.md markdown table
        run: |
          echo -e "## Table View\n" > stats-table.md
          header=$(head -n 1 workflow-stats.csv | sed 's/,/|/g' | sed 's/_/ /g')
          echo -e "|${header}|" >> stats-table.md
          metadata=$(head -n 1 workflow-stats.csv | sed 's/,/|/g' | sed 's/[^|]/-/g')
          echo -e "|${metadata}|" >> stats-table.md
          tail -n +2 workflow-stats.csv | sed 's/,/|/g; s/^/|/; s/$/|/' >> stats-table.md

      - name: Convert workflow-stats.CSV to stream-diagram.md mermaid diagram
        run: |
          echo -e "## Value Stream View\n" > stream-diagram.md
          echo -e '```mermaid' >> stream-diagram.md
          echo -e 'timeline' >> stream-diagram.md
          head -n 1 workflow-stats.csv | sed 's/,/ : /g' | sed 's/_/ /g' | awk -F'|' '{for(i=1;i<=NF;i++) printf("%s%s", "    ", $i, i==NF?"\n":", ")}' | sed 's/^/  /' >> stream-diagram.md
          tail -n +2 workflow-stats.csv | sed 's/,/ : /g' | awk -F'|' '{for(i=1;i<=NF;i++) printf("%s%s", "\n    ", $i, i==NF?"\n":", ")}' | sed 's/^/  /' >> stream-diagram.md
          echo -e '\n```' >> stream-diagram.md

      - name: Combine into issue content
        run: |
          echo "Combine output files"
          cat stream-diagram.md stats-table.md > issue_view.md

      - name: Publish content to a new GitHub Issue
        uses: peter-evans/create-issue-from-file@v4
        with:
          title: Workflow runs summary `${{ env.REPO_NAME }}` repo (${{ env.START_DATE }} - ${{ env.END_DATE }})
          content-filepath: issue_view.md

      - name: Upload all .txt .csv .md files to artifact
        uses: actions/upload-artifact@v3
        with:
          name: workflow-stats
          path: |
            stats-table.md
            stream-diagram.md
            workflow-stats.csv
            runs.json
```

Below is an example of the `stats-table.md` file:

```md
|workflow name|average duration|median duration|success rate|total runs|
|-------------|----------------|---------------|------------|----------|
|workflow_1|17.00|17.00|100.00|1|
|workflow_2|36.17|36.50|53.70|54|
|workflow_3|3.00|2.00|100.00|3|
```

</details>

This will further convert `workflow-stats.csv` file containing workflow metrics into a markdown table, mermaid diagram, and publishes it to a new issue.

### 3. Monthly report for the whole org and post to a GitHub Issue

<details>

```yml
name: Monthly SLOs Report

on:
  schedule:
    - cron: '0 0 1 * *'

jobs:
  evaluate-actions-consumption:
    runs-on: ubuntu-latest
    env:
      GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      OWNER_NAME: ${{ github.repository_owner }}

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set dates
        run: |
          echo "START_DATE=$(date -d '-14 days' +%Y-%m-%d)" >> "$GITHUB_ENV"
          echo "END_DATE=$(date +%Y-%m-%d)" >> "$GITHUB_ENV"
          
      - name: Test docker action
        uses: KittyChiu/workflow-metrics@v0.4.5
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          START_DATE: ${{ env.START_DATE }}
          END_DATE: ${{ env.END_DATE }}

      - name: Convert org-workflow-stats.csv to stats-table.md markdown table
        run: |
          echo -e "## Table View\n" > stats-table.md
          header=$(head -n 1 org-workflow-stats.csv | sed 's/,/|/g' | sed 's/_/ /g')
          echo -e "|${header}|" >> stats-table.md
          metadata=$(head -n 1 org-workflow-stats.csv | sed 's/,/|/g' | sed 's/[^|]/-/g')
          echo -e "|${metadata}|" >> stats-table.md
          tail -n +2 org-workflow-stats.csv | sed 's/,/|/g; s/^/|/; s/$/|/' >> stats-table.md

      - name: Publish result to a new issue
        uses: peter-evans/create-issue-from-file@v4
        with:
          title: Workflow runs summary for `${{ env.OWNER_NAME }}` org (${{ env.START_DATE }} - ${{ env.END_DATE }})
          content-filepath: stats-table.md

      - name: Upload all .txt .csv .md files to artifact
        uses: actions/upload-artifact@v3
        with:
          name: workflow-stats
          path: |
            stats-table.md
            org-workflow-stats.csv
            org-runs.json
```

Below is an example of the `stats-table.md` file:

```md
|repository name|workflow name|average duration|median duration|success rate|total runs|
|---------------|-------------|----------------|---------------|------------|----------|
|repo_1|Test|3.00|3.00|100.00|1|
|repo_1|Build|20.20|17.00|80.00|5|
|repo_1|Deploy|17.00|17.00|100.00|1|
|repo_2|Governance Validation|2.00|2.00|100.00|1|
|repo_2|Linter|2.00|2.00|100.00|1|
|repo_3|Superlinter|25.38|23.00|30.00|50|
|repo_3|Long Build|36.17|36.50|53.70|54|
|repo_3|Smoke Test|19.69|14.00|23.08|13|
```

</details>

This will analyse workflow runs in the selected organisation, including all workflows for each repository.

## Contributing

Please see the [contributing guidelines](CONTRIBUTING.md) for more information.

## License

This project is licensed under the [MIT License](LICENSE).
