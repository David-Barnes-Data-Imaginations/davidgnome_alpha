import json
import sys
from pathlib import Path

"""
Configuration module for davidgnome.

This module handles reading and writing configuration settings for the davidgnome
application, particularly which AI backend to use (gpt, claude, or ollama).
Configuration is stored in a JSON file at ~/.config/davidgnome/config.json.
"""

# Fix: Use the correct path - either project directory or user config directory
CONFIG_PATH = Path(__file__).parent / "config.json"  # For project directory
# OR if you want user config directory:
# CONFIG_PATH = Path.home() / ".config/davidgnome/config.json"

def get_backend():
    """
    Get the currently configured AI backend.

    Reads the configuration file and returns the name of the configured backend.
    If the configuration file doesn't exist or doesn't specify a backend,
    defaults to "ollama".

    Returns:
        str: The name of the backend ("gpt", "claude", "ollama", etc.)
    """
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH) as f:
           return json.load(f).get("backend", "ollama")
    return "ollama"

def set_backend(name):
    """
    Set the AI backend to use.

    Updates the configuration file with the specified backend name.
    Creates the configuration directory and file if they don't exist.

    Args:
        name (str): The name of the backend to use ("gpt", "claude", "ollama", etc.)
    """
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump({"backend": name}, f)

# Handle command line usage
if __name__ == "__main__":
    if len(sys.argv) > 1:
        set_backend(sys.argv[1])