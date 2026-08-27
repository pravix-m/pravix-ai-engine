"""
Pravix Sphere — Daily Content Generator
Generates a caption + image for LinkedIn/Instagram using the Gemini API,
picks a topic from config.json, and writes output to /output for the
posting step to pick up.

Required environment variable:
  GEMINI_API_KEY   (set as a GitHub Actions secret)

Usage:
  python generate_post.py
"""

import json
import os
import random
import sys
from datetime import datetime, timezone
from pathlib import Path

import google.generativeai as genai

ROOT = Path(__file__).parent
OUTPUT_DIR = ROOT / "output"
OUTPUT_DIR.mkdir(exist_ok=True)


def load_config():
    with open(ROOT / "config.json") as f:
        return json.load(f)


def build_prompt(cfg):
    brand = cfg["brand"]
    topic = random.choice(cfg["content_topics"])
    style_notes = "; ".join(cfg["post_style_notes"])

    prompt = f"""
You are writing a social media post for {brand['name']} ({brand['handle']}),
tagline: "{brand['tagline']}". Positioning: {brand['positioning']}.
Audience: {brand['audience']}. Tone: {brand['tone']}.

Topic: {topic}

Style rules: {style_notes}

Write:
1. A LinkedIn version (3-5 short paragraphs, professional but warm)
2. An Instagram version (shorter, punchier, same core message)
3. A one-line image concept description (for generating a simple branded
   graphic — describe mood/colors/style only, no text overlay needed)

Return ONLY valid JSON with keys: linkedin_text, instagram_text, image_concept
"""
    return prompt, topic


def generate(cfg):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY not set in environment.", file=sys.stderr)
        sys.exit(1)

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-3.6-flash")

    prompt, topic = build_prompt(cfg)
    response = model.generate_content(prompt)

    raw = response.text.strip()
    # Strip markdown code fences if Gemini wraps the JSON
    if raw.startswith("```"):
        raw = raw.strip("`")
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        print("WARNING: model did not return clean JSON, saving raw text.")
        data = {
            "linkedin_text": raw,
            "instagram_text": raw,
            "image_concept": "abstract blue and green gradient, modern, minimal",
        }

    data["topic"] = topic
    data["generated_at"] = datetime.now(timezone.utc).isoformat()
    return data


def main():
    cfg = load_config()
    post = generate(cfg)

    out_path = OUTPUT_DIR / "latest_post.json"
    with open(out_path, "w") as f:
        json.dump(post, f, indent=2)

    print(f"Generated post saved to {out_path}")
    print(json.dumps(post, indent=2))


if __name__ == "__main__":
    main()
