# Platforms — YouTube first, everything else after

## YouTube Live

### Do this today, before you need it

Enabling live streaming is not instant. Historically YouTube requires the channel to
be **phone-verified**, have **no live-streaming restrictions in the last 90 days**,
and then imposes a **waiting period (about 24 hours) before your first stream**.
Turn it on now so it's ready when you are. *Verify current requirements at
youtube.com/features — the gates change.*

Note also that streaming **from a phone** has historically required a subscriber
threshold that desktop/encoder streaming does not. We're streaming from OBS, so
this doesn't block us — but it's why "just go live from your phone" may not work.

### Connect OBS

1. YouTube Studio → **Create → Go live** → **Streaming software** tab.
2. Create the stream. Set **Title**, **Category**, thumbnail, and
   **Visibility: Unlisted** for tests / **Public** for real episodes.
3. Copy the **Stream key**.
4. OBS → **Settings → Stream** → Service **YouTube - RTMPS** → paste the key.

   Or use **Connect Account**, which lets you set the title and go live from inside
   OBS. Convenient; it also means OBS holds an account token, so only do it on a
   machine you control.

**Never show the stream key on screen.** It's a password. If it leaks, reset it in
YouTube Studio. This is one of the reasons the screen-hygiene checklist in
`SETUP.md` matters — the OBS settings window is a common accidental reveal.

### Settings to match

| Setting | Value |
|---|---|
| Resolution / FPS | 1920×1080 @ 30 |
| Bitrate | 6000 Kbps CBR (4500 if upload is tight) |
| Keyframe interval | 2s |
| Audio | AAC, 48 kHz, 128–160 Kbps stereo |
| Latency | **Normal** — gives the biggest buffer against network hiccups. Use Low latency only when live Q&A timing genuinely hurts. |
| DVR | On — lets late arrivals scrub back |

### After each stream

The archive becomes a normal video. Rename it properly, write a real description
with timestamps, and set a thumbnail — the archive out-earns the live audience over
time, usually by a lot. Chapters (timestamps in the description starting at `0:00`)
turn a 45-minute session into something people actually navigate.

## Adding a second platform

Don't, until four episodes have shipped clean. When you do:

### Option A — `obs-multi-rtmp` (free, from your laptop)
An OBS plugin that adds extra RTMP outputs. Each destination is a full copy of the
stream leaving your machine, so:
- Required upload = bitrate × number of destinations, plus headroom.
- Two destinations at 6000 Kbps wants ~20 Mbps of real, sustained upload.
- If upload is the constraint, drop to 4500 Kbps per destination rather than dropping
  a platform.

Install from the plugin's GitHub releases, matched to your OBS major version.

### Option B — cloud relay (Restream, Castr, and similar)
You push one stream to them; they fan it out. Upload cost stays flat no matter how
many destinations. Costs a subscription, and free tiers generally put their branding
on your stream. *Check current pricing and terms directly — they move.*

**Recommendation:** if you have wired ethernet and 25+ Mbps sustained upload, use the
plugin and keep the money. Otherwise pay for the relay.

### Per-platform gotchas

- **Twitch** — easiest addition, no gate. Different aspect/overlay conventions but
  our 1080p canvas is fine.
- **TikTok Live** — an RTMP key requires LIVE access on the account, historically
  gated behind a follower threshold. Also natively vertical; a 16:9 stream will letterbox.
  If TikTok matters, plan a separate vertical scene collection rather than fighting it.
- **Instagram** — no general third-party RTMP ingest. Treat IG as a place you post
  clips cut from the recording, not a live destination.
- **LinkedIn Live** — requires applying for access first.
- **X** — available, low effort, low return. Add it last.

## Repurposing (the part that compounds)

Every session already produces:
- a local MKV recording (higher quality than the platform archive),
- replay-buffer clips you saved with a hotkey during the stream,
- a YouTube archive with chapters.

That's the raw material for Shorts, Reels, and TikToks without a second filming
session. Cut vertical clips from the 60-second replay saves — you already flagged
the good moments live, which is the hard part.
