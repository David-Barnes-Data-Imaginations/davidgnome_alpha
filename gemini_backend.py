import os
import sys

"""
Gemini backend module for davidgnome.

This module provides functionality to interact with Google's Gemini models.
It handles API key management, client initialization, and includes mock implementations
for when the API key is not available or the Google Generative AI library is not installed.
"""

# Read the key from the environment
API_KEY: str | None = os.getenv("GEMINI_API_KEY")


# Mock classes for when API key is not available
class MockGemini:
    """Mock implementation of the Gemini client."""

    def generate_content(self, content):
        """Create a mock response based on the input."""
        user_message = content if isinstance(content, str) else ""

        if "help" in user_message.lower():
            response_content = "I'm Gemini, here to help! What can I do for you?"
        elif "system" in user_message.lower():
            response_content = "Here's some system information and assistance based on your query."
        elif "history" in user_message.lower():
            response_content = "Based on your terminal history, here are some suggestions."
        else:
            response_content = "I understand your request. Here's a helpful response based on the context provided."

        return MockGenerateContentResponse(response_content)


class MockGenerateContentResponse:
    """Mock response object that mimics the structure of Gemini API responses."""

    def __init__(self, text):
        self.text = text

if API_KEY:
    try:
        import google.generativeai as genai

        genai.configure(api_key=API_KEY)
        client = genai.GenerativeModel('gemini-pro')
    except ImportError:
        print("Warning: google-generativeai library not installed, using mock client", file=sys.stderr)
        client = MockGemini()
    except Exception as e:
        print(f"Warning: Failed to initialize Gemini client: {e}", file=sys.stderr)
        client = MockGemini()

def query(prompt, history, system_info):
    """
    Query the Gemini model with the given prompt, history, and system information.

    Args:
        prompt (str): The user's question or prompt.
        history (list): List of recent terminal commands.
        system_info (str): Information about the user's system.

    Returns:
        str: The response text from Gemini.
    """
    full_prompt = f"Terminal history: {', '.join(history[-10:])}\n\nSystem: {system_info}\n\nQuestion: {prompt}"
    response = client.generate_content(full_prompt)
    return response.text