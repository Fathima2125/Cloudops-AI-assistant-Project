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
