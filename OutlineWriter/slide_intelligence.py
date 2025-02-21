"""
slide_intelligence.py - Enhanced slide generation with consulting principles
"""

from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
import re
import logging
from enum import Enum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SlideType(Enum):
    ISSUE_ANALYSIS = "issue_analysis"
    BEFORE_AFTER = "before_after"
    THREE_COLUMN = "three_column"
    TIMELINE = "timeline"
    EXECUTIVE_SUMMARY = "executive_summary"

@dataclass
class SlidePattern:
    type: SlideType
    structure: List[str]
    transitions: List[str]
    example_title: str
    example_content: List[str]

@dataclass
class TitleStructure:
    insight: str
    action: Optional[str]
    metric: Optional[str]
    impact: Optional[str]

class SlideIntelligence:
    """Enhanced slide generation incorporating consulting best practices."""
    
    def __init__(self):
        self.patterns = self._initialize_patterns()
        self.title_rules = self._initialize_title_rules()
        self.content_rules = self._initialize_content_rules()
    
    def _initialize_patterns(self) -> Dict[SlideType, SlidePattern]:
        """Initialize common consulting slide patterns."""
        return {
            SlideType.ISSUE_ANALYSIS: SlidePattern(
                type=SlideType.ISSUE_ANALYSIS,
                structure=["Problem", "Analysis", "Recommendation"],
                transitions=["leads to", "therefore", "as a result"],
                example_title="Product Knowledge Gaps Reduce Revenue by 30%",
                example_content=[
                    "Current knowledge assessment shows critical gaps",
                    "Impact analysis reveals missed opportunities",
                    "Targeted training program can close gaps"
                ]
            ),
            SlideType.BEFORE_AFTER: SlidePattern(
                type=SlideType.BEFORE_AFTER,
                structure=["Current State", "Changes", "Future State"],
                transitions=["transforms into", "improves to", "results in"],
                example_title="Training Program Boosts Product Knowledge from 40% to 90%",
                example_content=[
                    "Current baseline assessment",
                    "Implementation of new training modules",
                    "Projected improvement metrics"
                ]
            ),
            # Add more patterns...
        }
    
    def _initialize_title_rules(self) -> List[Dict]:
        """Initialize rules for title generation."""
        return [
            {
                "pattern": "{Action} {Target} through {Method}",
                "example": "Increase revenue through targeted training",
                "components": ["action", "target", "method"]
            },
            {
                "pattern": "{Finding} leads to {Impact}",
                "example": "Product knowledge gaps reduce revenue by 30%",
                "components": ["finding", "impact"]
            },
            # Add more patterns...
        ]
    
    def _initialize_content_rules(self) -> Dict:
        """Initialize rules for content structure."""
        return {
            "max_bullets": 5,
            "bullet_structure": {
                "start_with_verb": True,
                "include_metric": True,
                "max_words": 12
            },
            "visual_rules": {
                "charts_per_slide": 1,
                "white_space_ratio": 0.3,
                "font_hierarchy": ["Title", "Main Message", "Supporting Points"]
            }
        }
    
    def generate_compelling_title(self, raw_insight: str, context: Dict) -> str:
        """Generate a compelling slide title following consulting principles."""
        # Clean and structure the raw insight
        structure = self._parse_title_structure(raw_insight)
        
        # Apply title rules
        if structure.metric:
            title = f"{structure.insight} {structure.impact} by {structure.metric}"
        else:
            title = f"{structure.insight} {structure.impact}"
        
        return self._clean_title(title)
    
    def _parse_title_structure(self, raw_insight: str) -> TitleStructure:
        """Parse raw insight into structured components."""
        # Implementation of parsing logic
        # This would use NLP to identify components
        return TitleStructure(
            insight=raw_insight,
            action=None,
            metric=None,
            impact=None
        )
    
    def _clean_title(self, title: str) -> str:
        """Clean and format the title following best practices."""
        # Remove weak phrases
        weak_phrases = [
            "There are",
            "Based on",
            "Analysis shows",
            "Our research indicates"
        ]
        cleaned = title
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
        """Convert passive to active voice."""
        passive_patterns = [
            r"is being",
            r"are being",
            r"has been",
            r"have been"
        ]
        
        active_text = text
        for pattern in passive_patterns:
            if re.search(pattern, active_text, re.IGNORECASE):
                active_text = re.sub(pattern, "", active_text)
        
        return active_text
    
    def build_logical_flow(self, title: str, context: Dict) -> Dict:
        """Build logical flow from title to supporting content."""
        # Select appropriate pattern
        pattern = self._select_pattern(title, context)
        
        # Generate main message
        main_message = self._generate_main_message(title, pattern)
        
        # Generate supporting points
        supporting_points = self._generate_supporting_points(title, pattern, context)
        
        return {
            "title": title,
            "main_message": main_message,
            "supporting_points": supporting_points,
            "pattern": pattern.type.value
        }
    
    def _select_pattern(self, title: str, context: Dict) -> SlidePattern:
        """Select the most appropriate slide pattern."""
        # Implementation would use NLP to match title and context to pattern
        return self.patterns[SlideType.ISSUE_ANALYSIS]
    
    def _generate_main_message(self, title: str, pattern: SlidePattern) -> str:
        """Generate main message that aligns with title and pattern."""
        return f"Analysis reveals significant impact on {title.lower()}"
    
    def _generate_supporting_points(
        self, title: str, pattern: SlidePattern, context: Dict
    ) -> List[str]:
        """Generate supporting points following pattern structure."""
        return [
            f"Identify key areas of {title.lower()}",
            f"Analyze impact through {pattern.transitions[0]}",
            f"Implement solutions via {pattern.transitions[1]}"
        ]
    
    def ensure_consistency(self, slide_content: Dict) -> Tuple[bool, List[str]]:
        """Check consistency between title and content."""
        issues = []
        
        # Check title-message alignment
        if not self._check_message_alignment(
            slide_content["title"], 
            slide_content["main_message"]
        ):
            issues.append("Main message doesn't clearly support title")
        
        # Check supporting points
        for point in slide_content["supporting_points"]:
            if not self._check_point_relevance(slide_content["title"], point):
                issues.append(f"Supporting point may be off-topic: {point}")
        
        return len(issues) == 0, issues
    
    def _check_message_alignment(self, title: str, message: str) -> bool:
        """Check if main message aligns with title."""
        # Implementation would use NLP to check semantic alignment
        return True
    
    def _check_point_relevance(self, title: str, point: str) -> bool:
        """Check if supporting point is relevant to title."""
        # Implementation would use NLP to check semantic relevance
        return True

if __name__ == "__main__":
    # Example usage
    slide_content = {
        "title": "Market Analysis Shows 30% Growth Opportunity in Digital Banking",
        "supporting_points": [
            "Current market share is 15%",
            "Competitor analysis reveals gaps",
            "Digital adoption trending upward"
        ]
    }
    
    metrics = {
        "market_share": 0.15,
        "growth_rate": 0.30,
        "digital_adoption_trend": "increasing"
    }
    
    intelligence = SlideIntelligence()
    
    print("\nVisual Suggestions:")
    print(intelligence.suggest_visuals(slide_content, metrics))
    
    print("\nEnhanced Supporting Points:")
    print(intelligence.enhance_supporting_points(slide_content["supporting_points"], metrics))
    
    print("\nResearch Requirements:")
    print(intelligence.get_research_requirements(slide_content))
    
    print("\nTitle Improvement Suggestions:")
    print(intelligence.suggest_title_improvements(slide_content["title"])) 