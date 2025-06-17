import os
import subprocess
import re

"""
Utility functions for davidgnome.

This module provides helper functions for retrieving terminal history
and system information to provide context for AI queries.
"""

def get_terminal_history():
    """
    Retrieve the user's terminal command history.

    Reads the bash history file (~/.bash_history) and returns its contents
    as a list of command strings. If the history file doesn't exist,
    returns an empty list.

    Returns:
        list: A list of recent terminal commands, or an empty list if the history file is not found.
    """
    history_file = os.path.expanduser("~/.bash_history")  # or fish/zsh
    if os.path.exists(history_file):
        with open(history_file) as f:
            return f.read().splitlines()
    return []

def get_system_info():
    """
    Retrieve information about the user's system.

    Runs the 'neofetch' command to get detailed system information,
    including OS, kernel version, CPU, memory, etc. Removes ANSI escape
    codes from the output for clean text.

    Returns:
        str: A string containing system information, or an error message if neofetch fails.
    """
    try:
        output = subprocess.check_output(["neofetch", "--stdout"], text=True)
        return re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', output)
    except:
        return "System info unavailable"
