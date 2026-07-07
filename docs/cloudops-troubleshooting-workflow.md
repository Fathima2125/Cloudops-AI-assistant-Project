# CloudOps Troubleshooting Workflow

## Overview

This workflow summarizes the common troubleshooting process used across the Lambda timeout, EKS CrashLoopBackOff, and EC2 Nginx incident reports.

Although each incident involved a different service, the CloudOps approach was similar: read the logs, identify the failing component, determine the likely root cause, assess impact, recommend a safe fix, and document prevention steps.

## Incidents Compared

| Incident Report | Service | Main Symptom | Likely Root Cause |
| --- | --- | --- | --- |
| `lambda-timeout-report.md` | AWS Lambda | Function timed out after 30 seconds | Timeout, slow code, dependency delay, or insufficient resources |
| `eks-crashloop-report.md` | Amazon EKS / Kubernetes | Pod repeatedly restarted with `CrashLoopBackOff` | Application could not connect to PostgreSQL |
| `ec2-nginx-report.md` | Amazon EC2 / Nginx | Nginx failed to start | Port `80` was already in use |

## Common Troubleshooting Process

### 1. Identify the Affected Service

The first step is to determine which service or component is failing.

Examples:

- AWS Lambda function timing out.
- Kubernetes pod entering `CrashLoopBackOff`.
- Nginx service failing on an EC2 instance.

This helps narrow the investigation to the right logs, metrics, dashboards, and commands.

### 2. Read the Log Evidence

Cloud Engineers start with the strongest available evidence from logs.

Examples:

- `Task timed out after 30.03 seconds`
- `CrashLoopBackOff`
- `Error connecting to PostgreSQL`
- `Failed to bind to port 80`

The goal is to avoid guessing and base the investigation on actual system output.

### 3. Identify the Main Failure Pattern

After reading the logs, the engineer identifies the type of failure.

Common patterns from these reports:

- Timeout: the service did not finish within the allowed time.
- Dependency failure: the application could not connect to a required database.
- Port conflict: two processes attempted to use the same network port.

Recognizing the pattern helps choose the next troubleshooting step.

### 4. Assess Severity and Impact

The engineer then decides how serious the incident is.

Severity depends on:

- Whether production traffic is affected.
- Whether users are impacted.
- Whether the issue is recurring.
- Whether the service is critical.
- Whether retries or repeated restarts are increasing cost or risk.

For example, one Lambda timeout may be Medium severity, while repeated pod restarts or a failed public web service may be High severity.

### 5. Confirm the Root Cause

The root cause should be confirmed with additional read-only investigation before making changes.

Examples:

- For Lambda: check CloudWatch Logs, duration metrics, memory usage, and downstream dependency latency.
- For EKS: check pod events, previous container logs, Kubernetes Service endpoints, secrets, and database health.
- For EC2 Nginx: check which process is using port `80`, validate Nginx config, and inspect service status.

This step prevents engineers from applying the wrong fix.

### 6. Apply a Safe Remediation Plan

Recommended fixes should be practical and low-risk.

Examples:

- Increase Lambda memory or add timeout handling after confirming the bottleneck.
- Correct PostgreSQL connection settings or service routing after verifying the database path.
- Stop the conflicting process or change service ports after confirming what owns port `80`.

CloudOps remediation should avoid destructive actions unless there is clear approval and rollback planning.

### 7. Validate Recovery

After remediation, the engineer verifies that the service recovered.

Validation examples:

- Lambda invocations complete successfully.
- Kubernetes pod reaches `Running` and passes readiness checks.
- Nginx starts successfully and responds to HTTP health checks.
- Error logs stop appearing.
- Dashboards and alerts return to normal.

### 8. Document Prevention Steps

Every incident should produce follow-up actions that reduce repeat failures.

Common prevention actions:

- Add monitoring and alerts.
- Improve logging and tracing.
- Add readiness and health checks.
- Create or update runbooks.
- Validate configuration during deployment.
- Add retry logic with backoff.
- Review resource sizing and timeout settings.

## Simple Interview Explanation

A Cloud Engineer troubleshoots incidents by starting with the logs, identifying the affected service, and looking for the strongest error message. Then they map the error to a failure pattern, such as timeout, dependency failure, or port conflict.

After that, they assess severity, confirm the root cause using read-only checks, apply the safest fix, validate recovery, and document preventive actions. The goal is not just to fix the current issue, but also to reduce the chance of the same issue happening again.

## Standard Workflow Checklist

1. Identify the affected service.
2. Read the key log lines.
3. Determine the failure pattern.
4. Assess severity and impact.
5. Confirm the root cause with read-only checks.
6. Recommend or apply a safe fix.
7. Validate recovery.
8. Document prevention and lessons learned.

## Conclusion

The three incident reports show that CloudOps troubleshooting is a repeatable process. Whether the issue is Lambda, EKS, or EC2, the engineer follows the same core method: gather evidence, understand impact, isolate the cause, fix safely, verify recovery, and improve prevention.
