# Terraform Review Report

## Executive Summary

This report reviews `terraform/sample-vpc.tf`, which defines a basic AWS VPC, public subnet, security group, and EC2 instance. The configuration is useful for demonstrating Terraform review skills, but it should not be used as-is for production workloads.

The main production concern is public exposure. SSH is open to the internet, instances launched in the subnet receive public IP addresses, and HTTP is allowed without TLS. The configuration also contains hardcoded values, missing tags, limited reliability design, and several Terraform best-practice gaps.

Overall risk level: **High** for production use.

## Severity Summary

| Severity | Count | Summary |
| --- | ---: | --- |
| Critical | 0 | No critical findings were identified in this small sample. |
| High | 1 | SSH is exposed to the public internet. |
| Medium | 6 | Public IP assignment, HTTP exposure, hardcoded AMI, missing tags, single-subnet design, and EC2 security group usage need improvement. |
| Low | 5 | Broad egress, hardcoded region and instance type, DNS settings, and version constraints should be cleaned up. |

## Findings

### 1. SSH Is Open to the Internet

- Finding: The security group allows inbound SSH access from `0.0.0.0/0`.
- Severity: High
- Affected Resource: `aws_security_group.web_sg`
- Why It Matters: Public SSH exposure increases the risk of brute-force attempts, credential attacks, unauthorized access, and automated internet scanning.
- Recommendation: Restrict SSH to a trusted administrative CIDR range, use a VPN or bastion host, or prefer AWS Systems Manager Session Manager for administrative access.

### 2. Instances Launched in the Public Subnet Receive Public IPs

- Finding: `map_public_ip_on_launch` is set to `true`.
- Severity: Medium
- Affected Resource: `aws_subnet.public`
- Why It Matters: Automatically assigning public IP addresses increases the chance that compute resources become internet-accessible unintentionally.
- Recommendation: Disable automatic public IP assignment by default unless public exposure is explicitly required. Place private workloads in private subnets and expose only required services through controlled entry points such as load balancers.

### 3. HTTP Is Open to the Internet Without TLS

- Finding: The security group allows inbound HTTP traffic from `0.0.0.0/0` on port `80`.
- Severity: Medium
- Affected Resource: `aws_security_group.web_sg`
- Why It Matters: Plain HTTP does not encrypt traffic and is not appropriate for sensitive application communication.
- Recommendation: For production workloads, prefer HTTPS on port `443` with managed certificates. If HTTP is needed, use it only for redirecting to HTTPS.

### 4. Broad Outbound Access Is Allowed

- Finding: The security group allows all outbound traffic to `0.0.0.0/0`.
- Severity: Low
- Affected Resource: `aws_security_group.web_sg`
- Why It Matters: Broad egress is common but can increase impact if an instance is compromised, allowing unrestricted outbound communication.
- Recommendation: Restrict egress where practical based on application requirements, such as package repositories, APIs, monitoring endpoints, or VPC endpoints.

### 5. AWS Region Is Hardcoded

- Finding: The provider region is hardcoded as `us-east-1`.
- Severity: Low
- Affected Resource: `provider "aws"`
- Why It Matters: Hardcoded regions make reuse across environments harder and can lead to accidental deployment in the wrong region.
- Recommendation: Use an input variable such as `var.aws_region` and define environment-specific values separately.

### 6. AMI ID Is Hardcoded

- Finding: The EC2 instance uses a hardcoded AMI value: `ami-12345678`.
- Severity: Medium
- Affected Resource: `aws_instance.web`
- Why It Matters: Hardcoded AMI IDs can become outdated, unavailable in other regions, or invalid. The sample value may not resolve to a real approved image.
- Recommendation: Use a data source to look up an approved AMI dynamically, or manage AMI IDs through environment-specific variables.

### 7. Instance Type Is Hardcoded

- Finding: The EC2 instance type is hardcoded as `t2.micro`.
- Severity: Low
- Affected Resource: `aws_instance.web`
- Why It Matters: Hardcoded instance sizing limits flexibility and can create cost, performance, or compatibility issues across environments.
- Recommendation: Use a variable such as `var.instance_type` with a sensible default.

### 8. Missing Resource Tags

- Finding: The VPC, subnet, security group, and EC2 instance do not define tags.
- Severity: Medium
- Affected Resources: `aws_vpc.main`, `aws_subnet.public`, `aws_security_group.web_sg`, `aws_instance.web`
- Why It Matters: Tags are important for ownership, cost allocation, environment separation, automation, and incident response.
- Recommendation: Add standard tags such as `Name`, `Environment`, `Owner`, `Project`, `ManagedBy`, and `CostCenter`.

### 9. No Availability Zone Strategy

- Finding: The subnet does not specify an availability zone and only one subnet is defined.
- Severity: Medium
- Affected Resource: `aws_subnet.public`
- Why It Matters: A single subnet limits availability and does not support multi-AZ resilience.
- Recommendation: Define subnets across multiple availability zones for production architectures.

### 10. VPC DNS Settings Are Not Explicit

- Finding: The VPC does not explicitly enable DNS support or DNS hostnames.
- Severity: Low
- Affected Resource: `aws_vpc.main`
- Why It Matters: Many AWS services and operational patterns rely on predictable DNS behavior.
- Recommendation: Set `enable_dns_support = true` and `enable_dns_hostnames = true` when the workload requires DNS resolution and hostnames.

### 11. EC2 Resource Uses `security_groups` With a VPC Security Group ID

- Finding: The EC2 instance sets `security_groups = [aws_security_group.web_sg.id]`.
- Severity: Medium
- Affected Resource: `aws_instance.web`
- Why It Matters: In a VPC, `vpc_security_group_ids` is the clearer and preferred argument for security group IDs. Using `security_groups` is associated with EC2-Classic style naming behavior and can cause confusion.
- Recommendation: Replace `security_groups` with `vpc_security_group_ids`.

### 12. No Terraform Version or Provider Version Constraints

- Finding: The configuration does not include a `terraform` block with required Terraform and AWS provider versions.
- Severity: Low
- Affected Resource: Terraform configuration
- Why It Matters: Missing version constraints can cause behavior changes when different Terraform or provider versions are used.
- Recommendation: Add a `terraform` block with `required_version` and `required_providers`.

## Clear Remediation Steps

1. Restrict SSH access by replacing `0.0.0.0/0` with a trusted administrative CIDR range, or remove SSH access and use AWS Systems Manager Session Manager.
2. Disable automatic public IP assignment on the subnet unless the instance must be directly reachable from the internet.
3. Replace direct HTTP exposure with HTTPS through a load balancer and a managed TLS certificate.
4. Add standard tags to all resources for ownership, environment tracking, cost allocation, and operational visibility.
5. Move hardcoded values into variables, including region, VPC CIDR, subnet CIDR, AMI ID, instance type, and allowed SSH CIDR.
6. Use `vpc_security_group_ids` on the EC2 instance instead of `security_groups`.
7. Add Terraform and AWS provider version constraints to make runs more predictable.
8. Add a multi-AZ subnet strategy if this design is expanded beyond a learning sample.
9. Review outbound access and restrict egress where application requirements are known.
10. Validate the final design with `terraform fmt`, `terraform validate`, and a manual security review before applying any changes.

## Positive Observations

- The Terraform file is small and easy to review.
- Resource relationships are clear: the subnet references the VPC, and the instance references the subnet.
- The security group uses descriptions for ingress rules, which improves readability.
- The configuration is suitable as a simple teaching example for Terraform review workflows.

## Recommended Improved Terraform Changes

The Terraform file was not modified. Recommended future improvements include:

- Replace hardcoded values with variables for region, CIDR ranges, AMI ID, instance type, and allowed SSH CIDR.
- Restrict SSH access to a trusted CIDR range or remove SSH entirely in favor of AWS Systems Manager Session Manager.
- Prefer HTTPS over HTTP for internet-facing application traffic.
- Add standard tags to every resource.
- Use `vpc_security_group_ids` for the EC2 instance.
- Add Terraform and provider version constraints.
- Define multiple subnets across availability zones for higher reliability.
- Disable automatic public IP assignment unless the workload explicitly requires public access.
- Consider using private subnets and a load balancer for production-style web architectures.

## Interview Explanation

I reviewed this Terraform file as if it were a lightweight CloudOps security assessment. I first identified the main resources, then checked common operational risk areas: network exposure, access control, hardcoded configuration, tagging, reliability, and Terraform maintainability.

The most important issue is the security group rule that allows SSH from `0.0.0.0/0`. In an interview, I would explain that this is a high-risk pattern because it exposes administrative access to the entire internet. My preferred remediation would be to remove public SSH and use AWS Systems Manager Session Manager. If SSH is required, I would restrict it to a known corporate or VPN CIDR range.

I would also call out that this design is acceptable as a learning sample, but production infrastructure should separate public and private resources, use HTTPS, define version constraints, tag resources, and avoid hardcoded values. The report demonstrates how AI can help accelerate review, while the engineer remains responsible for validating the recommendations before making changes.

## What I Learned

- Small Terraform files can still contain meaningful production risks.
- Security group rules are one of the most important areas to review in AWS infrastructure.
- Public subnet settings and public IP assignment should be treated as intentional design decisions, not defaults.
- Tags are operationally important for cost tracking, incident response, ownership, and automation.
- AI-assisted reviews are most useful when paired with structured prompts, clear severity levels, and human validation.

## Conclusion

This Terraform sample is a strong portfolio artifact because it shows how a CloudOps assistant can review infrastructure code, identify practical risks, and produce a professional report. The configuration should remain unchanged until the findings are reviewed and prioritized. For production use, the first remediation should be closing public SSH access, followed by reducing public exposure, adding tags, and replacing hardcoded values with reusable variables.

No changes were made to `terraform/sample-vpc.tf`.
