# Threat Model

## Assets

- Authentication tokens
- Signing keys
- User identities and roles
- Operational metadata
- Internal-only service responses
- Password-reset capability

## Trust boundaries

- External client → public API
- API → internal service network
- Authenticated subject → object-level resources
- Token claims → authorization decisions

## Threats

- **Spoofing:** unsigned or weakly signed JWTs can allow identity or role spoofing.
- **Tampering:** a client can alter unverified claims such as `role`.
- **Information disclosure:** operational notes can expose credential-like data; IDOR can expose other profiles.
- **Elevation of privilege:** forged admin claims can reach privileged diagnostics.
- **SSRF:** user-controlled URLs can cause the API to cross the network trust boundary and reach internal services.

## Security objectives

Strong cryptographic token verification, object-level authorization on every resource lookup, no secrets in normal API responses, strict URL validation, outbound network restrictions, and clear separation of authentication from authorization.
