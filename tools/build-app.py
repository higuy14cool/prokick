#!/usr/bin/env python3
"""Rebuild prokick-app/index.html from the master game file.

Run after editing "ProKick_League_Selection_Updated (1).html":
    python3 tools/build-app.py
"""
import io
import pathlib
import re
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
<link rel="apple-touch-icon" sizes="152x152" href="icons/apple-touch-icon-152.png">
<link rel="apple-touch-icon" sizes="167x167" href="icons/apple-touch-icon-167.png">
<link rel="apple-touch-icon" sizes="180x180" href="icons/apple-touch-icon.png">
<link rel="mask-icon" href="icons/icon-192.png" color="#22c55e">
<style>
.pk-ball img.pk-applogo{width:clamp(84px,13vw,116px);height:auto;display:block;border-radius:24%;box-shadow:0 10px 26px #0006}
</style>
"""

SW_REGISTER = """<script>
if('serviceWorker' in navigator && location.protocol.indexOf('http')===0){
  window.addEventListener('load',function(){navigator.serviceWorker.register('sw.js').catch(function(){});});
}
</script>
<style>
.pk-installbtn{position:fixed;right:14px;bottom:14px;z-index:2;display:inline-flex;align-items:center;gap:7px;padding:11px 16px;border:1px solid #4ade80;border-radius:999px;background:linear-gradient(145deg,#15803d,#052e16);color:#eafff1;font:800 12px/1 system-ui,-apple-system,sans-serif;letter-spacing:.9px;cursor:pointer;box-shadow:0 8px 22px #0009}
.pk-installbtn[hidden]{display:none}
.pk-installbtn:active{transform:translateY(1px)}
.pk-installnote{position:fixed;right:14px;bottom:62px;z-index:3;max-width:235px;padding:10px 13px;border:1px solid #2c6e47;border-radius:12px;background:#08150f;color:#d7fbe4;font:600 12px/1.5 system-ui,-apple-system,sans-serif;box-shadow:0 10px 26px #000a;text-align:left}
.pk-installnote[hidden]{display:none}
@media(max-width:560px){.pk-screen .pk-copyright{bottom:64px}}
</style>
<button id="pkInstallBtn" class="pk-installbtn" type="button" hidden>&#11015; INSTALL APP</button>
<div id="pkInstallNote" class="pk-installnote" hidden></div>
<script>
(function(){
  var home=document.getElementById('pkHome'),btn=document.getElementById('pkInstallBtn'),note=document.getElementById('pkInstallNote');
  if(!home||!btn||!note)return;
  var standalone=false;
  try{standalone=(window.matchMedia&&window.matchMedia('(display-mode: standalone)').matches)||window.navigator.standalone===true;}catch(e){}
  if(standalone)return;
  home.appendChild(btn);home.appendChild(note);btn.hidden=false;
  var deferred=null,isIOS=/iphone|ipad|ipod/i.test(navigator.userAgent);
  window.addEventListener('beforeinstallprompt',function(e){e.preventDefault();deferred=e;});
  window.addEventListener('appinstalled',function(){btn.hidden=true;note.hidden=true;deferred=null;});
  btn.addEventListener('click',function(){
    if(deferred){
      note.hidden=true;var p=deferred;deferred=null;
      p.prompt();
      if(p.userChoice&&p.userChoice.then)p.userChoice.then(function(r){if(r&&r.outcome==='accepted')btn.hidden=true;});
      return;
    }
    if(!note.hidden){note.hidden=true;return;}
    note.textContent=isIOS?'Tap Share, then "Add to Home Screen".':'Open the browser menu and choose "Install app".';
    note.hidden=false;
  });
})();
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
]


def main() -> int:
    html = SRC.read_text(encoding="utf-8")
    # The master embeds the logo inline; the app build serves it from icons/.
    html = re.sub(r'(class="pk-applogo" src=")data:image/png;base64,[^"]*"', r'\1icons/icon-192.png"', html)
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
