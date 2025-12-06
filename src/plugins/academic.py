# src/plugins/academic.py
"""Academic database plugin for TechSpring.
Provides a wrapper around the arXiv API (or similar) for searching scholarly articles.
Replace with a concrete API as needed.
"""
import requests
import urllib.parse

class AcademicPlugin:
    def __init__(self):
        self.base_url = "http://export.arxiv.org/api/query"

    def search(self, query: str, max_results: int = 5):
        # Simple arXiv query; returns list of dicts with title and summary
        params = {
            "search_query": f"all:{urllib.parse.quote(query)}",
            "start": 0,
            "max_results": max_results,
        }
        response = requests.get(self.base_url, params=params, timeout=10)
        response.raise_for_status()
        # Very basic parsing of ATOM XML; for brevity, extract titles and summaries via string ops
        entries = []
        raw = response.text
        for entry in raw.split("<entry>")[1:]:
            title_start = entry.find("<title>") + 7
            title_end = entry.find("</title>")
            summary_start = entry.find("<summary>") + 9
            summary_end = entry.find("</summary>")
            title = entry[title_start:title_end].strip()
            summary = entry[summary_start:summary_end].strip()
            entries.append({"title": title, "summary": summary})
        return entries
