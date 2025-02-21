"""
Streamlit app for the OutlineWriter presentation generator.
"""

import streamlit as st
import random
import json
import os
from pathlib import Path
from content_generator import EnhancedContentGenerator, ProjectInput
from slide_intelligence import SlideIntelligence

# Ensure proper file paths
APP_DIR = Path(__file__).parent
TEMPLATE_PATH = APP_DIR / 'action_titles_template.txt'

# Initialize session state
if 'app_state' not in st.session_state:
    st.session_state.app_state = {
        'storyline': [],
        'supporting_points': {},
        'final_deck': [],
        'findings_and_objectives': "",
        'uploaded_files': [],
        'ollama_status': None
    }

def check_ollama_connection():
    """Check if Ollama is running."""
    import requests
    try:
        response = requests.get('http://localhost:11434/api/tags')
        return response.status_code == 200
    except:
        return False

def load_mckinsey_templates():
    """Load McKinsey-style templates."""
    try:
        if not TEMPLATE_PATH.exists():
            st.error(f"Template file not found at {TEMPLATE_PATH}")
            return ""
        
        with open(TEMPLATE_PATH, 'r') as f:
            return f.read()
    except Exception as e:
        st.error(f"Could not load templates: {str(e)}")
        return ""

# Wellness tips during processing
WELLNESS_TIPS = [
    "☕ Perfect time for a coffee break!",
    "🚶‍♂️ Take a quick walk to refresh your mind",
    "👀 Give your eyes a rest - look at something 20 feet away for 20 seconds",
    "🧘‍♂️ Try a quick meditation or breathing exercise",
    "💪 Do some quick desk stretches"
]

def get_random_wellness_tip() -> str:
    return random.choice(WELLNESS_TIPS)

def main():
    st.title("OutlineWriter - Consulting Presentation Generator")
    
    # Check Ollama connection
    if st.session_state.app_state['ollama_status'] is None:
        ollama_running = check_ollama_connection()
        st.session_state.app_state['ollama_status'] = ollama_running
        
    if not st.session_state.app_state['ollama_status']:
        st.error("""
        ⚠️ Ollama is not running. Please start Ollama first:
        ```bash
        ollama run llama2
        ```
        """)
        return
    
    # Check template file
    if not TEMPLATE_PATH.exists():
        st.error(f"""
        ⚠️ Template file not found. Please ensure 'action_titles_template.txt' exists in:
        {APP_DIR}
        """)
        return
    
    st.write("""
    Generate structured outlines for consulting presentations following best practices.
    Just fill in the key details below and let AI do the heavy lifting!
    """)
    
    # Project Type Selection
    project_type = st.radio(
        "Select Project Type",
        ["Project", "Proposal"],
        help="Choose 'Project' for ongoing work or 'Proposal' for new opportunities"
    )
    
    # Basic Information
    st.subheader("Basic Information")
    col1, col2 = st.columns(2)
    with col1:
        client_name = st.text_input(
            label="Client Name",
            help="Enter the client's name",
            key="client_name"
        )
    with col2:
        industry = st.text_input(
            label="Industry",
            help="Enter the client's industry",
            key="industry"
        )
    
    # Consolidated Findings & Objectives
    st.subheader("Findings & Objectives")
    findings_objectives = st.text_area(
        label="Enter your key findings and objectives",
        help="Combine your findings and objectives in a single text field",
        key="findings_objectives",
        height=200,
        value=st.session_state.app_state.get('findings_and_objectives', '')
    )
    
    # Save findings and objectives to state
    if findings_objectives != st.session_state.app_state.get('findings_and_objectives'):
        st.session_state.app_state['findings_and_objectives'] = findings_objectives
    
    # File Upload
    st.subheader("Upload Supporting Files (Optional)")
    uploaded_file = st.file_uploader(
        label="Upload CSV, Excel, or PDF files",
        type=["csv", "xlsx", "pdf"],
        help="Upload files containing relevant data or insights",
        key="file_uploader"
    )
    
    if uploaded_file:
        file_info = {
            'name': uploaded_file.name,
            'type': uploaded_file.type,
            'size': uploaded_file.size
        }
        if file_info not in st.session_state.app_state['uploaded_files']:
            st.session_state.app_state['uploaded_files'].append(file_info)
            st.success(f"File uploaded: {uploaded_file.name}")
    
    # Number of Slides
    num_slides = st.select_slider(
        "Number of Slides",
        options=[3, 5, 7, 10],
        value=5,
        help="Select the desired number of slides"
    )
    
    # Generate Button
    if st.button("Generate Presentation Outline"):
        if not (client_name and industry and findings_objectives):
            st.error("Please fill in all required fields (client, industry, and findings/objectives)")
            return
        
        try:
            # Create progress indicators
            progress_bar = st.progress(0)
            status_text = st.empty()
            tips_text = st.empty()
            
            # Show initial tip
            tips_text.info(f"While I work on your presentation... {get_random_wellness_tip()}")
            
            # Load templates
            template_text = load_mckinsey_templates()
            if not template_text:
                return
            
            # Create project input
            project = ProjectInput(
                client_name=client_name,
                industry=industry,
                problem_statement=findings_objectives,
                key_findings=[findings_objectives],  # We'll parse this better in production
                objectives=[],  # We'll parse this better in production
                project_type=project_type
            )
            
            # Generate presentation with progress updates
            generator = EnhancedContentGenerator()
            slides = []
            
            for i in range(num_slides):
                progress = (i + 1) / num_slides
                progress_bar.progress(progress)
                status_text.text(f"Generating slide {i+1} of {num_slides}...")
                
                if i % 2 == 0:
                    tips_text.info(f"While I work on your presentation... {get_random_wellness_tip()}")
                
                try:
                    # Generate slide
                    raw_slides = generator.generate_presentation(project, 1)
                    if raw_slides:
                        raw_slide = raw_slides[0]
                        if isinstance(raw_slide, str):
                            raw_slide = json.loads(raw_slide)
                        
                        # Create slide structure
                        slide = {
                            'title': raw_slide.get('title', f"Slide {i+1}"),
                            'main_message': raw_slide.get('main_message', 'Main message not available'),
                            'supporting_points': raw_slide.get('supporting_points', ['Point not available']),
                            'section': raw_slide.get('section', generator._get_section_type(i, num_slides))
                        }
                        slides.append(slide)
                except Exception as e:
                    st.error(f"Error generating slide {i+1}: {str(e)}")
                    continue
            
            # Clear progress indicators
            progress_bar.empty()
            status_text.empty()
            tips_text.empty()
            
            # Store generated content
            st.session_state.app_state['storyline'] = slides
            
            # Display results
            if slides:
                st.success("✨ Presentation outline generated successfully!")
                
                # Display slides
                for i, slide in enumerate(slides, 1):
                    with st.expander(f"Slide {i}: {slide['title']}", expanded=True):
                        st.markdown("**Main Message:**")
                        st.write(slide['main_message'])
                        
                        st.markdown("**Supporting Points:**")
                        for point in slide['supporting_points']:
                            st.markdown(f"- {point}")
            else:
                st.warning("No slides were generated. Please try again.")
        
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    
    # Tips and Guidelines in Sidebar
    with st.sidebar:
        st.subheader("💡 Tips for Better Results")
        st.markdown("""
        - Be specific in your findings and objectives
        - Include metrics when available
        - Keep inputs concise but informative
        """)
        
        st.subheader("📚 About Templates")
        st.markdown("""
        **Standard 5-Slide Structure:**
        1. Executive Summary
        2. Current State
        3. Key Issues
        4. Solution Approach
        5. Implementation
        """)

if __name__ == "__main__":
    main()