#!/usr/bin/env python3
"""
Generate an importable OBS scene collection for the Disheveled Studio stream.

Capture-device source IDs are OS-specific, so a scene collection is not portable
between macOS and Windows. Generate the one that matches the machine you stream from.

    python3 build-scenes.py --os macos
    python3 build-scenes.py --os windows --overlays "C:/Users/you/DISHELEVED/stream/overlays"

With no --overlays, browser source URLs contain the literal token __OVERLAYS__,
which you can find/replace in any text editor before importing.
"""

import argparse, json, uuid, pathlib

BASE_W, BASE_H = 1920, 1080

# OBS source type IDs, per platform.
IDS = {
    "macos": {
        "camera":  "av_capture_input_v2",
        "display": "screen_capture",
        "mic":     "coreaudio_input_capture",
    },
    "windows": {
        "camera":  "dshow_input",
        "display": "monitor_capture",
        "mic":     "wasapi_input_capture",
        "desktop": "wasapi_output_capture",
    },
    "linux": {
        "camera":  "v4l2_input",
        "display": "xshm_input",
        "mic":     "pulse_input_capture",
        "desktop": "pulse_output_capture",
    },
}


def source(name, sid, settings=None, *, muted=False, volume=1.0):
    """One OBS source object. Sensible defaults for every field OBS expects."""
    return {
        "prev_ver": 503383552,
        "name": name,
        "uuid": str(uuid.uuid4()),
        "id": sid,
        "versioned_id": sid,
        "settings": settings or {},
        "mixers": 255 if sid.endswith(("_input_capture", "_output_capture", "_input", "_input_v2")) else 0,
        "sync": 0,
        "flags": 0,
        "volume": volume,
        "balance": 0.5,
        "enabled": True,
        "muted": muted,
        "push-to-mute": False,
        "push-to-mute-delay": 0,
        "push-to-talk": False,
        "push-to-talk-delay": 0,
        "hotkeys": {},
        "deinterlace_mode": 0,
        "deinterlace_field_order": 0,
        "monitoring_type": 0,
        "private_settings": {},
    }


def browser(name, url, w=BASE_W, h=BASE_H, fps=30):
    return source(name, "browser_source", {
        "url": url,
        "width": w,
        "height": h,
        "fps_custom": True,
        "fps": fps,
        "reroute_audio": False,
        "restart_when_active": True,   # overlays re-arm (countdown, animations) on scene entry
        "shutdown": True,              # stop rendering when hidden — saves CPU on a laptop
        "webpage_control_level": 1,
    })


def item(src, item_id, *, pos=(0, 0), scale=(1.0, 1.0), crop=(0, 0, 0, 0), visible=True):
    l, t, r, b = crop
    return {
        "name": src["name"],
        "source_uuid": src["uuid"],
        "visible": visible,
        "locked": False,
        "rot": 0.0,
        "pos": {"x": float(pos[0]), "y": float(pos[1])},
        "scale": {"x": float(scale[0]), "y": float(scale[1])},
        "align": 5,
        "bounds_type": 0,
        "bounds_align": 0,
        "bounds": {"x": 0.0, "y": 0.0},
        "crop_left": l, "crop_top": t, "crop_right": r, "crop_bottom": b,
        "id": item_id,
        "group_item_backup": False,
        "scale_filter": "disable",
        "blend_method": "default",
        "blend_type": "normal",
        "show_transition": {"duration": 0},
        "hide_transition": {"duration": 0},
        "private_settings": {},
    }


def scene(name, items):
    """Scenes are sources of type `scene`; their children live in settings.items.
    OBS renders items back-to-front, so the list is reversed on write."""
    s = source(name, "scene")
    s["settings"] = {
        "id_counter": len(items),
        "custom_size": False,
        "items": list(reversed(items)),
    }
    return s


def build(os_key, overlays):
    ids = IDS[os_key]
    ov = overlays.rstrip("/")

    def f(page, query=""):
        return f"file://{ov}/{page}{query}"

    # ---- shared sources (one instance, referenced by several scenes) ----
    standby = browser("OVL — Starting Soon", f("starting-soon.html", "?mins=10&title=Sip%20%26%20Teach%20%E2%80%94%20Episode%20001"))
    brb     = browser("OVL — BRB", f("brb.html"))
    outro   = browser("OVL — Outro", f("ending.html"))
    lower   = browser("OVL — Lower Third", f("lower-third.html", "?name=LOGAN%20STOUT&role=Disheveled%20Studio%20%E2%80%94%20Founder&hold=10"))
    bug     = browser("OVL — Bug + Strap", f("bug.html", "?topic=Collection%20001%20%E2%80%94%20Site%20Walkthrough"))
    site    = browser("WEB — Disheveled Site", "https://loganbstout.github.io/DISHELEVED/")

    cam = source("CAM — Main", ids["camera"])
    dsp = source("SCR — Display", ids["display"])
    mic = source("AUD — Mic", ids["mic"])

    audio = [mic]
    if "desktop" in ids:
        audio.append(source("AUD — Desktop", ids["desktop"]))

    # Picture-in-picture geometry, 1920x1080 canvas.
    PIP = dict(pos=(1416, 764), scale=(0.24, 0.24))          # bottom-right, 461x259
    SPLIT_SCR = dict(pos=(32, 206), scale=(0.62, 0.62))      # left, 1190x670
    SPLIT_CAM = dict(pos=(1262, 362), scale=(0.33, 0.33))    # right, 634x356

    scenes = [
        scene("00 — STANDBY",  [item(standby, 1)]),
        scene("01 — CAMERA",   [item(cam, 1), item(bug, 2), item(lower, 3)]),
        scene("02 — LAPTOP",   [item(dsp, 1), item(cam, 2, **PIP), item(bug, 3)]),
        scene("03 — SITE DEMO",[item(site, 1), item(cam, 2, **PIP), item(bug, 3)]),
        scene("04 — SPLIT",    [item(dsp, 1, **SPLIT_SCR), item(cam, 2, **SPLIT_CAM), item(bug, 3)]),
        scene("05 — BRB",      [item(brb, 1)]),
        scene("06 — OUTRO",    [item(outro, 1)]),
    ]

    sources = [standby, brb, outro, lower, bug, site, cam, dsp] + audio + scenes

    return {
        "DesktopAudioDevice1": {},
        "AuxAudioDevice1": {},
        "current_scene": "00 — STANDBY",
        "current_program_scene": "00 — STANDBY",
        "current_preview_scene": "01 — CAMERA",
        "scene_order": [{"name": s["name"]} for s in scenes],
        "name": "Disheveled Live",
        "sources": sources,
        "groups": [],
        "quick_transitions": [
            {"name": "Cut",  "duration": 300, "hotkeys": [], "id": 1, "fade_to_black": False},
            {"name": "Fade", "duration": 300, "hotkeys": [], "id": 2, "fade_to_black": False},
        ],
        "transitions": [],
        "current_transition": "Fade",
        "transition_duration": 300,
        "preview_locked": False,
        "scaling_enabled": False,
        "scaling_level": 0,
        "scaling_off_x": 0.0,
        "scaling_off_y": 0.0,
        "virtual-camera": {"type2": 3},
        "modules": {},
        "version": 2,
    }


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--os", dest="os_key", choices=sorted(IDS), required=True)
    ap.add_argument("--overlays", default="__OVERLAYS__",
                    help="absolute path to stream/overlays on the streaming machine")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    out = pathlib.Path(a.out) if a.out else pathlib.Path(__file__).parent / f"disheveled-scenes.{a.os_key}.json"
    out.write_text(json.dumps(build(a.os_key, a.overlays), indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {out}")
