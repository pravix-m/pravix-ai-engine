"""
Pravix Sphere — Posting Step
Takes output/latest_post.json + output/latest_image.png and pushes them
to LinkedIn + Instagram via Zernio.

>>> ACTION NEEDED FROM YOU <<<
This file intentionally does NOT hardcode Zernio's API calls, because
I don't have the exact integration code from your Hasun pipeline in
front of me (it lives in that private repo). To connect this:

  1. Open your Hasun pipeline repo, find the script that calls Zernio
     to post to LinkedIn/Instagram.
  2. Copy that function in below, in `post_via_zernio()`.
  3. Set ZERNIO_API_KEY (and any other secret it needs) as a GitHub
     Actions secret in THIS repo, same as you did for Hasun.

Everything else (config toggle, dry-run safety, logging) is ready to go.
"""

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).parent
OUTPUT_DIR = ROOT / "output"


def load_config():
    with open(ROOT / "config.json") as f:
        return json.load(f)


def load_post():
    with open(OUTPUT_DIR / "latest_post.json") as f:
        return json.load(f)


def post_via_zernio(platform: str, text: str, image_path: Path):
    """
    PLACEHOLDER — paste your working Zernio call from the Hasun pipeline
    here. Keep the same function signature so the rest of the script
    doesn't need to change.

    Example shape (replace with your real one):

        import requests
        resp = requests.post(
            "https://api.zernio.com/v1/posts",
            headers={"Authorization": f"Bearer {os.environ['ZERNIO_API_KEY']}"},
            json={"platform": platform, "text": text, "image_path": str(image_path)},
        )
        resp.raise_for_status()
        return resp.json()
    """
    raise NotImplementedError(
        "post_via_zernio() is a placeholder — paste your Hasun Zernio "
        "integration code here before enabling live posting."
    )


def main():
    cfg = load_config()

    if not cfg["posting"].get("enabled", False):
        print("Posting is disabled in config.json (posting.enabled = false). "
              "Flip it to true once you've connected Zernio and reviewed a "
              "few dry runs. Exiting safely without posting.")
        return

    post = load_post()
    image_path = OUTPUT_DIR / "latest_image.png"

    for platform in cfg["posting"]["platforms"]:
        text_key = f"{platform}_text"
        text = post.get(text_key, post.get("linkedin_text", ""))
        print(f"Posting to {platform}...")
        result = post_via_zernio(platform, text, image_path)
        print(f"  -> {platform} result: {result}")


if __name__ == "__main__":
    main()
