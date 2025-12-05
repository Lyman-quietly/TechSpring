# TechSpring: Automated Tech Trend Researcher

TechSpring is an automated tool designed to research recent technology trends, analyze active discussions, and generate comprehensive PDF reports. It leverages DuckDuckGo for broad searches and OpenAI's LLMs for in-depth analysis and summarization.

## Features

- **Automated Trend Research**: Scrapes the web for the latest viral and actively discussed technology topics.
- **Intelligent Filtering**: Uses LLMs (`gpt-oss`) to identify topics with significant debate or controversy.
- **Deep Dive Analysis**: Synthesizes information from multiple sources to provide a balanced technical summary.
- **PDF Report Generation**: Produces professionally formatted PDF reports with Japanese font support and Markdown-based styling.
- **Modular Architecture**: Clean separation of concerns (Config, Research Service, PDF Generator).

## Prerequisites

- **Python**: 3.8 or higher
- **Git**
- **OpenAI API Key**: Required for topic filtering and summarization.

## Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/YourUsername/TechSpring.git
    cd TechSpring
    ```

2.  **Set up a virtual environment** (recommended):
    ```bash
    # Windows
    python -m venv .venv
    .venv\Scripts\activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Environment Configuration**:
    Create a `.env` file in the project root and add your OpenAI API key:
    ```env
    OPENAI_API_KEY=your_api_key_here
    ```

## Usage

Run the main script to start the research and report generation process:

```bash
python src/main.py
```

The program will:
1.  Perform a search for recent tech trends.
2.  Filter for active topics.
3.  Generate a PDF report in the `report/` directory (e.g., `report/research_report_20251206.pdf`).

## Project Structure

```text
TechSpring/
├── data/                   # Input data (e.g., markdown templates)
├── report/                 # Generated PDF reports
├── src/
│   ├── services/
│   │   ├── researcher.py   # Search and LLM logic
│   │   └── pdf_generator.py# PDF creation logic
│   ├── config.py           # Configuration settings
│   └── main.py             # Entry point
├── .env                    # Environment variables (not committed)
├── .gitignore
├── requirements.txt
└── README.md
```

## License

MIT License
