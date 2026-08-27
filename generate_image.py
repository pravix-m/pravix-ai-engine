"""
Pravix Sphere — Image Generator
Takes the image_concept from latest_post.json and generates a branded
image using Gemini's image generation model. Saves as output/latest_image.png

Required environment variable:
  GEMINI_API_KEY
"""

import json
import os
import sys
from pathlib import Path

import google.generativeai as genai

ROOT = Path(__file__).parent
OUTPUT_DIR = ROOT / "output"


def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY not set.", file=sys.stderr)
        sys.exit(1)

    post_path = OUTPUT_DIR / "latest_post.json"
    if not post_path.exists():
        print("ERROR: run generate_post.py first.", file=sys.stderr)
        sys.exit(1)

    with open(post_path) as f:
        post = json.load(f)

    concept = post.get("image_concept", "modern blue and green abstract gradient")

    genai.configure(api_key=api_key)

    # TEMP DIAGNOSTIC: list available models so we can pick the right one
    available = [m.name for m in genai.list_models() if "image" in m.name.lower() or "generateContent" in getattr(m, "supported_generation_methods", [])]
    raise RuntimeError("MODEL_LIST: " + " | ".join(available))

    model = genai.GenerativeModel("gemini-2.0-flash-exp-image-generation")

    full_prompt = (
        f"A clean, professional social media graphic. Style: {concept}. "
        f"Brand colors: deep blue (#1E3A8A), green accent (#22C55E). "
        f"No text or words in the image. Modern, minimal, high quality."
    )

    response = model.generate_content(full_prompt)

    image_saved = False
    for part in response.candidates[0].content.parts:
        if hasattr(part, "inline_data") and part.inline_data:
            img_path = OUTPUT_DIR / "latest_image.png"
            with open(img_path, "wb") as f:
                f.write(part.inline_data.data)
            print(f"Image saved to {img_path}")
            image_saved = True
            break

    if not image_saved:
        print("WARNING: no image returned by model. Posting step should "
              "fall back to a template/logo graphic.", file=sys.stderr)


if __name__ == "__main__":
    main()
