# Stout Intel / SIPS marketing assets

Ten carousel posts and ten annotated platform graphics for the SIPS platform,
built to slot into the existing **Stout Intel LinkedIn Engine** (Notion:
`🔗 Stout Intel — LinkedIn Engine` → `📣 LinkedIn Posts`).

Everything here is generated from JSON specs, so copy and colour are edits
rather than redraws.

```
brand/          colourway tokens, stylesheets, fonts
render/         render.py (specs to PNG and PDF) and ui.py (interface mockups)
tools/check.py  content gate and render checks
carousels/      specs, post copy, rendered output
platform-tours/ specs and rendered output for the annotated graphics
```

## Rendering

```bash
python3 render/render.py carousels/specs/*.json          # all ten carousels
python3 render/render.py platform-tours/specs/*.json     # all ten graphics
python3 render/render.py --size ig_post carousels/specs/05-*.json
python3 tools/check.py                                   # gate + render checks
```

Rendering uses the Chromium already on the machine. Screenshots go through
`headless_shell` because full Chromium subtracts about 87px of window inset and
silently clips the bottom of every capture. Override the binaries with
`CHROME_BIN` and `CHROME_SHELL` if the paths differ.

## The ten carousels

Numbering continues after the existing carousels 01 to 04. Each one anchors to a
dated build or measurement, per the engine's rule that nothing is an opinion
without a receipt.

| # | Post | Anchor | Persona | Colourway |
|---|------|--------|---------|-----------|
| 05 | C14 · The first five minutes, and what nobody had to type | adoption law, 15 Aug 2026 | sales rep | Cobalt |
| 06 | C15 · The owner's screen, and the five questions it answers first | repo audit + production read, 15 Aug 2026 | shop owner | Carbon |
| 07 | C16 · The client's door, and the email they never have to send | portal and approvals, 8 Aug 2026 | client | Bone |
| 08 | B39 · What would the second customer see? | Phase 1 tenant isolation | shop owner | Machine |
| 09 | B40 · Half my product demoed as an empty page | demo tenant walkthrough, 9 Sep 2026 | shop owner | Oxide |
| 10 | B41 · Paid is not done, and delivered is not done either | build 24 plus the delivery loop | sales rep | Cobalt |
| 11 | C17 · Three days of green tests and a dead button | tracking crash, 8 Sep 2026 | shop owner | Oxide |
| 12 | C11 · The tool that reads your settings lied to me | config read, 9 Sep 2026 | shop owner | Machine |
| 13 | C13 · I wrote the brand rules, then broke them thirteen times | brand kit system, 5 Sep 2026 | shop owner | Bone |
| 14 | C12 · The scary number that had already stopped mattering | a figure carried five weeks | shop owner | Carbon |

Rows 08 to 14 consume the `Idea` rows already sitting in the posts database
(B39, B40, B41, C11, C12, C13 and the green tests lesson) which had no assets
against them. Rows 05 to 07 are new and are the three persona tours.

Each carousel produces:

* `carousels/out/<id>-<slug>.pdf` — the LinkedIn document post, 1200x1350 per page
* `carousels/out/<id>-<slug>-li_doc-slide-NN.png` — the same slides as images
* `carousels/out/<id>-<slug>-ig_post-slide-NN.png` — 1080x1350 for Instagram
* `carousels/copy/<POST>-<slug>.md` — hook, post copy, first comment, image spec, gate notes

## The ten annotated graphics

These are the feature and offering visuals, one set per SIPS user type.

| File | Shows |
|------|-------|
| `rep-01-pipeline-board` | the board, with what filled each field |
| `rep-02-the-job-record` | one job, the status ladder, and which fields a machine wrote |
| `rep-03-what-the-rep-gets` | what a rep touches, gets, and is never asked to do |
| `owner-01-the-morning-screen` | the needs attention queue, plus the gaps it admits to |
| `owner-02-the-controls` | team access, demo mode, per client portal control |
| `owner-03-the-whole-inventory` | every surface in the platform with an honest maturity marker |
| `client-01-the-portal` | live jobs, tracking per box, and the walls |
| `client-02-the-approval` | the two button proof decision and its receipt |
| `client-03-what-the-client-gets` | what a client gets, never sees, and never pays for |
| `platform-01-what-is-on-offer` | the three doors: platform access, free tools, portal account |

### These are reconstructions, not screenshots

The task asked for screenshots. Two things stopped that, and the substitute is
better for publishing anyway:

1. The engine's standing gate says **no live SIPS screenshots, demo tenant
   only**.
2. The platform is not reachable from this environment.

So every screen is drawn in HTML from the documented feature inventory, with
sample rows that are visibly labelled as samples and a `DEMO TENANT` badge in
the window bar. Every graphic also carries the line "Reconstruction drawn for
this document with sample rows. Not a screenshot of a live book."

If you would rather ship real captures, take them from demo mode and the pins
and key column can be laid over them with the same spec format.

## The content gate

`tools/check.py` enforces the publishing rules mechanically rather than by eye:

* no dash characters in any human readable string
* no employer or client names
* no money, margin or pay figures
* never opening on the word the gate forbids
* a demo tenant note wherever a screen is claimed
* a `/sips` call to action present

It also reads every rendered PNG for exact dimensions, an unclipped footer band,
and ink bleeding into the outer margin. Current state: **0 failures, 0
warnings** over 10 specs, 10 copy files and 180 renders.

## Two things to check before publishing

1. **Colour values are placeholders.** `brand/tokens.json` names the real
   colourways but the hex values were matched by eye to the shipped drops, since
   the brand-v2 values live in the local render scripts. Swap them in that one
   file and re run to restyle everything.
2. **Nothing is scheduled and no row is gated.** Every copy file carries
   `gate_passed: false`. The claims in each post trace to the dated sources in
   the anchor column, but they are worth a read before anything goes out.
