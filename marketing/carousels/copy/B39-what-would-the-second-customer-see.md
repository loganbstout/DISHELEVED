---
title: "B39 · What would the second customer see?"
type: Document post
series: Build drop
image_variant: carousel
asset: carousels/out/08-what-would-the-second-customer-see.pdf
persona: the shop owner
anchor: "Phase 1 tenant isolation, SIPS product strategy 15 August 2026. Schema audit at commit ec37b81."
cta: "/sips request access"
status: Assets ready
gate_passed: false
---

## Hook
Before I let anybody else onto my platform I asked one question. What would the second customer be able to see?

## Post
Before I let anybody else onto my platform I asked one question. What would the second customer be able to see?

I had a working system, eleven people in it every day, and shops asking about a pilot. So I went looking for the thing that would embarrass me. Not a bug. A shape.

It was one column. That was the whole blocker. Not a module, not a rewrite. One column that quietly assumed there would only ever be one company in here, in a database 104 models deep.

Software that grows up inside one business always grows that assumption. Every table gets written by somebody who knows exactly whose data it is, because at that moment there is only one answer.

Five things have to be true before a second name can sign in. Every row knows which company owns it. Every query filters by that before a page renders. Every file sits in a private bucket served to one session. Every integration writes back to the tenant that owns it. And every one of those has a test that fails loudly when it breaks.

The fifth is the one people skip, and it is the only one still working after you forget you built the other four.

Finding this before a pilot cost three weeks of unglamorous work with nobody watching. Finding it during a pilot costs a customer seeing a name they should never have seen.

So pilots open when isolation closes, not before.

If you have software that grew inside your own company and you are thinking about selling it, go find the place where you assumed there would only ever be one of you. It is in there.

## First comment
The document walks the five conditions and the stop gate that keeps me honest about them. Promo shops can request access: [https://stoutintel.com/sips](https://stoutintel.com/sips)

## Image spec
```json
{"variant": "carousel", "file": "carousels/out/08-what-would-the-second-customer-see.pdf", "slides": 8, "colourway": "Machine", "size": "1200x1350"}
```

## Gate notes
Gate run: zero dash characters, no client or employer names, no money figures, no live screenshots. Model and route counts are the repository audit figures.
