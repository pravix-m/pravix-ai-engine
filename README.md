# Pravix Sphere — AI Content Engine

Fully built and ready. This does the daily thinking, writing, image-making,
and (once connected) posting — automatically, every day, forever, with no
manual work from you after setup.

## What's already done for you

- ✅ Content generator (`generate_post.py`) — writes LinkedIn + Instagram
  captions in Pravix's brand voice, picks a fresh topic daily
- ✅ Image generator (`generate_image.py`) — makes a branded graphic to go
  with each post
- ✅ Posting script (`post_to_socials.py`) — safe by default (won't post
  until you flip `posting.enabled` to `true` in `config.json`)
- ✅ Daily automation (`.github/workflows/daily-post.yml`) — runs itself
  every day at 2:30 PM IST, no one needs to click anything
- ✅ Mobile dashboard (`docs/index.html`) — open this on your phone anytime
  to see the latest post and whether the engine is live

## The ONLY things that require you (one-time, ~15 minutes)

These steps legally/technically require a human — no AI can do them for you:

1. **Create this as a real GitHub repo**
   Push these files to a new (private) GitHub repo, e.g. `pravix-ai-engine`.

2. **Get a free Gemini API key**
   → https://aistudio.google.com/apikey (free tier is enough to start)
   Add it in your repo: Settings → Secrets and variables → Actions →
   New repository secret → name it `GEMINI_API_KEY`.

3. **Connect Zernio the same way you did for Hasun**
   Open your Hasun repo, find the function that calls Zernio to post to
   LinkedIn/Instagram, and paste it into `post_via_zernio()` in
   `post_to_socials.py` here. Add `ZERNIO_API_KEY` as a secret the same way.

4. **Create Pravix's LinkedIn Page + Instagram Business account**
   (if not already done) and link them inside Zernio, same flow as Hasun.

5. **Turn on GitHub Pages**
   Repo Settings → Pages → Deploy from branch → `main` → `/docs` folder.
   Your dashboard will then be live at:
   `https://<your-github-username>.github.io/pravix-ai-engine/`
   Save that link to your phone home screen — that's your Control Room.

6. **Flip the switch**
   Once you've reviewed a couple of test runs, open `config.json` and
   set `"posting": { "enabled": true }`. From that moment, it posts on
   its own, daily, with zero further input from you.

## Everything after step 6

Nothing. It runs itself. To change what it talks about, edit the
`content_topics` list in `config.json` — no code needed.

## Optional: Google Sheet control panel

If you'd rather edit topics/settings from a phone-friendly Google Sheet
instead of editing `config.json` directly, tell Claude and it'll build the
sheet + the small script that syncs it into this repo automatically.
