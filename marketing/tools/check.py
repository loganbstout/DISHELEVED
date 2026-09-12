#!/usr/bin/env python3
"""Gate and render checks for Stout Intel assets.

  python3 tools/check.py

Two passes:
  GATE   reads every spec and copy file and enforces the LinkedIn engine rules
         (no dash characters, no Brand+Aid naming, no money figures, never
         opening on "AI", a demo tenant note wherever a screen is claimed).
  RENDER reads every PNG and checks exact size, that the footer band actually
         carries pixels (the clipping bug), and that nothing bleeds into the
         outer margin.
"""
import json, os, re, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKENS = json.load(open(os.path.join(ROOT, "brand", "tokens.json")))
DASHES = "-‐‑‒–—―−"
BANNED = [r"Brand\+Aid", r"brand ?aid"]
MONEY = re.compile(r"[$£€]\s?\d|\b\d+(\.\d+)?\s?(percent margin|margin)\b|\bcommission of\b", re.I)
# "url" is a mock address bar, not prose, so the dash rule does not apply to it
SKIP_KEYS = {"id", "slug", "sizes", "colourway", "persona", "anchor", "asset", "file",
             "_note", "type", "numbered", "on", "off", "wide", "h1size", "hot", "url"}

fails, warns = [], []


def strings(node, key=None, path=""):
    """Yield (path, text) for human readable strings only."""
    if isinstance(node, dict):
        for k, v in node.items():
            yield from strings(v, k, f"{path}.{k}")
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from strings(v, key, f"{path}[{i}]")
    elif isinstance(node, str) and key not in SKIP_KEYS:
        yield path, node


def gate():
    specs = sorted(glob.glob(os.path.join(ROOT, "*", "specs", "*.json")))
    copies = sorted(glob.glob(os.path.join(ROOT, "carousels", "copy", "*.md")))
    for sp in specs:
        spec = json.load(open(sp))
        name = os.path.basename(sp)
        for path, txt in strings(spec):
            for ch in txt:
                if ch in DASHES:
                    fails.append(f"{name}{path}: dash character in copy -> {txt[:70]!r}")
                    break
            for b in BANNED:
                if re.search(b, txt, re.I):
                    fails.append(f"{name}{path}: names the employer -> {txt[:70]!r}")
            if MONEY.search(txt):
                fails.append(f"{name}{path}: money or margin figure -> {txt[:70]!r}")
            if re.match(r"^\s*(ai|a\.i\.)\b", txt, re.I):
                fails.append(f"{name}{path}: opens on AI -> {txt[:70]!r}")
        blob = json.dumps(spec)
        if "stoutintel.com/sips" not in blob:
            warns.append(f"{name}: no /sips call to action")
        if re.search(r"screen|dashboard|board|portal|tour", blob, re.I) and not re.search(r"demo tenant", blob, re.I):
            warns.append(f"{name}: claims a screen with no demo tenant note")
    for cp in copies:
        txt = open(cp).read()
        name = os.path.basename(cp)
        body = re.split(r"^## ", txt, flags=re.M)
        for chunk in body:
            if chunk.startswith(("Post", "First comment", "Hook")):
                for ln in chunk.splitlines():
                    if ln.startswith(("Post", "First comment", "Hook")) or not ln.strip():
                        continue
                    if any(c in ln for c in DASHES) and "](" not in ln:
                        fails.append(f"{name}: dash character -> {ln.strip()[:70]!r}")
                    if MONEY.search(ln):
                        fails.append(f"{name}: money or margin figure -> {ln.strip()[:70]!r}")
        for b in BANNED:
            if re.search(b, txt, re.I):
                fails.append(f"{name}: names the employer")
    return len(specs), len(copies)


def render_checks():
    try:
        from PIL import Image
    except ImportError:
        warns.append("pillow missing, render checks skipped")
        return 0
    pngs = sorted(glob.glob(os.path.join(ROOT, "*", "out", "*.png")))
    for p in pngs:
        name = os.path.basename(p)
        m = re.search(r"-(li_doc|ig_post|li_square|tour_wide)-", name)
        im = Image.open(p).convert("RGB")
        if m:
            want = tuple(TOKENS["sizes"][m.group(1)])
            if im.size != want:
                fails.append(f"{name}: size {im.size}, expected {want}")
        w, h = im.size
        bg = im.getpixel((w - 3, 3))
        # carousel slides carry a boundary note and slide number in the bottom band;
        # tour graphics instead have to prove that content reaches the lower third
        if os.sep + "carousels" + os.sep in p:
            band = im.crop((60, h - 110, w - 60, h - 20))
            if len(band.getcolors(maxcolors=200000) or []) < 12:
                fails.append(f"{name}: footer band looks empty, likely clipped")
        else:
            band = im.crop((40, int(h * 0.66), w - 40, h - 30))
            if len(band.getcolors(maxcolors=200000) or []) < 12:
                fails.append(f"{name}: lower third is empty, layout did not fill")
        # nothing but the accent spine may sit in the outer margin
        for box, where in (((10, 0, 40, h), "left"), ((w - 30, 0, w, h), "right"),
                           ((0, 0, w, 20), "top"), ((0, h - 12, w, h), "bottom")):
            strip = im.crop(box)
            off = [c for c, col in (strip.getcolors(maxcolors=200000) or []) if col != bg]
            if sum(off) > strip.size[0] * strip.size[1] * 0.02:
                warns.append(f"{name}: ink in the {where} margin")
    return len(pngs)


if __name__ == "__main__":
    ns, nc = gate()
    npng = render_checks()
    print(f"checked {ns} specs, {nc} copy files, {npng} renders\n")
    for w in warns:
        print(f"  WARN  {w}")
    for f in fails:
        print(f"  FAIL  {f}")
    print(f"\n{len(fails)} failures, {len(warns)} warnings")
    sys.exit(1 if fails else 0)
