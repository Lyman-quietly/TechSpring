import os
import markdown
from fpdf import FPDF
from src.config import Config

class PDFGenerator:
    def __init__(self, output_path="report.pdf"):
        self.output_path = output_path
        self.pdf = FPDF()
        self.pdf.add_page()
        
        self.font_loaded = False
        # Load fonts from Config
        for font_path_r, font_path_b in Config.FONT_CANDIDATES:
            if os.path.exists(font_path_r):
                try:
                    # Register Regular
                    self.pdf.add_font("JPFont", style="", fname=font_path_r)
                    
                    # Register Bold (use Bold file if exists, else Regular)
                    if os.path.exists(font_path_b):
                        self.pdf.add_font("JPFont", style="B", fname=font_path_b)
                        self.pdf.add_font("JPFont", style="BI", fname=font_path_b)
                    else:
                        self.pdf.add_font("JPFont", style="B", fname=font_path_r)
                        self.pdf.add_font("JPFont", style="BI", fname=font_path_r)

                    # Register Italic (fallback to Regular)
                    self.pdf.add_font("JPFont", style="I", fname=font_path_r)

                    self.pdf.set_font("JPFont", size=11)
                    self.font_loaded = True
                    print(f"Loaded font family: {font_path_r} (Bold: {font_path_b})")
                    break
                except Exception as e:
                    print(f"Failed to load {font_path_r}: {e}")
        
        if not self.font_loaded:
            print("Warning: No suitable Japanese font found/loaded. Using Arial (Japanese characters may not display).")
            self.pdf.set_font("Arial", size=11)

    def generate_from_markdown(self, markdown_content):
        """
        Converts markdown content to HTML and then writes it to PDF.
        """
        # Convert Markdown to HTML
        html_content = markdown.markdown(markdown_content, extensions=['extra', 'tables', 'nl2br'])
        
        # Ensure the font is set for the HTML rendering context
        if self.font_loaded:
             self.pdf.set_font("JPFont", size=11)
        
        # Write HTML
        try:
            self.pdf.write_html(html_content)
        except Exception as e:
            print(f"Error writing HTML to PDF: {e}")
            import traceback
            traceback.print_exc()
            return
        
        # Save
        try:
            self.pdf.output(self.output_path)
            print(f"PDF saved to {self.output_path}")
        except Exception as e:
             print(f"Error saving PDF: {e}")

def generate_report_from_markdown(md_content, output_exists_path):
    """
    Parses a simple markdown report and generates a PDF.
    """
    generator = PDFGenerator(output_path=output_exists_path)
    generator.generate_from_markdown(md_content)
