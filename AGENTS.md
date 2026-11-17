# Project notes

## Files
- `ProKick_League_Selection_Updated (1).html` — the master game (single file, everything inline).
- `prokick-app/` — installable website/PWA build: `index.html` (generated), `manifest.webmanifest`, `sw.js`, `vendor/three.min.js`, `audio/crowd-cheer.mp3`, `icons/*`.
- `tools/build-app.py` — regenerates `prokick-app/index.html` from the master file.

## Workflow
1. Edit the master HTML only.
2. `python3 tools/build-app.py` re-syncs the site copy (local three.js/audio paths, PWA head tags, service-worker registration).
3. Bump `CACHE` in `prokick-app/sw.js` (`prokick-vN`) whenever game code changes, or installed copies keep the old shell.
4. Verify: `node --check` on the extracted inline scripts, then load `http://localhost:8142/` and play a match.

Preview: `cd prokick-app && python3 -m http.server 8142`.

## Offline single-file build

`python3 tools/build-offline.py` writes `prokick-offline.html`: the master HTML with
three.min.js inlined (from `prokick-app/vendor/`) and the crowd-cheer mp3 embedded as a
data URI (`window.PK_CHEER_SRC`, also used for the goal-replay track). It needs no network
at all, which matters when the game is opened from a device's file browser instead of a
web server. `ProKick-Offline.zip` is just that one file, for AirDrop/iCloud transfer.
Note: iOS Files previews HTML without running JavaScript, so that path still cannot play.

## Offline single-file build (preferred delivery)
The user plays on an Apple tablet from the Files app, not from a hosted URL: the
workspace preview host (daytonaproxy01.eu) puts its own sign-in in front of the
page once the workspace sleeps, then lands on /callback with `404 sandbox not
found`. That is a host login, never the game — never present a preview URL as
"the app" again.

Build and package a login-free copy after every change to the master file:
    python3 tools/build-offline.py          # -> prokick-offline.html (self-contained)
    python3 - <<'PY'
    import zipfile, pathlib
    with zipfile.ZipFile('ProKick-Offline.zip','w',zipfile.ZIP_DEFLATED) as z:
        z.write('prokick-offline.html','ProKick.html')
    PY

`prokick-offline.html` must make zero network requests (three.js and the crowd
cheer are inlined); verify with a headless run before handing it over.

## Live site
Published at https://higuy14cool.github.io/prokick/ (repo `higuy14cool/prokick`,
public, Pages source = `master` / `/docs`). To ship a change: edit the master
file, run `python3 tools/build-app.py`, then `cp -r prokick-app/. docs/` and
commit + push `docs/` (Pages rebuilds in about 30-60 s).
