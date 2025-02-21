import logging
import requests
import json
from typing import Dict, List

from models import ProjectContext

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def generate_outline(context: ProjectContext, model_name: str) -> List[Dict]:
    """Generate a presentation outline from the project context."""
    prompt = f"""Create a McKinsey-style presentation outline.

Project Context:
{json.dumps(context.to_dict(), indent=2)}

Example format:
[{{
  "t": "Executive Summary",  // title
  "k": ["Key point 1", "Key point 2"],  // key points
  "v": "2x2 matrix"  // visual type
}}]

Requirements:
1. Each slide needs clear message
2. Use action-oriented titles
3. 3-4 key points per slide
4. Specific visual type

Return array of slides following this exact format."""

    try:
        response = _generate_text(prompt, model_name)
        logger.debug(f"Raw response from model: {response}")
        
        # Extract and clean JSON from response
        json_str = _extract_json_from_response(response)
        logger.debug(f"Cleaned JSON string: {json_str}")
        
        # Parse and validate JSON structure
        content = json.loads(json_str)
        
        # Convert compact format to full format
        if isinstance(content, list):
            outline = []
            for slide in content:
                full_slide = {
                    "title": slide.get("t", "Untitled Slide"),
                    "type": _infer_slide_type(slide.get("t", "")),
                    "key_points": slide.get("k", []),
                    "visuals": slide.get("v", "Basic layout")
                }
                outline.append(full_slide)
            return outline
        
        raise ValueError("Generated content is not a list")
        
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON from model response: {str(e)}")
        return _generate_fallback_outline(context)
    except Exception as e:
        logger.error(f"Unexpected error in generate_outline: {str(e)}")
        raise

def generate_slide_content(slide_info: Dict, context: ProjectContext, model_name: str) -> Dict:
    """Generate detailed content for a single slide."""
    # Use compact format for prompt
    prompt = f"""Create slide content.

Input: {{
  "t": "{slide_info['title']}",
  "type": "{slide_info['type']}",
  "k": {json.dumps(slide_info['key_points'])},
  "v": "{slide_info['visuals']}"
}}

Project Context:
{json.dumps(context.to_dict(), indent=2)}

Return JSON with this structure:
{{
  "l": {{  // layout
    "n": "type_name",
    "t": "content_type"
  }},
  "s": [  // shapes
    {{
      "t": "TITLE",  // type
      "p": {{  // position
        "x": 1000000,
        "y": 1000000,
        "w": 8000000,
        "h": 1000000
      }},
      "c": [  // content
        {{
          "t": "text",
          "s": {{  // style
            "f": 32,  // font size
            "b": true  // bold
          }}
        }}
      ]
    }}
  ]
}}

Rules:
1. Keep JSON compact
2. Use short keys
3. Include all points
4. Match visual type"""

    try:
        response = _generate_text(prompt, model_name)
        logger.debug(f"Raw slide content response: {response}")
        
        # Extract and clean JSON from response
        json_str = _extract_json_from_response(response)
        logger.debug(f"Cleaned JSON string: {json_str}")
        
        # Parse compact format
        content = json.loads(json_str)
        
        # Convert compact format to full format
        full_content = _convert_to_full_format(content, slide_info)
        
        return full_content
        
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON from model response: {str(e)}")
        return _generate_fallback_slide_content(slide_info)
    except Exception as e:
        logger.error(f"Unexpected error in generate_slide_content: {str(e)}")
        raise

def enhance_content(content: Dict, context: ProjectContext, model_name: str) -> Dict:
    """Enhance slide content with better phrasing and structure."""
    enhance_prompt = f"""Improve this slide content:

Slide Content:
{json.dumps(content, indent=2)}

Project Context:
{json.dumps(context.to_dict(), indent=2)}

Requirements:
- Rephrase titles to be more impactful
- Ensure content supports the title 
- Use parallel structure for bullet points
- Add specific metrics where possible
- Improve the visual description

Return the enhanced content in the same JSON format."""

    try:  
        response = _generate_text(enhance_prompt, model_name)
        logger.debug(f"Raw enhanced content response: {response}")
        
        # Extract and clean JSON from response
        json_str = _extract_json_from_response(response)
        logger.debug(f"Cleaned JSON string: {json_str}")
        
        # Parse enhanced content
        enhanced_content = json.loads(json_str)
        
        return enhanced_content
    
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON from model response: {str(e)}")
        return content
    except Exception as e:
        logger.error(f"Unexpected error in enhance_content: {str(e)}")
        raise

def _generate_text(prompt: str, model_name: str) -> str:
    """Generate text using the specified model."""
    api_base = "http://localhost:11434/api/generate"
    
    data = {
        "model": model_name,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "top_p": 0.9,
            "stop": ["\n\n", "```"]
        }
    }
    
    try:
        response = requests.post(api_base, json=data)
        response.raise_for_status()
        return response.json()["response"].strip()
    except Exception as e:
        logger.error(f"Error generating text: {e}")
        return ""

def _extract_json_from_response(response: str) -> str:
    """Extract JSON from the model response."""
    logger.debug("Original response:")
    logger.debug(response)
    
    # Remove any markdown code block indicators and surrounding whitespace
    clean_response = response.replace('```json', '').replace('```', '').strip()
    
    # If we don't have a JSON array yet, try to generate one from the key points
    if not (clean_response.startswith('[') or clean_response.startswith('{')):
        # Extract lines that look like bullet points
        lines = clean_response.split('\n')
        points = []
        for line in lines:
            if line.strip().startswith(('-', '*', '•')):
                points.append(line.strip().lstrip('-*• ').strip())
        
        if points:
            # Create a basic JSON structure from the points
            json_structure = [
                {
                    "title": "Key Points",
                    "type": "executive_summary",
                    "key_points": points,
                    "visuals": "Simple bullet point layout"
                }
            ]
            return json.dumps(json_structure, indent=2)
    
    # If the response doesn't start with [ or {, try to find them
    if not clean_response.startswith('[') and not clean_response.startswith('{'):
        json_start = clean_response.find('[')
        if json_start == -1:
            json_start = clean_response.find('{')
        if json_start == -1:
            raise ValueError("No JSON structure found in response")
        clean_response = clean_response[json_start:]
    
    # If the response doesn't end with ] or }, try to find them
    if not clean_response.endswith(']') and not clean_response.endswith('}'):
        json_end = clean_response.rfind(']')
        if json_end == -1:
            json_end = clean_response.rfind('}')
        if json_end == -1:
            raise ValueError("No JSON structure found in response")
        clean_response = clean_response[:json_end + 1]
    
    logger.debug("Extracted JSON structure:")
    logger.debug(clean_response)
    
    # Replace Python-style values
    replacements = [
        ("'", '"'),  # Replace single quotes with double quotes
        ('True', 'true'),
        ('False', 'false'),
        ('None', 'null')
    ]
    
    for old, new in replacements:
        clean_response = clean_response.replace(old, new)
    
    # Remove any trailing commas in arrays and objects
    lines = clean_response.split('\n')
    clean_lines = []
    for i, line in enumerate(lines):
        line = line.rstrip()
        if not line:
            continue
        
        # Remove trailing commas before closing brackets
        if line.rstrip().endswith(','):
            next_line = next((l.strip() for l in lines[i + 1:] if l.strip()), '')
            if next_line.startswith('}') or next_line.startswith(']'):
                line = line.rstrip(',')
        
        clean_lines.append(line)
    
    json_str = '\n'.join(clean_lines)
    logger.debug("Cleaned JSON string:")
    logger.debug(json_str)
    
    return json_str

def _infer_slide_type(title: str) -> str:
    """Infer slide type from title."""
    title_lower = title.lower()
    if "summary" in title_lower or "overview" in title_lower:
        return "executive_summary"
    if "problem" in title_lower or "challenge" in title_lower:
        return "problem_statement"
    if "solution" in title_lower or "approach" in title_lower:
        return "solution"
    if "next" in title_lower or "step" in title_lower:
        return "roadmap"
    if any(word in title_lower for word in ["data", "metric", "number", "stat"]):
        return "data"
    if "conclusion" in title_lower or "recommendation" in title_lower:
        return "conclusion"
    return "content"

def _generate_fallback_outline(context: ProjectContext) -> List[Dict]:
    """Generate a basic outline as fallback."""
    return [
        {
            "title": "Executive Summary",
            "type": "executive_summary",
            "key_points": [context.client_situation],
            "visuals": "Title slide with key message"
        }
    ]

def _generate_fallback_slide_content(slide_info: Dict) -> Dict:
    """Generate basic slide content as fallback."""
    return {
        "layout": {
            "name": slide_info["type"].title(),
            "type": "basic"
        },
        "shapes": [
            {
                "type": "TITLE",
                "location": {
                    "x": 1000000,
                    "y": 1000000,
                    "width": 8000000,
                    "height": 1000000
                },
                "textContent": [{
                    "text": slide_info["title"],
                    "style": {
                        "fontSize": 32,
                        "isBold": True
                    }
                }]
            },
            {
                "type": "BODY",
                "location": {
                    "x": 1000000,
                    "y": 2500000,
                    "width": 8000000,
                    "height": 4000000
                },
                "textContent": [{
                    "text": point,
                    "style": {
                        "fontSize": 24,
                        "isBold": False
                    }
                } for point in slide_info["key_points"]]
            }
        ]
    }

def _convert_to_full_format(content: Dict, slide_info: Dict) -> Dict:
    """Convert compact JSON format to full format."""
    full_content = {
        "layout": {
            "name": content.get("l", {}).get("n", slide_info["type"].title()),
            "type": content.get("l", {}).get("t", "content")
        },
        "shapes": []
    }
    
    # Convert shapes to full format
    for shape in content.get("s", []):
        full_shape = {
            "type": shape.get("t", "BODY"),
            "location": {
                "x": shape.get("p", {}).get("x", 1000000),
                "y": shape.get("p", {}).get("y", 2500000),
                "width": shape.get("p", {}).get("w", 8000000),
                "height": shape.get("p", {}).get("h", 4000000)
            },
            "textContent": []
        }
        
        # Convert text content
        for text in shape.get("c", []):
            full_text = {
                "text": text.get("t", ""),
                "style": {
                    "fontSize": text.get("s", {}).get("f", 24),
                    "isBold": text.get("s", {}).get("b", False)
                }
            }
            full_shape["textContent"].append(full_text)
        
        full_content["shapes"].append(full_shape)
    
    # Ensure required shapes exist
    if not any(s["type"] == "TITLE" for s in full_content["shapes"]):
        full_content["shapes"].insert(0, {
            "type": "TITLE",
            "location": {
                "x": 1000000,
                "y": 1000000,
                "width": 8000000,
                "height": 1000000
            },
            "textContent": [{
                "text": slide_info["title"],
                "style": {
                    "fontSize": 32,
                    "isBold": True
                }
            }]
        })
    
    if not any(s["type"] == "BODY" for s in full_content["shapes"]):
        full_content["shapes"].append({
            "type": "BODY",
            "location": {
                "x": 1000000,
                "y": 2500000,
                "width": 8000000,
                "height": 4000000
            },
            "textContent": [{
                "text": point,
                "style": {
                    "fontSize": 24,
                    "isBold": False
                }
            } for point in slide_info["key_points"]]
        })
    
    return full_content 