# tests/test_plugins.py
"""Unit tests for TechSpring data source plugins.
These tests mock external HTTP calls to avoid network dependency.
"""
import unittest
from unittest.mock import patch, MagicMock

# Import plugins (relative import assuming tests run from project root)
from src.plugins.news import NewsPlugin
from src.plugins.academic import AcademicPlugin
from src.plugins.sns import SNSPlugin

class TestNewsPlugin(unittest.TestCase):
    @patch('src.plugins.news.requests.get')
    def test_fetch_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "articles": [
                {"title": "Test News", "description": "Desc", "url": "http://example.com"}
            ]
        }
        mock_get.return_value = mock_response
        plugin = NewsPlugin()
        results = plugin.fetch('test query', max_results=1)
        self.assertIsInstance(results, list)
        self.assertEqual(results[0]['title'], 'Test News')
        self.assertIn('content', results[0])

class TestAcademicPlugin(unittest.TestCase):
    @patch('src.plugins.academic.requests.get')
    def test_search_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.text = """
        <entry>
            <title>Paper Title</title>
            <summary>Paper summary.</summary>
        </entry>
        """
        mock_get.return_value = mock_response
        plugin = AcademicPlugin()
        results = plugin.search('quantum computing', max_results=1)
        self.assertIsInstance(results, list)
        self.assertEqual(results[0]['title'], 'Paper Title')
        self.assertIn('summary', results[0])

class TestSNSPlugin(unittest.TestCase):
    @patch('src.plugins.sns.requests.get')
    def test_search_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "data": [
                {"id": "1", "text": "Tweet content", "author_id": "123", "created_at": "2025-01-01T00:00:00Z"}
            ]
        }
        mock_get.return_value = mock_response
        plugin = SNSPlugin()
        results = plugin.search('AI ethics', max_results=1)
        self.assertIsInstance(results, list)
        self.assertEqual(results[0]['text'], 'Tweet content')

if __name__ == '__main__':
    unittest.main()
