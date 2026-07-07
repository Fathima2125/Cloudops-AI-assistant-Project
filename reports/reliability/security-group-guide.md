# AWS Concept Explainer

## Executive Summary

Opening SSH to `0.0.0.0/0` means any public IP address on the internet can attempt to connect to port `22` on the protected resource. This is considered a security risk because SSH is an administrative access path, and exposing it broadly increases the chance of brute-force attacks, credential abuse, vulnerability scanning, and unauthorized access attempts.

In AWS, this issue commonly appears in security group rules for EC2 instances. A safer approach is to restrict SSH to trusted networks, use a VPN or bastion host, or avoid public SSH by using AWS Systems Manager Session Manager.

## AWS Concept

- Concept: Security group rule allowing SSH from `0.0.0.0/0`
- Related AWS service or feature: Amazon EC2 security groups, AWS Systems Manager Session Manager, Amazon VPC, AWS IAM
- Common use case: Reviewing inbound access rules for EC2 instances and other VPC resources

## Explanation

Security groups act like virtual firewalls for AWS resources. They control inbound and outbound traffic based on protocol, port, and source or destination.

SSH uses port `22` and is commonly used for Linux server administration. When a security group allows SSH from `0.0.0.0/0`, it means the instance accepts SSH connection attempts from anywhere on the internet.

That does not mean every attacker can log in successfully, because authentication is still required. However, it greatly increases exposure. Attackers can continuously scan the internet for open SSH ports and attempt password attacks, stolen key usage, or exploitation of weak server configurations.

For CloudOps work, SSH access should be treated as sensitive administrative access. It should be limited, monitored, and replaced with safer access patterns where possible.

## Best Practices

- Do not allow SSH from `0.0.0.0/0` for production instances.
- Restrict SSH access to a trusted corporate, VPN, or administrator CIDR range.
- Prefer AWS Systems Manager Session Manager for shell access without opening inbound SSH.
- Use IAM controls, logging, and least privilege for administrative access.
- Use a bastion host only when required, and restrict access to it tightly.
- Avoid password-based SSH authentication; use managed keys or stronger access controls.
- Monitor security group changes with AWS CloudTrail and AWS Config.
- Use security group descriptions so the reason for each rule is clear.
- Review inbound rules regularly as part of security hygiene.
- Remove temporary SSH rules after troubleshooting is complete.

## Common Mistakes

- Opening SSH to `0.0.0.0/0` for convenience and forgetting to remove it.
- Assuming key-based SSH alone is enough to make public SSH safe.
- Using the same SSH key across many instances or environments.
- Allowing SSH to production instances from personal home IPs without a managed access process.
- Not monitoring failed SSH attempts or suspicious login behavior.
- Leaving old bastion hosts exposed to the internet.
- Not documenting why a security group rule exists.
- Using broad CIDR ranges when a narrower trusted range is available.

## Troubleshooting Tips

1. Review the EC2 security group inbound rules and look for port `22` open to `0.0.0.0/0` or `::/0`.
2. Confirm whether SSH is actually required for the workload.
3. Check whether AWS Systems Manager Session Manager can be used instead.
4. If SSH is required, identify the smallest trusted CIDR range that should have access.
5. Review CloudTrail for recent security group rule changes.
6. Check AWS Config or security findings for unrestricted SSH alerts.
7. Review instance logs for repeated failed login attempts.
8. Confirm that the instance uses strong authentication and does not allow password login.
9. Remove unused SSH rules after maintenance or troubleshooting.
10. Document the approved access path in the runbook.

## Interview Explanation

Opening SSH to `0.0.0.0/0` is risky because it exposes administrative access to the whole internet. Even if the instance uses SSH keys, attackers can still scan the server, attempt brute-force access, try stolen keys, or exploit weak configurations.

In AWS, I would avoid public SSH where possible and use Systems Manager Session Manager. If SSH is required, I would restrict it to a trusted VPN or corporate CIDR range, monitor access, and remove temporary rules after use.

## Real-World Examples

- A developer temporarily opens SSH to `0.0.0.0/0` to debug an EC2 instance and forgets to close it. The instance is then exposed to continuous internet scanning.
- A production bastion host allows SSH from anywhere. If a private key is leaked, an attacker has a direct path to the environment.
- A security group is copied from a test environment to production with an unrestricted SSH rule, creating an avoidable production exposure.
- An old EC2 instance remains running with port `22` open and no owner tag, making it harder for the team to know whether the access is still needed.

## Official AWS Documentation References

Review the following official AWS documentation topics:

- Amazon EC2 security groups
- Security group rules for different use cases
- Amazon VPC security groups
- AWS Systems Manager Session Manager
- AWS IAM permissions for Session Manager
- AWS CloudTrail monitoring for security group changes
- AWS Config managed rules for restricted SSH
- Amazon EC2 key pairs and Linux instance access
