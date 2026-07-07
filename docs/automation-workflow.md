# Automation Workflow

## Overview

`scripts/analyze.py` is a small CLI helper for the CloudOps AI Assistant project. It does not call an AI API yet. Its current job is to prepare an analysis workflow by validating the input file, selecting the correct prompt template, and showing where the final report should be saved.

## How It Works

### 1. User Provides Input Type and File

The user runs the script with two required arguments:

- `--type` tells the script what kind of analysis to prepare.
- `--file` tells the script which Terraform file or log file should be analyzed.

Supported analysis types:

- `terraform`
- `log`

### 2. Script Validates the File

The script checks whether the file provided with `--file` exists.

If the file does not exist, the script stops and prints an error message. This prevents the workflow from continuing with a bad path.

### 3. Script Selects the Correct Prompt Template

The script chooses a prompt based on the analysis type:

| Analysis Type | Prompt Template |
| --- | --- |
| `terraform` | `prompts/terraform-review.md` |
| `log` | `prompts/log-analysis.md` |

### 4. Script Decides the Output Report Path

The script builds the report path from the input filename.

Examples:

- `sample-logs/lambda-timeout.log` becomes `reports/incidents/lambda-timeout-analysis.md`
- `terraform/sample-vpc.tf` becomes `reports/security/sample-vpc-review.md`

Terraform reports are saved under:

```text
reports/security/
```

Log analysis reports are saved under:

```text
reports/incidents/
```

### 5. Future Versions Can Connect to AI

Future versions of this script could connect to:

- An AI API
- A local model
- A Codex workflow
- An MCP server
- A report generation pipeline

For now, the script stays simple and safe. It only prints the planned prompt and output path.

## Example Commands

### Terraform Analysis

```bash
python3 scripts/analyze.py --type terraform --file terraform/sample-vpc.tf
```

Dry run:

```bash
python3 scripts/analyze.py --type terraform --file terraform/sample-vpc.tf --dry-run
```

Expected output report:

```text
reports/security/sample-vpc-review.md
```

### Log Analysis

```bash
python3 scripts/analyze.py --type log --file sample-logs/lambda-timeout.log
```

Dry run:

```bash
python3 scripts/analyze.py --type log --file sample-logs/lambda-timeout.log --dry-run
```

Expected output report:

```text
reports/incidents/lambda-timeout-analysis.md
```

## Why This Matters

This workflow makes the project more realistic while keeping it beginner-friendly. It shows how a CloudOps assistant can move from manual prompt usage toward repeatable automation without adding unnecessary backend services yet.
