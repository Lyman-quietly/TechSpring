import json
from duckduckgo_search import DDGS
import ollama

# Plugin imports
from src.plugins import NewsPlugin, AcademicPlugin, SNSPlugin

class TechResearcher:
    def __init__(self, model=None):
        self.ddgs = DDGS()
        self.model = model
        # Initialize plugin registry
        self.plugins = {}
        self.load_plugins()

    def load_plugins(self):
        """Instantiate and register available data source plugins."""
        self.plugins["news"] = NewsPlugin()
        self.plugins["academic"] = AcademicPlugin()
        self.plugins["sns"] = SNSPlugin()

    def perform_broad_search(self, query="technology trends viral active discussion last week", source: str = None):
        """Perform a broad search.
        If `source` is specified, delegate to the corresponding plugin.
        Otherwise, fall back to DuckDuckGo.
        """
        if source:
            plugin = self.plugins.get(source)
            if not plugin:
                raise ValueError(f"Unknown source plugin: {source}")
            if hasattr(plugin, "fetch"):
                return plugin.fetch(query, max_results=10)
            elif hasattr(plugin, "search"):
                return plugin.search(query, max_results=10)
            else:
                raise AttributeError(f"Plugin {source} does not provide a fetch/search method")
        print(f"Broad Search for '{query}'...")
        results = self.ddgs.text(query, max_results=10)
        return results

    def filter_active_topics(self, search_results):
        # Prepare a prompt for the LLM
        if ollama.ChatCompletion is not None:   # Check if Ollama ChatCompletion API is available
            try:
                prompt = f"""
                Analyze the following search results and identify 3 distinct technology topics that are currently generating active debate or controversy.
                Return a JSON list of objects with 'title' and 'query' keys.
                        
                Search Results:
                {json.dumps(search_results, indent=2)}
                """
                response = ollama.ChatCompletion(model=self.model).generate(prompt)  # Use Ollama ChatCompletion API
                # 返ってきたテキストをJSONとしてパース
                # Ollamaは直接文字列を返す
                selected_topics = json.loads(response)['topics']  # Assuming LLM returns wrapped json
                return selected_topics
            
            except Exception as e:
                print(f"  LLM Error: {e}")
                summary = "Error generating summary."
        else:
            # Fallback / Demo Logic
            print("  (Using fallback selection)")
            selected_topics = [
                {"title": "Agentic AI & Reward Hacking", "query": "Anthropic reward hacking"},
                {"title": "Vibe Coding vs AI Engineering", "query": "vibe coding debate"},
                {"title": "Model Context Protocol (MCP)", "query": "Model Context Protocol adoption"},
            ]
            return selected_topics

    def conduct_deep_dive(self, topics):
        print("Conducting Deep Dive...")
        report_sections = []
        for topic in topics:
            print(f"  Researching: {topic['title']}...")
            results = self.ddgs.text(topic['query'] + " latest discussion opinions analysis", max_results=5)
            
            if self.openai_client:
                try:
                    prompt = f"""
                    Synthesize the following search results into a concise technical summary for the topic '{topic['title']}'.
                    Focus on:
                    1. What is the core technology?
                    2. Why is it controversial or actively discussed right now?
                    3. Key arguments from different sides.
                    
                    Search Results:
                    {json.dumps(results, indent=2)}
                    """
                    
                    response = self.openai_client.chat.completions.create(
                        model="gpt-oss",
                        messages=[
                            {"role": "system", "content": "You are a technical research assistant."},
                            {"role": "user", "content": prompt}
                        ],
                    )
                    summary = response.choices[0].message.content
                except Exception as e:
                    print(f"  LLM Error: {e}")
                    summary = "Error generating summary."
            else:
                 # Fallback
                summary = f"Summary of {topic['title']}:\n"
                for r in results[:3]:
                    summary += f"- {r['title']}: {r['body']}\n"
            
            report_sections.append({"title": topic['title'], "content": summary})
        return report_sections

    def search_all_sources(self, query: str):
        """Run the query against all configured plugins and aggregate results."""
        aggregated = []
        for name, plugin in self.plugins.items():
            try:
                if hasattr(plugin, "fetch"):
                    results = plugin.fetch(query)
                elif hasattr(plugin, "search"):
                    results = plugin.search(query)
                else:
                    continue
                aggregated.extend(results)
            except Exception as e:
                print(f"Plugin {name} error: {e}")
        return aggregated
