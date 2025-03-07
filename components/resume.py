"""
Resume component with interactive sections and skill visualization.
"""

import streamlit as st
import logging
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
import numpy as np
from components.timeline import display_timeline
from components.skills_viz import display_skills_section
from data.resume_data import (
    personal_info, skills, work_experience, certifications, 
    categorized_skills, testimonials
)

# Configure component-level logging
logger = logging.getLogger(__name__)

# Set Plotly defaults for dark mode compatibility
pio.templates.default = "plotly_dark"

def display_certification_card(cert):
    """
    Display a single certification with interactive elements.
    """
    try:
        st.markdown(f"""
        <div class="cert-card">
            <div class="cert-header">
                <h3>{cert['name']}</h3>
                <span class="cert-issuer">{cert['issuer']}</span>
            </div>
            <div class="cert-details">
                <p class="cert-date">Issued: {cert['date_earned']}</p>
                <p class="cert-id">ID: {cert.get('credential_id', 'N/A')}</p>
                {f'<a href="{cert["url"]}" target="_blank" class="cert-link">View Certificate →</a>' 
                if 'url' in cert else ''}
            </div>
        </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        logger.error(f"Error displaying certification card: {str(e)}")
        st.error(f"Could not display certification: {cert.get('name', 'Unknown')}")

def display_testimonial(testimonial):
    """
    Display a single testimonial with styling.
    """
    try:
        st.markdown(f"""
        <div class="testimonial-card">
            <div class="testimonial-quote">
                <i class="fas fa-quote-left"></i>
                {testimonial['quote']}
                <i class="fas fa-quote-right"></i>
            </div>
            <div class="testimonial-author">
                <div class="author-name">{testimonial['author']}</div>
                <div class="author-title">{testimonial['title']} | {testimonial['company']}</div>
                <div class="author-relation">({testimonial['relationship']})</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        logger.error(f"Error displaying testimonial: {str(e)}")
        st.error(f"Could not display testimonial from: {testimonial.get('author', 'Unknown')}")

def load_resume_css():
    """
    Load custom CSS for resume components.
    """
    st.markdown("""
    <style>
        /* Profile section styling */
        .profile-container {
            display: flex;
            background-color: #1F2937;
            padding: 2rem;
            border-radius: 0.5rem;
            margin-bottom: 2rem;
            align-items: center;
        }
        
        .profile-image {
            border-radius: 50%;
            width: 150px;
            height: 150px;
            border: 3px solid #60A5FA;
        }
        
        .profile-info {
            margin-left: 2rem;
        }
        
        .profile-info h1 {
            margin: 0;
            color: #F3F4F6 !important;
            font-size: 2rem;
        }
        
        .profile-info h2 {
            margin: 0.5rem 0 1rem 0;
            color: #60A5FA !important;
            font-size: 1.5rem;
        }
        
        .profile-info p {
            color: #D1D5DB;
            font-size: 1rem;
            line-height: 1.5;
        }
        
        /* Section headers */
        .section-header {
            color: #F3F4F6 !important;
            margin-top: 2rem;
            margin-bottom: 1rem;
            border-bottom: 1px solid #374151;
            padding-bottom: 0.5rem;
        }
        
        /* Certification cards */
        .cert-card {
            background-color: #374151;
            border-radius: 0.5rem;
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .cert-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 15px rgba(0, 0, 0, 0.2);
        }
        
        .cert-header {
            margin-bottom: 1rem;
        }
        
        .cert-header h3 {
            margin: 0;
            color: #F3F4F6 !important;
            font-size: 1.2rem;
        }
        
        .cert-issuer {
            color: #60A5FA;
            font-size: 0.9rem;
            font-weight: 500;
        }
        
        .cert-details {
            color: #D1D5DB;
            font-size: 0.9rem;
        }
        
        .cert-date, .cert-id {
            margin: 0.25rem 0;
        }
        
        .cert-link {
            display: inline-block;
            color: #60A5FA;
            margin-top: 0.5rem;
            text-decoration: none;
            font-weight: 500;
            transition: color 0.2s;
        }
        
        .cert-link:hover {
            color: #93C5FD;
            text-decoration: underline;
        }
        
        /* Download resume button */
        .download-resume {
            display: inline-block;
            background-color: #1E40AF;
            color: #F3F4F6;
            padding: 0.75rem 1.5rem;
            border-radius: 0.375rem;
            text-decoration: none;
            font-weight: 500;
            margin-top: 2rem;
            transition: background-color 0.2s;
        }
        
        .download-resume:hover {
            background-color: #2563EB;
        }
        
        /* Skills category selector */
        .skill-category-selector {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 1rem;
        }
        
        .skill-category-button {
            background-color: #374151;
            color: #D1D5DB;
            border: 1px solid #4B5563;
            border-radius: 4px;
            padding: 6px 12px;
            font-size: 0.9rem;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .skill-category-button.active {
            background-color: #1E40AF;
            color: #F3F4F6;
            border-color: #2563EB;
        }
        
        .skill-category-button:hover {
            background-color: #4B5563;
            color: #F3F4F6;
        }
        
        /* Testimonial cards */
        .testimonial-card {
            background-color: #1F2937;
            border-left: 4px solid #60A5FA;
            border-radius: 0.5rem;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .testimonial-quote {
            color: #E5E7EB;
            font-style: italic;
            margin-bottom: 1rem;
            position: relative;
            padding-left: 10px;
            line-height: 1.6;
        }
        
        .testimonial-quote i {
            color: #60A5FA;
            opacity: 0.6;
            margin: 0 5px;
        }
        
        .testimonial-author {
            text-align: right;
        }
        
        .author-name {
            color: #F3F4F6;
            font-weight: 600;
            font-size: 1rem;
        }
        
        .author-title {
            color: #9CA3AF;
            font-size: 0.9rem;
        }
        
        .author-relation {
            color: #60A5FA;
            font-size: 0.8rem;
            font-style: italic;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Add Font Awesome for quote icons
    st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">', unsafe_allow_html=True)

def display_resume():
    """
    Display the interactive resume page.
    """
    try:
        load_resume_css()
        
        # Profile section
        st.markdown("""
        <div class="profile-container">
            <img src="https://media.licdn.com/dms/image/v2/D5603AQEzEnXV23Hz-Q/profile-displayphoto-shrink_200_200/profile-displayphoto-shrink_200_200/0/1698954572182?e=1746662400&v=beta&t=URqecwO406XNBHXRTyIhADtN23usyaTDM6DqSHS0li0" 
                alt="Profile" class="profile-image">
            <div class="profile-info">
                <h1>{name}</h1>
                <h2>{title}</h2>
                <p>{summary}</p>
            </div>
        </div>
        """.format(**personal_info), unsafe_allow_html=True)
        
        # Skills visualization
        logger.info("Starting skills visualization rendering")
        display_skills_section(skills, categorized_skills)
        
        # Work Experience Timeline
        logger.info("Starting work experience timeline rendering")
        try:
            display_timeline(work_experience)
        except Exception as e:
            logger.error(f"Error displaying timeline: {str(e)}")
            st.error("Could not display work experience timeline")
        
        # Testimonials section
        st.markdown('<h2 class="section-header">Testimonials</h2>', unsafe_allow_html=True)
        try:
            for testimonial in testimonials:
                display_testimonial(testimonial)
        except Exception as e:
            logger.error(f"Error displaying testimonials: {str(e)}")
            st.error("Could not display testimonials")
        
        # Certifications
        st.markdown('<h2 class="section-header">Certifications</h2>', unsafe_allow_html=True)
        try:
            cert_cols = st.columns(2)
            for i, cert in enumerate(certifications):
                with cert_cols[i % 2]:
                    display_certification_card(cert)
        except Exception as e:
            logger.error(f"Error displaying certifications: {str(e)}")
            st.error("Could not display certifications")
        
        # Download Resume Button
        st.markdown("""
        <a href="#" class="download-resume" onclick="alert('PDF download will be implemented')">
            📄 Download Full Resume (PDF)
        </a>
        """, unsafe_allow_html=True)
    except Exception as e:
        logger.error(f"Error in display_resume: {str(e)}")
        st.error(f"An error occurred while displaying the resume: {str(e)}")

# Removed the direct call to display_resume() here to prevent duplicate execution