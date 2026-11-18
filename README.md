# code-feedback

A small command-line tool that sends a code file to an LLM (Claude) and prints
teaching-assistant style feedback: bugs, style, missing edge cases, and one
thing done well.

## Setup

```
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your-key-here      # Windows PowerShell: $env:ANTHROPIC_API_KEY="your-key-here"
```

## Usage

```
python feedback.py examples/buggy_average.py
python feedback.py examples/buggy_average.py --level beginner
```

## Tests

```
pytest -v
```

The tests use a fake client, so they run without an API key. GitHub Actions
runs them automatically on every push and pull request.
