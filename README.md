# Level 2 — Hardened Low-Overhead API
Python standard-library HTTP service for `/healthz`, `/readyz`, and `/api/time`; deliberately few runtime dependencies.

## Run
```bash
docker build -t secure-api .
docker run --rm --read-only --cap-drop=ALL --security-opt no-new-privileges -p 8000:8000 secure-api
curl -i http://localhost:8000/healthz
curl -i http://localhost:8000/api/time
python -m unittest discover -s tests
```
For production use a reverse proxy and TLS terminator; this educational service is not an Internet-ready application server.

## Security and latency
Non-root UID, read-only filesystem option, container capability drop, bounded request path, no dynamic dependencies or secrets, security headers, JSON size limit. For comparisons collect latency distributions under load and report machine specifications. No unmeasured latency claims.
