#!/usr/bin/env python3
"""Build prokick-offline.html: one self-contained file with the 3D engine and
crowd audio embedded, so the game runs with no network access (opened from disk
or from a device's file browser instead of a web server)."""
import base64
import io
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MASTER = os.path.join(ROOT, "ProKick_League_Selection_Updated (1).html")
OUT = os.path.join(ROOT, "prokick-offline.html")
THREE = os.path.join(ROOT, "prokick-app", "vendor", "three.min.js")
CHEER = os.path.join(ROOT, "prokick-app", "audio", "crowd-cheer.mp3")

CDN_TAG = '<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>'
CHEER_URL = ("https://raw.githubusercontent.com/opstiger/aiba-percent-battle/main/"
             "assets/aiba-audio/crowd-cheer-stadium.mp3")
REPLAY_URL = "https://pixabay.com/sound-effects/download/490555/?attachment="


def main():
    html = io.open(MASTER, encoding="utf-8").read()
    three = io.open(THREE, encoding="utf-8").read()
    cheer = base64.b64encode(open(CHEER, "rb").read()).decode("ascii")

    assert html.count(CDN_TAG) == 1, "three.js script tag not found"
    html = html.replace(CDN_TAG, "<script>\n" + three + "\n</script>")

    embed = ("<script>window.PK_CHEER_SRC='data:audio/mpeg;base64,%s';</script>\n" % cheer)
    html = html.replace("</head>", embed + "</head>", 1)

    assert html.count("'" + CHEER_URL + "'") == 1, "cheer url not found"
    html = html.replace("'" + CHEER_URL + "'", "window.PK_CHEER_SRC")
    assert html.count("'" + REPLAY_URL + "'") == 1, "replay url not found"
    html = html.replace("'" + REPLAY_URL + "'", "window.PK_CHEER_SRC")

    left = [u for u in ("https://", "http://") if u in html]
    io.open(OUT, "w", encoding="utf-8").write(html)
    print("build-offline: wrote %s (%d bytes)" % (os.path.basename(OUT), len(html.encode("utf-8"))))
    print("build-offline: remaining absolute urls ->", [u for u in left] or "none referenced at load time")


if __name__ == "__main__":
    main()
