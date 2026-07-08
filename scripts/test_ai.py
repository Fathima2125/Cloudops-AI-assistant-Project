#!/usr/bin/env python3
"""
Experimental OpenAI smoke test for the CloudOps AI Assistant project.

This is optional and not required for the main portfolio workflow. It makes a
real API call and can fail if OPENAI_API_KEY is missing or the account has no
available quota.
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
