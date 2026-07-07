# Learning Notes

## Phase 3: Terraform AI Reviewer

In this phase, I used Codex as an AI-assisted Terraform reviewer for a small AWS VPC example. The goal was not to deploy infrastructure, but to practice how a CloudOps engineer can review infrastructure-as-code for security, reliability, maintainability, and operational readiness.

### How Codex Reviewed Terraform

Codex reviewed the Terraform file by checking the resources, network rules, hardcoded values, tagging, and Terraform best practices. It identified the VPC, subnet, security group, and EC2 instance, then produced a structured Markdown review report with findings, severity levels, recommendations, and remediation steps.

This showed how AI can help speed up first-pass infrastructure review while still requiring a human engineer to validate the findings before making changes.

### Common Terraform Risks Found

The review identified several common risks:

- SSH access was open to the internet with `0.0.0.0/0`.
- The public subnet automatically assigned public IP addresses.
- The AMI ID, AWS region, CIDR blocks, and instance type were hardcoded.
- Resources did not have tags for ownership, environment, or cost tracking.
- Terraform and AWS provider version constraints were missing.
- The EC2 instance used `security_groups` instead of `vpc_security_group_ids`.

### Why Open SSH Is Risky

Open SSH is risky because it exposes administrative access to every IP address on the internet. Attackers and automated scanners constantly look for open port `22`, then attempt brute-force logins, credential attacks, or exploitation of weak configurations.

A safer approach is to restrict SSH to a trusted CIDR range, use a VPN or bastion host, or avoid public SSH entirely by using AWS Systems Manager Session Manager.

### Why Tags and Variables Matter

Tags matter because they make cloud resources easier to manage. They help teams understand ownership, environment, cost allocation, project context, and operational responsibility. In CloudOps work, good tagging also supports reporting, cleanup, automation, and incident response.

Variables matter because they make Terraform reusable and safer to operate. Instead of hardcoding values like region, CIDR ranges, AMI IDs, and instance types, variables allow the same Terraform code to be used across different environments with different inputs.

### How This Helps CloudOps Work

This phase showed how an AI CloudOps Assistant can support practical infrastructure review. Codex helped turn a small Terraform file into:

- A professional security review report.
- A before-and-after Terraform comparison.
- An improved Terraform example with safer defaults.
- Clear interview-ready explanations of the changes.

For CloudOps work, this approach can help engineers review infrastructure faster, document risks clearly, explain recommendations to others, and maintain a safer human-reviewed workflow before applying changes.

## Phase 4: AI-Assisted Cloud Log Analysis

In this phase, I used Codex to analyze sample cloud logs and generate professional incident reports. The goal was to practice how Cloud Engineers read logs, identify root causes, assess severity, recommend fixes, and document prevention steps.

### Reading Cloud Logs

I learned that cloud logs often contain short but important clues. A single error message can point to the failing service, the failure type, and the next investigation step.

Examples from this phase:

- Lambda timeout logs showed the function exceeded its timeout and used most of its memory.
- EKS logs showed a pod in `CrashLoopBackOff` because the application could not connect to PostgreSQL.
- EC2 Nginx logs showed the service could not start because port `80` was already in use.

The key skill is to identify the strongest evidence in the log instead of guessing.

### Root Cause Analysis

Root cause analysis means connecting the error message to the underlying technical problem.

In these examples:

- The Lambda issue was likely caused by a timeout, slow dependency, insufficient resources, or too much work in one invocation.
- The Kubernetes issue was likely caused by a failed PostgreSQL dependency or incorrect database configuration.
- The EC2 issue was caused by a port conflict where another process was already using port `80`.

I learned that root cause should be stated carefully. If the log does not prove the full cause, the report should explain what is known, what is likely, and what information is still missing.

### AI-Assisted Troubleshooting

Codex helped turn raw log messages into structured incident reports. It helped organize the analysis into sections such as executive summary, root cause, severity, impact, recommended fix, prevention, and missing information.

This showed that AI can support CloudOps troubleshooting by:

- Summarizing confusing logs in simple language.
- Identifying likely failure patterns.
- Suggesting safe read-only investigation steps.
- Producing consistent Markdown reports.
- Helping document prevention and lessons learned.

AI does not replace engineering judgment. The engineer still needs to validate the root cause, confirm the environment, and approve any production changes.

### Differences Between Lambda, Kubernetes, and EC2 Issues

Lambda issues often involve timeout settings, memory usage, retries, event sources, and downstream dependencies. Troubleshooting usually starts with CloudWatch Logs, duration metrics, memory usage, and invocation errors.

Kubernetes issues often involve pod status, container restarts, service discovery, secrets, readiness probes, and dependencies such as databases. Troubleshooting usually starts with pod logs, `kubectl describe pod`, previous container logs, service endpoints, and recent deployment changes.

EC2 issues often involve operating system services, ports, processes, packages, and systemd status. Troubleshooting usually starts with service logs, port checks, process checks, and configuration validation.

The services are different, but the troubleshooting process is similar: read the evidence, identify the failing component, assess impact, confirm the root cause, recommend a safe fix, and document prevention.

### How Codex Helped Analyze Logs

Codex helped create a repeatable workflow for log analysis. I created a reusable prompt template in `prompts/log-analysis.md`, then used it to analyze Lambda, EKS, and EC2 logs.

The outputs became professional incident reports in `reports/incidents/`, plus a shared troubleshooting workflow in `docs/cloudops-troubleshooting-workflow.md`.

This helped show how an AI CloudOps Assistant can support real operational work by turning logs into clear explanations, action steps, and portfolio-ready documentation.

## Phase 5: Automation CLI Script

In this phase, I built a small Python CLI script at `scripts/analyze.py`. The script prepares an analysis workflow for Terraform files and cloud logs. It does not call an AI API yet, but it helps standardize how inputs, prompts, and report paths are selected.

### What I Built

The CLI accepts:

- `--type terraform` or `--type log`
- `--file` for the input file path
- `--dry-run` to preview the workflow without creating or modifying files

The script validates that the input file exists, selects the correct prompt template, and generates the expected output report path.

Examples:

- Terraform input uses `prompts/terraform-review.md` and saves reports under `reports/security/`.
- Log input uses `prompts/log-analysis.md` and saves reports under `reports/incidents/`.

### Why CLI Automation Is Useful in CloudOps

CLI automation is useful because CloudOps work often needs to be repeatable, fast, and consistent. Engineers frequently analyze logs, review infrastructure files, generate reports, and follow runbooks from the terminal.

This script helps by:

- Reducing manual path selection mistakes.
- Making the analysis workflow consistent.
- Supporting repeatable Terraform and log review steps.
- Keeping the project simple and easy to demonstrate.
- Creating a foundation for future automation.

### How the Script Maps Inputs to Prompts and Reports

The script maps the analysis type to a prompt and report folder:

| Analysis Type | Prompt Template | Report Folder | Filename Pattern |
| --- | --- | --- | --- |
| `terraform` | `prompts/terraform-review.md` | `reports/security/` | `<input-name>-review.md` |
| `log` | `prompts/log-analysis.md` | `reports/incidents/` | `<input-name>-analysis.md` |

For example:

- `terraform/sample-vpc.tf` becomes `reports/security/sample-vpc-review.md`.
- `sample-logs/lambda-timeout.log` becomes `reports/incidents/lambda-timeout-analysis.md`.

### How This Prepares the Project for AI API or MCP Integration

The script separates workflow setup from AI execution. That makes it easier to add automation later without redesigning the project.

A future version could:

- Read the selected prompt file.
- Read the selected input file.
- Send both to the OpenAI API or an MCP server.
- Save the generated Markdown report to the output path.
- Add safety checks before any infrastructure-changing recommendation.

This phase moves the project from manual prompt usage toward a more automated CloudOps assistant while keeping the current version beginner-friendly and safe.
