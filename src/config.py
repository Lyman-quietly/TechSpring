import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    model = "gpt-oss:20b"
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    OUTPUT_DIR = os.path.join(PROJECT_ROOT, "report")
    
    
    # Paths
    EXISTING_REPORT_PATH = os.path.join(PROJECT_ROOT, "data", "research_report.md")

    # Fonts
    FONT_CANDIDATES = [
        ("C:\\Windows\\Fonts\\YuGothM.ttc", "C:\\Windows\\Fonts\\YuGothB.ttc"),
        ("C:\\Windows\\Fonts\\meiryo.ttc", "C:\\Windows\\Fonts\\meiryob.ttc"),
        ("C:\\Windows\\Fonts\\msgothic.ttc", "C:\\Windows\\Fonts\\msgothic.ttc"), 
    ]
