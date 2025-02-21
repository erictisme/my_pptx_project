from dataclasses import dataclass, field
from typing import List, Dict, Optional
import json

@dataclass
class SlideContent:
    """Represents the content structure of a slide."""
    title: str
    points: List[str]
    visual_type: str = "bullet_points"
    layout_type: str = "Title and Content"

@dataclass
class StyleGuide:
    """McKinsey style guidelines."""
    fonts: Dict[str, Dict[str, any]] = None
    colors: Dict[str, str] = None
    spacing: Dict[str, float] = None
    
    def __post_init__(self):
        self.fonts = {
            "title": {"name": "Arial", "size": 32},
            "subtitle": {"name": "Arial", "size": 24},
            "body": {"name": "Arial", "size": 18},
            "caption": {"name": "Arial", "size": 14}
        }
        
        self.colors = {
            "primary": "#000000",      # Black
            "secondary": "#0085CA",    # McKinsey Blue
            "background": "#FFFFFF",   # White
            "accent1": "#7B7B7B",     # Gray
            "accent2": "#4A90E2"      # Light Blue
        }
        
        self.spacing = {
            "title_margin_top": 0.5,    # inches
            "content_margin_left": 0.75,
            "paragraph_spacing": 12.0,   # points
            "line_spacing": 1.2         # multiplier
        }

@dataclass
class ResearchInput:
    """Research and analysis inputs"""
    methods: List[str]
    key_findings: List[str]
    data_sources: List[str]
    limitations: Optional[List[str]] = None
    assumptions: Optional[List[str]] = None

@dataclass
class ProjectObjective:
    """Project objectives and success metrics"""
    primary_goal: str
    success_metrics: List[str]
    stakeholders: List[str]
    constraints: Optional[List[str]] = None
    dependencies: Optional[List[str]] = None

@dataclass
class ProjectContext:
    """Complete project context"""
    # Basic Info
    project_id: str
    client_name: str
    industry: str
    engagement_type: str  # e.g., Strategy, Operations, Digital
    project_phase: str    # e.g., Discovery, Analysis, Implementation
    timeline: Dict[str, str]  # e.g., {"start": "2024-02", "end": "2024-06"}
    client_situation: str
    why_now: str
    research: ResearchInput
    objectives: ProjectObjective
    
    # Optional fields
    sub_industry: Optional[str] = None
    region: str = "Global"
    previous_work: Optional[str] = None
    team_context: Optional[Dict[str, str]] = None
    special_requirements: Optional[List[str]] = None

    def to_dict(self) -> Dict:
        """Convert to dictionary format"""
        return {
            "metadata": {
                "project_id": self.project_id,
                "client": self.client_name,
                "industry": self.industry,
                "sub_industry": self.sub_industry,
                "region": self.region,
                "engagement_type": self.engagement_type,
                "project_phase": self.project_phase,
                "timeline": self.timeline
            },
            "context": {
                "client_situation": self.client_situation,
                "why_now": self.why_now,
                "previous_work": self.previous_work
            },
            "research": {
                "methods": self.research.methods,
                "key_findings": self.research.key_findings,
                "data_sources": self.research.data_sources,
                "limitations": self.research.limitations,
                "assumptions": self.research.assumptions
            },
            "objectives": {
                "primary_goal": self.objectives.primary_goal,
                "success_metrics": self.objectives.success_metrics,
                "stakeholders": self.objectives.stakeholders,
                "constraints": self.objectives.constraints,
                "dependencies": self.objectives.dependencies
            },
            "additional": {
                "team_context": self.team_context,
                "special_requirements": self.special_requirements
            }
        }
    
    def save(self, filename: str):
        """Save context to JSON file"""
        with open(filename, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    @classmethod
    def load(cls, filename: str) -> 'ProjectContext':
        """Load context from JSON file"""
        with open(filename, 'r') as f:
            data = json.load(f)
        
        # Reconstruct nested objects
        research = ResearchInput(
            methods=data["research"]["methods"],
            key_findings=data["research"]["key_findings"],
            data_sources=data["research"]["data_sources"],
            limitations=data["research"]["limitations"],
            assumptions=data["research"]["assumptions"]
        )
        
        objectives = ProjectObjective(
            primary_goal=data["objectives"]["primary_goal"],
            success_metrics=data["objectives"]["success_metrics"],
            stakeholders=data["objectives"]["stakeholders"],
            constraints=data["objectives"]["constraints"],
            dependencies=data["objectives"]["dependencies"]
        )
        
        return cls(
            project_id=data["metadata"]["project_id"],
            client_name=data["metadata"]["client"],
            industry=data["metadata"]["industry"],
            engagement_type=data["metadata"]["engagement_type"],
            project_phase=data["metadata"]["project_phase"],
            timeline=data["metadata"]["timeline"],
            client_situation=data["context"]["client_situation"],
            why_now=data["context"]["why_now"],
            research=research,
            objectives=objectives,
            sub_industry=data["metadata"]["sub_industry"],
            region=data["metadata"]["region"],
            previous_work=data["context"]["previous_work"],
            team_context=data["additional"]["team_context"],
            special_requirements=data["additional"]["special_requirements"]
        ) 