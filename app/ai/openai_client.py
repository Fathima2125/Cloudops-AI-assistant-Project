"""
Experimental OpenAI API helper for the CloudOps AI Assistant project.

This module is optional and is not part of the main working demo. The current
project workflow uses Codex, local prompts, the CLI helper, and the AWS
Documentation MCP Server. Use this file only for future API-backed experiments
when an OpenAI API key and quota are available.
"""

import os
from pathlib import Path

from openai import OpenAI


PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_FILE = PROJECT_ROOT / ".env"
DEFAULT_MODEL = "gpt-4o-mini"


def load_env_file(env_path=ENV_FILE):
    """
    Load key=value pairs from a local .env file into environment variables.

    This is intentionally small and beginner-friendly. It supports simple lines
    like OPENAI_API_KEY=your_key_here and ignores comments or blank lines.
    Existing environment variables are not overwritten.
    """
    if not env_path.exists():
        return

    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()

        # Skip blank lines and comments.
        if not line or line.startswith("#"):
            continue

        # Skip malformed lines instead of failing the whole script.
        if "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")

        if key and key not in os.environ:
            os.environ[key] = value


def create_openai_client():
    """
    Load the API key and return an initialized OpenAI client.

    Raises:
        RuntimeError: If OPENAI_API_KEY is missing after loading .env.
    """
    load_env_file()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is missing. Add it to .env or export it in your shell."
        )

    return OpenAI(api_key=api_key)


def generate_ai_response(prompt, input_text, model=None):
    """
    Send a prompt and input text to OpenAI and return the response text.

    Args:
        prompt: The instruction or reusable prompt template.
        input_text: The file content, log text, Terraform code, or AWS question.
        model: Optional model override. If not provided, OPENAI_MODEL from .env is
            used, then DEFAULT_MODEL as a fallback.

    Returns:
        The generated AI response as plain text.
    """
    client = create_openai_client()
    selected_model = model or os.getenv("OPENAI_MODEL", DEFAULT_MODEL)

    response = client.responses.create(
        model=selected_model,
        input=[
            {
                "role": "system",
                "content": prompt,
            },
            {
                "role": "user",
                "content": input_text,
            },
        ],
    )

    return response.output_text
