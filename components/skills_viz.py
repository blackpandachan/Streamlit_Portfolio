"""
Skills visualization component.
This is a specialized component for reliable skills radar chart visualization.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.io as pio
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Set Plotly rendering options for better compatibility
pio.templates.default = "plotly_dark"

def create_basic_radar_chart(skills_data):
    """
    Create a very basic radar chart for skills visualization.
    Uses minimal styling to ensure compatibility.
    
    Args:
        skills_data (dict): Dictionary of skills with their proficiency levels (0-10)
        
    Returns:
        plotly.graph_objects.Figure or None: The radar chart figure or None if creation fails
    """
    try:
        # Extract skills and values
        categories = list(skills_data.keys())
        values = list(skills_data.values())
        
        # Radar charts need at least 3 points
        if len(categories) < 3:
            st.warning(f"Need at least 3 skills for radar chart. Found {len(categories)}.")
            return None
            
        # Create simplest possible radar chart
        fig = go.Figure()
        
        # Add trace with improved styling
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            fillcolor='rgba(65, 105, 225, 0.4)',
            line=dict(color='#3B82F6', width=2),
            name='Skills'
        ))
        
        # Use enhanced layout with bigger size
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True, 
                    range=[0, 10],
                    tickfont=dict(size=10),
                    tickvals=[0, 2, 4, 6, 8, 10],
                    gridcolor='rgba(255, 255, 255, 0.15)'
                ),
                angularaxis=dict(
                    tickfont=dict(size=12, color='white'),
                    gridcolor='rgba(255, 255, 255, 0.15)'
                ),
                bgcolor='rgba(0, 0, 0, 0)'
            ),
            height=600,  # Increased height
            width=700,   # Added explicit width
            margin=dict(l=80, r=80, t=20, b=20),  # Adjusted margins
            paper_bgcolor='rgba(0, 0, 0, 0)',  # Transparent background
            plot_bgcolor='rgba(0, 0, 0, 0)',   # Transparent plot area
        )
        
        return fig
    except Exception as e:
        logger.error(f"Error creating basic radar chart: {str(e)}")
        st.error(f"Could not create skills visualization: {str(e)}")
        return None

def display_skills_section(skills, categorized_skills):
    """
    Display the skills section with radar chart and textual representation.
    
    Args:
        skills (dict): Dictionary of all skills
        categorized_skills (dict): Dictionary of categorized skills
    """
    st.markdown("<h2 style='display: flex; align-items: center;'>Skills & Expertise <span style='margin-left: 10px;'>📊</span></h2>", unsafe_allow_html=True)
    
    # Category selection with improved styling
    categories = ["All Skills"] + list(categorized_skills.keys())
    selected_category = st.selectbox(
        "Filter by category",
        categories,
        index=0
    )
    
    # Get skills for selected category
    if selected_category == "All Skills":
        skills_to_display = skills
    else:
        skills_to_display = categorized_skills[selected_category]
    
    # Create columns for layout with adjusted ratio for better chart visibility
    col1, col2 = st.columns([4, 3])
    
    with col1:
        # Try to create and display radar chart
        chart = create_basic_radar_chart(skills_to_display)
        if chart:
            st.plotly_chart(chart, use_container_width=True, config={'displayModeBar': False})
        else:
            st.warning("Could not create radar chart visualization.")
    
    with col2:
        # Enhanced skill level display
        st.markdown("### Skill Levels")
        for skill, level in skills_to_display.items():
            # Create a custom HTML progress bar with enhanced styling
            percentage = level * 10
            color = "#3B82F6"  # Base blue color
            
            # Add visual indicator for proficiency level
            level_indicator = "Expert" if level >= 9 else "Advanced" if level >= 7 else "Intermediate" if level >= 5 else "Beginner"
            
            st.markdown(f"""
            <div style="margin-bottom: 16px;">
                <div style="font-weight: 500; margin-bottom: 4px; display: flex; justify-content: space-between;">
                    <span>{skill}</span>
                    <span style="color: #9CA3AF;">{level}/10</span>
                </div>
                <div style="height: 8px; background-color: rgba(75, 85, 99, 0.3); border-radius: 4px; overflow: hidden;">
                    <div style="width: {percentage}%; height: 100%; background-color: {color}; border-radius: 4px; transition: width 0.5s ease;"></div>
                </div>
                <div style="text-align: right; font-size: 0.7em; color: #9CA3AF; margin-top: 2px;">{level_indicator}</div>
            </div>
            """, unsafe_allow_html=True)