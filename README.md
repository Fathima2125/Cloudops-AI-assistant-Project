CloudOps AI Assistant
=====================

CloudOps AI Assistant is a small, portfolio-friendly project that demonstrates how Codex and AI-assisted workflows can support cloud operations tasks from the command line.

The project focuses on practical CloudOps review workflows: Terraform review, log analysis, incident summarization, reliability recommendations, security observations, and Markdown report generation. It is intentionally lightweight and does not include a web API, Docker setup, Kubernetes deployment, or CI pipeline yet.

Project Scope
-------------

This repository is intended to contain:

- Reusable prompts for AI-assisted CloudOps analysis.
- Sample AWS-style logs for troubleshooting demonstrations.
- Sample Terraform files for infrastructure review.
- Generated Markdown reports for incidents, security findings, and reliability observations.
- Documentation covering architecture, safe usage, and AI action boundaries.

Example Workflows
-----------------

- Use `prompts/terraform-review.md` to review `terraform/sample-vpc.tf`.
- Use `prompts/log-analysis.md` to analyze logs in `sample-logs/`.
- Use `prompts/incident-report.md` to generate incident summaries.
- Store completed analysis in `reports/` or one of its category folders.
- Review every recommendation manually before running any AWS or Terraform command.

CLI Automation Workflow
-----------------------

The project includes a small helper script at `scripts/analyze.py`. The script prepares an analysis workflow by validating an input file, selecting the correct prompt template, and showing the expected output report path.

For Terraform analysis:

```bash
python3 scripts/analyze.py --type terraform --file terraform/sample-vpc.tf
```

For log analysis:

```bash
python3 scripts/analyze.py --type log --file sample-logs/lambda-timeout.log
```

Dry-run mode shows the planned analysis without creating or modifying files:

```bash
python3 scripts/analyze.py --type log --file sample-logs/lambda-timeout.log --dry-run
```

Current limitation: `scripts/analyze.py` prepares the analysis workflow, but it does not directly call an AI API yet.

Future enhancement: connect the script to the OpenAI API or an MCP server so it can generate reports automatically while preserving human review and safety controls.

Repository Structure
--------------------

- `docs/` - architecture, security, AI safety, learning notes, and future enhancements.
- `prompts/` - reusable prompts for Codex-assisted CloudOps tasks.
- `sample-logs/` - example logs for incident and troubleshooting analysis.
- `terraform/` - sample infrastructure code for review.
- `reports/` - generated or curated CloudOps reports.
- `reports/incidents/` - incident-focused reports.
- `reports/security/` - security review reports.
- `reports/reliability/` - reliability and operational health reports.
- `.env.example` - local environment variable template.
- `notes.md` - working notes, ideas, and planning details.
- `README.md` - project overview and onboarding entry point.

Environment
-----------

Create a local `.env` file from `.env.example` when API-backed workflows are needed:

```env
OPENAI_API_KEY=
AWS_REGION=us-east-1
AWS_PROFILE=default
LOG_LEVEL=INFO
```

Do not commit `.env` or any real credentials.

Safety Model
------------

The assistant is designed for read-only analysis and human-reviewed recommendations. Infrastructure-changing actions such as applying Terraform, modifying IAM, restarting services, or changing security groups require explicit human approval outside the assistant workflow. Destructive or secret-exfiltration actions are blocked by project policy.

Status
------

This project is in early CLI-focused setup. The current goal is to keep it understandable, demonstrable, and safe while showing realistic CloudOps AI workflows.
