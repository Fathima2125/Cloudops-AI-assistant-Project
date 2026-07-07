# Cloud Log Analysis Report

## Executive Summary

The Nginx service on an EC2 instance failed to start because port `80` was already in use by another process. Since Nginx could not bind to the HTTP port, the web service was unable to start successfully.

This issue may cause the website or application hosted behind Nginx to become unavailable until the port conflict is resolved.

## Root Cause

The most likely root cause is a port conflict on port `80`.

Nginx needs to bind to port `80` to serve HTTP traffic. The log shows that another process is already using that port, so Nginx cannot start.

Possible causes include:

- Another web server, such as Apache or another Nginx process, is already running.
- A previous Nginx process did not shut down cleanly.
- A container or application process is listening directly on port `80`.
- A deployment or configuration change started a second service on the same port.

## Simple Explanation

Only one process can listen on port `80` at a time. Nginx tried to start and use port `80`, but another process was already using it. Because of that, Nginx failed to start.

## Severity Assessment

- Severity: High
- Reason: If this EC2 instance serves production web traffic, Nginx being down can cause customer-facing HTTP requests to fail. Severity may be Medium if this is a development instance, standby instance, or non-critical service.

## Key Log Evidence

```text
nginx.service: Failed to start.
```

The Nginx service did not start successfully.

```text
Address already in use
```

The operating system rejected the bind attempt because the port is occupied.

```text
Failed to bind to port 80
```

Nginx could not attach to the HTTP port.

```text
Another process is using port 80.
```

The direct cause is a competing process already listening on port `80`.

## Recommended Fixes

1. Identify the process using port `80` with a command such as `sudo lsof -i :80` or `sudo ss -tulpn | grep :80`.
2. Confirm whether the process using port `80` is expected.
3. If the process is not needed, stop or disable it safely.
4. If another web service is intentionally running, update either Nginx or the other service to use a different port.
5. Check the Nginx configuration for duplicate `listen 80` directives or conflicting server blocks.
6. Validate the Nginx configuration with `sudo nginx -t`.
7. Restart Nginx after resolving the conflict.
8. Confirm the service is healthy with `systemctl status nginx` and an HTTP health check.

## Preventive Actions

1. Add monitoring for Nginx service status and failed starts.
2. Add an HTTP health check for the web endpoint.
3. Include port conflict checks in deployment scripts or runbooks.
4. Use configuration management to ensure only the intended service owns port `80`.
5. Review startup dependencies so services start in the correct order.
6. Document a standard incident runbook for web server startup failures.
7. Alert on repeated Nginx restart failures or systemd service failures.

## Assumptions and Missing Information

Assumptions:

- The log came from an EC2 instance running Nginx as a systemd service.
- Nginx is expected to serve HTTP traffic on port `80`.
- The instance may be hosting a website, application frontend, or reverse proxy.

Missing information:

- EC2 instance ID and environment.
- Full `systemctl status nginx` output.
- Output showing which process is using port `80`.
- Nginx site configuration files.
- Whether the instance is production, staging, or development.
- Whether this happened after a deployment or restart.

## Final Notes

The next best action is to identify the process currently using port `80`, confirm whether it should be running, and then safely remove the conflict before restarting Nginx.
