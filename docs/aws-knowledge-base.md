# AWS Knowledge Base

## Overview

This knowledge base summarizes the AWS concepts covered so far in the CloudOps AI Assistant project. The topics are organized by category to make them easier to review for CloudOps practice, troubleshooting, and interview preparation.

## Compute

### AWS Lambda Timeout

AWS Lambda functions have a configured timeout. If the function does not finish before that limit, AWS stops the invocation and marks it as failed.

Key points:

- Timeouts can be caused by slow code, slow downstream dependencies, large payloads, insufficient memory, or networking delays.
- Lambda memory also affects available CPU, so increasing memory can sometimes improve performance.
- CloudWatch Logs and Lambda metrics are the first places to check during troubleshooting.
- Important metrics include duration, errors, throttles, concurrent executions, and memory usage.

Best practices:

- Set timeout values based on realistic testing.
- Add logs around slow operations such as database calls and external API calls.
- Use AWS X-Ray or structured tracing for dependency latency.
- Add explicit client-side timeouts for SDK, HTTP, and database calls.
- Use retries carefully to avoid duplicate work or retry storms.

Related guide:

- `reports/reliability/lambda-timeout-guide.md`

## Networking

### Application Load Balancer vs Network Load Balancer

Application Load Balancer and Network Load Balancer are both part of Elastic Load Balancing, but they operate at different layers and are used for different traffic patterns.

Key points:

- ALB works at Layer 7 and is best for HTTP, HTTPS, APIs, web apps, and microservices.
- ALB supports host-based and path-based routing.
- NLB works at Layer 4 and is best for TCP, UDP, TLS, static IP requirements, and high-throughput workloads.
- NLB is useful for network-level forwarding, PrivateLink endpoint services, and low-latency traffic.

Best practices:

- Use ALB for application-aware web routing.
- Use NLB for non-HTTP protocols, static IPs, and very high performance.
- Configure health checks carefully.
- Choose internal load balancers for private services.
- Monitor target health, latency, HTTP errors, and rejected connections.

Related guide:

- `reports/reliability/alb-nlb-guide.md`

### Security Groups and SSH Access

Security groups control inbound and outbound traffic for AWS resources. Opening SSH to `0.0.0.0/0` allows any public IP address to attempt SSH access.

Key points:

- SSH on port `22` is administrative access and should be restricted.
- Public SSH increases exposure to scanning, brute-force attempts, stolen key attempts, and weak configuration risks.
- Key-based authentication helps, but it does not remove the exposure created by public SSH.

Best practices:

- Do not allow SSH from `0.0.0.0/0` for production resources.
- Restrict SSH to a trusted VPN, corporate network, or administrator CIDR.
- Prefer AWS Systems Manager Session Manager when possible.
- Monitor security group changes with CloudTrail and AWS Config.
- Remove temporary SSH access after troubleshooting.

Related guide:

- `reports/reliability/security-group-guide.md`

## Security

### IAM Roles vs IAM Users

IAM users and IAM roles are both AWS identities, but they should be used differently. IAM users are usually for people or long-lived identities. IAM roles are for temporary, delegated access.

Key points:

- IAM users can have long-term credentials such as passwords and access keys.
- IAM roles use temporary credentials and are safer for workloads.
- EC2 instances should use IAM roles through instance profiles.
- Lambda functions should use Lambda execution roles.
- Roles need trust policies and permission policies.

Best practices:

- Prefer IAM roles for AWS services and applications.
- Avoid hardcoding IAM user access keys in code, servers, or environment files.
- Use least privilege permissions.
- Use MFA or federated access for human users.
- Review IAM policies regularly and remove unused permissions.

Examples:

- EC2 should use an instance profile role to read from S3.
- Lambda should use an execution role to write logs or access a specific AWS service.

Related guide:

- `reports/reliability/IAM-role--guide.md`

### Secure Administrative Access

Secure administrative access combines IAM, security groups, logging, and approved access paths.

Key points:

- Avoid direct public SSH when possible.
- Prefer temporary credentials and audited access.
- Use least privilege for both human and workload access.
- Use logs and monitoring to detect risky access changes.

Useful AWS services and features:

- AWS IAM
- AWS Systems Manager Session Manager
- AWS CloudTrail
- AWS Config
- Amazon EC2 security groups

## Infrastructure as Code

### Terraform Backend

A Terraform backend defines where Terraform stores its state file. Terraform state tracks the infrastructure managed by Terraform, so backend design is important for safe team workflows.

Key points:

- Local state is risky for shared or production infrastructure.
- Remote state gives teams and automation a shared source of truth.
- In AWS, S3 is commonly used for Terraform remote state.
- State files can contain sensitive information and should be protected.
- State corruption or loss can cause unsafe infrastructure changes.

Best practices:

- Use remote state for team and production workflows.
- Store state in S3 with versioning enabled.
- Encrypt state, preferably with AWS KMS where appropriate.
- Restrict access with least-privilege IAM policies.
- Separate state by environment and module.
- Do not commit `.tfstate` files to Git.
- Avoid manually editing state unless following a controlled recovery process.

Related guide:

- `reports/reliability/terraform-backend-guide.md`

### Terraform Review and Security

Terraform code should be reviewed for security, reliability, cost, and maintainability before being applied.

Key points:

- Open SSH, hardcoded values, missing tags, and broad network rules are common risks.
- Variables make Terraform reusable across environments.
- Tags improve ownership, cost tracking, automation, and incident response.
- Provider version constraints make Terraform behavior more predictable.
- Human review is required before applying infrastructure changes.

Related reports:

- `reports/security/terraform-review-report.md`
- `reports/security/terraform-before-after-comparison.md`

## Summary

The AWS concepts covered so far focus on practical CloudOps work:

- Compute reliability with Lambda timeout troubleshooting.
- Networking decisions with ALB, NLB, security groups, and SSH exposure.
- Security fundamentals with IAM users, IAM roles, least privilege, and safe access.
- Infrastructure as Code practices with Terraform review and backend design.

Together, these topics form a strong foundation for analyzing cloud issues, explaining AWS concepts clearly, and documenting operational recommendations in a professional way.
