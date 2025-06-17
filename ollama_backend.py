import requests
from prompts import SYSTEM_PROMPT_OLLAMA
"""
Ollama backend module for davidgnome.

This module provides functionality to interact with a locally running Ollama API server.
It sends queries to the Ollama API and returns the responses.
"""

def query(prompt, history, system_info, model="linux_gnome"):
    """
    Query the Ollama API with the given prompt, history, and system information.

    This function formats the input data into a structured prompt that includes
    recent terminal history and system information, then sends it to a locally
    running Ollama API server.

    Args:
        prompt (str): The user's question or prompt.
        history (list): List of recent terminal commands.
        system_info (str): Information about the user's system.
        model (str, optional): The name of the Ollama model to use. Defaults to "linux_gnome".

    Returns:
        str: The response text from the Ollama model.

    Raises:
        RuntimeError: If the API request fails.
    """
    full_prompt = f"Terminal history: {', '.join(history[-10:])}\n\nSystem: {system_info}\n\nQuestion: {prompt}"
    res = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": model,
            "messages": [{"role": "system", "content": SYSTEM_PROMPT_OLLAMA},
                         {"role": "user", "content": full_prompt}],
            "stream": False
        }
    )
    if res.ok:
        return res.json()['message']['content']
    else:
        raise RuntimeError(f"Ollama error: {res.status_code} - {res.text}")
