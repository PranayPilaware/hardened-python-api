import io
import json
import unittest
from unittest.mock import Mock
from http import HTTPStatus
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import Handler

class TestHandler(unittest.TestCase):
    def test_routes(self):
        self.assertEqual({"/healthz", "/readyz", "/api/time"}, __import__("app").ROUTES)

    def test_json_structure(self):
        data = {"status": "ok"}
        self.assertEqual(json.loads(json.dumps(data)), data)

if __name__ == "__main__":
    unittest.main()
