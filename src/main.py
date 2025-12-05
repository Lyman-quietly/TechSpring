import os
import sys
from datetime import datetime

# Add project root to sys.path to ensure absolute imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import Config
from src.services.researcher import TechResearcher
from src.services.pdf_generator import generate_report_from_markdown

def main():
    print("--- Starting Tech Research Automation Program (Modular) ---")
    
    # Initialize OpenAI Client
    openai_client = None
    if Config.OPENAI_API_KEY:
        from openai import OpenAI
        openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)
    
    # 1. Run the "Program" flow
    researcher = TechResearcher(openai_client=openai_client)
    
    # For demo purposes, we do a broad search but skip full generation to reuse the artifact
    results = researcher.perform_broad_search()
    topics = researcher.filter_active_topics(results)
    
    # 2. Generate PDF from existing report artifact
    # In a real run, you would use data from step_3_deep_dive
    
    if not os.path.exists(Config.OUTPUT_DIR):
        os.makedirs(Config.OUTPUT_DIR)
        
    date_str = datetime.now().strftime("%Y%m%d")
    base_filename = f"research_report_{date_str}"
    output_pdf_path = os.path.join(Config.OUTPUT_DIR, f"{base_filename}.pdf")
    
    # Check for duplicate filenames
    counter = 1
    while os.path.exists(output_pdf_path):
        output_pdf_path = os.path.join(Config.OUTPUT_DIR, f"{base_filename}_{counter}.pdf")
        counter += 1
    
    print(f"\n--- Generating PDF from {Config.EXISTING_REPORT_PATH} ---")
    
    if os.path.exists(Config.EXISTING_REPORT_PATH):
        with open(Config.EXISTING_REPORT_PATH, "r", encoding="utf-8") as f:
            content = f.read()
        
        generate_report_from_markdown(content, output_pdf_path)
    else:
        print(f"Error: Could not find report at {Config.EXISTING_REPORT_PATH}")

if __name__ == "__main__":
    main()
