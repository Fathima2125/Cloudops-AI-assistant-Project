# Lambda Timeout Incident Report

## Executive Summary

An AWS Lambda invocation timed out after approximately 30 seconds. The log shows the function ran for `30003 ms`, then AWS terminated the execution because it exceeded the configured timeout.

The function was configured with `128 MB` of memory and used `118 MB`, which is close to the memory limit. This may indicate that the function was under-provisioned, running inefficient code, processing too much data, or waiting on a slow downstream dependency.

## AWS Service Involved

- Primary service: AWS Lambda
- Supporting service: Amazon CloudWatch Logs
- Possible related services: API Gateway, SQS, EventBridge, DynamoDB, RDS, or an external API, depending on what triggered the Lambda function

## Root Cause

The direct root cause is that the Lambda function exceeded its configured execution timeout.

The exact application-level cause is not visible from the provided log because there are no custom application logs, stack traces, dependency timings, or request details. Based on the available evidence, the most likely causes are:

- The Lambda timeout value was too low for the workload.
- The function code took too long to complete.
- A downstream service, database, or external API call was slow.
- The function had insufficient memory, which can also limit available CPU.
- The function processed too much work in a single invocation.

## Severity

- Severity: Medium
- Reason: A single Lambda timeout can cause one failed request or job, but it does not prove a full service outage. However, repeated timeouts can create user-facing failures, retry storms, delayed processing, and higher operational cost.
- Escalation condition: Treat this as High severity if the timeout affects production traffic, payment flows, authentication, data processing, customer-facing APIs, or happens repeatedly within a short time window.

## Impact

The affected Lambda invocation did not complete successfully. Any work expected from that invocation may have failed, been retried, or remained incomplete.

Possible business or operational impact:

- Failed API response if the Lambda was serving a request.
- Delayed queue or event processing if the Lambda was event-driven.
- Increased retry attempts and additional AWS cost.
- Duplicate processing risk if retries are not idempotent.
- Poor user experience if the timeout is part of a customer-facing workflow.
- Reduced confidence in the reliability of the workload if timeouts repeat.

## Key Log Evidence

```text
START RequestId: xxxxxxxxx Version: $LATEST
```

The Lambda invocation started successfully.

```text
Task timed out after 30.03 seconds
```

AWS stopped the function because it exceeded the configured timeout.

```text
Duration: 30003 ms
Memory Size: 128 MB
Max Memory Used: 118 MB
```

The function ran for about 30 seconds and used most of its available memory.

## Recommended Fix

1. Review the Lambda timeout setting and confirm whether a 30-second limit is appropriate for this workload.
2. Check CloudWatch Logs for application-level messages before the timeout to identify the slow operation.
3. Increase Lambda memory if the function is consistently close to the memory limit. More memory can also provide more CPU capacity.
4. Add timing logs around major code sections, database calls, API calls, and external dependencies.
5. Add timeout handling for downstream calls so the function fails gracefully before the Lambda runtime timeout.
6. Split large jobs into smaller units of work if the function is processing too much data in one invocation.
7. If this function is triggered by a queue, verify retry and dead-letter queue behavior.
8. Test the updated configuration with realistic payloads before applying changes to production.

## Prevention

1. Create CloudWatch alarms for Lambda errors, timeouts, duration, and throttles.
2. Alert when Lambda duration approaches the configured timeout.
3. Monitor memory usage and right-size functions that regularly use most of their allocated memory.
4. Use AWS X-Ray or structured logs to trace slow downstream calls.
5. Define a runbook for Lambda timeout investigation.
6. Use idempotency for event processing so retries do not cause duplicate side effects.
7. Add load and integration tests for expected payload sizes.
8. Review timeout, memory, and retry settings during deployment reviews.

## Simple Explanation

The Lambda function started, but it did not finish before its time limit expired. AWS stopped it after about 30 seconds. The function also used most of its available memory, so it may need better tuning, smaller work batches, or investigation into slow code or slow dependencies.

## Final Notes

The next best action is to review related CloudWatch logs and metrics for the same request ID. The team should confirm whether this was a one-time timeout or a recurring issue before making production changes.
