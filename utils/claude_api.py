"""
Utility to interact with the Anthropic Claude API for the portfolio chatbot.
"""

import os
import anthropic
from typing import List, Dict, Any

class ClaudeChat:
    """
    A class to handle Claude chat interactions with proper context management.
    """
    
    def __init__(self, api_key: str = None, model: str = "claude-3-haiku-20240307"):
        """
        Initialize the Claude chat integration.
        
        Args:
            api_key: The Anthropic API key (if None, will try to get from environment)
            model: The Claude model to use
        """
        # Use provided API key or try to get from environment
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("No API key provided. Set ANTHROPIC_API_KEY environment variable or pass api_key parameter.")
            
        self.model = model
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.system_prompt = ""
        
    def set_system_prompt(self, resume_context: Dict[str, Any]):
        """
        Set up the system prompt with resume context for better responses.
        
        Args:
            resume_context: Dictionary containing resume information
        """
        self.system_prompt = f"""
        You are an AI assistant representing Kelby James Enevold for job opportunities. 
        You're helping potential employers learn more about Kelby's qualifications and fit for roles.
        
        Here is Kelby's background information:
        - Current goal: Find a role that leverages AWS and AI/GenAI expertise, focusing on technical enablement or implementation
        - Most recent role: {resume_context['work_experience'][0]['title']} at {resume_context['work_experience'][0]['company']}
        - Key strengths: {', '.join(resume_context['chatbot_context']['strengths'])}
        - Unique attributes: {', '.join(resume_context['chatbot_context']['unique_selling_points'])}
        - Job preferences: {', '.join(resume_context['chatbot_context']['job_seeking_preferences'])}
        
        Guidelines for your responses:
        1. Be honest and accurate about Kelby's experience and qualifications
        2. Highlight relevant skills and achievements that match the employer's question
        3. Don't exaggerate or fabricate experiences
        4. If you don't know something, acknowledge that rather than making up information
        5. Be professional but conversational in tone
        6. For technical questions, demonstrate Kelby's expertise where relevant
        7. When discussing salary expectations or availability, suggest they contact Kelby directly
        8. Emphasize Kelby's passion for AWS, AI technologies, and technical enablement
        
        Always aim to represent Kelby accurately and positively, increasing the likelihood of advancing
        in the job process. Focus on factual information from the resume.
        """
        
    def get_response(self, user_message: str) -> str:
        """
        Get a response from Claude based on the user's message.
        
        Args:
            user_message: The message from the user/employer
            
        Returns:
            Claude's response as a string
        """
        try:
            # Call the Claude API with the system prompt and user message
            response = self.client.messages.create(
                model=self.model,
                system=self.system_prompt,
                messages=[
                    {"role": "user", "content": user_message}
                ],
                max_tokens=1000,
            )
            return response.content[0].text
        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}. Please try again or contact Kelby directly."

# Mock version for development without API key
class MockClaudeChat:
    """
    A mock version of the ClaudeChat class for development without an API key.
    """
    
    def __init__(self, *args, **kwargs):
        self.system_prompt = ""
    
    def set_system_prompt(self, resume_context: Dict[str, Any]):
        """Sets the mock system prompt"""
        self.system_prompt = "Mock system prompt set"
    
    def get_response(self, user_message: str) -> str:
        """
        Return mock responses based on keywords in the user message.
        
        Args:
            user_message: The message from the user/employer
            
        Returns:
            A mock response as a string
        """
        user_message = user_message.lower()
        
        if "experience" in user_message or "background" in user_message:
            return "Kelby has over 15 years of experience in IT, with a strong focus on AWS cloud technologies, training, and AI implementation. Most recently, Kelby served as a Technical Enablement Lead at Mission Cloud, developing AI/GenAI solutions and cloud training programs."
            
        elif "aws" in user_message or "cloud" in user_message:
            return "Kelby has extensive AWS experience across multiple services including Bedrock, Q, OpenSearch, EC2, RDS, S3, and CloudFormation. Kelby has held AWS certifications including Solutions Architect Associate, SysOps Administrator Associate, and Database Specialty, and has worked directly at AWS as a Cloud Support Engineer."
            
        elif "ai" in user_message or "generative" in user_message or "claude" in user_message:
            return "Kelby has hands-on experience with AI and GenAI technologies, including building RAG systems with Amazon Bedrock, creating Custom GPTs, and implementing AI solutions for business teams. Kelby also developed and launched an AI/GenAI Essentials course completed by over 240 employees."
            
        elif "training" in user_message or "teaching" in user_message or "education" in user_message:
            return "Kelby excels in technical training and enablement, having created AWS certification programs, developed an apprenticeship program with a 73% conversion rate to full-time roles, and served as an AWS Training Architect at Linux Academy/A Cloud Guru creating courses and hands-on labs."
            
        elif "salary" in user_message or "compensation" in user_message:
            return "For specific discussions about salary expectations and compensation, I'd recommend reaching out to Kelby directly via email at kelby.james.enevold@gmail.com or phone at 208-553-8095."
            
        else:
            return "I'd be happy to tell you more about Kelby's experience and qualifications. Feel free to ask about specific skills, projects, or how Kelby might fit with your team's needs. Kelby is particularly skilled in AWS technologies, AI implementation, and technical training/enablement."