#!/usr/bin/env python3
"""Rebuild prokick-app/index.html from the master game file.

Run after editing "ProKick_League_Selection_Updated (1).html":
    python3 tools/build-app.py
"""
import io
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "ProKick_League_Selection_Updated (1).html"
OUT = ROOT / "prokick-app" / "index.html"

HEAD_ADD = """<meta name="description" content="ProKick - free browser football game: Classic Match, Futsal, Penalties, 2v2 and the Apex Cup tournament.">
<meta name="theme-color" content="#08150f">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="ProKick">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" type="image/png" sizes="32x32" href="icons/favicon-32.png">
<link rel="icon" type="image/png" sizes="192x192" href="icons/icon-192.png">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<style>
.pk-ball img.pk-applogo{width:clamp(84px,13vw,116px);height:auto;display:block;border-radius:24%;box-shadow:0 10px 26px #0006}
</style>
"""

SW_REGISTER = """<script>
if('serviceWorker' in navigator && location.protocol.indexOf('http')===0){
  window.addEventListener('load',function(){navigator.serviceWorker.register('sw.js').catch(function(){});});
}
</script>
</body>"""

REPLACEMENTS = [
    (
        '<meta name="viewport" content="width=device-width,initial-scale=1">',
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">',
    ),
    (
        "<script src=\"https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js\"></script>",
        '<script src="vendor/three.min.js"></script>',
    ),
    (
        "https://raw.githubusercontent.com/opstiger/aiba-percent-battle/main/assets/aiba-audio/crowd-cheer-stadium.mp3",
        "audio/crowd-cheer.mp3",
    ),
    ('<title>ProKick</title>', '<title>ProKick</title>\n' + HEAD_ADD),
    (
        '<div class="pk-ball">⚽</div>',
        '<div class="pk-ball"><img class="pk-applogo" src="icons/icon-192.png" alt="ProKick logo" width="116" height="116"></div>',
    ),
]


def main() -> int:
    html = SRC.read_text(encoding="utf-8")
    for old, new in REPLACEMENTS:
        if old not in html:
            print(f"build-app: pattern not found: {old[:60]}", file=sys.stderr)
            return 1
        html = html.replace(old, new, 1)

    if not html.rstrip().endswith("</html>"):
        print("build-app: unexpected source layout (no closing </html>)", file=sys.stderr)
        return 1

    html = html.rstrip()
    html = html[: html.rfind("</body>")] + SW_REGISTER + "\n</html>\n"
    OUT.write_text(html, encoding="utf-8")
    print(f"build-app: wrote {OUT.relative_to(ROOT)} ({len(html)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
