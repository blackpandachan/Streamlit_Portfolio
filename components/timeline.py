"""
Professional timeline component with visual connection between summary cards and details.
"""

import streamlit as st
from datetime import datetime

def format_date(date_str):
    """Format date string to display format."""
    try:
        date = datetime.strptime(date_str, "%Y-%m")
        return date.strftime("%b %Y")
    except:
        return date_str

def render_timeline_item(item, index, is_left=True):
    """
    Render a timeline item with preview on one side and expandable details on the opposite side.
    
    Args:
        item: The work experience item data
        index: Unique identifier for this timeline item
        is_left: Whether the preview card should be on the left
    """
    # Get active status to determine if this row should be highlighted
    is_active = f"show_details_{index}" in st.session_state and st.session_state[f"show_details_{index}"]
    
    # Create a visual connection container when active
    if is_active:
        st.markdown(f"""
        <div class="timeline-connection-container active-timeline-item" id="connection-{index}">
        </div>
        """, unsafe_allow_html=True)
    
    # Create columns - wider center for the timeline
    cols = st.columns([5, 1.8, 5])
    
    # Set preview and details columns based on left/right positioning
    preview_col = cols[0] if is_left else cols[2]
    details_col = cols[2] if is_left else cols[0]
    
    # Timeline center column with year indicator
    year = datetime.strptime(item['start_date'], "%Y-%m").year
    with cols[1]:
        st.markdown(f"""
        <div class="timeline-center">
            <div class="timeline-year">{year}</div>
            <div class="timeline-dot{' active-dot' if is_active else ''}"></div>
            <div class="timeline-line"></div>
        </div>
        """, unsafe_allow_html=True)
    
    # Preview card (always visible)
    with preview_col:
        st.markdown(f"""
        <div class="timeline-preview-card{' active-card' if is_active else ''}" id="preview-{index}">
            <div class="timeline-preview-header">
                <h3 class="timeline-preview-title">{item['title']}</h3>
                <p class="timeline-preview-company">{item['company']}</p>
            </div>
            <div class="timeline-preview-dates">
                <i class="timeline-icon">📅</i> {format_date(item['start_date'])} - {format_date(item['end_date'])}
            </div>
            <div class="timeline-preview-description">
                {item['description'][:150]}{'...' if len(item['description']) > 150 else ''}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Use Streamlit's native button for interactivity
        view_details = st.button(f"{'Hide Details' if is_active else 'View Details'}", key=f"btn_{index}")
    
    # Details section (expandable on opposite side)
    with details_col:
        # Instead of directly toggling in the button callback, we'll create a key-based system
        if view_details:
            # Toggle the current view state
            if f"show_details_{index}" not in st.session_state:
                st.session_state[f"show_details_{index}"] = True
            else:
                st.session_state[f"show_details_{index}"] = not st.session_state[f"show_details_{index}"]
            
            # Hide all other details
            for k in st.session_state:
                if k.startswith("show_details_") and k != f"show_details_{index}":
                    st.session_state[k] = False
            
            # Force a rerun to apply the changes
            st.rerun()
        
        # Only show if this item's details are set to show in session state
        if is_active:
            # Create details container with proper styling
            st.markdown(f"""
            <div class="timeline-details-card" id="details-{index}">
                <h3 class="details-title">{item['title']}</h3>
                <p class="timeline-description">{item['description']}</p>
            """, unsafe_allow_html=True)
            
            # Skills section
            st.markdown("<h4 class=\"skills-header\">Skills & Technologies</h4>", unsafe_allow_html=True)
            
            # Render skills badges properly
            skills_html = ""
            for skill in item['skills']:
                skills_html += f'<span class="skill-badge">{skill}</span> '
            
            st.markdown(f"""<div class="skills-scrollable">{skills_html}</div>""", unsafe_allow_html=True)
            
            # Achievements section
            if 'achievements' in item and item['achievements']:
                st.markdown("<h4 class=\"achievements-header\">Key Achievements</h4>", unsafe_allow_html=True)
                
                for achievement in item['achievements']:
                    st.markdown(f"""
                    <div class="achievement-item">
                        <span class="achievement-bullet">•</span>
                        <span class="achievement-text">{achievement}</span>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Close the main div
            st.markdown("</div>", unsafe_allow_html=True)

def load_timeline_css():
    """
    Load custom CSS for the interactive timeline.
    """
    st.markdown("""
    <style>
    /* Professional typography */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Timeline container */
    .timeline-container {
        position: relative;
        padding: 2rem 0;
        font-family: 'Inter', sans-serif;
    }
    
    /* Active row connection container */
    .timeline-connection-container {
        position: absolute;
        left: 0;
        right: 0;
        height: 100%;
        margin: -20px 0;
        z-index: -1;
    }
    
    .active-timeline-item {
        background-color: rgba(37, 99, 235, 0.05);
        border-radius: 12px;
        border-left: 4px solid rgba(37, 99, 235, 0.3);
        border-right: 4px solid rgba(37, 99, 235, 0.3);
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
    }
    
    /* Preview card styling - always visible */
    .timeline-preview-card {
        background-color: #1F2937;
        border: 1px solid #374151;
        border-radius: 8px;
        padding: 1.25rem;
        margin-bottom: 0.75rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        position: relative;
        transition: all 0.3s ease;
        border-left: 4px solid #2563EB;
    }
    
    .timeline-preview-card.active-card {
        background-color: #1E3A8A;
        border-color: #60A5FA;
        box-shadow: 0 8px 15px rgba(37, 99, 235, 0.2);
        transform: translateY(-3px);
    }
    
    .timeline-preview-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.15);
        border-color: #3B82F6;
    }
    
    .timeline-preview-header {
        display: flex;
        flex-direction: column;
        margin-bottom: 0.5rem;
    }
    
    .timeline-preview-title {
        color: #F3F4F6;
        font-size: 1.15rem;
        font-weight: 600;
        margin: 0 0 0.25rem 0;
    }
    
    .timeline-preview-company {
        color: #60A5FA;
        font-size: 1rem;
        font-weight: 500;
        margin: 0 0 0.5rem 0;
    }
    
    .timeline-preview-dates {
        color: #9CA3AF;
        font-size: 0.9rem;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
    }
    
    .timeline-preview-description {
        color: #D1D5DB;
        font-size: 0.95rem;
        line-height: 1.5;
        margin-bottom: 1rem;
    }
    
    /* Styling the Streamlit button to match our design */
    .stButton > button {
        background-color: #2563EB;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 4px;
        font-weight: 500;
        width: 100%;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background-color: #1D4ED8;
        transform: translateY(-2px);
    }
    
    /* Details card */
    .timeline-details-card {
        background-color: #111827;
        border: 1px solid #374151;
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 0.75rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        border-left: 4px solid #3B82F6;
        animation: fadeIn 0.3s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    .details-title {
        color: #F3F4F6;
        font-size: 1.25rem;
        font-weight: 600;
        margin: 0 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #374151;
    }
    
    /* Timeline description */
    .timeline-description {
        color: #F3F4F6;
        line-height: 1.7;
        margin-bottom: 1.75rem;
        font-size: 1.05rem;
    }
    
    /* Section headers */
    .skills-header, .achievements-header {
        color: #60A5FA;
        margin: 1.75rem 0 1rem 0;
        font-size: 1.15rem;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    
    /* Skills badges in horizontal scrollable container */
    .skills-scrollable {
        display: flex;
        flex-wrap: wrap;
        gap: 0.75rem;
        margin-bottom: 1.75rem;
    }
    
    .skill-badge {
        background: linear-gradient(135deg, #1E40AF, #3B82F6);
        color: #F3F4F6;
        padding: 0.4rem 1rem;
        border-radius: 999px;
        font-size: 0.85rem;
        font-weight: 500;
        letter-spacing: 0.3px;
        box-shadow: 0 3px 5px rgba(0,0,0,0.2);
        white-space: nowrap;
    }
    
    /* Achievements with bullets */
    .achievement-item {
        display: flex;
        margin-bottom: 1rem;
        align-items: baseline;
    }
    
    .achievement-bullet {
        color: #60A5FA;
        margin-right: 0.75rem;
        font-size: 1.25rem;
    }
    
    .achievement-text {
        color: #D1D5DB;
        line-height: 1.6;
        font-size: 1rem;
    }
    
    /* Timeline center elements */
    .timeline-center {
        position: relative;
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 0 0 60px 0;
    }
    
    .timeline-year {
        background: #2563EB;
        color: #F9FAFB;
        padding: 0.4rem 0.85rem;
        border-radius: 999px;
        font-size: 0.9rem;
        font-weight: 600;
        margin-bottom: 1rem;
        text-align: center;
        min-width: 4.5rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        letter-spacing: 0.5px;
    }
    
    .timeline-dot {
        width: 18px;
        height: 18px;
        background: #60A5FA;
        border-radius: 50%;
        margin: 0 auto;
        position: relative;
        z-index: 10;
        border: 3px solid #111827;
        box-shadow: 0 0 0 1px #60A5FA, 0 0 10px rgba(96, 165, 250, 0.5);
        transition: all 0.3s ease;
    }
    
    .timeline-dot.active-dot {
        background: #FEF08A;
        border: 3px solid #111827;
        box-shadow: 0 0 0 1px #FEF08A, 0 0 15px rgba(254, 240, 138, 0.7);
        transform: scale(1.2);
    }
    
    .timeline-line {
        position: absolute;
        top: 3.5rem;
        bottom: 0;
        left: 50%;
        width: 4px;
        background: linear-gradient(to bottom, #1E40AF, #60A5FA 20%, #60A5FA 80%, #1E40AF);
        transform: translateX(-50%);
        z-index: 1;
        opacity: 0.7;
    }
    
    /* Career title styling */
    .career-title {
        text-align: center;
        margin: 2rem 0 3.5rem 0;
        padding-bottom: 1.5rem;
        border-bottom: 2px solid #374151;
    }
    
    .career-title h2 {
        color: #F3F4F6;
        font-size: 2rem;
        font-weight: 600;
        margin-bottom: 0.75rem;
    }
    
    .career-title p {
        color: #D1D5DB;
        font-size: 1.1rem;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .timeline-preview-card,
        .timeline-details-card {
            padding: 1rem !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def display_timeline(work_experience):
    """
    Display work experience as a professional interactive timeline with side-expanding details.
    """
    # Initialize session state for timeline details if not already done
    if 'timeline_initialized' not in st.session_state:
        for i in range(len(work_experience)):
            st.session_state[f"show_details_{i}"] = False
        st.session_state['timeline_initialized'] = True
    
    load_timeline_css()
    
    # Professional header section
    st.markdown("""
    <div class="career-title">
        <h2>Professional Journey</h2>
        <p>Review my career progression and explore each role in detail</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sort experience by start date (newest first)
    sorted_experience = sorted(
        work_experience, 
        key=lambda x: datetime.strptime(x['start_date'], "%Y-%m"),
        reverse=True
    )
    
    try:
        # Create timeline container
        with st.container():
            for i, experience in enumerate(sorted_experience):
                render_timeline_item(experience, index=i, is_left=(i % 2 == 0))
                
                # Add spacing between timeline items
                st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Could not display work experience timeline: {str(e)}")