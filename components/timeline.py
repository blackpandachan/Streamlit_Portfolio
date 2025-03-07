"""
Professional timeline component for displaying work experience and achievements.
Enhanced with better spacing and visual treatments.
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

def render_timeline_item(item, is_left=True):
    """
    Render a single timeline item with animation and interactivity.
    Enhanced spacing and visual treatments.
    """
    # Use a wider center column for the timeline line and better spacing
    cols = st.columns([5, 1.8, 5]) if is_left else st.columns([5, 1.8, 5])
    
    # Content column
    content_col = cols[0] if is_left else cols[2]
    with content_col:
        # Create expandable card with professional styling
        with st.expander(f"**{item['title']} | {item['company']}**", expanded=False):
            # Format dates with better typography
            st.markdown(f"""
            <div class="timeline-period">
                <i class="timeline-icon">📅</i> 
                <span class="timeline-dates">{format_date(item['start_date'])} - {format_date(item['end_date'])}</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Description with improved spacing
            st.markdown(f"<p class='timeline-description'>{item['description']}</p>", unsafe_allow_html=True)
            
            # Skills section
            st.markdown("<h4 class='skills-header'>Skills & Technologies</h4>", unsafe_allow_html=True)
            
            # Wrap skills in a scrollable container for better display
            skill_html = ' '.join([f'<span class="skill-badge">{skill}</span>' for skill in item['skills']])
            st.markdown(f"""
            <div class="skills-scrollable">
                {skill_html}
            </div>
            """, unsafe_allow_html=True)
            
            # Achievements section
            if 'achievements' in item and item['achievements']:
                st.markdown("<h4 class='achievements-header'>Key Achievements</h4>", unsafe_allow_html=True)
                for achievement in item['achievements']:
                    st.markdown(f"""
                    <div class="achievement-item">
                        <span class="achievement-bullet">•</span>
                        <span class="achievement-text">{achievement}</span>
                    </div>
                    """, unsafe_allow_html=True)
    
    # Empty middle column to add spacing when collapsed
    # This improves the appearance of the timeline when items are collapsed
    cols[0 if not is_left else 2].markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
    
    # Timeline center column with year indicator - enhanced visual treatment
    with cols[1]:
        # For the timeline center, show a year indicator and vertical line
        year = datetime.strptime(item['start_date'], "%Y-%m").year
        
        st.markdown(f"""
        <div class="timeline-center">
            <div class="timeline-year">{year}</div>
            <div class="timeline-dot"></div>
            <div class="timeline-line"></div>
        </div>
        """, unsafe_allow_html=True)

def load_timeline_css():
    """
    Load custom CSS for a professional timeline component with enhanced styling.
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
    
    /* Streamlit expander customization for timeline */
    .streamlit-expanderHeader {
        background-color: #1F2937 !important;
        border: 1px solid #374151 !important;
        border-radius: 8px !important;
        padding: 1.25rem !important;
        margin-bottom: 2rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
    }
    
    .streamlit-expanderHeader:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 15px rgba(0,0,0,0.15) !important;
        border-color: #4B5563 !important;
    }
    
    .streamlit-expanderHeader[aria-expanded="true"] {
        border-bottom-left-radius: 0 !important;
        border-bottom-right-radius: 0 !important;
        border-bottom: none !important;
        box-shadow: none !important;
        background-color: #2563EB !important;
    }
    
    .streamlit-expanderContent {
        background-color: #111827 !important;
        border: 1px solid #374151 !important;
        border-top: none !important;
        border-bottom-left-radius: 8px !important;
        border-bottom-right-radius: 8px !important;
        padding: 1.75rem !important;
        margin-bottom: 2rem !important;
    }
    
    /* Timeline period with icon */
    .timeline-period {
        display: flex;
        align-items: center;
        margin-bottom: 1.25rem;
        color: #9CA3AF;
        font-size: 1rem;
    }
    
    .timeline-icon {
        margin-right: 0.5rem;
        font-style: normal;
    }
    
    .timeline-dates {
        font-weight: 500;
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
        .streamlit-expanderHeader {
            padding: 1rem !important;
        }
        
        .streamlit-expanderContent {
            padding: 1.5rem !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def display_timeline(work_experience):
    """
    Display work experience as a professional interactive timeline.
    """
    load_timeline_css()
    
    # Professional header section
    st.markdown("""
    <div class="career-title">
        <h2>Professional Journey</h2>
        <p>Expand each role to explore details, skills, and key achievements</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Container for the timeline to add spacing from other sections
    st.markdown('<div style="padding: 20px 0;"></div>', unsafe_allow_html=True)
    
    # Sort experience by start date (newest first)
    sorted_experience = sorted(
        work_experience, 
        key=lambda x: datetime.strptime(x['start_date'], "%Y-%m"),
        reverse=True
    )
    
    # Create timeline container
    with st.container():
        for i, experience in enumerate(sorted_experience):
            render_timeline_item(experience, is_left=(i % 2 == 0))
            
            # Add spacing between timeline items
            st.markdown('<div style="height: 30px;"></div>', unsafe_allow_html=True)