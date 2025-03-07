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
    page_title="Kelby Enevold | AWS & AI Expert",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Import components
from components.header import load_css, render_navigation, render_footer
from components.resume import display_resume
from components.chatbot import display_chat_ui
from data.resume_data import personal_info, key_achievements

def display_home():
    """
    Display the home page content.
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
                """<a href='#' id='view-resume-btn' style='text-decoration:none;'>
                <div style='background-color:#1E40AF; color:#F3F4F6; padding:0.75rem 1.5rem; 
                border-radius:0.5rem; text-align:center; font-weight:500; margin-top:1rem;'>
                View Resume</div></a>""",
                unsafe_allow_html=True,
            )

        with col_btn2:
            st.markdown(
                """<a href='#' id='chat-btn' style='text-decoration:none;'>
                <div style='background-color:#F3F4F6; color:#1E40AF; padding:0.75rem 1.5rem; 
                border-radius:0.5rem; text-align:center; font-weight:500; margin-top:1rem; 
                border:1px solid #1E40AF;'>
                Chat With Me</div></a>""",
                unsafe_allow_html=True,
            )
    
    with col2:
        # Profile image placeholder
        st.image("https://media.licdn.com/dms/image/v2/D5603AQEzEnXV23Hz-Q/profile-displayphoto-shrink_200_200/profile-displayphoto-shrink_200_200/0/1698954572182?e=1746662400&v=beta&t=URqecwO406XNBHXRTyIhADtN23usyaTDM6DqSHS0li0", width=300)
    
    # Create three highlight cards
    cards = st.columns(3)
    
    card_data = [
        {
            "icon": "☁️",
            "title": "AWS Expert",
            "description": "Extensive experience with AWS services including Bedrock, EC2, RDS, S3, and CloudFormation."
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
    
    for i, card in enumerate(card_data):
        with cards[i]:
            st.markdown(f"""
            <div style="border:1px solid #374151; border-radius:8px; padding:1.5rem; height:100%;
                        transition: transform 0.2s, box-shadow 0.2s; background-color:#1F2937;">
                <div style="font-size:2rem; margin-bottom:1rem; color:#F3F4F6;">{card['icon']}</div>
                <h3 style="margin-top:0; color:#1E40AF; font-weight:600;">{card['title']}</h3>
                <p style="color:#F3F4F6;">{card['description']}</p>
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
    
    # Call to action to chat
    st.markdown(
        """<div style="text-align:center; margin-top:3rem; margin-bottom:3rem; 
                padding:2rem; background-color:#111827; border-radius:8px;">
                <h2 style="margin-top:0; color:#F3F4F6;">Want to learn more about my experience?</h2>
                <p style="margin-bottom:1.5rem; color:#D1D5DB;">Ask my AI assistant questions about my background, skills, and qualifications.</p>
                <a href="#" id="chat-cta-btn" style="background-color:#1E40AF; color:#F3F4F6; 
                text-decoration:none; padding:0.75rem 1.5rem; border-radius:0.5rem; 
                font-weight:500;">Chat Now</a>
                </div>""",
        unsafe_allow_html=True
    )

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
            <p>Connect with me on LinkedIn</p>
        </div>
        """, unsafe_allow_html=True)

def main():
    """
    Main function to run the Streamlit app.
    """
    try:
        # Load CSS (page config is now at the top of the file)
        load_css()
        
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
            </style>
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
