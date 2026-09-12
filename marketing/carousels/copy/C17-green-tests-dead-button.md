---
title: "C17 · Three days of green tests and a dead button"
type: Document post
series: Lesson
image_variant: carousel
asset: carousels/out/11-green-tests-dead-button.pdf
persona: the shop owner
anchor: "Shipping tracking crash, session 8 September 2026. The 401 read as proof of deployment, build C01."
cta: "/sips request access"
status: Assets ready
gate_passed: false
---

## Hook
For three days every test in our platform was green and the one button a sales rep needed most was dead.

## Post
For three days every test in our platform was green and the one button a sales rep needed most was dead.

The tests were not lying. They had never been asked the question. They covered the functions underneath, and the failure was in the wiring between the page and those functions, which no test had an opinion about.

So every check I ran agreed with me, and all of them were answering something other than what I thought I was asking.

There are four checks that will agree with you for free. A test suite that never loads the page a person uses. A deploy that reports success for shipping the old build. A login wall that answers before your code does, so a refusal at the front door looks like proof the room exists. And a log with no errors in it because nothing ran.

I have been caught by all four. The worst one was telling somebody a feature was live when it was not, because the thing I checked could not tell the difference.

So the rule now is that the build proves it, not the test suite. Open the page a human opens, press the thing a human presses, watch a real record change. It costs about ninety seconds and it has caught four of these.

The same trap exists with no code involved. Your process document says the confirmation goes out. Your inbox says the mail merge ran. Neither of those is a client holding a confirmation.

Pick the one thing you are most certain works because a report says so, then go be the customer for five minutes.

The report is a claim. The click is the proof.

## First comment
The document has the four silent checks and what I do instead. Promo shops can request access: [https://stoutintel.com/sips](https://stoutintel.com/sips)

## Image spec
```json
{"variant": "carousel", "file": "carousels/out/11-green-tests-dead-button.pdf", "slides": 8, "colourway": "Oxide", "size": "1200x1350"}
```

## Gate notes
Gate run: zero dash characters, no client names, no money figures, no live screenshots.
