# Architecture

The range has three logical components: the public Industrial Asset API, a localhost-only Python assessment toolkit, and a Docker-network-only internal console used to demonstrate SSRF impact.

```mermaid
flowchart TB
    A[Assessment Toolkit] --> B[Industrial Asset API :8080]
    B --> C[(Synthetic in-memory data)]
    B -. vulnerable URL preview .-> D[Internal Console :3001]
```

The intended trust boundary is between the public API and the internal console. Vulnerable mode intentionally violates that boundary through server-side URL fetching.
