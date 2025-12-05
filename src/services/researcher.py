import json
from duckduckgo_search import DDGS

class TechResearcher:
    def __init__(self, openai_client=None):
        self.ddgs = DDGS()
        self.openai_client = openai_client

    def step_1_broad_search(self, query="technology trends viral active discussion last week"):
        print(f"Step 1: Broad Search for '{query}'...")
        results = self.ddgs.text(query, max_results=10)
        return results

    def step_2_filter_topics(self, search_results):
        print("Step 2: Filtering topics (using LLM: gpt-oss)...")
        if self.openai_client:
            try:
                # Prepare a prompt for the LLM
                prompt = f"""
                Analyze the following search results and identify 3 distinct technology topics that are currently generating active debate or controversy.
                Return a JSON list of objects with 'title' and 'query' keys.
                
                Search Results:
                {json.dumps(search_results, indent=2)}
                """
                
                response = self.openai_client.chat.completions.create(
                    model="gpt-oss",
                    messages=[
                        {"role": "system", "content": "You are a helpful tech researcher."},
                        {"role": "user", "content": prompt}
                    ],
                    response_format={"type": "json_object"}
                )
                content = response.choices[0].message.content
                selected_topics = json.loads(content)['topics'] # Assuming LLM returns wrapped json
                return selected_topics
            except Exception as e:
                print(f"LLM Error: {e}. Falling back to heuristic.")
        
        # Fallback / Demo Logic
        print("  (Using fallback selection)")
        selected_topics = [
            {"title": "Agentic AI & Reward Hacking", "query": "Anthropic reward hacking"},
            {"title": "Vibe Coding vs AI Engineering", "query": "vibe coding debate"},
            {"title": "Model Context Protocol (MCP)", "query": "Model Context Protocol adoption"},
        ]
        return selected_topics

    def step_3_deep_dive(self, topics):
        print("Step 3: Deep Dive...")
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
