import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    OUTPUT_DIR = os.path.join(PROJECT_ROOT, "report")
    
    
    # Paths
    EXISTING_REPORT_PATH = r"C:\Users\lyman\.gemini\antigravity\brain\b0b07f77-05d8-42ae-bc4e-e7bf2fd8af61\research_report.md"

    # Fonts
    FONT_CANDIDATES = [
        ("C:\\Windows\\Fonts\\YuGothM.ttc", "C:\\Windows\\Fonts\\YuGothB.ttc"),
        ("C:\\Windows\\Fonts\\meiryo.ttc", "C:\\Windows\\Fonts\\meiryob.ttc"),
        ("C:\\Windows\\Fonts\\msgothic.ttc", "C:\\Windows\\Fonts\\msgothic.ttc"), 
    ]
