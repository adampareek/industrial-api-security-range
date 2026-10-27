# Remediation Guide

## IASR-01 — Sensitive information exposure
Never place passwords, API keys, recovery tokens, or connection strings in user-visible metadata. Store secrets in a dedicated secret manager and return only necessary fields.

## IASR-02 — JWT `alg: none`
Configure an explicit algorithm allowlist and validate signature, issuer, audience, expiration, and required claims before authorization.

## IASR-03 — Weak signing secret
Use high-entropy random signing keys stored outside source code and rotate them through managed secret storage.

## IASR-04 — BOLA / IDOR
Object identifiers are not authorization controls. Verify that the authenticated subject is authorized for the requested object.

## IASR-05 — Privilege escalation
Trust role claims only after cryptographic token verification and perform explicit authorization at sensitive endpoints.

## IASR-06 — SSRF
Permit only required schemes, reject embedded credentials, resolve and validate destinations, block private/loopback/link-local ranges, disable or validate redirects, and enforce outbound network policy.
