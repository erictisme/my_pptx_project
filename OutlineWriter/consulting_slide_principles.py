"""
consulting_slide_principles.py

This module outlines essential principles for creating effective consulting slides.
"""

import re
import json
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class SlideTitle:
    text: str
    insight: str
    supporting_detail: Optional[str] = None

@dataclass
class SlideStructure:
    title: SlideTitle
    main_message: str
    supporting_points: List[str]
    detailed_explanations: Optional[Dict[str, List[str]]] = None

class ConsultingSlideGenerator:
    def __init__(self):
        self.templates = self._load_templates()
        self.title_patterns = self._load_title_patterns()
    
    def generate_compelling_title(self, raw_insight: str, context: Dict) -> SlideTitle:
        """
        Generates a concise, powerful slide title following consulting best practices.
        
        Args:
            raw_insight: The core insight to convey
            context: Project context including industry, client, etc.
        
        Returns:
            SlideTitle object with main insight and optional supporting detail
        """
        # Clean and structure the raw insight
        cleaned = self._clean_title(raw_insight)
        
        # Split into main insight and supporting detail if needed
        parts = cleaned.split("...")
        main_insight = parts[0].strip()
        supporting = parts[1].strip() if len(parts) > 1 else None
        
        return SlideTitle(
            text=cleaned,
            insight=main_insight,
            supporting_detail=supporting
        )
    
    def build_logical_flow(self, title: SlideTitle, context: Dict) -> SlideStructure:
        """
        Creates a logical flow of content that supports the title's message.
        
        Args:
            title: SlideTitle object
            context: Project context
        
        Returns:
            SlideStructure with main message and supporting points
        """
        # Select appropriate template based on title and context
        template = self._select_template(title, context)
        
        # Generate main message that aligns with title
        main_message = self._generate_main_message(title, template)
        
        # Generate supporting points following template structure
        supporting_points = self._generate_supporting_points(title, template, context)
        
        return SlideStructure(
            title=title,
            main_message=main_message,
            supporting_points=supporting_points
        )
    
    def ensure_consistency(self, structure: SlideStructure) -> Tuple[bool, List[str]]:
        """
        Checks consistency between title and content, returns (is_consistent, issues).
        """
        issues = []
        
        # Check title-message alignment
        if not self._check_message_alignment(structure.title, structure.main_message):
            issues.append("Main message doesn't clearly support title")
        
        # Check supporting points
        for point in structure.supporting_points:
            if not self._check_point_relevance(structure.title, point):
                issues.append(f"Supporting point may be off-topic: {point}")
        
        return len(issues) == 0, issues
    
    def _clean_title(self, raw_title: str) -> str:
        """Cleans and structures a raw title."""
        # Remove common weak phrases
        weak_phrases = [
            "There are",
            "Based on",
            "Analysis shows",
            "Our research indicates"
        ]
        cleaned = raw_title
        for phrase in weak_phrases:
            cleaned = cleaned.replace(phrase, "")
        
        # Ensure active voice
        cleaned = self._ensure_active_voice(cleaned)
        
        # Limit length
        words = cleaned.split()
        if len(words) > 12:
            cleaned = " ".join(words[:12]) + "..."
        
        return cleaned.strip()
    
    def _ensure_active_voice(self, text: str) -> str:
        """Attempts to convert passive to active voice."""
        passive_patterns = [
            r"is being",
            r"are being",
            r"has been",
            r"have been",
            r"was being",
            r"were being"
        ]
        
        active_text = text
        for pattern in passive_patterns:
            if re.search(pattern, active_text, re.IGNORECASE):
                # This is a simplified conversion - in practice, you'd need
                # more sophisticated NLP to do this properly
                active_text = re.sub(pattern, "", active_text)
        
        return active_text
    
    def _load_templates(self) -> Dict:
        """Loads slide templates."""
        return {
            "issue_analysis": {
                "name": "Issue-Analysis-Recommendation",
                "structure": ["Problem", "Analysis", "Recommendation"],
                "transitions": ["leads to", "therefore", "as a result"]
            },
            "before_after": {
                "name": "Before-After Comparison",
                "structure": ["Current State", "Changes", "Future State"],
                "transitions": ["transforms into", "improves to", "results in"]
            },
            "three_column": {
                "name": "Three-Column Analysis",
                "structure": ["Problem", "Root Causes", "Actions"],
                "transitions": ["caused by", "addressed through", "resolved via"]
            }
        }
    
    def _load_title_patterns(self) -> List[Dict]:
        """Loads title patterns for different slide types."""
        return [
            {
                "type": "insight",
                "pattern": "{Finding} leads to {Impact}",
                "example": "Product knowledge gaps reduce revenue by 30%"
            },
            {
                "type": "action",
                "pattern": "{Action} {Target} through {Method}",
                "example": "Increase revenue through targeted training"
            },
            {
                "type": "comparison",
                "pattern": "{Current} transforms to {Future} via {Method}",
                "example": "Basic product knowledge evolves to expertise via hands-on training"
            }
        ]

    def _select_template(self, title: SlideTitle, context: Dict) -> Dict:
        """Selects most appropriate template based on title and context."""
        # Implementation would use NLP to match title and context to template
        return self.templates["issue_analysis"]  # Simplified for example
    
    def _generate_main_message(self, title: SlideTitle, template: Dict) -> str:
        """Generates main message that aligns with title and template."""
        # Implementation would use template structure to craft message
        return f"Analysis of {title.insight} shows significant impact"  # Simplified
    
    def _generate_supporting_points(
        self, title: SlideTitle, template: Dict, context: Dict
    ) -> List[str]:
        """Generates supporting points following template structure."""
        # Implementation would use template and context to generate points
        return [
            f"Point 1 about {title.insight}",
            f"Point 2 about {title.insight}",
            f"Point 3 about {title.insight}"
        ]  # Simplified
    
    def _check_message_alignment(self, title: SlideTitle, message: str) -> bool:
        """Checks if main message aligns with title."""
        # Implementation would use NLP to check semantic alignment
        return True  # Simplified
    
    def _check_point_relevance(self, title: SlideTitle, point: str) -> bool:
        """Checks if supporting point is relevant to title."""
        # Implementation would use NLP to check semantic relevance
        return True  # Simplified

# Example usage
if __name__ == "__main__":
    generator = ConsultingSlideGenerator()
    
    # Example context
    context = {
        "client": "MUFG",
        "industry": "Banking",
        "focus_area": "Training"
    }
    
    # Generate title
    title = generator.generate_compelling_title(
        "Product knowledge gaps are causing revenue loss",
        context
    )
    
    # Build content structure
    structure = generator.build_logical_flow(title, context)
    
    # Check consistency
    is_consistent, issues = generator.ensure_consistency(structure)
    
    # Print results
    print("=== Generated Slide ===")
    print(f"Title: {title.text}")
    print(f"Main Message: {structure.main_message}")
    print("\nSupporting Points:")
    for point in structure.supporting_points:
        print(f"- {point}")
    
    print("\nConsistency Check:", "PASS" if is_consistent else "FAIL")
    if issues:
        print("Issues found:")
        for issue in issues:
            print(f"- {issue}") 