"""
Unit tests for YouTube Streaming & Search API.
"""
import os
import sys
import unittest

WORKSPACE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if WORKSPACE not in sys.path:
    sys.path.insert(0, WORKSPACE)

from kanban import create_app
from kanban.services.youtube import get_youtube_account_status, resolve_video_stream, search_youtube


class TestYouTubeEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app.config["TESTING"] = True
        cls.client = cls.app.test_client()

    def test_search_and_account_status(self):
        """Testa busca no catálogo do YouTube e verificação de status de conta."""
        status = get_youtube_account_status()
        self.assertIn("mode", status)
        self.assertIn("browser", status)
        self.assertIn("adblock_active", status)

        # Rota de conta
        r_acc = self.client.get("/api/youtube/account")
        self.assertEqual(r_acc.status_code, 200)

        # Busca com termo conhecido
        results = search_youtube("Kamisa 10", limit=3)
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
        first = results[0]
        self.assertIn("id", first)
        self.assertIn("title", first)

        # Rota HTTP de busca
        r_search = self.client.get("/api/youtube/search?q=Kamisa+10")
        self.assertEqual(r_search.status_code, 200)
        data = r_search.get_json()
        self.assertIn("results", data)
        self.assertGreater(len(data.get("results", [])), 0)

    def test_info_and_stream(self):
        """Testa resolução de stream para reprodução sem embed."""
        video_id = "GrH68P0o60U"
        info = resolve_video_stream(video_id)
        self.assertIsNotNone(info)
        self.assertIn("direct_url", info)

        # Proxy de streaming (HTTP 206 Partial Content)
        r_stream = self.client.get(f"/api/youtube/stream/{video_id}", headers={"Range": "bytes=0-1024"})
        self.assertIn(r_stream.status_code, [200, 206])
        self.assertTrue(r_stream.headers.get("Content-Type", "").startswith("video/"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
