"""
Main application file for Kelby Enevold's portfolio website.
"""

import streamlit as st
import os
import logging
import traceback

# Set Python path to include the current directory
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("portfolio_app.log")
    ]
)
logger = logging.getLogger(__name__)

# Set page config - must be the first Streamlit command
st.set_page_config(
    page_title="Kelby Enevold | AI Expert, Trainer, Veteran",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Import components
from components.header import load_css, render_navigation, render_footer
from components.resume import display_resume
from components.chatbot import display_chat_ui
from data.resume_data import personal_info, key_achievements

def display_enhanced_header():
    """
    Display an enhanced header with modern styling and visual elements.
    Makes sure to override any existing styling.
    """
    # Add enhanced header CSS with higher specificity and !important flags
    st.markdown("""
    <style>
    /* Reset any background styles that might interfere */
    .main-header, .header-container, div[data-testid="stAppViewContainer"] > div:first-child {
        background: none !important;
        background-color: transparent !important;
        box-shadow: none !important;
        border: none !important;
    }
    
    /* Enhanced header styling with high specificity */
    body .enhanced-header {
        position: relative;
        border-radius: 12px !important;
        padding: 2rem !important;
        margin-bottom: 1.5rem !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
        border-bottom: 3px solid #3B82F6 !important;
        overflow: hidden !important;
        text-align: center !important;
        z-index: 10 !important;
    }
    
    /* Full-width gradient background */
    body .enhanced-header::after {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        bottom: 0 !important;
        background: linear-gradient(90deg, #10172a 0%, #1E3A8A 85%, #1E3A8A 100%) !important;
        background-size: 100% 100% !important;
        z-index: 0 !important;
    }
    
    /* Decorative accent */
    body .enhanced-header::before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        right: 0 !important;
        width: 300px !important;
        height: 100% !important;
        background: linear-gradient(135deg, rgba(96, 165, 250, 0.1) 0%, rgba(37, 99, 235, 0) 100%) !important;
        z-index: 1 !important;
    }
    
    /* Force position to ensure it's on top */
    body .header-content {
        position: relative !important;
        z-index: 2 !important;
    }
    
    body .header-name {
        color: #F9FAFB !important;
        font-size: 2.6rem !important;
        font-weight: 700 !important;
        margin-bottom: 0.5rem !important;
        letter-spacing: -0.025em !important;
    }
    
    body .header-title {
        color: #60A5FA !important;
        font-size: 1.5rem !important;
        font-weight: 500 !important;
        opacity: 0.95 !important;
        letter-spacing: 0.5px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        flex-wrap: wrap !important;
    }
    
    body .header-badge {
        display: inline-block !important;
        background: linear-gradient(90deg, #1E40AF, #3B82F6) !important;
        color: white !important;
        font-size: 0.875rem !important;
        font-weight: 500 !important;
        padding: 0.25rem 0.75rem !important;
        border-radius: 9999px !important;
        margin: 0.5rem 0.75rem !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
    }
    
    body .header-badge.aws {
        background: linear-gradient(90deg, #FF9900, #FFC400) !important;
        color: #0F1629 !important;
    }
    
    body .header-badge.ai {
        background: linear-gradient(90deg, #1E40AF, #3B82F6) !important;
    }
    
    body .header-badge.veteran {
        background: linear-gradient(90deg, #991B1B, #DC2626) !important;
    }
    
    body .enhanced-header-container {
        background-color: transparent !important;
        padding: 0 !important;
        margin-bottom: -1rem !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Render enhanced header with a wrapper container
    st.markdown("""
    <div class="enhanced-header-container">
        <div class="enhanced-header">
            <div class="header-content">
                <h1 class="header-name">Kelby Enevold</h1>
                <div class="header-title">
                    <span class="header-badge ai">AI Expert</span>
                    <span class="header-badge aws">AWS Cloud</span>
                    <span class="header-badge">Technical Trainer</span>
                    <span class="header-badge veteran">Veteran</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_home():
    """
    Display the home page content with improved card layout.
    """
    # Hero section
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown(
            f"""<h1 style='font-size:3.5rem; margin-bottom:1.5rem; color:#F3F4F6;'>
            Hey, I'm {personal_info['name'].split()[0]}</h1>""", 
            unsafe_allow_html=True
        )
        
        st.markdown(
            f"""<p style='font-size:1.5rem; color:#D1D5DB; margin-bottom:2rem;'>
            AWS & AI Expert specializing in technical enablement and cloud solutions.
            </p>""", 
            unsafe_allow_html=True
        )
        
        st.markdown(f"<p style='color:#F3F4F6;'>{personal_info['summary']}</p>", unsafe_allow_html=True)
        
        # Call-to-action buttons
        col_btn1, col_btn2, _ = st.columns([1.2, 1.2, 2])
        with col_btn1:
            st.markdown(
                """<a href='https://www.linkedin.com/in/enevoldk/' target="_blank" id='view-resume-btn' style='text-decoration:none;'>
                <div style='background-color:#1E40AF; color:#F3F4F6; padding:0.75rem 1.5rem; 
                border-radius:0.5rem; text-align:center; font-weight:500; margin-top:1rem;'>
                View My LinkedIn</div></a>""",
                unsafe_allow_html=True,
            )

        with col_btn2:
            if st.markdown(
                """<a href="#" onclick="document.getElementById('chat-btn-trigger').click(); return false;" id='chat-btn' style='text-decoration:none;'>
                <div style='background-color:#F3F4F6; color:#1E40AF; padding:0.75rem 1.5rem; 
                border-radius:0.5rem; text-align:center; font-weight:500; margin-top:1rem; 
                border:1px solid #1E40AF;'>
                Talk to my Chatbot</div></a>""",
                unsafe_allow_html=True,
            ):
                pass
            
            # Hidden button to be triggered by JavaScript
            if st.button("Click Here!", key="chat-btn-trigger", help=None, on_click=None, args=None, kwargs=None, type="primary", disabled=False, use_container_width=False):
                st.session_state.current_tab = "Chat With Assistant"
                st.rerun()
    
    with col2:
        # Profile image placeholder
        st.image("https://media.licdn.com/dms/image/v2/D5603AQEzEnXV23Hz-Q/profile-displayphoto-shrink_200_200/profile-displayphoto-shrink_200_200/0/1698954572182?e=1746662400&v=beta&t=URqecwO406XNBHXRTyIhADtN23usyaTDM6DqSHS0li0", width=300)
    
    # Add shared CSS for card styling
    st.markdown("""
    <style>
    .feature-card {
        border: 1px solid #374151;
        border-radius: 8px;
        padding: 1.5rem;
        background-color: #1F2937;
        height: 100%;
        position: relative;
        transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
        display: flex;
        flex-direction: column;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
        border-color: #3B82F6;
    }
    
    .feature-card:before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #1E40AF, #3B82F6);
        border-top-left-radius: 8px;
        border-top-right-radius: 8px;
    }
    
    .card-icon {
        font-size: 2.5rem;
        margin-bottom: 1.25rem;
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover .card-icon {
        transform: scale(1.1);
    }
    
    .card-title {
        color: #60A5FA;
        font-weight: 600;
        font-size: 1.35rem;
        margin-top: 0;
        margin-bottom: 1rem;
    }
    
    .card-description {
        color: #D1D5DB;
        line-height: 1.6;
    }
    
    /* Hide the hidden button */
    button[data-testid="baseButton-secondary"]:has(+ div:contains("hidden-chat-trigger")) {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create three highlight cards using Streamlit columns
    st.markdown("<div style='margin-top: 2rem; margin-bottom: 2rem;'></div>", unsafe_allow_html=True)
    cards = st.columns(3)
    
    card_data = [
        {
            "icon": "☁️",
            "title": "AWS Expert",
            "description": "Extensive experience with AWS services including Core services, Bedrock, Opensearch, and more."
        },
        {
            "icon": "🤖",
            "title": "AI/GenAI Specialist",
            "description": "Built RAG systems, Custom GPTs, and implemented AI solutions for enterprise teams."
        },
        {
            "icon": "📚",
            "title": "Technical Enablement",
            "description": "Created successful training programs and certifications for AWS cloud and AI technologies."
        }
    ]
    
    # Apply the custom card styling to each column
    for i, card in enumerate(card_data):
        with cards[i]:
            st.markdown(f"""
            <div class="feature-card">
                <div class="card-icon">{card['icon']}</div>
                <h3 class="card-title">{card['title']}</h3>
                <p class="card-description">{card['description']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Key achievements section
    st.markdown(
        "<h2 style='margin-top:3rem; margin-bottom:1.5rem; color:#F3F4F6;'>Key Achievements</h2>", 
        unsafe_allow_html=True
    )
    achievement_cols = st.columns(2)
    
    for i, achievement in enumerate(key_achievements[:4]):  # Show only top 4 achievements
        col_idx = i % 2
        with achievement_cols[col_idx]:
            st.markdown(f"""
            <div style="background-color:#1F2937; border-left:4px solid #1E40AF; 
                       padding:1.25rem; margin-bottom:1rem; color:#F3F4F6;">
                {achievement}
            </div>
            """, unsafe_allow_html=True)
    
    
    # Hidden button to be triggered by JavaScript
    if st.button("Talk to my Chatbot", key="chat-cta-trigger", help=None, on_click=None, args=None, kwargs=None, type="primary", disabled=False, use_container_width=False):
        st.session_state.current_tab = "Chat With Assistant"
        st.rerun()

def display_contact():
    """
    Display the contact section.
    """
    st.markdown("<h2 style='color:#F3F4F6;'>Contact Me</h2>", unsafe_allow_html=True)
    
    st.markdown(
        "<p style='color:#D1D5DB;'>If you'd like to get in touch, feel free to reach out through any of these channels:</p>", 
        unsafe_allow_html=True
    )
    
    contact_cols = st.columns(3)
    
    # Email
    with contact_cols[0]:
        st.markdown(f"""
        <div style="text-align:center; padding:1.5rem; border:1px solid #374151; 
                  border-radius:8px; height:100%; background-color:#1F2937; color:#F3F4F6;">
            <div style="font-size:2rem; margin-bottom:1rem;">✉️</div>
            <h3 style="margin-top:0;">Email</h3>
            <p>{personal_info['email']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Phone
    with contact_cols[1]:
        st.markdown(f"""
        <div style="text-align:center; padding:1.5rem; border:1px solid #374151; 
                  border-radius:8px; height:100%; background-color:#1F2937; color:#F3F4F6;">
            <div style="font-size:2rem; margin-bottom:1rem;">📞</div>
            <h3 style="margin-top:0;">Phone</h3>
            <p>{personal_info['phone']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # LinkedIn (placeholder - add real LinkedIn URL if available)
    with contact_cols[2]:
        st.markdown(f"""
        <div style="text-align:center; padding:1.5rem; border:1px solid #374151; 
                  border-radius:8px; height:100%; background-color:#1F2937; color:#F3F4F6;">
            <div style="font-size:2rem; margin-bottom:1rem;">🔗</div>
            <h3 style="margin-top:0;">LinkedIn</h3>
            <p><a href="https://www.linkedin.com/in/enevoldk/" target="_blank" style="color: #60A5FA; text-decoration: none;">Connect with me on LinkedIn</a></p>
        </div>
        """, unsafe_allow_html=True)

def main():
    """
    Main function to run the Streamlit app.
    """
    try:
        # Load CSS (page config is now at the top of the file)
        load_css()
        
        # Display enhanced header (new addition)
        display_enhanced_header()
        
        # Custom theme settings for better accessibility
        st.markdown(
            """
            <style>
            /* Message input styling */
            .stTextInput>div>div>input {
                background-color: #374151;
                color: #F3F4F6;
            }
            
            /* Chat message containers */
            .stChatMessage {
                background-color: #1F2937;
                border: 1px solid #374151;
                border-radius: 8px;
            }
            
            .stChatMessage.user {
                background-color: #374151;
            }
            
            /* Header styling */
            .stApp > header {
                background-color: #1E1E1E;
                color: #F3F4F6;
            }
            
            /* Button styling */
            .stButton button {
                border-radius: 0.375rem;
                font-weight: 500;
                transition: background-color 0.2s;
            }
            
            .stButton button[data-baseweb="button"] {
                border-radius: 0.375rem;
            }
            
            .stButton button[kind="primary"] {
                background-color: #1E40AF;
            }
            
            .stButton button[kind="primary"]:hover {
                background-color: #2563EB;
            }
            
            .stButton button[kind="secondary"] {
                background-color: #374151;
                color: #F3F4F6;
            }
            
            .stButton button[kind="secondary"]:hover {
                background-color: #4B5563;
            }
            
            /* Hide the default tabs visually but keep them for state management */
            .stTabs [data-baseweb="tab-list"] {
                display: none;
            }
            
            /* Main content area */
            .main .block-container {
                background-color: #1E1E1E;
            }
            
            /* Chat input area */
            .stChatInputContainer {
                background-color: #374151;
                border: 1px solid #374151;
            }
            
            /* Hide all hidden trigger buttons */
            button[data-testid="baseButton-primary"] {
                display: none !important;
            }

            /* But show normal primary buttons */
            button[data-testid="baseButton-primary"]:not([kind="secondary"]):not(:has(+ div:contains("hidden-"))) {
                display: inline-flex !important;
            }
            """,
            unsafe_allow_html=True,
        )

        # Render navigation and get tabs (tabs are hidden but used for state)
        tabs = render_navigation()
        
        # Display content based on current tab in session state
        current_tab = st.session_state.get('current_tab', 'Home')
        
        if current_tab == "Home":
            display_home()
        elif current_tab == "Resume":
            display_resume()
        elif current_tab == "Chat With Assistant":
            display_chat_ui()
        elif current_tab == "Contact":
            display_contact()
        
        # Render footer
        render_footer()
    
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        logger.error(traceback.format_exc())
        st.error(f"An error occurred: {str(e)}")
        st.code(traceback.format_exc())

if __name__ == "__main__":
    main()