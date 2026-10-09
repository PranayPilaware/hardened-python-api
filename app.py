from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os

ROUTES = {"/healthz", "/readyz", "/api/time"}

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        route = self.path.split("?", 1)[0]
        if route not in ROUTES:
            self.respond(404, {"error": "not found"})
            return
        if route == "/api/time":
            self.respond(200, {"utc": datetime.now(timezone.utc).isoformat()})
        else:
            self.respond(200, {"status": "ok"})

    def respond(self, code, data):
        body = json.dumps(data, separators=(",", ":")).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.end_headers()
        self.wfile.write(body)

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    if not (1 <= port <= 65535):
        raise ValueError("invalid port")
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()
