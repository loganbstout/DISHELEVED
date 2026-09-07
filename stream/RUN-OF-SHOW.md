# Run of Show — Sip & Teach

A repeatable 45-minute episode. Same shape every week, so the format stops being a
decision and you can spend your attention on the teaching.

## The night before (10 min)

- Pick **one** topic. One. "How the drop page hides the drop date" beats "the site."
- Write three bullets you must land, on paper, off-screen.
- Open every tab, file, and terminal you'll need. Close everything else.
- Create the YouTube stream, set title/thumbnail/visibility.

## T-30 — Setup

- [ ] Wired ethernet plugged in; speed test shows enough sustained upload
- [ ] OBS open, correct scene collection (*Disheveled Live*) loaded
- [ ] Camera and mic devices selected and showing in the mixer
- [ ] Mic peaks around -12 dB when you talk normally
- [ ] Desktop audio audible in the mixer, sitting below your voice
- [ ] Do Not Disturb / Focus Assist **on**
- [ ] Password manager closed; no `.env`, tokens, or customer data on screen
- [ ] Browser zoom 125–150%; terminal font bumped up; **checked in the OBS preview**
- [ ] Overlay text updated for this episode (see "Overlay text" below)
- [ ] Water/coffee in reach. It's called Sip & Teach.

## T-10 — `00 — STANDBY`

Go live into the standby scene with the countdown running. Nobody arrives on time;
this is what gives them a reason to stay while they wait. Music optional — if you
use any, use something licensed for stream, or the archive gets claimed.

## The episode

| Time | Scene | What happens |
|---|---|---|
| 0:00–2:00 | `01 — CAMERA` | Who you are, what Disheveled is, what today's one topic is. Lower third auto-hides after 10s. |
| 2:00–5:00 | `03 — SITE DEMO` | Show the thing before explaining it. Let people see the finished result first. |
| 5:00–30:00 | `02 — LAPTOP` | The teach. Narrate what you're doing *and why*, not just what you're clicking. |
| 30:00–42:00 | `01` / `04 — SPLIT` | Questions from chat. Read each one out loud — the archive viewer can't see chat. |
| 42:00–45:00 | `06 — OUTRO` | What's next week, where the drop lives, ask for the subscribe. Let the outro sit ~30s before you stop. |

Anything goes wrong: **F4 to `05 — BRB`**, fix it, come back. Never debug on camera
in silence — that's where viewers leave.

## While teaching — the things that actually matter

- **Say the file name out loud** before you open it. People are watching on phones.
- **Zoom in more than feels necessary.** If you're squinting, they can't read it at all.
- **Pause on results.** When something renders, stop moving the mouse for three
  seconds so it's screenshottable.
- **Narrate mistakes.** A bug you hit live and fix is the most valuable footage in
  the episode. Do not cut away from it.
- **Read every chat message aloud** before answering, and say the person's name.
- **Update the strap** — the `bug.html` overlay's "Now Covering" line — when you
  change subject. It orients anyone arriving mid-stream.

## Overlay text — where to change what

All overlay copy is set through URL parameters on the OBS browser source. Edit the
source (double-click it in OBS) and change the URL query string. No file editing.

**`starting-soon.html`**
| Param | Does |
|---|---|
| `mins=10` | Countdown length from when the scene loads |
| `at=2026-09-14T19:00` | Count down to a wall-clock time instead (local time) |
| `title=` | Episode line |
| `tagline=` | Second line under it |
| `ticker=A\|B\|C` | Bottom marquee items, pipe-separated |
| `brand=` | Top eyebrow text |

**`lower-third.html`** — `name=`, `role=`, `note=`, `hold=10` (seconds before it
auto-hides; omit to keep it up). Pass an empty value (`role=`) to hide that line.

**`bug.html`** — `mark=` (corner wordmark), `topic=` (the "Now Covering" strap),
`live=0` to hide the LIVE pill, `strap=0` to hide the strap entirely.

**`brb.html`** — `note=`, `ticker=`.

**`ending.html`** — `next=`, `site=`, `social=`, `ticker=`.

Spaces and punctuation need URL encoding: space is `%20`, `&` is `%26`, an em dash
is `%E2%80%94`. Easiest path: type the URL in a browser address bar first, confirm
it looks right, then paste the encoded version into OBS.

Set the drop-day countdown against the real date with `at=` and leave `00 — STANDBY`
up for as long as you want — it's a live countdown page with your brand on it.

## After (15 min, same day)

- [ ] Stop the stream, then stop the recording
- [ ] Remux the MKV to MP4 (**File → Remux Recordings**)
- [ ] YouTube: real title, description, **timestamp chapters starting at `0:00`**, thumbnail
- [ ] Pull 2–3 vertical clips from the replay-buffer saves
- [ ] Note the questions you couldn't answer — those are next week's episodes

## Failure playbook

| Symptom | Do this |
|---|---|
| Dropped frames climbing (OBS status bar red) | Lower bitrate mid-stream in Settings → Output. Don't stop the stream. |
| Nobody can hear you | F4 to BRB. Check mic isn't muted in OBS *and* not muted at the OS. Check the right device is selected. |
| Echo / doubled audio | You're capturing desktop audio *and* have speakers on into the mic. Use headphones. |
| Overlay is blank or white | Right-click the source → **Refresh**. If still blank, the file path is wrong — check the `file://` URL. |
| Countdown stuck from last time | The browser source needs **Refresh browser when scene becomes active** checked. |
| Screen capture is black (macOS) | Screen Recording permission wasn't granted, or was granted after OBS launched. Grant it, then fully quit and reopen OBS. |
| Stream key rejected | Key was regenerated in YouTube Studio. Copy the current one. |

> The outro's `site=` defaults to the GitHub Pages URL because that's the address
> that definitely exists today. The moment there's a custom domain, set
> `ending.html?site=yourdomain.com` on that browser source.
