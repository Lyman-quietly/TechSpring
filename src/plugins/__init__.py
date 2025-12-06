# src/plugins/__init__.py
"""Plugin package for TechSpring data source extensions.
Exports plugin classes for dynamic discovery.
"""

from .news import NewsPlugin
from .academic import AcademicPlugin
from .sns import SNSPlugin

__all__ = ["NewsPlugin", "AcademicPlugin", "SNSPlugin"]
