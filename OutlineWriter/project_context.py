from dataclasses import dataclass, field
from typing import List, Dict, Optional
import json
import logging
from datetime import datetime

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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
    # Non-default arguments (must come first)
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
    
    # Default arguments (must come after non-default arguments)
    project_type: str = "Project"  # or "Proposal"
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

def create_example_context() -> ProjectContext:
    """Create an example project context"""
    research = ResearchInput(
        methods=[
            "Stakeholder interviews (15 executives)",
            "Market analysis of competitors",
            "Customer journey mapping",
            "Financial impact modeling"
        ],
        key_findings=[
            "40% of customers report friction in digital channels",
            "Legacy systems cause 60% of service delays",
            "Competitors investing $200M in digital transformation"
        ],
        data_sources=[
            "Internal customer satisfaction surveys",
            "IT system performance logs",
            "Industry analyst reports"
        ],
        limitations=[
            "Limited access to legacy system documentation",
            "Incomplete customer transaction history"
        ],
        assumptions=[
            "Current IT budget remains stable",
            "No major regulatory changes expected"
        ]
    )
    
    objectives = ProjectObjective(
        primary_goal="Transform digital customer experience to drive 30% growth",
        success_metrics=[
            "Reduce customer friction by 50%",
            "Increase digital adoption to 80%",
            "Improve NPS by 20 points"
        ],
        stakeholders=[
            "Chief Digital Officer",
            "Head of Customer Experience",
            "IT Leadership Team"
        ],
        constraints=[
            "6-month implementation timeline",
            "Fixed IT budget for FY2024",
            "Regulatory compliance requirements"
        ],
        dependencies=[
            "Legacy system upgrade completion",
            "Customer data migration",
            "Team training program"
        ]
    )
    
    return ProjectContext(
        project_id="DT2024-001",
        client_name="Global Bank Corp",
        industry="Financial Services",
        sub_industry="Retail Banking",
        region="North America",
        engagement_type="Digital Transformation",
        project_phase="Strategy Development",
        timeline={"start": "2024-02", "end": "2024-08"},
        client_situation="Leading retail bank facing digital disruption and customer churn",
        why_now="Increasing competition from digital-first banks and declining NPS",
        previous_work="Customer Strategy Review (2023)",
        research=research,
        objectives=objectives,
        team_context={
            "team_size": "8 consultants",
            "location": "Hybrid (NYC office + remote)",
            "client_team": "4 client team members dedicated"
        },
        special_requirements=[
            "Board presentation in May 2024",
            "Regulatory compliance review needed",
            "Change management focus"
        ]
    )

def main():
    """Example usage of ProjectContext"""
    # Create example context
    context = create_example_context()
    
    # Save to file
    context.save("project_context.json")
    logger.info("Saved example context to project_context.json")
    
    # Load from file
    loaded_context = ProjectContext.load("project_context.json")
    logger.info("Successfully loaded context from file")
    
    # Print some key information
    print("\n=== Project Context Summary ===")
    print(f"\nClient: {loaded_context.client_name}")
    print(f"Industry: {loaded_context.industry} ({loaded_context.sub_industry})")
    print(f"Engagement: {loaded_context.engagement_type}")
    print(f"\nSituation: {loaded_context.client_situation}")
    print(f"Why Now: {loaded_context.why_now}")
    
    print("\nKey Findings:")
    for finding in loaded_context.research.key_findings:
        print(f"• {finding}")
    
    print("\nObjectives:")
    print(f"Primary Goal: {loaded_context.objectives.primary_goal}")
    print("\nSuccess Metrics:")
    for metric in loaded_context.objectives.success_metrics:
        print(f"• {metric}")

if __name__ == "__main__":
    main() 