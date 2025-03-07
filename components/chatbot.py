"""
Chatbot component for portfolio website using streamlit-chat for UI and Claude API for responses.
"""

import streamlit as st
from utils.claude_api import ClaudeChat, MockClaudeChat
from data.resume_data import (
    personal_info, skills, work_experience, certifications, 
    key_achievements, chatbot_context
)
import os
import json
from datetime import datetime
import time
import requests
import logging

# Configure component-level logging
logger = logging.getLogger(__name__)

def load_chatbot_css():
    """
    Load custom CSS for the chatbot component.
    """
    st.markdown("""
    <style>
    /* Chat message container styling for dark mode */
    .chat-message {
        padding: 1.5rem; 
        border-radius: 0.5rem; 
        margin-bottom: 1rem; 
        display: flex;
        background: #1F2937; /* Dark background */
        color: #F3F4F6;      /* Light text */
    }
    .chat-message.user {
        background: #374151; /* Slightly lighter for user messages */
    }
    .chat-message.assistant {
        background: #1F2937; /* Dark for assistant messages */
    }
    .chat-message .avatar {
        width: 40px; 
        min-width: 40px; 
        margin-right: 1rem;
    }
    .chat-message .avatar img {
        max-width: 100%; 
        max-height: 100%; 
        border-radius: 50%;
    }
    .chat-message .message {
        width: 100%;
    }
    /* Quick question buttons */
    .quick-question {
        display: inline-block;
        margin: 0.25rem;
        padding: 0.5rem 1rem;
        background: #1E40AF;
        color: #F3F4F6;
        border-radius: 20px;
        cursor: pointer;
        font-size: 0.875rem;
        transition: all 0.2s;
    }
    .quick-question:hover {
        background: #2563EB;
        transform: translateY(-1px);
    }
    /* Typing indicator */
    .typing-indicator {
        display: flex;
        align-items: center;
        margin: 1rem 0;
    }
    .typing-dot {
        width: 8px;
        height: 8px;
        margin: 0 2px;
        background-color: #1E40AF;
        border-radius: 50%;
        animation: typing 1s infinite ease-in-out;
    }
    .typing-dot:nth-child(2) { animation-delay: 0.2s; }
    .typing-dot:nth-child(3) { animation-delay: 0.4s; }
    @keyframes typing {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    /* Dark mode input styling */
    .stTextInput > div > div > input {
        border-radius: 20px;
        background-color: #374151;
        color: #F3F4F6;
        border: 1px solid #374151;
    }
    /* Dark mode button styling */
    .stButton>button {
        border-radius: 20px;
        padding: 0.5rem 1rem;
        background-color: #1E40AF;
        color: #F3F4F6;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

def initialize_chat(resume_data):
    """
    Initialize the chat component with Claude API or mock version.
    
    Args:
        resume_data: Dictionary with resume information for context
    
    Returns:
        Initialized chat client
    """
    # Get API key from session state or environment
    api_key = st.session_state.get('anthropic_api_key', os.environ.get("ANTHROPIC_API_KEY", ""))
    
    # Initialize chat client (real or mock based on API key availability)
    if api_key:
        chat_client = ClaudeChat(api_key=api_key)
    else:
        # For development/demo without API key, use mock responses
        chat_client = MockClaudeChat()
    
    # Set system prompt with resume context
    chat_client.set_system_prompt(resume_data)
    
    return chat_client

def display_api_key_input():
    """
    Display a form for the user to input their Anthropic API key.
    """
    with st.expander("😊 Set Anthropic API Key (optional)", expanded=False):
        st.write(
            "To use Claude for real responses, you can provide your Anthropic API key. "
            "If no key is provided, the chatbot will use pre-programmed responses. "
            "Your key is stored only in this session and not saved permanently."
        )
        
        api_key = st.text_input(
            "Anthropic API Key", 
            value=st.session_state.get('anthropic_api_key', ""), 
            type="password",
            help="Enter your Anthropic API key to enable live Claude responses."
        )
        
        if st.button("Save API Key"):
            st.session_state['anthropic_api_key'] = api_key
            st.success("API key saved for this session!")
            st.rerun()

def render_chat_message(message, is_user=False):
    """
    Render a single chat message with the appropriate styling.
    
    Args:
        message: The message text to display
        is_user: Whether this is a user message (True) or assistant message (False)
    """
    if is_user:
        avatar_url = "https://ui-avatars.com/api/?name=You&background=60A5FA&color=fff"
        alignment = "flex-end"
        message_type = "user"
    else:
        avatar_url = "https://ui-avatars.com/api/?name=KJE&background=1E40AF&color=fff"
        alignment = "flex-start"
        message_type = "assistant"
    
    st.markdown(f"""
    <div class="chat-message {message_type}" style="align-self: {alignment};">
        <div class="avatar">
            <img src="{avatar_url}">  
        </div>
        <div class="message">{message}</div>
    </div>
    """, unsafe_allow_html=True)

def render_quick_questions():
    """
    Display quick question buttons for common queries.
    """
    st.markdown("#### Quick Questions")
    questions = [
        "What are your key AWS skills?",
        "Tell me about your recent projects",
        "What certifications do you have?",
        "What's your experience with AI/ML?",
        "Describe your leadership experience",
        "What are your career achievements?"
    ]
    
    cols = st.columns(2)
    for i, question in enumerate(questions):
        with cols[i % 2]:
            if st.button(question, key=f"quick_q_{i}", use_container_width=True):
                return question
    return None

def export_conversation():
    """
    Export the current conversation history to a JSON file.
    """
    if not st.session_state.chat_history:
        st.warning("No conversation to export yet!")
        return
        
    # Prepare conversation data
    conversation_data = {
        "timestamp": datetime.now().isoformat(),
        "messages": st.session_state.chat_history
    }
    
    # Convert to JSON string
    json_str = json.dumps(conversation_data, indent=2)
    
    # Create download button
    st.download_button(
        label="📥 Export Conversation",
        data=json_str,
        file_name=f"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json"
    )

def display_chat_ui():
    """
    Display the chat interface and handle message exchanges.
    """
    # Create a dictionary with all resume data for context
    resume_data = {
        "personal_info": personal_info,
        "skills": skills,
        "work_experience": work_experience,
        "certifications": certifications,
        "key_achievements": key_achievements,
        "chatbot_context": chatbot_context
    }
    
    # Initialize chat history in session state if it doesn't exist
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Get chat client
    chat_client = initialize_chat(resume_data)
    
    # Load custom CSS
    load_chatbot_css()
    
    # Create columns for title and export button
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("### 💬 Ask me about Kelby's experience")
    with col2:
        export_conversation()
    
    st.markdown("Ask questions about Kelby's skills, experience, or qualifications for your role!")
    
    # Display quick questions
    quick_question = render_quick_questions()
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history:
            render_chat_message(message["text"], message["is_user"])
    
    # User input
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input(
            "Type your question here:",
            key="user_input",
            placeholder="Example: What experience do you have with AWS?"
        )
        submit_button = st.form_submit_button("Send message")
    
    # Process user input when submitted
    if submit_button and user_input or quick_question:
        input_text = quick_question if quick_question else user_input
        
        # Add user message to chat history
        st.session_state.chat_history.append(
            {"text": input_text, "is_user": True}
        )
        
        # Show typing indicator
        with st.empty():
            st.markdown("""
            <div class="typing-indicator">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
            """, unsafe_allow_html=True)
            
            # Get response from Claude
            response = chat_client.get_response(input_text)
            
            # Add assistant response to chat history
            st.session_state.chat_history.append(
                {"text": response, "is_user": False}
            )
        
        # Rerun to update UI
        st.rerun()

    # Sample questions for inspiration
    st.markdown("### Sample questions to ask:")
    sample_questions = [
        "What AWS services are you most experienced with?",
        "Tell me about your experience with Generative AI",
        "How have you implemented RAG systems?",
        "What training programs have you developed?",
        "What makes you a good fit for a cloud engineering role?"
    ]
    
    # Display sample questions as clickable buttons
    cols = st.columns(2)
    for i, question in enumerate(sample_questions):
        with cols[i % 2]:
            if st.button(question, key=f"sample_q_{i}"):
                # Add user message to chat history
                st.session_state.chat_history.append(
                    {"text": question, "is_user": True}
                )
                
                # Get response from Claude
                response = chat_client.get_response(question)
                
                # Add assistant response to chat history
                st.session_state.chat_history.append(
                    {"text": response, "is_user": False}
                )
                
                # Rerun to update UI
                st.rerun()

def call_anthropic_api(prompt, api_key):
    """
    Call the Anthropic Claude API with the given prompt.
    
    Args:
        prompt: The user's query
        api_key: Anthropic API key
    
    Returns:
        The generated response text or an error message
    """
    try:
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": api_key,
            "content-type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        # Build system prompt with context
        system_prompt = f"""
        You are an AI assistant representing {personal_info['name']}, a {personal_info['title']}. 
        Your task is to answer questions about {personal_info['name']}'s background, experience, skills, and qualifications.
        
        Here's information about {personal_info['name']} to help you respond accurately:
        
        PERSONAL SUMMARY:
        {personal_info['summary']}
        
        KEY STRENGTHS:
        {', '.join(chatbot_context['strengths'])}
        
        UNIQUE SELLING POINTS:
        {', '.join(chatbot_context['unique_selling_points'])}
        
        JOB PREFERENCES:
        {', '.join(chatbot_context['job_seeking_preferences'])}
        
        PROJECT HIGHLIGHTS:
        """
        
        # Add project highlights
        for project in chatbot_context.get('project_highlights', []):
            system_prompt += f"\n- {project['name']}: {project['description']}"
            system_prompt += f"\n  Technologies: {', '.join(project['technologies'])}"
        
        # Add FAQs for context
        system_prompt += "\n\nFREQUENTLY ASKED QUESTIONS:"
        for faq in chatbot_context.get('frequently_asked_questions', []):
            system_prompt += f"\n- Q: {faq['question']}"
            system_prompt += f"\n  A: {faq['answer']}"
            
        system_prompt += """
        
        IMPORTANT INSTRUCTIONS:
        1. Always represent yourself as if you are {personal_info['name']}. Use first-person pronouns (I, me, my).
        2. Be professional but conversational in your tone.
        3. If asked about your AI nature, politely redirect to {personal_info['name']}'s qualifications.
        4. Keep responses concise and focused on {personal_info['name']}'s professional background.
        5. If you don't have specific information, say so rather than inventing details.
        """
        
        data = {
            "model": "claude-instant-1",
            "max_tokens": 500,
            "messages": [{"role": "user", "content": prompt}],
            "system": system_prompt
        }
        
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        # Extract the response content
        response_data = response.json()
        return response_data["content"][0]["text"]
    
    except requests.exceptions.RequestException as e:
        logger.error(f"API request error: {str(e)}")
        return f"Sorry, I encountered an error communicating with the AI service. Error: {str(e)}"
    except (KeyError, json.JSONDecodeError, IndexError) as e:
        logger.error(f"Response parsing error: {str(e)}")
        return "Sorry, I couldn't process the response from the AI service."
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return f"An unexpected error occurred: {str(e)}"

def format_message(message, is_user=False):
    """
    Format a chat message with appropriate styling.
    
    Args:
        message: The message text
        is_user: Boolean indicating if the message is from the user
    """
    message_class = "user-message" if is_user else "assistant-message"
    return f'<div class="message {message_class}">{message}</div>'

def display_typing_indicator():
    """Display a typing indicator animation."""
    return """
    <div class="typing-indicator">
        <span class="dot"></span>
        <span class="dot"></span>
        <span class="dot"></span>
    </div>
    """

def display_chatbot():
    """
    Display the interactive chatbot component.
    """
    try:
        load_chatbot_css()
        
        st.markdown("## Chat with Me")
        st.markdown("Ask me anything about my experience, skills, or how I can help your organization.")
        
        # Initialize chat history in session state if it doesn't exist
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = [
                {
                    "role": "assistant", 
                    "content": f"Hi there! I'm {personal_info['name']}, a {personal_info['title']}. How can I help you today?"
                }
            ]
        
        # Initialize typing state
        if 'is_typing' not in st.session_state:
            st.session_state.is_typing = False
        
        # Quick question buttons
        st.markdown("<div class='quick-questions'>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        
        # Define quick questions from FAQs and common queries
        quick_questions = [
            "What are your core skills?",
            "Tell me about your experience with AWS",
            "What AI projects have you worked on?",
            "How do you approach technical training?",
            "What are you looking for in your next role?",
            "Can you share some testimonials?"
        ]
        
        # Additional questions from FAQs
        if 'frequently_asked_questions' in chatbot_context:
            for faq in chatbot_context['frequently_asked_questions']:
                if faq['question'] not in quick_questions and len(quick_questions) < 9:
                    quick_questions.append(faq['question'])
        
        # Display quick question buttons
        with col1:
            for i in range(0, min(3, len(quick_questions))):
                if st.button(quick_questions[i], key=f"quick_{i}", use_container_width=True):
                    st.session_state.chat_history.append({"role": "user", "content": quick_questions[i]})
                    st.session_state.is_typing = True
                    st.experimental_rerun()
        
        with col2:
            for i in range(3, min(6, len(quick_questions))):
                if st.button(quick_questions[i], key=f"quick_{i}", use_container_width=True):
                    st.session_state.chat_history.append({"role": "user", "content": quick_questions[i]})
                    st.session_state.is_typing = True
                    st.experimental_rerun()
        
        with col3:
            for i in range(6, min(9, len(quick_questions))):
                if i < len(quick_questions):
                    if st.button(quick_questions[i], key=f"quick_{i}", use_container_width=True):
                        st.session_state.chat_history.append({"role": "user", "content": quick_questions[i]})
                        st.session_state.is_typing = True
                        st.experimental_rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Display chat container
        chat_container = st.container()
        with chat_container:
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            
            # Display chat history
            for message in st.session_state.chat_history:
                st.markdown(
                    format_message(message["content"], message["role"] == "user"),
                    unsafe_allow_html=True
                )
            
            # Show typing indicator if applicable
            if st.session_state.is_typing:
                st.markdown(display_typing_indicator(), unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Chat input
        with st.form(key="chat_form", clear_on_submit=True):
            col1, col2 = st.columns([4, 1])
            
            with col1:
                user_input = st.text_input(
                    "Your message:",
                    key="user_message",
                    placeholder="Type your message here..."
                )
            
            with col2:
                submit_button = st.form_submit_button("Send")
        
        # API key input (optional)
        with st.expander("API Settings", expanded=False):
            api_key = st.text_input(
                "Enter Anthropic API Key (optional):",
                type="password",
                help="Your API key will not be stored permanently"
            )
        
        # Add export conversation button
        if st.button("Export Conversation", key="export_chat"):
            # Create text representation of the conversation
            export_text = "# Conversation with Portfolio Chatbot\n\n"
            for msg in st.session_state.chat_history:
                role = "You" if msg["role"] == "user" else personal_info['name']
                export_text += f"**{role}**: {msg['content']}\n\n"
            
            # Create download link
            st.download_button(
                label="Download Conversation",
                data=export_text,
                file_name="portfolio_chat_export.md",
                mime="text/markdown"
            )
        
        # Process new message if submitted
        if submit_button and user_input:
            # Add user message to chat history
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            st.session_state.is_typing = True
            st.experimental_rerun()
        
        # Process the response if we're in typing state
        if st.session_state.is_typing:
            # Get the last user message
            last_user_message = next((msg["content"] for msg in reversed(st.session_state.chat_history) 
                                     if msg["role"] == "user"), None)
            
            if last_user_message:
                # Small delay to simulate typing
                time.sleep(0.5)
                
                # Use a default API key if not provided
                current_api_key = api_key if api_key else "dummy-api-key-for-demo-purposes"
                
                # Get response from API
                response = call_anthropic_api(last_user_message, current_api_key)
                
                # Add response to chat history
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                
                # Turn off typing indicator
                st.session_state.is_typing = False
                
                # Rerun to update the UI
                st.experimental_rerun()
    
    except Exception as e:
        logger.error(f"Error in display_chatbot: {str(e)}")
        st.error(f"An error occurred in the chatbot component: {str(e)}")

# This is removed to prevent automatic execution during import
