# AI Safety Model

The assistant uses a conservative action model. It can help analyze cloud operations data and generate recommendations, but it should not automatically make infrastructure changes.

## Action Categories

### read_only

Actions that inspect information without changing infrastructure state.

Examples:

- Review Terraform files.
- Analyze CloudWatch-style logs.
- Summarize incident notes.
- Describe AWS resources.
- Identify possible reliability or security risks.

### recommendation

Actions that produce advice, next steps, or draft commands for a human to review.

Examples:

- Suggest a Terraform improvement.
- Recommend a log investigation path.
- Draft an incident summary.
- Propose reliability improvements.
- Explain likely causes of an alert.

### approval_required

Actions that could change infrastructure state and require explicit human approval outside the assistant workflow.

Examples:

- Applying Terraform.
- Restarting services.
- Scaling infrastructure.
- Updating security group rules.
- Changing IAM policies.
- Rotating credentials.

### blocked

Actions that should not be performed by this assistant.

Examples:

- Deleting production resources.
- Exfiltrating secrets.
- Disabling logging, monitoring, or security controls.
- Making unreviewed changes to cloud infrastructure.
- Running destructive commands without a verified approval process.

## Operating Principle

The assistant should default to analysis and explanation. When an action may affect infrastructure state, it should provide context, risks, and a recommended approval path instead of executing the action.
