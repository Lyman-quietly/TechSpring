# src/plugins/news.py
"""News API plugin for TechSpring.
Provides a simple wrapper around a generic news service.
Replace the placeholder implementation with a real API (e.g., NewsAPI.org) as needed.
"""
import os
import requests

class NewsPlugin:
    def __init__(self):
        # Expect an environment variable NEWS_API_KEY for authentication
        self.api_key = os.getenv("NEWS_API_KEY")
        self.endpoint = "https://newsapi.org/v2/everything"

    def fetch(self, query: str, max_results: int = 10):
        if not self.api_key:
            raise RuntimeError("NEWS_API_KEY environment variable not set")
        params = {
            "q": query,
            "pageSize": max_results,
            "apiKey": self.api_key,
            "language": "en",
        }
        response = requests.get(self.endpoint, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        # Normalize to a list of dicts with 'title' and 'content'
        results = []
        for article in data.get("articles", []):
            results.append({
                "title": article.get("title"),
                "content": article.get("description") or article.get("content"),
                "url": article.get("url"),
            })
        return results
