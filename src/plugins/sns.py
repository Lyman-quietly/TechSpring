# src/plugins/sns.py
"""Social Media (SNS) plugin for TechSpring.
Provides a wrapper around a generic social media search API.
Replace the placeholder with a real service (e.g., Twitter API v2) as needed.
"""
import os
import requests

class SNSPlugin:
    def __init__(self):
        # Expect environment variable SNS_BEARER_TOKEN for authentication (e.g., Twitter)
        self.bearer_token = os.getenv("SNS_BEARER_TOKEN")
        self.endpoint = "https://api.twitter.com/2/tweets/search/recent"

    def search(self, query: str, max_results: int = 10):
        if not self.bearer_token:
            raise RuntimeError("SNS_BEARER_TOKEN environment variable not set")
        headers = {"Authorization": f"Bearer {self.bearer_token}"}
        params = {
            "query": query,
            "max_results": max_results,
            "tweet.fields": "author_id,created_at,text",
        }
        response = requests.get(self.endpoint, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        results = []
        for tweet in data.get("data", []):
            results.append({
                "id": tweet.get("id"),
                "text": tweet.get("text"),
                "author_id": tweet.get("author_id"),
                "created_at": tweet.get("created_at"),
            })
        return results
