import os
import json
from datetime import datetime
from duckduckgo_search import DDGS
from fpdf import FPDF
from dotenv import load_dotenv

load_dotenv()

class TechResearcher:
    def __init__(self):
        self.ddgs = DDGS()
        # Initialize OpenAI client if key is present
        self.openai_client = None
        if os.getenv("OPENAI_API_KEY"):
            from openai import OpenAI
            self.openai_client = OpenAI()

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

class PDFGenerator:
    def __init__(self, output_path="report.pdf"):
        self.output_path = output_path
        self.pdf = FPDF()
        self.pdf.add_page()
        
        # Add a Japanese font
        # Try multiple common Windows fonts
        font_candidates = [
            "C:\\Windows\\Fonts\\YuGothM.ttc",
            "C:\\Windows\\Fonts\\meiryo.ttc",
            "C:\\Windows\\Fonts\\msmincho.ttc",
            "C:\\Windows\\Fonts\\msgothic.ttc", 
        ]
        
        font_loaded = False
        for font_path in font_candidates:
            if os.path.exists(font_path):
                try:
                    self.pdf.add_font("JPFont", "", font_path)
                    self.pdf.set_font("JPFont", size=11) # Slightly smaller font
                    font_loaded = True
                    print(f"Loaded font: {font_path}")
                    break
                except Exception as e:
                    print(f"Failed to load {font_path}: {e}")
        
        if not font_loaded:
            print("Warning: No suitable Japanese font found/loaded. Using Arial (Japanese characters may not display).")
            self.pdf.set_font("Arial", size=12)

    def add_title(self, title):
        self.pdf.set_font_size(16)
        self.pdf.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT", align='C')
        self.pdf.ln(5)
        self.pdf.set_font_size(11)

    def add_section(self, title, content):
        self.pdf.set_font_size(14)
        # Check if bold font needs to be added or just use same font
        self.pdf.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
        self.pdf.set_font_size(11)
        self.pdf.multi_cell(0, 6, content)
        self.pdf.ln(5)

    def save(self):
        self.pdf.output(self.output_path)
        print(f"PDF saved to {self.output_path}")

def generate_report_from_markdown(md_content, output_exists_path):
    """
    Parses a simple markdown report and generates a PDF.
    """
    generator = PDFGenerator(output_path=output_exists_path)
    
    # Simple markdown parser
    lines = md_content.split('\n')
    for line in lines:
        try:
            if line.startswith("# "):
                generator.add_title(line[2:])
            elif line.startswith("## "):
                generator.add_section(line[3:], "")
            elif line.startswith("### "):
                # Subheader, treat as bold-ish line
                generator.pdf.set_font_size(12)
                generator.pdf.cell(0, 8, line[4:], new_x="LMARGIN", new_y="NEXT")
                generator.pdf.set_font_size(11)
            elif line.strip() == "":
                continue
            elif line.strip().startswith("- ") or line.strip().startswith("* "):
                 # Use a simple hyphen instead of bullet to avoid font metric issues
                 generator.pdf.multi_cell(180, 6, "  - " + line.strip()[2:])
            else:
                generator.pdf.multi_cell(180, 6, line)
        except Exception as e:
            print(f"Warning: Could not render line: '{line}'. Error: {e}")
            
    generator.save()

if __name__ == "__main__":
    # 1. Run the "Program" flow (Mock/Demo)
    print("--- Starting Tech Research Automation Program ---")
    researcher = TechResearcher()
    results = researcher.step_1_broad_search()
    topics = researcher.step_2_filter_topics(results)
    # report_data = researcher.step_3_deep_dive(topics) # Skip deep dive for speed in this demo run
    
    # 2. "Additional Request": Output the SPECIFIC summary report relevant to the user's previous request
    # retrieving content from the artifact we created earlier
    
    existing_report_path = r"C:\Users\lyman\.gemini\antigravity\brain\b0b07f77-05d8-42ae-bc4e-e7bf2fd8af61\research_report.md"
    
    # Generate filename with timestamp
    date_str = datetime.now().strftime("%Y%m%d")
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(project_root, "report")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    output_pdf_path = os.path.join(output_dir, f"research_report_{date_str}.pdf")
    
    print(f"\n--- Processing 'Additional Request': Generating PDF from {existing_report_path} ---")
    
    if os.path.exists(existing_report_path):
        with open(existing_report_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        generate_report_from_markdown(content, output_pdf_path)
    else:
        print(f"Error: Could not find report at {existing_report_path}")

