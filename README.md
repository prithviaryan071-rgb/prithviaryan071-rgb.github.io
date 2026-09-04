# Portfolio — Prithvi C Balaji

Static site. No build step, no dependencies. Everything is one HTML file plus assets.

```
index.html                        the whole site
Prithvi-C-Balaji-Resume.pdf       linked from the nav, the hero and the footer
assets/img/                       photos and slide images
assets/docs/                      the deck, the case study, the prototype, the guides
```

## Putting it live on GitHub Pages

Your site is the repo `prithviaryan071-rgb.github.io`.

1. Copy `index.html`, `Prithvi-C-Balaji-Resume.pdf` and the `assets` folder into the top level of that repo,
   replacing the existing `index.html`.
2. Commit and push to the default branch.
3. GitHub rebuilds in about a minute. Hard-refresh (Ctrl/Cmd + Shift + R) — the old page is usually cached.

If you prefer to do it in the browser: open the repo, **Add file → Upload files**, drag the whole lot in, commit.

## Before you publish — two things to check

**1. The deck.** `assets/docs/GIGA-CHAT-WhatsApp-support-automation-deck.pdf` is 18 of the original 22 slides. I removed
the four that carried real customer names and phone numbers from the ticketing system, and the ones showing the live bot
number and QR code. What's left still contains internal ticket volumes, so get a nod from your manager before it sits on
a public URL. If they say no, delete the file and the link to it in `index.html` (search for `support-automation-deck`) —
the slide images that stay tell the story anyway.

**2. The prototype.** `assets/docs/sales-intelligence-agent-prototype.py` had a live Google Sheet ID in it, which would
have given anyone read access to an internal sales tracker. That's now a placeholder, and the sample rows use invented
manager, dealer and customer names. Don't paste the original back in.

The terminal screenshot has the manager and dealer names covered for the same reason.

## Editing it

Text lives in plain HTML — search for the sentence you want to change and type over it. To swap a photo, drop the new
file into `assets/img/` and update both `src` and `data-full` on that `figure` (they point at the same image; `data-full`
is what the click-to-enlarge view uses).

Fonts (Lora and IBM Plex Sans) load from Google Fonts. If you'd rather not depend on that, delete the two `<link>` tags
in the head and the page falls back to Georgia and your system sans, which still looks fine.
