import json
import threading
import unittest
from datetime import datetime
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import urlopen
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import Handler


class APITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        cls.url = f"http://127.0.0.1:{cls.server.server_port}"
        cls.worker = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.worker.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.worker.join(timeout=3)
        cls.server.server_close()

    def request(self, route):
        try:
            response = urlopen(self.url + route, timeout=3)
        except HTTPError as error:
            response = error
        with response:
            return response.status, dict(response.headers), json.loads(response.read())

    def test_health_endpoint(self):
        status, headers, data = self.request("/healthz")
        self.assertEqual(status, 200)
        self.assertEqual(data, {"status": "ok"})
        self.assertEqual(headers["Cache-Control"], "no-store")

    def test_readiness_endpoint(self):
        status, _, data = self.request("/readyz")
        self.assertEqual(status, 200)
        self.assertEqual(data["status"], "ok")

    def test_utc_time_endpoint(self):
        status, _, data = self.request("/api/time")
        self.assertEqual(status, 200)
        self.assertIn("utc", data)
        self.assertIsNotNone(datetime.fromisoformat(data["utc"]).tzinfo)

    def test_unknown_path_returns_404(self):
        status, _, data = self.request("/api/not-found")
        self.assertEqual(status, 404)
        self.assertEqual(data, {"error": "not found"})

    def test_security_headers(self):
        _, headers, _ = self.request("/healthz")
        self.assertEqual(headers["X-Content-Type-Options"], "nosniff")
        self.assertEqual(headers["X-Frame-Options"], "DENY")
        self.assertTrue(headers["Content-Type"].startswith("application/json"))

    def test_health_querystring(self):
        status, _, data = self.request("/healthz?trace=ignored")
        self.assertEqual(status, 200)
        self.assertEqual(data["status"], "ok")


if __name__ == "__main__":
    unittest.main()
