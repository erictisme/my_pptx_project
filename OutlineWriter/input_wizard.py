from typing import List, Dict, Optional
import json
from project_context import ProjectContext, ResearchInput, ProjectObjective

def get_input(prompt: str, required: bool = True, default: str = None) -> str:
    """Get input from user with optional default value."""
    if default:
        prompt = f"{prompt} (default: {default}): "
    else:
        prompt = f"{prompt}: "
    
    while True:
        value = input(prompt).strip()
        if value:
            return value
        if not required and default is not None:
            return default
        if not required:
            return ""
        print("This field is required. Please provide a value.")

def get_list_input(prompt: str, required: bool = True) -> List[str]:
    """Get list input from user."""
    print(f"\n{prompt} (Enter empty line when done)")
    items = []
    while True:
        item = input("> ").strip()
        if not item:
            if items or not required:
                break
            print("At least one item is required.")
            continue
        items.append(item)
    return items

def get_timeline() -> Dict[str, str]:
    """Get project timeline."""
    start = get_input("Project start date (YYYY-MM)")
    end = get_input("Project end date (YYYY-MM)")
    return {"start": start, "end": end}

def get_deck_size() -> str:
    """Get desired deck size."""
    while True:
        size = get_input("Desired deck size (<5, 5-10, or 10-20 slides)").lower()
        if size in ["<5", "5-10", "10-20"]:
            return size
        print("Please choose one of: <5, 5-10, or 10-20")

def collect_project_context() -> ProjectContext:
    """Interactive wizard for collecting project context."""
    print("\n=== Project Context Wizard ===")
    print("Please provide the following information about your project.\n")
    
    # Basic Info
    print("\n--- Basic Information ---")
    project_id = get_input("Project ID (e.g., DT2024-001)")
    client_name = get_input("Client name")
    industry = get_input("Industry")
    sub_industry = get_input("Sub-industry (optional)", required=False)
    region = get_input("Region", required=False, default="Global")
    
    # Project Details
    print("\n--- Project Details ---")
    engagement_type = get_input("Engagement type (e.g., Strategy, Operations, Digital)")
    project_phase = get_input("Project phase (e.g., Discovery, Analysis, Implementation)")
    timeline = get_timeline()
    deck_size = get_deck_size()
    
    # Client Context
    print("\n--- Client Context ---")
    client_situation = get_input("Client situation (current state)")
    why_now = get_input("Why now? (urgency/motivation)")
    previous_work = get_input("Previous work (optional)", required=False)
    
    # Research
    print("\n--- Research and Analysis ---")
    methods = get_list_input("Research methods used")
    key_findings = get_list_input("Key findings")
    data_sources = get_list_input("Data sources")
    limitations = get_list_input("Limitations (optional)", required=False)
    assumptions = get_list_input("Assumptions (optional)", required=False)
    
    research = ResearchInput(
        methods=methods,
        key_findings=key_findings,
        data_sources=data_sources,
        limitations=limitations,
        assumptions=assumptions
    )
    
    # Objectives
    print("\n--- Project Objectives ---")
    primary_goal = get_input("Primary goal")
    success_metrics = get_list_input("Success metrics")
    stakeholders = get_list_input("Key stakeholders")
    constraints = get_list_input("Constraints (optional)", required=False)
    dependencies = get_list_input("Dependencies (optional)", required=False)
    
    objectives = ProjectObjective(
        primary_goal=primary_goal,
        success_metrics=success_metrics,
        stakeholders=stakeholders,
        constraints=constraints,
        dependencies=dependencies
    )
    
    # Team Context
    print("\n--- Team Context (optional) ---")
    team_size = get_input("Team size (optional)", required=False)
    location = get_input("Team location (optional)", required=False)
    client_team = get_input("Client team involvement (optional)", required=False)
    
    team_context = {}
    if team_size:
        team_context["team_size"] = team_size
    if location:
        team_context["location"] = location
    if client_team:
        team_context["client_team"] = client_team
    
    # Special Requirements
    print("\n--- Special Requirements (optional) ---")
    special_requirements = get_list_input("Special requirements", required=False)
    
    # Create ProjectContext
    context = ProjectContext(
        project_id=project_id,
        client_name=client_name,
        industry=industry,
        engagement_type=engagement_type,
        project_phase=project_phase,
        timeline=timeline,
        client_situation=client_situation,
        why_now=why_now,
        research=research,
        objectives=objectives,
        sub_industry=sub_industry,
        region=region,
        previous_work=previous_work,
        team_context=team_context,
        special_requirements=special_requirements
    )
    
    # Save context
    context.save("project_context.json")
    
    # Save deck size
    with open("deck_config.json", "w") as f:
        json.dump({"deck_size": deck_size}, f)
    
    return context

def main():
    """Run the input wizard."""
    try:
        context = collect_project_context()
        print("\nProject context saved successfully!")
        print("You can now run content_generator.py to generate your presentation content.")
    except KeyboardInterrupt:
        print("\n\nInput cancelled. No changes were saved.")
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("Please try again.")

if __name__ == "__main__":
    main() 