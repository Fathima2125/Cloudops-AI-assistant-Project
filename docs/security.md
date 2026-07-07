# Security

This project is designed for safe, local AI-assisted CloudOps analysis. It should be used to review files, logs, and reports without exposing secrets or making automatic infrastructure changes.

## Secrets Handling

- Store local credentials in `.env`, not in source-controlled files.
- Use `.env.example` only as a template for required variable names.
- Do not commit API keys, AWS credentials, private keys, certificates, kubeconfig files, or production logs containing sensitive data.
- Redact account IDs, tokens, customer data, IP addresses, and hostnames when creating public portfolio examples.
- Keep generated reports free of secrets before committing them.

## OpenAI API Key

`OPENAI_API_KEY` should be loaded from the local environment when needed. It should never be hardcoded into prompts, scripts, reports, or documentation.

## AWS Usage

Use a dedicated AWS profile for experiments and demos. The profile should have the minimum permissions needed for read-only review, such as describing resources, reading logs, and viewing configuration metadata.

Recommended default posture:

- Prefer read-only IAM policies.
- Use a sandbox AWS account when testing.
- Avoid production accounts for portfolio demonstrations.
- Review every suggested command before running it.
- Do not allow the assistant to apply Terraform, delete resources, rotate credentials, or change security groups automatically.

## Safe Review Process

AI-generated CloudOps recommendations should be treated as advisory. Before acting on a recommendation, confirm the affected account, region, resource name, blast radius, rollback plan, and approval requirement.
