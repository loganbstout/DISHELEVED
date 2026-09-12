---
title: "C15 · The owner's screen, and the five questions it answers before you ask"
type: Document post
series: Lesson
image_variant: carousel
asset: carousels/out/06-one-screen-that-answers-first.pdf
persona: the shop owner
anchor: "Repository audit at ec37b81 and live production read, both 15 August 2026."
cta: "/sips request access"
status: Assets ready
gate_passed: false
---

## Hook
Five questions used to be five conversations. I got tired of being the report.

## Post
Five questions used to be five conversations. I got tired of being the report.

What is actually in the pipeline. Which jobs are late and who is waiting on whom. What closed this time last year and never came back. Which deals have gone quiet and nobody has admitted it. What the team did all week.

Every one of those is a meeting in most shops, and the answer is whatever the person with the best memory says it is.

So I counted what was really in the database. 136 deals. 196 production jobs. 241 companies. 1,808 logged activities. 4,000 queued jobs the system ran without being asked. Eleven people in it daily.

Then I added the only rule that has survived contact with reality: a feature ships only if it can fill its own fields. That single line killed a nine week plan and four of the five modules a research report told me to build.

The one I kept is the one where the input surface is a chat channel people already post in. It asks nothing of anybody, so it filled itself.

And the part I say out loud before any demo: the data richness comes from absorbing what your team already sends. A shop on a different system installs this and gets an empty database. That makes the honest market narrow and specific today, and it makes the roadmap one absorption adapter per system rather than more features.

I would rather tell you that first than sell you a pilot that starves.

What is the question you ask your team every Monday that your software should already answer?

## First comment
The document walks the owner side, including the maturity of every surface and what it cannot see. Promo shops can request access here: [https://stoutintel.com/sips](https://stoutintel.com/sips)

## Image spec
```json
{"variant": "carousel", "file": "carousels/out/06-one-screen-that-answers-first.pdf", "slides": 10, "colourway": "Carbon", "size": "1200x1350"}
```

## Gate notes
Gate run over spec and copy: zero dash characters, no client or employer names, no margin or pay figures, no live screenshots, demo tenant stated on every screen claim. Capability counts read from the repository and the production database rather than recalled.
