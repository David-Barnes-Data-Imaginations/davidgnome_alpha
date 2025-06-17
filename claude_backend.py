import os
import sys
from prompts import SYSTEM_PROMPT

"""
Claude AI backend module for davidgnome.

This module provides functionality to interact with Anthropic's Claude AI model.
It handles API key management, client initialization, and includes mock implementations
for when the API key is not available or the Anthropic library is not installed.
"""

# Read the key from the environment
API_KEY: str | None = os.getenv("ANTHROPIC_API_KEY")

# Mock classes for when API key is not available
class MockAnthropic:
    """
    Mock implementation of the Anthropic client.

    Used when the real Anthropic API key is not available or the library is not installed.

    Attributes:
        api_key (str): The API key (real or mock).
        messages (MockMessages): Messages interface for creating responses.
    """
    def __init__(self, api_key):
        """
        Initialize the mock Anthropic client.

        Args:
            api_key (str): The API key (real or mock).
        """
        self.api_key = api_key
        self.messages = MockMessages()

class MockMessages:
    """
    Mock implementation of the Anthropic messages interface.

    Provides a simplified version of the message creation functionality
    that returns predefined responses based on keywords in the input.
    """
    def create(self, model, max_tokens, messages):
        """
        Create a mock response based on the input messages.

        Args:
            model (str): The model name (ignored in mock implementation).
            max_tokens (int): Maximum number of tokens (ignored in mock implementation).
            messages (list): List of message dictionaries with 'role' and 'content' keys.

        Returns:
            MockResponse: A mock response object containing generated text.
        """
        # Simulate a response based on the input
        user_message = messages[-1]["content"] if messages else ""

        # Simple response generation based on keywords
        if "help" in user_message.lower():
            response_content = "I'm Claude, here to help! What would you like assistance with?"
        elif "system" in user_message.lower():
            response_content = "Based on your system information, here's my analysis and suggestions."
        elif "history" in user_message.lower():
            response_content = "Looking at your terminal history, I can provide some helpful insights."
        else:
            response_content = "I understand your request. Here's a thoughtful response based on the context provided."

        return MockResponse(response_content)

class MockResponse:
    """
    Mock response object that mimics the structure of Anthropic API responses.

    Attributes:
        content (list): List of MockContent objects.
    """
    def __init__(self, content):
        """
        Initialize a mock response with the given content.

        Args:
            content (str): The text content of the response.
        """
        self.content = [MockContent(content)]

class MockContent:
    """
    Mock content object that mimics the structure of Anthropic API response content.

    Attributes:
        text (str): The text content.
    """
    def __init__(self, text):
        """
        Initialize a mock content object with the given text.

        Args:
            text (str): The text content.
        """
        self.text = text

# Initialize the client (use mock if no API key)
if API_KEY:
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=API_KEY)
    except ImportError:
        print("Warning: Anthropic library not installed, using mock client")
        client = MockAnthropic(api_key=API_KEY)
else:
    print("Warning: ANTHROPIC_API_KEY not set, using mock client")
    client = MockAnthropic(api_key="mock-key")

def query(prompt, history, system_info):
    """
    Query the Claude AI model with the given prompt, history, and system information.

    This function formats the input data into a structured prompt that includes
    recent terminal history and system information, then sends it to the Claude API
    (or mock implementation if the API is not available).

    Args:
        prompt (str): The user's question or prompt.
        history (list): List of recent terminal commands.
        system_info (str): Information about the user's system.

    Returns:
        str: The response text from Claude.
    """
    full_prompt = f"Terminal history: {', '.join(history[-10:])}\n\nSystem: {system_info}\n\nQuestion: {prompt}"
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": full_prompt}
    ]

    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1000,
        messages=messages
    )

    return response.content[0].text
