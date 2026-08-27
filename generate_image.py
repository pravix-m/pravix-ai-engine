"""
Pravix Sphere — Image Generator
Takes the image_concept from latest_post.json and generates a branded
image using Gemini's image generation model. Saves as output/latest_image.png

Fails gracefully: if image generation isn't available (quota, deprecated
model name, etc.), the pipeline continues and posts text-only rather than
blocking the whole day's post.

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

# Try these in order -- first one that works, wins. Keeps this resilient
# to Google renaming/retiring image model versions over time.
CANDIDATE_MODELS = [
    "gemini-2.5-flash-image",
    "gemini-flash-latest",
    "gemini-2.0-flash-exp-image-generation",
]


def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("No GEMINI_API_KEY set -- skipping image, will post text-only.")
        return

    post_path = OUTPUT_DIR / "latest_post.json"
    if not post_path.exists():
        print("No post found -- skipping image step.")
        return

    with open(post_path) as f:
        post = json.load(f)

    concept = post.get("image_concept", "modern blue and green abstract gradient")
    full_prompt = (
        f"A clean, professional social media graphic. Style: {concept}. "
        f"Brand colors: deep blue (#1E3A8A), green accent (#22C55E). "
        f"No text or words in the image. Modern, minimal, high quality."
    )

    genai.configure(api_key=api_key)

    for model_name in CANDIDATE_MODELS:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(full_prompt)
            for part in response.candidates[0].content.parts:
                if hasattr(part, "inline_data") and part.inline_data:
                    img_path = OUTPUT_DIR / "latest_image.png"
                    with open(img_path, "wb") as f:
                        f.write(part.inline_data.data)
                    print(f"Image saved using {model_name} -> {img_path}")
                    return
        except Exception as e:
            print(f"Model {model_name} failed ({e}); trying next option.")
            continue

    print("WARNING: no image model succeeded. Continuing without an image "
          "-- the post will still go out as text-only.")


if __name__ == "__main__":
    main()
