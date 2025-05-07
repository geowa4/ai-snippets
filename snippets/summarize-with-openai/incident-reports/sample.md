Kubernetes Cluster Incident Report

Impacted Products Overview

Product	Severity	Status	Updated Date
Product A	High	Resolved	2025-05-07 10:00 AM
Product B	Medium	Ongoing	2025-05-07 11:00 AM
Product C	Low	Resolved	2025-05-07 09:45 AM

Incident Description

An incident was detected within the Kubernetes cluster, affecting several products hosted on the platform. The root cause of the issue was a misconfigured ingress controller that caused connectivity issues, leading to product downtime. The incident began around 9:00 AM on May 7th, 2025, and affected both internal and external services. After swift action, Product A and Product C were resolved by 10:00 AM, but Product B remains under investigation.

Sequence of Events
	•	2025-05-07 09:00 AM: Alert triggered regarding degraded service for Product A and Product B due to ingress controller misconfiguration.
	•	2025-05-07 09:15 AM: Engineers begin diagnosing the ingress controller configuration and identify the misconfiguration causing the connectivity issue.
	•	2025-05-07 09:30 AM: Service for Product A is restored by fixing the ingress rule.
	•	2025-05-07 09:45 AM: Product C is verified as unaffected and restored to normal operation.
	•	2025-05-07 10:00 AM: Product A marked as resolved, and full connectivity is restored.
	•	2025-05-07 10:30 AM: Product B remains impacted, further investigation continues.
	•	2025-05-07 11:00 AM: Product B connectivity issue partially resolved, with a remaining 20% degraded performance.