import os
import sys
from prompts import SYSTEM_PROMPT

"""
GPT backend module for davidgnome.

This module provides functionality to interact with OpenAI's GPT models.
It handles API key management, client initialization, and includes mock implementations
for when the API key is not available or the OpenAI library is not installed.
"""

# Read the key from the environment
API_KEY: str | None = os.getenv("OPENAI_API_KEY")

# Mock classes for when API key is not available
class MockOpenAI:
    """
    Mock implementation of the OpenAI client.

    Used when the real OpenAI API key is not available or the library is not installed.

    Attributes:
        api_key (str): The API key (real or mock).
        chat (MockChat): Chat interface for creating completions.
    """
    def __init__(self, api_key):
        """
        Initialize the mock OpenAI client.

        Args:
            api_key (str): The API key (real or mock).
        """
        self.api_key = api_key
        self.chat = MockChat()

class MockChat:
    """
    Mock implementation of the OpenAI chat interface.

    Attributes:
        completions (MockCompletions): Completions interface for creating responses.
    """
    def __init__(self):
        """
        Initialize the mock chat interface.
        """
        self.completions = MockCompletions()

class MockCompletions:
    """
    Mock implementation of the OpenAI completions interface.

    Provides a simplified version of the completion creation functionality
    that returns predefined responses based on keywords in the input.
    """
    def create(self, model, messages):
        """
        Create a mock completion based on the input messages.

        Args:
            model (str): The model name (ignored in mock implementation).
            messages (list): List of message dictionaries with 'role' and 'content' keys.

        Returns:
            MockResponse: A mock response object containing generated text.
        """
        # Simulate a response based on the input
        user_message = messages[-1]["content"] if messages else ""

        # Simple response generation based on keywords
        if "help" in user_message.lower():
            response_content = "I'm here to help! What would you like assistance with?"
        elif "system" in user_message.lower():
            response_content = "Here's some system information and assistance based on your query."
        elif "history" in user_message.lower():
            response_content = "Based on your terminal history, here are some suggestions."
        else:
            response_content = "I understand your request. Here's a helpful response based on the context provided."

        return MockResponse(response_content)

class MockResponse:
    """
    Mock response object that mimics the structure of OpenAI API responses.

    Attributes:
        choices (list): List of MockChoice objects.
    """
    def __init__(self, content):
        """
        Initialize a mock response with the given content.

        Args:
            content (str): The text content of the response.
        """
        self.choices = [MockChoice(content)]

class MockChoice:
    """
    Mock choice object that mimics the structure of OpenAI API response choices.

    Attributes:
        message (MockMessage): The message object containing the response content.
    """
    def __init__(self, content):
        """
        Initialize a mock choice with the given content.

        Args:
            content (str): The text content of the response.
        """
        self.message = MockMessage(content)

class MockMessage:
    """
    Mock message object that mimics the structure of OpenAI API response messages.

    Attributes:
        content (str): The text content of the message.
    """
    def __init__(self, content):
        """
        Initialize a mock message with the given content.

        Args:
            content (str): The text content of the message.
        """
        self.content = content

# Initialize the client (use mock if no API key)
if API_KEY:
    try:
        from openai import OpenAI
        client = OpenAI(api_key=API_KEY)
    except ImportError:
        print("Warning: OpenAI library not installed, using mock client")
        client = MockOpenAI(api_key=API_KEY)
else:
    print("Warning: OPENAI_API_KEY not set, using mock client")
    client = MockOpenAI(api_key="mock-key")

def query(prompt, history, system_info):
    """
    Query the GPT model with the given prompt, history, and system information.

    This function formats the input data into a structured prompt that includes
    recent terminal history and system information, then sends it to the OpenAI API
    (or mock implementation if the API is not available).

    Args:
        prompt (str): The user's question or prompt.
        history (list): List of recent terminal commands.
        system_info (str): Information about the user's system.

    Returns:
        str: The response text from GPT.
    """
    full_prompt = f"Terminal history: {', '.join(history[-10:])}\n\nSystem: {system_info}\n\nQuestion: {prompt}"
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": full_prompt}
    ]
    chat = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
    return chat.choices[0].message.content
