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
