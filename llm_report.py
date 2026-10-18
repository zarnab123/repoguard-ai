import json
import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv()


def generate_ai_report(audit_report: dict) -> str:
    """Turn evidence from the audit engine into a useful AI report."""
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY is missing. Add it to your .env file.")

    prompt = f"""
You are RepoGuard AI, a helpful software engineering reviewer.

Use ONLY the audit data below. Do not invent facts.
Write a concise Markdown report with these headings:

## Overall assessment
## Top priorities
## Suggested next actions

For each priority, explain why it matters in simple, professional language.
Focus on practical improvements a developer can make.

AUDIT DATA:
{json.dumps(audit_report, indent=2)}
"""

    client = Groq(api_key=api_key)

    completion = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": "You give precise, evidence-based repository reviews.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
        max_completion_tokens=700,
    )

    return completion.choices[0].message.content or "No AI report was generated."