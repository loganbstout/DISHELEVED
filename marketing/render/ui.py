#!/usr/bin/env python3
"""Build annotated interface mockups from a JSON spec.

The screens here are reconstructions drawn in HTML with demo tenant sample
data. They are not screenshots of a live platform, which the content gate
forbids, and every one of them carries a DEMO TENANT badge in the window bar.
"""
import html


def esc(t):
    return html.escape(str(t), quote=False)


ALLOWED = ("em", "b", "br")


def rich(t):
    """Escape everything, then restore a tiny tag whitelist."""
    t = html.escape(str(t), quote=False)
    for tag in ALLOWED:
        t = t.replace(f"&lt;{tag}&gt;", f"<{tag}>").replace(f"&lt;/{tag}&gt;", f"</{tag}>")
    return t


def mark(o):
    """A pin anchored to the element it marks, so no coordinates are needed."""
    return f'<span class="pinmark">{o["pin"]}</span>' if isinstance(o, dict) and o.get("pin") else ""


def pinned(o):
    return " pinned" if isinstance(o, dict) and o.get("pin") else ""


def block(b):
    k = b["kind"]
    if k == "statrow":
        return ('<div class="statrow">' + "".join(
            f'<div><div class="v">{esc(s["v"])}{mark(s)}</div>'
            f'<div class="l">{esc(s["l"])}</div></div>'
            for s in b["stats"]) + "</div>")

    if k == "board":
        cols = ""
        for c in b["columns"]:
            cards = ""
            for cd in c.get("cards", []):
                chip = (f'<div class="chip {cd.get("chipclass","")}">{esc(cd["chip"])}</div>'
                        if cd.get("chip") else "")
                meta = f'<div class="m">{esc(cd["m"])}</div>' if cd.get("m") else ""
                cards += (f'<div class="card{pinned(cd)}"><div class="t">{esc(cd["t"])}</div>'
                          f'{meta}{chip}{mark(cd)}</div>')
            cols += (f'<div class="col"><div class="ch"><span>{esc(c["name"])}</span>'
                     f'<span>{esc(c.get("count",""))}</span></div>{cards}</div>')
        return f'<div class="board">{cols}</div>'

    if k == "rows":
        head = "".join(f"<th>{esc(h)}</th>" for h in b["head"])
        body = ""
        for r in b["rows"]:
            # a row is either a list of cells, or {"cells": [...], "pin": n}
            pin_html, cells = "", r
            if isinstance(r, dict):
                pin_html, cells = mark(r), r["cells"]
            tds = []
            for cell in cells:
                if isinstance(cell, dict):
                    tds.append(f'<span class="chip {cell.get("c","")}">{esc(cell["chip"])}</span>')
                else:
                    tds.append(esc(cell))
            # the pin hangs off the last cell, where there is always clear space
            last = len(tds) - 1
            row = "".join(
                f'<td class="haspin">{c}{pin_html}</td>' if (i == last and pin_html) else f"<td>{c}</td>"
                for i, c in enumerate(tds))
            body += f"<tr>{row}</tr>"
        return f'<table class="ui"><tr>{head}</tr>{body}</table>'


    if k == "ladder":
        return ('<ul class="ladder">' + "".join(
            f'<li class="{s.get("state","")}{pinned(s)}"><i></i><span>{esc(s["t"])}</span>'
            f'{mark(s)}</li>' for s in b["steps"]) + "</ul>")

    if k == "panel":
        fields = "".join(
            f'<div class="k">{esc(f["k"])}</div>'
            f'<div class="v{" empty" if f.get("empty") else ""}{pinned(f)}">'
            f'{esc(f["v"])}{mark(f)}</div>'
            for f in b.get("fields", []))
        note = f'<div class="note" style="margin-top:12px">{rich(b["note"])}</div>' if b.get("note") else ""
        title = f'<div class="pt">{esc(b["title"])}</div>' if b.get("title") else ""
        inner = f'<div class="fields">{fields}</div>' if fields else ""
        return f'<div class="panel{pinned(b)}">{title}{inner}{note}{mark(b)}</div>'

    if k == "thread":
        msgs = "".join(
            f'<div class="msg {m.get("side","")}{pinned(m)}"><div class="w">{esc(m["w"])}</div>'
            f'<div class="x">{esc(m["x"])}</div>{mark(m)}</div>' for m in b["messages"])
        return f'<div class="thread">{msgs}</div>'

    if k == "buttons":
        return ('<div class="btnrow">' + "".join(
            f'<span class="btn {x.get("c","")}{pinned(x)}">{esc(x["t"])}{mark(x)}</span>'
            for x in b["buttons"]) + "</div>")

    if k == "note":
        return f'<div class="note">{rich(b["text"])}</div>'

    raise SystemExit(f"unknown ui block: {k}")


def window(app):
    nav = ""
    for n in app.get("nav", []):
        label = n["t"] if isinstance(n, dict) else n
        on = "on" if label == app.get("active") else ""
        nav += f'<a class="{on}{pinned(n)}">{esc(label)}{mark(n)}</a>' 
    crumb = f'<div class="crumb">{esc(app["crumb"])}</div>' if app.get("crumb") else ""
    title = f'<h3>{esc(app["title"])}</h3>' if app.get("title") else ""
    blocks = "".join(block(b) for b in app.get("blocks", []))
    badge = f'<span class="badge">{esc(app.get("badge", "Demo tenant"))}</span>'
    return (f'<div class="win"><div class="win-bar"><div class="dots"><i></i><i></i><i></i></div>'
            f'<div class="win-url{" pinned" if app.get("urlpin") else ""}">{esc(app.get("url", ""))}'
            f'{mark({"pin": app.get("urlpin")}) if app.get("urlpin") else ""}</div>{badge}</div>'
            f'<div class="win-body"><div class="nav">{nav}</div>'
            f'<div class="pane">{crumb}{title}{blocks}</div></div></div>')


def pins(items):
    return "".join(
        f'<div class="pin" style="left:{p["x"]}%;top:{p["y"]}%">{p["n"]}</div>' for p in items)


def key(spec):
    items = "".join(
        f'<li><div class="n">{k["n"]}</div><div><div class="t">{rich(k["t"])}</div>'
        f'<div class="d">{rich(k["d"])}</div></div></li>' for k in spec.get("key", []))
    foot = f'<div class="kf">{rich(spec["keyfoot"])}</div>' if spec.get("keyfoot") else ""
    return (f'<div class="key"><div class="kt">{esc(spec.get("keytitle", "What you are looking at"))}</div>'
            f'<ol>{items}</ol>{foot}</div>')


def head(spec):
    r = "".join(f"<div>{rich(x)}</div>" for x in spec.get("meta", []))
    return (f'<div class="t-head"><div class="l"><div class="k">{esc(spec["kicker"])}</div>'
            f'<h2>{rich(spec["h2"])}</h2></div><div class="r">{r}</div></div>')


def matrix(spec):
    cards = ""
    for c in spec["cards"]:
        lis = "".join(
            f'<li class="{"off" if (isinstance(i, dict) and i.get("off")) else ""}">'
            f'{rich(i["t"] if isinstance(i, dict) else i)}</li>' for i in c["items"])
        st = f'<div class="ms">{esc(c["state"])}</div>' if c.get("state") else ""
        ft = f'<div class="mfoot">{rich(c["foot"])}</div>' if c.get("foot") else ""
        cards += (f'<div class="mcard"><div class="mh"><div class="mt">{esc(c["title"])}</div>{st}</div>'
                  f'<ul>{lis}</ul>{ft}</div>')
    cols = spec.get("cols", 3)
    rows = -(-len(spec["cards"]) // cols)  # type scales up when there is only one row
    return f'<div class="matrix" data-rows="{rows}" style="--cols:{cols}">{cards}</div>'


def tour_html(spec):
    """One tour graphic: header, then either an annotated window plus key, or a matrix."""
    if spec.get("layout") == "matrix":
        return (f'<div class="tour" style="grid-template-columns:1fr">{head(spec)}{matrix(spec)}</div>')
    body = (f'<div style="position:relative;min-height:0;display:flex">{window(spec["app"])}'
            f'{pins(spec.get("pins", []))}</div>')
    return f'<div class="tour">{head(spec)}{body}{key(spec)}</div>'
