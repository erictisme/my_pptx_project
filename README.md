# OutlineWriter - AI-Powered Consulting Presentation Generator

## Overview

OutlineWriter is an AI-powered presentation generation system that leverages the Ollama API and McKinsey-style consulting frameworks to automatically generate structured presentation outlines. Built with Streamlit and modern Python practices, it combines natural language processing with consulting domain expertise to create compelling, data-driven presentations.

## Architecture

### Core Components

1. **Presentation Generation Pipeline**
   - `app.py`: Streamlit frontend and orchestration
   - `content_generator.py`: LLM integration and content generation
   - `slide_intelligence.py`: Slide structure and pattern management
   - `consulting_slide_principles.py`: Consulting best practices implementation

2. **Data Models**
   ```python
   @dataclass
   class ProjectInput:
       client_name: str
       industry: str
       problem_statement: str
       key_findings: List[str]
       objectives: List[str]
       project_type: str
   ```

3. **Template System**
   - `action_titles_template.txt`: Structured templates for slide generation
   - Pattern-based title generation
   - Hierarchical content organization

## Technical Requirements

- Python 3.8+
- Ollama API endpoint
- 8GB RAM recommended
- Unix-based OS preferred (macOS/Linux)

## Installation

1. **Clone & Setup**
   ```bash
   git clone https://github.com/erictisme/my_pptx_project.git
   cd my_pptx_project
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Ollama Setup**
   ```bash
   # Install Ollama (if not already installed)
   curl https://ollama.ai/install.sh | sh
   
   # Start Ollama server
   ollama run llama2
   ```

3. **Environment Configuration**
   - Ensure Ollama is running on `http://localhost:11434`
   - Verify template files are in the correct location

## Core Features

### 1. Intelligent Content Generation
- LLM-powered content generation with consulting principles
- Automatic section type detection
- Smart retry mechanism for API failures

### 2. Slide Structure Intelligence
```python
class SlideIntelligence:
    def generate_compelling_title(self, raw_insight: str, context: Dict) -> str
    def build_logical_flow(self, title: str, context: Dict) -> Dict
    def ensure_consistency(self, slide_content: Dict) -> Tuple[bool, List[str]]
```

### 3. Project Context Management
- Structured input collection
- Context persistence
- Automatic template selection

## Development Guide

### Adding New Features

1. **New Slide Types**
   ```python
   # In slide_intelligence.py
   class SlideType(Enum):
       NEW_TYPE = "new_type"
   ```

2. **Custom Templates**
   - Add patterns to `action_titles_template.txt`
   - Follow the established format:
   ```
   STRUCTURE: [Action/Finding] + [Supporting Detail]
   EXAMPLES:
   - "Pattern example..."
   ```

3. **Content Generation Rules**
   - Extend `EnhancedContentGenerator` class
   - Implement new generation strategies

### Error Handling

The system implements a robust error handling strategy:
- API connection retries
- Default content fallbacks
- Structured error logging

## API Integration

### Ollama API Interface
```python
def _generate_text(self, prompt: str) -> str:
    data = {
        "model": self.model_name,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "top_p": 0.9
        }
    }
    # API call implementation...
```

## Testing

1. **Unit Tests**
   ```bash
   python -m pytest tests/
   ```

2. **Integration Testing**
   ```bash
   python OutlineWriter/tests/test_minimal.py
   ```

## Performance Optimization

- Caching for template loading
- Batch processing for multiple slides
- Asynchronous API calls (planned)

## Roadmap

- [ ] Async content generation
- [ ] Custom template builder
- [ ] Enhanced error recovery
- [ ] PDF export functionality
- [ ] Real-time collaboration features

## Troubleshooting

Common issues and solutions:
1. **Ollama Connection**
   ```bash
   curl http://localhost:11434/api/tags
   ```

2. **Template Loading**
   - Verify file paths
   - Check file permissions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Implement changes
4. Submit a pull request

## License

MIT License - See LICENSE file for details

## Contact

- Eric Tan - [GitHub](https://github.com/erictisme) 