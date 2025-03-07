"""
Header component for portfolio website with navigation and theming.
"""

import streamlit as st

def load_css():
    """
    Load custom CSS for styling the entire application.
    """
    st.markdown("""
    <style>
        /* Main styling */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }
        
        /* Override Streamlit's default header styling */
        .stMarkdown h1, 
        .stMarkdown h2, 
        .stMarkdown h3,
        h1, h2, h3,
        div.stMarkdown h1,
        div.stMarkdown h2,
        div.stMarkdown h3 {
            color: #F3F4F6 !important;
            font-family: 'Inter', sans-serif !important;
        }

        /* Ensure markdown headers also follow the theme */
        .element-container div.stMarkdown h1,
        .element-container div.stMarkdown h2,
        .element-container div.stMarkdown h3 {
            color: #F3F4F6 !important;
        }
        
        /* Header styling */
        .main-header {
            background-color: #1E1E1E;
            padding: 1.5rem 0;
            border-bottom: 1px solid #2D3748;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        }
        
        .header-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 1rem;
        }
        
        .header-text {
            font-size: 1.5rem;
            font-weight: 600;
            color: #F3F4F6 !important;
            margin: 0;
        }
        
        /* Custom navigation styling */
        .nav-container {
            display: flex;
            justify-content: center;
            gap: 0.5rem;
            margin: 1rem 0 2rem 0;
            flex-wrap: wrap;
        }
        
        .nav-tab {
            display: inline-block;
            background-color: #1E40AF;
            color: #F3F4F6;
            padding: 0.75rem 1.5rem;
            border-radius: 0.375rem;
            text-decoration: none;
            font-weight: 500;
            transition: background-color 0.2s;
            cursor: pointer;
            text-align: center;
            min-width: 150px;
        }
        
        .nav-tab:hover {
            background-color: #2563EB;
        }
        
        .nav-tab.active {
            background-color: #2563EB;
            box-shadow: 0 0 0 2px #60A5FA;
        }
        
        /* Hide default streamlit tabs */
        .stTabs {
            display: none !important;
        }
        
        /* Responsive adjustments */
        @media (max-width: 768px) {
            .nav-container {
                flex-direction: column;
                width: 100%;
            }
            
            .nav-tab {
                width: 100%;
            }
            
            .header-text {
                font-size: 1.2rem;
            }
        }
        
        /* Footer styling */
        footer {
            text-align: center;
            padding: 2rem 0;
            margin-top: 3rem;
            border-top: 1px solid #374151;
            color: #D1D5DB;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Add custom script for tab functionality
    st.markdown("""
    <script>
    // This script will be ignored by Streamlit, but we're keeping it for documentation
    // The actual functionality is handled through the click event in Python
    </script>
    """, unsafe_allow_html=True)

def render_navigation():
    """
    Render the navigation/header section.
    """
    # Create responsive header
    st.markdown("""
    <div class="main-header">
        <div class="header-container">
            <div>
                <h1 class="header-text">Kelby Enevold | AWS & AI Expert</h1>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create the tabs for state management
    tabs = st.tabs(["Home", "Resume", "Chat With Assistant", "Contact"])
    
    # Get current tab from session state or default to Home
    if 'current_tab' not in st.session_state:
        st.session_state.current_tab = "Home"
    
    # Create custom navigation buttons
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("Home", key="home_btn", use_container_width=True, 
                    type="primary" if st.session_state.current_tab == "Home" else "secondary"):
            st.session_state.current_tab = "Home"
            st.rerun()
    
    with col2:
        if st.button("Resume", key="resume_btn", use_container_width=True,
                    type="primary" if st.session_state.current_tab == "Resume" else "secondary"):
            st.session_state.current_tab = "Resume"
            st.rerun()
    
    with col3:
        if st.button("Chat With Assistant", key="chat_btn", use_container_width=True,
                    type="primary" if st.session_state.current_tab == "Chat With Assistant" else "secondary"):
            st.session_state.current_tab = "Chat With Assistant"
            st.rerun()
    
    with col4:
        if st.button("Contact", key="contact_btn", use_container_width=True,
                    type="primary" if st.session_state.current_tab == "Contact" else "secondary"):
            st.session_state.current_tab = "Contact"
            st.rerun()
    
    # Add some spacing
    st.markdown("<div style='margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)
    
    return tabs

def render_footer():
    """
    Render the footer section.
    """
    st.markdown("""
    <footer>
        <p>&copy; 2025 Kelby Enevold | Created with Streamlit & Claude</p>
    </footer>
    """, unsafe_allow_html=True)