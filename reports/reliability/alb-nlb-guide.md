# AWS Concept Explainer

## Executive Summary

Application Load Balancer and Network Load Balancer are both AWS Elastic Load Balancing options, but they solve different problems. ALB is used for HTTP and HTTPS application traffic where routing decisions depend on request details such as paths, hostnames, headers, or target groups. NLB is used for high-performance TCP, UDP, and TLS traffic where low latency, static IP support, or very high throughput is important.

In simple terms: use ALB for web applications and API routing. Use NLB for network-level traffic, extreme performance, static IP needs, or non-HTTP protocols.

## AWS Concept

- Concept: Application Load Balancer vs Network Load Balancer
- Related AWS service or feature: Elastic Load Balancing, Application Load Balancer, Network Load Balancer, target groups, listeners, health checks
- Common use case: Choosing the correct load balancer for web apps, APIs, microservices, TCP services, and high-throughput workloads

## Explanation

An Application Load Balancer operates at Layer 7, the application layer. It understands HTTP and HTTPS traffic. Because it understands web requests, it can route traffic based on hostnames, URL paths, headers, query strings, and other request-level details.

An ALB is commonly used for:

- Websites
- REST APIs
- Microservices
- Containerized applications
- Path-based routing such as `/api` and `/admin`
- Host-based routing such as `app.example.com` and `api.example.com`

A Network Load Balancer operates at Layer 4, the transport layer. It forwards TCP, UDP, or TLS traffic without inspecting HTTP application details. It is designed for very high performance, low latency, and static IP support.

An NLB is commonly used for:

- TCP applications
- UDP workloads
- TLS pass-through
- High-performance services
- Static IP requirements
- PrivateLink endpoint services
- Workloads where preserving the client source IP is important

## ALB vs NLB Comparison

| Area | ALB | NLB |
| --- | --- | --- |
| OSI layer | Layer 7 | Layer 4 |
| Protocols | HTTP, HTTPS, gRPC | TCP, UDP, TLS |
| Routing | Path, host, headers, query strings | Port and protocol based |
| Best for | Web apps and APIs | High-performance network traffic |
| Static IP | Not the main use case | Supported |
| Client IP preservation | Uses headers like `X-Forwarded-For` | Preserves source IP in many common patterns |
| TLS handling | TLS termination for HTTPS apps | TLS termination or pass-through patterns |
| Typical targets | EC2, IPs, Lambda, containers | EC2, IPs, ALB as target in some architectures |

## Best Practices

- Use ALB for HTTP and HTTPS workloads that need application-aware routing.
- Use NLB for TCP, UDP, TLS pass-through, static IPs, or very high performance.
- Configure health checks carefully so unhealthy targets are removed from rotation.
- Use HTTPS listeners and managed certificates for internet-facing web applications.
- Use least-privilege security group rules for ALB and backend targets.
- For ALB, forward only required paths and hosts to the correct target groups.
- For NLB, confirm target ports, protocols, and network ACL rules.
- Monitor load balancer metrics such as target health, latency, errors, and rejected connections.
- Use access logs where appropriate for investigation and audit needs.
- Choose internal load balancers for private services that do not need internet exposure.

## Common Mistakes

- Using NLB for an HTTP app that needs path-based routing.
- Using ALB for non-HTTP TCP or UDP workloads.
- Forgetting to configure health checks correctly.
- Allowing public access when the load balancer should be internal.
- Misconfiguring security groups between the load balancer and targets.
- Not enabling HTTPS for public web traffic.
- Expecting ALB to provide static IP addresses like an NLB.
- Ignoring target group health and only checking whether the load balancer exists.
- Sending traffic to the wrong target group because listener rules are ordered incorrectly.
- Not monitoring 4xx and 5xx errors on ALB-backed applications.

## Troubleshooting Tips

1. Check whether the workload is HTTP/HTTPS or raw TCP/UDP/TLS.
2. Confirm the listener protocol and port are correct.
3. Check target group health status.
4. Review health check path, protocol, port, success codes, and timeout settings.
5. For ALB, check listener rule priority and path or host matching.
6. For ALB, review HTTP 4xx and 5xx metrics to separate client, application, and load balancer errors.
7. For NLB, check target ports, network ACLs, route tables, and security group rules on targets.
8. Confirm whether the load balancer is internet-facing or internal.
9. Verify DNS records point to the correct load balancer.
10. Review access logs and application logs together when investigating traffic failures.

## Interview Explanation

ALB and NLB are both AWS load balancers, but they work at different layers. ALB works at Layer 7 and is best for HTTP and HTTPS applications because it can route based on hostnames, paths, and headers. I would use ALB for web apps, APIs, and microservices.

NLB works at Layer 4 and is best for TCP, UDP, TLS, very high performance, low latency, and static IP requirements. I would use NLB for network services, non-HTTP workloads, or systems that need static IPs or very high throughput.

The simplest way to remember it is: ALB for application routing, NLB for network-level performance and protocol flexibility.

## When to Use ALB

Use ALB when:

- The application uses HTTP or HTTPS.
- You need path-based routing.
- You need host-based routing.
- You are running web applications, APIs, or microservices.
- You want to route traffic to different target groups based on request content.
- You need integration with containers or Lambda targets.

Example:

- Route `example.com/api` to an API target group.
- Route `example.com/admin` to an admin service target group.
- Route `api.example.com` and `app.example.com` to different services.

## When to Use NLB

Use NLB when:

- The workload uses TCP, UDP, or TLS.
- You need very high throughput or low latency.
- You need static IP addresses.
- You need TLS pass-through or network-level forwarding.
- You are exposing a PrivateLink endpoint service.
- You need to preserve source IP behavior for network workloads.

Example:

- Expose a high-throughput TCP service.
- Run a UDP-based application.
- Provide a static IP endpoint for allowlisting.
- Front a private service through AWS PrivateLink.

## Official AWS Documentation References

Review the following official AWS documentation topics:

- Elastic Load Balancing
- Application Load Balancer
- Network Load Balancer
- ALB listeners and listener rules
- NLB listeners
- Elastic Load Balancing target groups
- Elastic Load Balancing health checks
- ALB access logs
- NLB access logs
- AWS PrivateLink endpoint services
