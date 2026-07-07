# Terraform Before and After Comparison

## Overview

This comparison explains the difference between `terraform/sample-vpc.tf` and `terraform/sample-vpc-improved.tf` in simple Cloud Engineer interview language.

The original file is a basic Terraform example that creates a VPC, public subnet, security group, and EC2 instance. The improved file keeps the same general idea, but makes the configuration safer, more reusable, and closer to real CloudOps practices.

## Summary Table

| Area | Original Version | Improved Version |
| --- | --- | --- |
| SSH access | Allows SSH from `0.0.0.0/0` | Uses `allowed_ssh_cidr` so SSH must come from a trusted CIDR |
| Public IP behavior | Automatically assigns public IPs in the subnet | Disables automatic public IP assignment |
| Hardcoded values | Region, CIDR blocks, AMI, and instance type are hardcoded | Uses variables for region, CIDR blocks, AMI, instance type, project, and environment |
| Tags | No tags | Adds common tags for ownership, environment, and management |
| Provider control | No Terraform or provider version constraints | Adds Terraform and AWS provider version constraints |
| EC2 security group attachment | Uses `security_groups` | Uses `vpc_security_group_ids`, which is clearer for VPC security groups |
| DNS settings | Not explicitly configured | Enables VPC DNS support and DNS hostnames |
| Comments | Minimal context | Adds comments explaining the security and maintainability improvements |

## Key Differences Explained

### 1. SSH Access Is Safer

In the original file, SSH is open to the entire internet:

```hcl
cidr_blocks = ["0.0.0.0/0"]
```

That is risky because anyone on the internet can attempt to connect to port `22`.

In the improved version, SSH access uses a variable:

```hcl
cidr_blocks = [var.allowed_ssh_cidr]
```

The improved version also includes validation to prevent `0.0.0.0/0` from being used for SSH. In an interview, I would explain that administrative access should be restricted to a trusted office, VPN, or bastion network.

### 2. The Improved Version Is More Reusable

The original file hardcodes values such as:

- AWS region
- VPC CIDR block
- Subnet CIDR block
- AMI ID
- Instance type

The improved file moves these values into variables. This makes the Terraform easier to reuse across environments such as `dev`, `test`, and `prod`.

In interview terms: the original version is fine for a quick demo, but the improved version is better because it separates configuration from infrastructure logic.

### 3. Tags Were Added for CloudOps Visibility

The original file does not include tags. That makes it harder to identify ownership, environment, cost allocation, and operational responsibility.

The improved version adds common tags such as:

- `Project`
- `Environment`
- `ManagedBy`
- `Owner`
- `Name`

This is important in real AWS environments because tags help with billing, incident response, automation, and resource inventory.

### 4. Provider Version Constraints Were Added

The original file does not specify Terraform or AWS provider versions. That means different engineers could run the same code with different provider versions and potentially get different behavior.

The improved file adds:

```hcl
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
```

In interview language: version constraints make Terraform runs more predictable and reduce the chance of unexpected provider behavior.

### 5. EC2 Uses the Better VPC Security Group Argument

The original EC2 instance uses:

```hcl
security_groups = [
  aws_security_group.web_sg.id
]
```

The improved version uses:

```hcl
vpc_security_group_ids = [
  aws_security_group.web_sg.id
]
```

For EC2 instances inside a VPC, `vpc_security_group_ids` is clearer and more appropriate because it attaches security groups by ID.

### 6. Public IP Assignment Was Reduced

The original subnet automatically assigns public IP addresses:

```hcl
map_public_ip_on_launch = true
```

The improved version changes this to:

```hcl
map_public_ip_on_launch = false
```

This reduces accidental internet exposure. In a production design, I would usually keep application instances private and expose traffic through a load balancer or another controlled entry point.

## Interview Explanation

If I were explaining this in a Cloud Engineer interview, I would say:

The first Terraform file is a simple starting point, but it has common risks like public SSH, hardcoded values, no tags, and no provider version constraints. I improved it by making the infrastructure more secure and maintainable. I restricted SSH using a variable, added validation to avoid opening SSH to the internet, moved hardcoded values into variables, added common tags, pinned provider versions, and used `vpc_security_group_ids` for the EC2 instance.

I would also mention that I did not completely redesign the architecture. I kept the project small and portfolio-friendly, but improved the most important CloudOps concerns: security, reusability, visibility, and Terraform best practices.

## What This Shows

This before-and-after comparison shows that I can:

- Review Terraform for security and operational risks.
- Explain AWS networking issues in simple terms.
- Improve infrastructure code without changing the project scope.
- Apply CloudOps best practices such as tagging, variable usage, and provider constraints.
- Use AI-assisted review output and turn it into practical infrastructure improvements.

## Conclusion

`terraform/sample-vpc.tf` is a basic learning example. `terraform/sample-vpc-improved.tf` is a cleaner and safer version that better reflects Cloud Engineer and DevOps practices. The improved version is still intentionally small, but it demonstrates stronger thinking around security, maintainability, and operational readiness.
