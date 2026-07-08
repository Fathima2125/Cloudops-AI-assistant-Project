#!/usr/bin/env python3
"""
Simple OpenAI smoke test for the CloudOps AI Assistant project.

Run this script only when you want to make a real API call.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
from app.ai.openai_client import generate_ai_response


def main():
    """Send a simple test message to the AI model and print the response."""
    prompt = "You are a concise CloudOps assistant."
    input_text = "Say Hello CloudOps!"

    response = generate_ai_response(prompt, input_text)
    print(response)


if __name__ == "__main__":
    main()
