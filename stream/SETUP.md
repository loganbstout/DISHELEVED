# Setup — Install to first stream

Do this in order. Budget ~90 minutes the first time.

---

## 1. Install OBS Studio

Download from **https://obsproject.com** — the official site, not a mirror.

- **macOS:** grab the build that matches your chip (Apple Silicon vs Intel).
  On first launch macOS will ask for **Screen Recording**, **Camera**, and
  **Microphone** permission. Grant all three in System Settings → Privacy &
  Security, then **quit and reopen OBS** — permissions do not apply to a running app.
- **Windows:** run the installer. If SmartScreen warns, verify you're on
  obsproject.com and continue.

Skip the auto-configuration wizard, or run it and then override with the settings
in step 4 — we're setting these deliberately.

## 2. Get the overlay files onto the streaming machine

Clone this repo (or download it as a ZIP and unpack it) on the laptop you stream from.
Note the absolute path to `stream/overlays` — you need it in the next step.

```bash
git clone https://github.com/loganbstout/DISHELEVED.git
cd DISHELEVED/stream/overlays && pwd     # copy this path
```

Sanity check: open `starting-soon.html` in a browser. You should see the countdown
running against a black field with a scrolling ticker. If it looks unstyled, the
files got separated from `_brand.css` — keep the folder intact.

## 3. Import the scene collection

`obs/` ships two collections because OBS capture-device IDs differ by OS.

1. Open `obs/disheveled-scenes.macos.json` **or** `disheveled-scenes.windows.json`
   in any text editor.
2. Find/replace every `__OVERLAYS__` with your absolute overlays path from step 2.
   - macOS example: `/Users/logan/DISHELEVED/stream/overlays`
   - Windows example: `C:/Users/logan/DISHELEVED/stream/overlays`
     (**forward slashes**, and no `file://` prefix — the file already has one.)
3. Save.
4. In OBS: **Scene Collection → Import →** pick the file → **Import** → then
   **Scene Collection →** select *Disheveled Live*.

Prefer to regenerate cleanly instead of find/replace:

```bash
python3 stream/obs/build-scenes.py --os macos --overlays "/Users/logan/DISHELEVED/stream/overlays"
```

> Heads-up: these collections are generated to the OBS scene-collection schema and
> are valid JSON, but they were not import-tested against a running OBS — no OBS in
> the environment they were built in. If the import misbehaves on your version,
> build the scenes by hand from the table in step 5; it takes about 20 minutes and
> the result is identical.

**Devices are intentionally blank.** OBS cannot know your hardware. After importing,
double-click each of these and pick the real device:

- `CAM — Main` → your webcam
- `SCR — Display` → the monitor you'll teach from
- `AUD — Mic` → your microphone
- `AUD — Desktop` (Windows) → your speakers/output device

## 4. Settings that matter

**Settings → Video**
- Base (Canvas) Resolution: **1920×1080** — the overlays are built for this canvas.
- Output (Scaled) Resolution: **1920×1080**
- FPS: **30** (60 only if you're on a fast machine and the content moves; teaching content does not)

**Settings → Output → Output Mode: Advanced → Streaming**
- Encoder: **Apple VT H.264 Hardware** (Apple Silicon) / **NVIDIA NVENC H.264** (NVIDIA GPU) / **x264** with preset `veryfast` otherwise.
- Rate Control: **CBR**
- Bitrate: **6000 Kbps** for 1080p30. Drop to 4500 if your upload is under ~12 Mbps.
- Keyframe Interval: **2** seconds. Not 0, not 5 — YouTube rejects long intervals.
- Profile: `high`

**Settings → Output → Recording**
- Recording Path: somewhere with room. A 45-minute session is several GB.
- Recording Format: **MKV** (survives a crash; MP4 does not), then use
  **File → Remux Recordings** afterward to get an MP4 for editing.
- Check **Settings → General → "Automatically record when streaming."**
  The local recording is higher quality than the platform archive and is what you
  cut Shorts from.

**Settings → Audio**
- Sample Rate: **48 kHz**
- Channels: **Stereo**

**Settings → Output → Replay Buffer**
- Enable it, 60 seconds. Bind a hotkey (below). Every time something lands well on
  stream, hit it — that's your clip, no editing session required.

**Settings → Hotkeys** — set these and only these to start:

| Action | Suggested key |
|---|---|
| Switch to `01 — CAMERA` | F1 |
| Switch to `02 — LAPTOP` | F2 |
| Switch to `03 — SITE DEMO` | F3 |
| Switch to `05 — BRB` | F4 |
| Mute/Unmute `AUD — Mic` (push-to-mute) | F8 |
| Save Replay | F9 |

Bandwidth check before you trust any of this: run a speed test and confirm
**upload** is at least 1.5× your chosen bitrate, sustained. 6000 Kbps stream wants
~10 Mbps of real upload headroom.

## 5. The scenes (and how to rebuild them by hand)

| Scene | Contents | Use it for |
|---|---|---|
| `00 — STANDBY` | Starting Soon overlay | The 5–10 min before you talk. Countdown runs. |
| `01 — CAMERA` | Camera full-frame + bug + lower third | Open, close, and anything you say to the audience directly. |
| `02 — LAPTOP` | Display capture + camera PIP bottom-right + bug | The teaching scene. Most of the show. |
| `03 — SITE DEMO` | Browser source on the live site + camera PIP + bug | Showing the drop site without exposing your desktop. |
| `04 — SPLIT` | Screen left, camera right | Discussion where your face matters as much as the screen. |
| `05 — BRB` | BRB overlay | Refill, interruption, technical problem. |
| `06 — OUTRO` | Ending overlay | Last 60 seconds. Let it run before you hit Stop. |

To build a browser source by hand: **+ → Browser →** name it → check **Local file**
→ browse to the overlay → set **Width 1920, Height 1080** → check
**Shutdown source when not visible** and **Refresh browser when scene becomes active**
(that last one is what restarts the countdown each time you return to standby).

## 6. Audio routing

This is the part people get wrong, so read it even if you think you're fine.

**Windows** — desktop audio works natively. Add a `Desktop Audio` source
(WASAPI Output Capture) and you'll capture anything the laptop plays.

**macOS** — the OS does not hand app audio to OBS by default. Two options:

1. **Native (try this first).** Recent OBS versions on macOS 13+ include a
   **macOS Audio Capture** source built on ScreenCaptureKit. Add it, grant the
   permission prompt, pick "all desktop audio" or a specific app.
2. **BlackHole** (https://existential.audio/blackhole) — a free virtual audio
   device. Install the 2ch version, then in Audio MIDI Setup create a
   **Multi-Output Device** containing both your real output and BlackHole (so you
   still hear things), set it as the system output, and add BlackHole as an
   Audio Input Capture source in OBS. Use this if the native source isn't in your
   OBS version or misbehaves.

**Levels, both platforms:** talk normally and watch the mixer. Peaks should sit
around **-12 dB**, never touching 0. Then on the mic source add filters, in order:

1. **Noise Suppression** (RNNoise) — kills room hiss and fan noise.
2. **Noise Gate** — close threshold about -45 dB, open about -35 dB. Stops your
   keyboard and your breathing between sentences.
3. **Compressor** — ratio 4:1, threshold about -18 dB. Evens out leaning in and away.
4. **Limiter** — -3 dB. Insurance against a laugh or a cough blowing the stream out.

Desktop audio should sit clearly below your voice. If you play anything with music
in it, duck it — and be aware that copyrighted music will get the YouTube archive
muted or claimed even if the live stream runs fine.

## 7. Before you go live — screen hygiene

You are broadcasting your laptop. Treat the screen as public.

- **Notifications off.** macOS: Focus / Do Not Disturb. Windows: Focus Assist /
  "Do not disturb". Every unmuted message app is a live leak.
- **A clean browser profile** for streaming — no personal bookmarks bar, no
  autofill, no logged-in accounts you don't want on camera.
- **Close the password manager.** Close anything with tokens, API keys, `.env`
  files, or customer data. Assume every frame gets screenshotted, because on a good
  stream it does.
- **Make it readable.** Browser zoom **125–150%**. Terminal font **16–18pt**.
  Editor font bumped up. What's comfortable on your laptop is unreadable at 1080p
  on someone's phone. Check the OBS preview, not your screen.
- **Tidy the desktop and the dock/taskbar.** Rename the window you're about to share.
- **Capture one display, not both.** If you have a second monitor, keep OBS, chat,
  and your notes on the uncaptured one.

## 8. Test stream

Set the YouTube stream to **Unlisted** (see `PLATFORMS.md`), go live for 15 minutes,
talk, switch every scene, share the screen, then stop and **watch the archive back
with headphones**. You are checking exactly four things:

1. Is your voice clear and louder than everything else?
2. Is the smallest text on screen readable?
3. Did the stream hold bitrate the whole time? (OBS status bar: no dropped frames)
4. Do the overlays look right — countdown, lower third, ticker?

Fix what's broken. Then Phase 1.
