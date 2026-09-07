# Disheveled Studio — Streaming Kit

Everything needed to install OBS, run a **Sip & Teach** session, walk viewers
through the laptop, and stream to YouTube (plus whatever comes after).

Overlays are built from the same design tokens as `index.html` — the same black,
the same cream, the same `#c8ff00`, Bebas Neue and Space Mono — so the stream and
the drop site read as one brand.

## Read in this order

| Doc | What's in it |
|---|---|
| **[SCOPE.md](SCOPE.md)** | What we're building and in what phases. Stack decisions, gear priorities, platform gates. Start here. |
| **[SETUP.md](SETUP.md)** | Install OBS → import scenes → encoder settings → audio routing → screen hygiene → test stream. |
| **[PLATFORMS.md](PLATFORMS.md)** | YouTube setup end to end, then multistreaming options and per-platform gotchas. |
| **[RUN-OF-SHOW.md](RUN-OF-SHOW.md)** | The 45-minute episode format, pre-flight checklist, overlay text reference, failure playbook. |

## What's here

```
stream/
├── overlays/              browser sources — open any in a browser to preview
│   ├── starting-soon.html   countdown + ticker standby screen
│   ├── brb.html             be-right-back card
│   ├── ending.html          outro with next-session / drop / socials
│   ├── lower-third.html     name + role strap (transparent, auto-hides)
│   ├── bug.html             corner wordmark, LIVE pill, "now covering" strap
│   ├── _brand.css           shared tokens — keep this next to the HTML files
│   └── _ticker.js           shared marquee builder
└── obs/
    ├── disheveled-scenes.macos.json     importable scene collection
    ├── disheveled-scenes.windows.json   ditto, Windows capture IDs
    └── build-scenes.py                  regenerates either, with real paths baked in
```

All overlay copy is set with URL parameters on the OBS browser source — no file
editing to change an episode title. Full parameter list in
[RUN-OF-SHOW.md](RUN-OF-SHOW.md#overlay-text--where-to-change-what).

## Fastest path to a first stream

1. Turn on YouTube live streaming **today** — there's a waiting period before the
   first stream (see [PLATFORMS.md](PLATFORMS.md)).
2. Install OBS from https://obsproject.com and grant camera / mic / screen-recording
   permission, then restart it.
3. Find/replace `__OVERLAYS__` in the scene collection with your absolute path to
   `stream/overlays`, then **Scene Collection → Import**.
4. Pick your camera, mic, and display in the imported sources.
5. Set 1080p30, CBR 6000 Kbps, keyframe 2s.
6. Run a 15-minute **unlisted** test and watch it back with headphones.

Details and the reasoning for each of these are in [SETUP.md](SETUP.md).

## Preview an overlay without OBS

Open the file in any browser — they're standalone pages. Append parameters to try
copy changes:

```
overlays/starting-soon.html?mins=3&title=Sip%20%26%20Teach%20002&tagline=Building%20the%20drop%20page
overlays/lower-third.html?name=LOGAN%20STOUT&role=Founder&hold=8
overlays/bug.html?topic=Drop%20001%20%E2%80%94%20Behind%20the%20jacket
```

The transparent overlays (`lower-third`, `bug`) will look like floating panels on a
white page — that's correct. OBS composites them over the camera or screen.
