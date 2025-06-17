#!/usr/bin/env python3
"""Simple message helper - replaces 22 bloated scripts"""
import sys
from datetime import datetime

def add_message(agent_name, message):
    """Add message to log
    # @codebase-summary: feature="message_system" purpose="Agent message logging"
    # @codebase-summary: description="Appends timestamped messages from agents to msgs.md file for inter-agent communication tracking"
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    import os
    msgs_path = os.path.join(os.path.dirname(__file__), "msgs.md")
    with open(msgs_path, "a") as f:
        f.write(f"\n[{timestamp}] {agent_name}: {message}")

def read_messages(lines=10):
    """Read last N messages
    # @codebase-summary: feature="message_system" purpose="Message retrieval system"
    # @codebase-summary: description="Retrieves the last N messages from msgs.md file, filtering for timestamped agent messages"
    """
    try:
        import os
        msgs_path = os.path.join(os.path.dirname(__file__), "msgs.md")
        with open(msgs_path, "r") as f:
            all_lines = f.readlines()
            # Find message lines (start with [)
            msg_lines = [l.strip() for l in all_lines if l.strip().startswith('[')]
            return msg_lines[-lines:] if len(msg_lines) > lines else msg_lines
    except FileNotFoundError:
        return []

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 msg.py list [lines]        # List recent messages")
        print("  python3 msg.py read [lines]        # Same as list")
        print("  python3 msg.py latest              # Show latest message")
        print("  python3 msg.py add agent 'message' # Add new message")
    elif sys.argv[1] in ["read", "list"]:
        lines = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        messages = read_messages(lines)
        if messages:
            for msg in messages:
                print(msg)
        else:
            print("No messages found")
    elif sys.argv[1] == "latest":
        messages = read_messages(1)
        if messages:
            print(messages[0])
        else:
            print("No messages found")
    elif sys.argv[1] == "add" and len(sys.argv) >= 4:
        add_message(sys.argv[2], " ".join(sys.argv[3:]))
        print(f"Message added from {sys.argv[2]}")
    else:
        print("Invalid command. Use 'list', 'latest', or 'add'.")