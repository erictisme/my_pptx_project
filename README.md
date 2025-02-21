# OutlineWriter - AI-Powered Presentation Generator

OutlineWriter is an AI-powered tool that helps generate structured outlines for consulting presentations following best practices. It uses the Ollama API to generate content and follows McKinsey-style presentation patterns.

## Features

- Generate structured presentation outlines
- Follow consulting best practices
- Support for different project types (Project/Proposal)
- McKinsey-style templates and patterns
- Progress tracking with wellness tips
- File upload support for additional context

## Project Structure

```
OutlineWriter/
├── app.py                         # Main Streamlit application
├── content_generator.py           # Content generation logic
├── slide_intelligence.py          # Slide structure and patterns
├── consulting_slide_principles.py # Consulting principles
├── action_titles_template.txt     # Title patterns and examples
└── requirements.txt              # Project dependencies
```

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/my_pptx_project.git
cd my_pptx_project
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Start Ollama:
```bash
ollama run llama2
```

5. Run the application:
```bash
streamlit run OutlineWriter/app.py
```

## Dependencies

- Python 3.8+
- Streamlit
- Ollama
- Requests

## Usage

1. Select project type (Project/Proposal)
2. Enter basic information (client, industry)
3. Input findings and objectives
4. Optionally upload supporting files
5. Select number of slides
6. Click "Generate Presentation Outline"

## Contributing

Feel free to submit issues and enhancement requests! 