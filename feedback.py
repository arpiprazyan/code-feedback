"""Get AI feedback on a code file, like a teaching assistant would give.

Usage:
    python feedback.py examples/buggy_average.py
    python feedback.py my_code.py --level beginner
"""

import argparse
import os
import sys
from pathlib import Path

MODEL = "claude-haiku-5-5"  # small, fast and cheap model; fine for short feedback
MAX_TOKENS = 800

LANGUAGES = {
    ".py": "Python",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".java": "Java",
    ".c": "C",
    ".cpp": "C++",
    ".go": "Go",
}

SYSTEM_PROMPT = (
    "You are a teaching assistant for a university software engineering course. "
    "Give feedback that helps the student learn: point out bugs, readability "
    "problems and missing edge cases, and explain why they matter. "
    "Do not rewrite the whole program for them. Keep it short and use these "
    "sections: Bugs, Style, Edge cases, One thing done well."
)


def detect_language(path):
    """Guess the programming language from the file extension."""
    return LANGUAGES.get(Path(path).suffix.lower(), "unknown language")


def build_prompt(code, language, level):
    """Build the message we send to the model."""
    return (
        f"Student level: {level}\n"
        f"Language: {language}\n\n"
        f"Here is the student's code:\n\n{code}"
    )


def get_feedback(code, language="Python", level="intermediate", client=None):
    """Send the code to the LLM and return its feedback as a string.

    `client` can be passed in so tests can use a fake client instead of
    calling the real API.
    """
    if not code.strip():
        raise ValueError("The code file is empty.")

    if client is None:
        import anthropic  # imported here so tests don't need the package

        client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from the environment

    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": build_prompt(code, language, level)}],
    )
    return response.content[0].text


def main():
    parser = argparse.ArgumentParser(description="Get AI feedback on a code file.")
    parser.add_argument("file", help="path to the code file to review")
    parser.add_argument(
        "--level",
        choices=["beginner", "intermediate", "advanced"],
        default="intermediate",
        help="student level, which changes how detailed the explanations are",
    )
    args = parser.parse_args()

    path = Path(args.file)
    if not path.is_file():
        sys.exit(f"Error: file not found: {path}")

    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("Error: set the ANTHROPIC_API_KEY environment variable first.")

    code = path.read_text(encoding="utf-8")
    print(get_feedback(code, detect_language(path), args.level))


if __name__ == "__main__":
    main()
