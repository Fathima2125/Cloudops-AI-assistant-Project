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

## Phase 6: AI AWS Knowledge Assistant

In this phase, I built a reusable AWS concept explanation workflow. The goal was to help explain AWS topics in a consistent format for learning, troubleshooting, and interview preparation.

### What I Built

I created a reusable prompt template at `prompts/aws-explainer.md`. The template asks the AI to explain AWS concepts using a consistent structure:

- Executive Summary
- AWS Concept
- Explanation
- Best Practices
- Common Mistakes
- Troubleshooting Tips
- Interview Explanation
- Official AWS documentation references by topic or service name

I also used the template to generate AWS concept guides for topics such as:

- Lambda timeouts
- Security groups and open SSH
- IAM roles vs IAM users
- ALB vs NLB
- Terraform backends

The generated guides were saved under `reports/reliability/`, and the concepts were summarized in `docs/aws-knowledge-base.md`.

### Why AWS Documentation Matters

AWS documentation matters because cloud services change over time. Limits, features, pricing, recommended patterns, and security guidance can evolve. A CloudOps engineer should not rely only on memory or AI-generated explanations for final decisions.

Official AWS documentation helps confirm:

- Current service behavior
- Supported features
- Service limits and quotas
- Security recommendations
- Monitoring and troubleshooting options
- Configuration details

In this project, the prompt template tells the AI to mention relevant AWS documentation topics instead of copying documentation content. This keeps the output useful while reminding the engineer to verify important details from official sources.

### How AI Can Help Engineers Learn Faster

AI can help engineers learn faster by turning broad cloud topics into clear, structured explanations. Instead of reading several pages first, the engineer can start with a concise summary, understand the main idea, then go deeper into official documentation.

AI is useful for:

- Explaining complex AWS concepts in simple language.
- Comparing related services, such as ALB and NLB.
- Highlighting best practices and common mistakes.
- Creating interview-ready explanations.
- Connecting concepts to troubleshooting workflows.
- Building reusable notes and knowledge bases.

AI should support learning, not replace verification. The best workflow is to use AI for structure and explanation, then use official documentation for confirmation.

### How This Could Later Integrate With AWS Documentation MCP

A future version of this project could connect the AWS concept workflow to an AWS Documentation MCP server. Instead of only using local question files and prompt templates, the assistant could retrieve relevant official documentation context before generating a guide.

That future workflow could:

- Read an AWS question from `aws-questions/`.
- Select `prompts/aws-explainer.md`.
- Query AWS Documentation MCP for relevant service documentation.
- Generate a Markdown guide using both the local prompt and official documentation context.
- Save the output under `reports/reliability/`.
- Include official documentation topics for follow-up review.

This would make the AI AWS Knowledge Assistant more accurate and useful while keeping the project safe, educational, and portfolio-friendly.

## Phase 8: MCP Integration

In this phase, I connected the project workflow to the AWS Documentation MCP Server. The goal was to move from AI answers based only on local prompts and general model knowledge toward AI-assisted CloudOps reports that can use official AWS documentation as source context.

### What MCP Is

MCP stands for Model Context Protocol. It is a standard way for an AI assistant to connect to external tools, documentation sources, and systems through controlled servers.

Instead of giving the assistant unrestricted access to everything, MCP lets a project expose specific capabilities. For this project, the useful capability is documentation access: Codex can search and read AWS documentation through the AWS Documentation MCP Server.

### Why MCP Matters for AI Agents

MCP matters because AI agents are more useful when they can safely retrieve current, task-specific context. Without external tools, an assistant may rely only on its training data and the files in the repository. That can be enough for basic explanations, but it is weaker for cloud work where service limits, best practices, and documentation change over time.

For CloudOps, MCP helps an AI assistant:

- Look up official documentation before writing recommendations.
- Reduce guessing when explaining AWS services.
- Produce reports that are easier to verify.
- Keep the workflow safer by exposing only specific tool capabilities.
- Separate documentation access from infrastructure access.

### How Codex Can Use MCP Servers

Codex can use MCP servers as external tool providers. A project can configure an MCP server, and Codex can call the tools exposed by that server during a task.

In this project, Codex uses the AWS Documentation MCP Server to:

- Search AWS documentation for relevant Lambda, CloudWatch, and reliability topics.
- Read selected AWS documentation pages.
- Extract best practices and troubleshooting guidance.
- Use the documentation context to improve Markdown reports.
- Include official AWS documentation links for follow-up review.

This keeps the assistant useful while still respecting the project's safety model. The current MCP integration does not inspect live AWS accounts, change resources, run Terraform, or modify infrastructure.

### Why AWS Documentation MCP Is Useful for CloudOps

AWS Documentation MCP is useful for CloudOps because operational work often depends on accurate service behavior. When troubleshooting Lambda timeouts, for example, the assistant can confirm timeout limits, memory and CPU behavior, CloudWatch log fields, CloudWatch Logs Insights queries, and SQS visibility timeout guidance from AWS documentation.

This is valuable because CloudOps engineers need recommendations that are both practical and verifiable. A report is stronger when it can point back to official AWS documentation instead of only giving a general explanation.

For this project, AWS Documentation MCP improved the Lambda timeout workflow by helping generate documentation-based guidance for:

- Lambda timeout configuration.
- Memory and duration troubleshooting.
- External API timeout handling.
- CloudWatch Logs troubleshooting.
- CloudWatch Logs Insights queries.
- Interview-ready explanations.

### What I Learned from Adding MCP

I learned that MCP is a practical way to make an AI assistant more grounded without making it unsafe. The assistant can retrieve official documentation, but it does not need permission to touch production systems.

I also learned that MCP works best when the workflow is specific. Instead of asking for a broad AWS explanation, it is better to ask for a focused task, such as troubleshooting Lambda timeout issues using AWS documentation. This helps the assistant search for the right sources and produce a clearer report.

The biggest lesson is that AI-assisted CloudOps should combine three things:

- Local project context, such as prompts, reports, and learning notes.
- Official documentation, retrieved through a controlled MCP server.
- Human review before any operational change.

This phase made the project more realistic because it shows how an AI CloudOps Assistant can safely use external knowledge while staying within read-only, documentation-focused boundaries.
