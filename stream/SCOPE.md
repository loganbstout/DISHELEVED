# Streaming Scope — Disheveled Studio

What we're building, in what order, and what each step costs. Read this once;
then work from `SETUP.md` and `RUN-OF-SHOW.md`.

## What the stream is for

Three jobs, in priority order:

1. **Teach the build.** "Sip & Teach" — screen-share the laptop, walk through how
   the site, the drop mechanics, and the tooling actually work.
2. **Showcase the product.** Live walkthroughs of the Drop 001 site, the collection,
   the pieces. Live sessions on drop day.
3. **Field questions in public.** Chat is the support channel. Answering one person
   on stream answers a hundred later.

Everything below is chosen to serve #1 first, because a screen walkthrough is the
hardest one to make legible and the easiest one to do badly.

## The stack

| Layer | Choice | Why |
|---|---|---|
| Capture / mixing | **OBS Studio** | Free, cross-platform, does everything below. No credible reason to pay for an alternative at this stage. |
| Overlays | **Local HTML browser sources** (in `overlays/`) | Same design tokens as `index.html`, so the stream and the site read as one brand. Editable in a text editor, no subscription, no third-party account. |
| Primary platform | **YouTube Live** | Best archive, best search, best embed, no follower gate to start. |
| Second platform | **Deferred** — see Phase 2 | Multistreaming before you have one platform working is how streams die. |
| Clips | **OBS Replay Buffer** | One hotkey saves the last 60s. Feeds Shorts / TikTok / Reels from a session you were doing anyway. |

## Phases

### Phase 0 — Prove the pipe (do this first, ~90 min)
Install OBS, import the scene collection, connect YouTube, run one **unlisted**
15-minute test stream to nobody. Watch the archive back. Fix the audio.

Done when: you can watch a recording of yourself where the terminal text is
readable and your voice is louder than your keyboard.

### Phase 1 — Sip & Teach, live (weeks 1–4)
Public, weekly, same day and time. One topic per episode. 30–45 minutes.
Scenes: standby → camera → laptop walkthrough → Q&A → outro.

Done when: four episodes shipped without a technical stop.

### Phase 2 — Multistream + repurpose
Add a second destination only once Phase 1 is boring. Two routes, pick one:

- **`obs-multi-rtmp` plugin** — free, streams from your laptop to N destinations.
  Costs upload bandwidth (N × bitrate) and a little CPU. Right answer if your
  upload is fast and stable.
- **Restream / Castr (cloud relay)** — you send one stream up, they fan it out.
  Costs a monthly fee; free tiers generally brand the stream. Right answer if
  your upload is tight or flaky. *Check current pricing and free-tier terms before
  committing — they change.*

Platform reality check before you plan around any of these:

| Platform | Gate to know about |
|---|---|
| YouTube | Phone-verify the channel, then there is a waiting period (historically ~24h) before the first desktop stream. **Do this today**, not on stream day. |
| Twitch | Open to anyone. Easiest second destination. |
| TikTok Live | Needs LIVE access on the account (historically a follower threshold) before you get an RTMP key. |
| Instagram | No general-purpose RTMP for third-party encoders. Plan on native mobile, or don't plan on it. |
| LinkedIn Live | Requires applying for access. |
| X | Available, but treat as a bonus destination. |

*Verify each of these at the source when you get there — the gates move.*

### Phase 3 — Polish
Stream Deck or an OBS hotkey sheet, on-screen chat, guest calls, a drop-day
live-commerce format with the countdown overlay pointed at the real drop time.

## Gear

You have the laptop. In order of how much each dollar improves the stream:

1. **Wired ethernet** (adapter if the laptop has no port) — removes the single most
   common cause of a dropped stream. Cheap.
2. **A real microphone** — a USB condenser or dynamic mic on a stand. Audio is the
   whole thing; viewers forgive ugly video and leave over bad audio.
3. **One light** in front of you, off to one side. A window works if you always
   stream at the same hour.
4. **A second monitor** — lets you keep OBS, chat, and notes off the captured screen.
   Genuinely changes how relaxed the stream feels.
5. Camera: the built-in one is fine. Upgrade last.

## What we are explicitly not doing yet

- No paid streaming software.
- No green screen / background removal — it fails live and eats CPU you need for encoding.
- No custom stream bot or chat integrations.
- No multistream until Phase 2.
