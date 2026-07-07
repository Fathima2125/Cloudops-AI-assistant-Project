# AWS Concept Explainer

## Executive Summary

IAM users and IAM roles are both AWS Identity and Access Management identities, but they are used for different purposes. An IAM user usually represents a person or long-lived identity, while an IAM role is meant to be assumed temporarily by AWS services, applications, federated users, or workloads.

For CloudOps and DevOps work, IAM roles are usually preferred for AWS services such as EC2 and Lambda because they provide temporary credentials and reduce the need to store access keys. IAM users should be limited and carefully managed, especially when long-term credentials are involved.

## AWS Concept

- Concept: IAM roles vs IAM users
- Related AWS service or feature: AWS Identity and Access Management, IAM roles, IAM users, instance profiles, Lambda execution roles, AWS STS
- Common use case: Choosing the correct AWS identity type for people, EC2 instances, Lambda functions, and automation

## Explanation

An IAM user is an identity in AWS that can have a username, password, access keys, and permissions. IAM users are often used for human access or legacy automation, but they can become risky if long-term access keys are not rotated or protected.

An IAM role is an identity with permissions that can be assumed by a trusted entity. The trusted entity could be an AWS service, another AWS account, a federated identity provider, or a workload. Roles use temporary credentials, which makes them safer for applications and AWS services.

For example, an EC2 instance should not store permanent AWS access keys on disk. Instead, it should use an IAM role attached through an instance profile. The instance can then call AWS services using temporary credentials automatically provided by AWS.

Similarly, a Lambda function should use a Lambda execution role. The role grants only the permissions the function needs, such as writing logs to CloudWatch or reading from an S3 bucket.

## Best Practices

- Prefer IAM roles for AWS services such as EC2, Lambda, ECS, and EKS workloads.
- Avoid storing long-term access keys on servers, in code, or in environment files.
- Use least privilege permissions for both users and roles.
- Use IAM users only when a long-lived human or legacy identity is truly needed.
- Require MFA for human access where possible.
- Use IAM Identity Center or federation for workforce access instead of creating many IAM users.
- Attach IAM roles to EC2 instances using instance profiles.
- Use Lambda execution roles for Lambda permissions.
- Separate trust policies from permission policies conceptually: trust policies define who can assume the role, while permission policies define what the role can do.
- Review IAM policies regularly and remove unused permissions.

## Common Mistakes

- Creating IAM users for applications instead of using IAM roles.
- Hardcoding IAM user access keys inside application code.
- Giving EC2 instances or Lambda functions overly broad permissions such as `AdministratorAccess`.
- Forgetting that a role needs both a trust policy and permission policy.
- Using one shared IAM user for multiple people or services.
- Not rotating old access keys.
- Not enabling MFA for human users.
- Giving a Lambda execution role access to services it does not need.
- Confusing an EC2 instance profile with the IAM role itself.

## Troubleshooting Tips

1. If EC2 cannot access an AWS service, check whether an IAM role is attached through an instance profile.
2. Verify that the role policy allows the required action, such as `s3:GetObject` or `logs:CreateLogStream`.
3. Check the role trust policy to confirm the correct service can assume the role.
4. For Lambda, verify the function has the correct execution role attached.
5. Check CloudWatch Logs for `AccessDenied` or permission-related errors.
6. Use AWS CloudTrail to see which identity made a denied request.
7. Use IAM policy simulator or access analyzer tools to review permissions.
8. Confirm that resource policies, such as S3 bucket policies or KMS key policies, also allow the action.
9. Remove hardcoded credentials from application environments and switch to role-based access where possible.
10. Review whether permission boundaries, service control policies, or session policies are limiting access.

## Interview Explanation

An IAM user is usually for a person or long-lived identity, while an IAM role is for temporary access. AWS services like EC2 and Lambda should use roles instead of stored access keys.

For EC2, I would attach an IAM role through an instance profile so the instance can access services like S3 using temporary credentials. For Lambda, I would assign an execution role with only the permissions the function needs, such as writing logs to CloudWatch or reading from a specific S3 bucket.

The main idea is that users are for direct identities, while roles are for delegated and temporary access. In production, roles are safer for workloads because they reduce long-term credential exposure.

## EC2 Example

An EC2 instance needs to read objects from an S3 bucket.

Recommended approach:

- Create an IAM role for EC2.
- Attach a policy allowing only the required S3 read actions.
- Attach the role to the EC2 instance through an instance profile.
- Let the application use the AWS SDK default credential chain.

Avoid this approach:

- Creating an IAM user.
- Generating access keys.
- Copying those keys onto the EC2 instance.

## Lambda Example

A Lambda function needs to write logs to CloudWatch and read from DynamoDB.

Recommended approach:

- Create or update the Lambda execution role.
- Allow only the required CloudWatch Logs actions.
- Allow only the required DynamoDB read actions on the specific table.
- Attach the execution role to the Lambda function.

Avoid this approach:

- Storing IAM user access keys in Lambda environment variables.
- Giving the Lambda function broad administrator permissions.

## Official AWS Documentation References

Review the following official AWS documentation topics:

- AWS Identity and Access Management
- IAM users
- IAM roles
- IAM role trust policies
- IAM permission policies
- AWS Security Token Service
- IAM roles for Amazon EC2
- Instance profiles for Amazon EC2
- AWS Lambda execution role
- IAM best practices
- IAM Access Analyzer
