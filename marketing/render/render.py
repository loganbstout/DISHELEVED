#!/usr/bin/env python3
"""Render Stout Intel carousel and platform-tour assets from JSON specs.

  python3 render/render.py carousels/specs/*.json
  python3 render/render.py --size ig_post carousels/specs/05-*.json

One spec becomes: a multi page PDF per requested size (LinkedIn document post)
and one PNG per slide (Instagram / single image use). Colour comes from
brand/tokens.json, so restyling every asset is a one file edit.
"""
import json, os, re, subprocess, sys, html, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRAND = os.path.join(ROOT, "brand")
TOKENS = json.load(open(os.path.join(BRAND, "tokens.json")))
# headless_shell reports an exact viewport; full chromium subtracts ~87px of
# window inset, which silently clips the bottom of every screenshot.
CHROME = os.environ.get("CHROME_BIN", "/opt/pw-browsers/chromium")
SHELL = os.environ.get("CHROME_SHELL",
                       "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell")
CSS = open(os.path.join(BRAND, "brand.css")).read()


def esc(t):
    return html.escape(str(t), quote=False)


def rich(t):
    """Allow <em> only; escape the rest."""
    t = html.escape(str(t), quote=False)
    return t.replace("&lt;em&gt;", "<em>").replace("&lt;/em&gt;", "</em>")


def foot(sl, i, n):
    b = sl.get("boundary", "")
    # the float must precede the in flow text, or it drops to the next line
    return (f'<div class="foot"><div class="no">{i:02d} / {n:02d}</div>'
            f'<div class="boundary">{esc(b)}</div></div>')


def bar(sl, seal):
    return (f'<div class="bar"><div class="kicker">{esc(sl.get("kicker",""))}</div>'
            f'<div class="seal">{esc(seal)}</div></div>')


def body_html(sl):
    t = sl["type"]
    if t == "cover":
        h1 = f'<h1 style="--h1:{sl.get("h1size",104)}px">{rich(sl["headline"])}</h1>'
        sub = f'<p class="sub{" wide" if sl.get("wide") else ""}">{rich(sl["sub"])}</p>' if sl.get("sub") else ""
        return f'<div class="main">{h1}{sub}</div>'

    if t == "stat":
        eb = f'<div class="eyebrow">{esc(sl["eyebrow"])}</div>' if sl.get("eyebrow") else ""
        sub = f'<p class="lede">{rich(sl["sub"])}</p>' if sl.get("sub") else ""
        return (f'<div class="main">{eb}<div class="hero-stat">'
                f'<div class="v">{esc(sl["value"])}</div>'
                f'<div class="l">{rich(sl["label"])}</div></div>{sub}</div>')

    if t == "metrics":
        cells = "".join(f'<div class="metric"><div class="v">{esc(m["value"])}</div>'
                        f'<div class="l">{esc(m["label"])}</div></div>' for m in sl["metrics"])
        h = f'<h2>{rich(sl["h2"])}</h2>' if sl.get("h2") else ""
        return f'<div class="main">{h}<div class="metrics">{cells}</div></div>'

    if t == "body":
        h = f'<h2>{rich(sl["h2"])}</h2>' if sl.get("h2") else ""
        ps = "".join(f'<p class="lede{" dim" if i else ""}">{rich(p)}</p>'
                     for i, p in enumerate(sl.get("lede", [])))
        return f'<div class="main">{h}{ps}</div>'

    if t == "list":
        tag_ = "ol" if sl.get("numbered") else "ul"
        lis = ""
        for i, it in enumerate(sl["items"], 1):
            if isinstance(it, str):
                it = {"text": it}
            n = f'<span class="n">{i:02d}</span>' if sl.get("numbered") else '<span class="n">/</span>'
            tg = f'<span class="tag">{esc(it["tag"])}</span>' if it.get("tag") else ""
            lis += f'<li class="{"off" if it.get("off") else ""}">{n}<span>{rich(it["text"])}</span>{tg}</li>'
        h = f'<h2>{rich(sl["h2"])}</h2>' if sl.get("h2") else ""
        return f'<div class="main top">{h}<{tag_} class="steps">{lis}</{tag_}></div>'

    if t == "compare":
        def col(c):
            big = f'<div class="big">{esc(c["big"])}</div>' if c.get("big") else ""
            p = f'<p>{rich(c["p"])}</p>' if c.get("p") else ""
            return f'<div><h3>{esc(c["h3"])}</h3>{big}{p}</div>'
        h = f'<h2>{rich(sl["h2"])}</h2>' if sl.get("h2") else ""
        return f'<div class="main">{h}<div class="compare">{col(sl["left"])}{col(sl["right"])}</div></div>'

    if t == "table":
        RA = ' style="text-align:right"'
        head = "".join("<th%s>%s</th>" % (RA if j else "", esc(c))
                       for j, c in enumerate(sl["head"]))
        rows = ""
        for r in sl["rows"]:
            hot = len(r) > 2 and r[2]
            rows += (f'<tr><td>{rich(r[0])}</td>'
                     f'<td class="num{" hot" if hot else ""}">{esc(r[1])}</td></tr>')
        h = f'<h2>{rich(sl["h2"])}</h2>' if sl.get("h2") else ""
        return f'<div class="main top">{h}<table><tr>{head}</tr>{rows}</table></div>'

    if t == "law":
        src = f'<div class="src">{esc(sl["src"])}</div>' if sl.get("src") else ""
        return f'<div class="main"><div class="law"><div class="q">{rich(sl["quote"])}</div>{src}</div></div>'

    if t == "cta":
        h = f'<h2>{rich(sl["h2"])}</h2>' if sl.get("h2") else ""
        ps = "".join(f'<p class="lede">{rich(p)}</p>' for p in sl.get("lede", []))
        pills = ""
        if sl.get("pills"):
            pills = '<div class="pillrow">' + "".join(
                f'<span class="pill{" on" if p.get("on") else ""}">{esc(p["t"])}</span>'
                for p in sl["pills"]) + "</div>"
        cta = f'<div class="cta-line">{esc(sl["cta"])}</div>' if sl.get("cta") else ""
        return f'<div class="main">{h}{ps}{pills}{cta}</div>'

    if t == "raw":
        return f'<div class="main top">{sl["html"]}</div>'

    raise SystemExit(f"unknown slide type: {t}")


def slide_html(sl, seal, i, n):
    return f'<section class="slide">{bar(sl, seal)}{body_html(sl)}{foot(sl, i, n)}</section>'


def doc(spec, slides, w, h, cw, paged):
    c = TOKENS["colourways"][cw]
    vars_ = ";".join(f"--{k}:{v}" for k, v in c.items())
    page = (f"@page{{size:{w}px {h}px;margin:0}}" if paged else "")
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}\n'
            f':root{{{vars_};--w:{w}px;--h:{h}px}}{page}</style></head>'
            f'<body>{"".join(slides)}</body></html>')


def chrome(args, binary=None):
    b = binary or CHROME
    base = [b] + ([] if b == SHELL else ["--headless"]) + [ "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
            "--force-device-scale-factor=1", "--disable-dev-shm-usage",
            "--font-render-hinting=none", "--virtual-time-budget=4000"]
    subprocess.run(base + args, check=True, capture_output=True)


def render(spec_path, only_size=None):
    spec = json.load(open(spec_path))
    cw = spec.get("colourway", "Carbon")
    seal = spec.get("seal", "STOUT INTEL  ·  STOUTINTEL.COM/SIPS")
    slides = spec["slides"]
    n = len(slides)
    outdir = os.path.join(os.path.dirname(os.path.dirname(spec_path)), "out")
    os.makedirs(outdir, exist_ok=True)
    work = os.path.join(outdir, ".work")
    os.makedirs(work, exist_ok=True)
    # brand assets must sit beside the html for relative font urls
    for f in ("fonts",):
        dst = os.path.join(work, f)
        if not os.path.exists(dst):
            shutil.copytree(os.path.join(BRAND, f), dst)

    made = []
    for size_key in (only_size and [only_size] or spec.get("sizes", ["li_doc"])):
        w, h = TOKENS["sizes"][size_key]
        stem = f'{spec["id"]}-{spec["slug"]}'
        # multi page PDF (LinkedIn document post)
        if size_key == "li_doc":
            hp = os.path.join(work, f"{stem}.html")
            open(hp, "w").write(doc(spec, [slide_html(s, seal, i, n) for i, s in enumerate(slides, 1)],
                                    w, h, cw, paged=True))
            pdf = os.path.join(outdir, f"{stem}.pdf")
            chrome(["--no-pdf-header-footer", f"--print-to-pdf={pdf}", hp])
            made.append(pdf)
        # one PNG per slide
        for i, s in enumerate(slides, 1):
            hp = os.path.join(work, f"{stem}-{size_key}-{i:02d}.html")
            open(hp, "w").write(doc(spec, [slide_html(s, seal, i, n)], w, h, cw, paged=False))
            png = os.path.join(outdir, f"{stem}-{size_key}-slide-{i:02d}.png")
            chrome([f"--window-size={w},{h}", f"--screenshot={png}", hp], binary=SHELL)
            made.append(png)
    return made


if __name__ == "__main__":
    args = sys.argv[1:]
    size = None
    if "--size" in args:
        k = args.index("--size")
        size = args[k + 1]
        del args[k:k + 2]
    if not args:
        raise SystemExit(__doc__)
    total = []
    for p in args:
        got = render(p, size)
        total += got
        print(f"{os.path.basename(p)} -> {len(got)} files")
    print(f"\n{len(total)} files written")
