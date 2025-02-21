"""
Enhanced content generator for creating data-driven presentations.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
import requests
import json
import logging
import time
from requests.exceptions import RequestException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ProjectInput:
    client_name: str
    industry: str
    problem_statement: str
    key_findings: List[str]
    objectives: List[str]
    project_type: str

class EnhancedContentGenerator:
    """Generates structured, data-driven presentation content."""
    
    def __init__(self, model_name="llama2", max_retries=3, retry_delay=1):
        self.api_base = "http://localhost:11434/api/generate"
        self.model_name = model_name
        self.max_retries = max_retries
        self.retry_delay = retry_delay
    
    def _generate_text(self, prompt: str) -> str:
        """Generate text using Ollama API with retries."""
        data = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "stop": ["\n\n", "```"]
            }
        }
        
        for attempt in range(self.max_retries):
            try:
                response = requests.post(self.api_base, json=data, timeout=30)
                response.raise_for_status()
                return response.json()["response"].strip()
            except RequestException as e:
                logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                    continue
                logger.error(f"All attempts failed to call Ollama API: {str(e)}")
                # Return a default response structure
                return json.dumps({
                    "title": "Analysis of Current Situation",
                    "main_message": "Key findings indicate areas for improvement",
                    "supporting_points": [
                        "Current state assessment completed",
                        "Multiple opportunities identified",
                        "Implementation plan in development"
                    ],
                    "section": self._get_section_type(0, 1)
                })
    
    def _get_section_type(self, index: int, total_slides: int) -> str:
        """Determine section type based on slide position."""
        if index == 0:
            return "EXECUTIVE_SUMMARY"
        elif index == total_slides - 1:
            return "IMPLEMENTATION"
        elif index < total_slides // 2:
            return "CURRENT_STATE"
        else:
            return "SOLUTION_APPROACH"
    
    def generate_presentation(self, project: ProjectInput, num_slides: int = 1) -> List[Dict]:
        """Generate structured presentation content."""
        slides = []
        
        for i in range(num_slides):
            section = self._get_section_type(i, num_slides)
            
            # Generate insight
            prompt = f"""As a McKinsey consultant, generate a key insight for a {section} slide.

Context:
- Client: {project.client_name}
- Industry: {project.industry}
- Problem: {project.problem_statement}
- Project Type: {project.project_type}

Key Findings:
{chr(10).join(f"- {finding}" for finding in project.key_findings)}

Objectives:
{chr(10).join(f"- {obj}" for obj in project.objectives)}

Generate a JSON response with:
1. A clear title (action-oriented)
2. Main message (1 sentence)
3. 3 supporting points
4. Section type

Example format:
{{
    "title": "Product Knowledge Gaps Reduce Revenue by 30%",
    "main_message": "Current training program effectiveness shows significant room for improvement",
    "supporting_points": [
        "Only 40% of bankers complete current training modules",
        "Product complexity leads to 30% longer onboarding time",
        "Digital tools could reduce training time by 25%"
    ],
    "section": "CURRENT_STATE"
}}

Return ONLY the JSON, no other text:"""
            
            try:
                response = self._generate_text(prompt)
                content = json.loads(response)
                slides.append(content)
            except Exception as e:
                logger.error(f"Error generating insight: {str(e)}")
                # Return a default slide structure
                slides.append({
                    "title": f"Analysis of {project.industry} Situation",
                    "main_message": "Key findings indicate areas for improvement",
                    "supporting_points": [
                        "Current state assessment completed",
                        "Multiple opportunities identified",
                        "Implementation plan in development"
                    ],
                    "section": section
                })
        
        return slides

if __name__ == "__main__":
    # Example usage
    project = ProjectInput(
        client_name="MUFG",
        industry="Banking",
        problem_statement="Improve product knowledge among bankers",
        key_findings=[
            "Current training program reaches only 60% of target audience",
            "Product complexity leads to 40% longer onboarding time",
            "Digital tools could reduce training time by 30%"
        ],
        objectives=[
            "Increase training program reach to 90% within 6 months",
            "Reduce onboarding time by 25%",
            "Implement digital training tools"
        ],
        project_type="Project"
    )
    
    generator = EnhancedContentGenerator()
    slides = generator.generate_presentation(project, 3)
    print(json.dumps(slides, indent=2)) 