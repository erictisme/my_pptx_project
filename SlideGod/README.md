# AI PowerPoint Generator

This system helps you create McKinsey-style presentations using AI. It learns from example presentations and generates new ones following similar styling patterns.

## Features

- Extracts styling patterns from example presentations
- Generates presentation content using GPT-4
- Applies consistent McKinsey-style formatting
- Handles text, tables, charts, and images
- Maintains professional spacing and alignment

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your OpenAI API key:
```bash
export OPENAI_API_KEY='your-api-key-here'
```

3. Prepare your base template:
- Use `inspect_layouts.py` to view available layouts in your template
- Create a base template with your desired master slides

## Usage

1. Extract styling patterns from an example presentation:
```python
from ai_presentation_generator import PresentationStyleExtractor

extractor = PresentationStyleExtractor()
extractor.analyze_presentation("example.pptx")
extractor.save_patterns("style_patterns.json")
```

2. Generate a new presentation:
```python
from ai_presentation_generator import PresentationGenerator

generator = PresentationGenerator("style_patterns.json", "your-openai-api-key")
brief = """
Create a presentation on digital transformation strategy:
- Current market challenges
- Digital opportunities
- Implementation roadmap
- Expected outcomes
"""
generator.generate_presentation(brief, "output.pptx")
```

## File Structure

- `ai_presentation_generator.py`: Main AI generation logic
- `json_to_slides.py`: Converts JSON to PowerPoint
- `ppt_to_json.py`: Converts PowerPoint to JSON
- `inspect_layouts.py`: Utility to inspect template layouts

## Styling Guidelines

The system extracts and applies the following styling elements:

1. Colors
   - Primary text color
   - Background colors
   - Accent colors

2. Fonts
   - Font families
   - Size hierarchies
   - Text styles (bold, italic, etc.)

3. Spacing
   - Paragraph spacing
   - Line spacing
   - Margins and padding

4. Layouts
   - Slide templates
   - Element positioning
   - Common patterns

## Contributing

Feel free to contribute by:
1. Adding support for more elements
2. Improving pattern extraction
3. Enhancing AI generation
4. Adding new styling features

## License

MIT License 