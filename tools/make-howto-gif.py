"""Render assets/how-to-connect-github.gif — an animated walkthrough of the
account menu -> Connectors -> GitHub -> Connect flow."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 900, 620
BG = (11, 20, 16)
PANEL = (22, 33, 27)
PANEL_HI = (30, 46, 37)
LINE = (46, 66, 54)
TEXT = (234, 245, 238)
MUTED = (138, 162, 148)
ACCENT = (110, 242, 160)
WHITE = (247, 250, 248)
GH = (36, 41, 46)

F = "/usr/share/fonts/truetype/dejavu/"
f_title = ImageFont.truetype(F + "DejaVuSans-Bold.ttf", 26)
f_big = ImageFont.truetype(F + "DejaVuSans-Bold.ttf", 34)
f_mid = ImageFont.truetype(F + "DejaVuSans-Bold.ttf", 20)
f_txt = ImageFont.truetype(F + "DejaVuSans.ttf", 18)
f_small = ImageFont.truetype(F + "DejaVuSans.ttf", 15)
f_cap = ImageFont.truetype(F + "DejaVuSans-Bold.ttf", 22)


def ease(t):
    return 3 * t * t - 2 * t * t * t


def lerp(a, b, t):
    return a + (b - a) * t


def rp(d, box, r=14, fill=PANEL, outline=LINE, width=2):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)


def centered(d, text, cx, y, font, fill=TEXT):
    w = d.textlength(text, font=font)
    d.text((cx - w / 2, y), text, font=font, fill=fill)


def app_frame(d):
    d.rectangle([0, 0, W, H], fill=BG)
    # top bar
    d.rectangle([0, 0, W, 62], fill=(14, 24, 19))
    d.line([0, 62, W, 62], fill=LINE, width=2)
    d.text((26, 18), "Lemon Code", font=f_title, fill=TEXT)
    # logo dot
    d.ellipse([196, 22, 214, 40], fill=ACCENT)


def avatar(d, hi=0.0):
    cx, cy, r = W - 42, 31, 17
    if hi > 0:
        d.ellipse([cx - r - 8 - 12 * hi, cy - r - 8 - 12 * hi,
                   cx + r + 8 + 12 * hi, cy + r + 8 + 12 * hi],
                  outline=ACCENT, width=int(2 + 3 * hi))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(44, 78, 60), outline=ACCENT if hi > .5 else LINE, width=2)
    d.text((cx - 9, cy - 11), "PP", font=f_small, fill=TEXT)


def cursor(d, x, y, pulse=0.0):
    if pulse > 0:
        d.ellipse([x - 14 - 10 * pulse, y - 14 - 10 * pulse, x + 14 + 10 * pulse, y + 14 + 10 * pulse],
                  outline=(255, 255, 255, ), width=2)
    pts = [(x, y), (x + 17, y + 20), (x + 7, y + 21), (x + 12, y + 31),
           (x + 5, y + 34), (x, y + 24), (x - 4, y + 30)]
    d.polygon(pts, fill=WHITE, outline=(20, 20, 20))
    d.line(pts[:3], fill=(20, 20, 20), width=2)


def caption(d, step, text):
    d.rounded_rectangle([24, H - 84, W - 24, H - 24], radius=16, fill=(16, 28, 22), outline=LINE, width=2)
    d.rounded_rectangle([40, H - 68, 74, H - 40], radius=8, fill=ACCENT)
    n = str(step)
    d.text((57 - d.textlength(n, font=f_mid) / 2, H - 66), n, font=f_mid, fill=(9, 26, 17))
    d.text((90, H - 66), text, font=f_cap, fill=TEXT)


def menu(d, prog):
    x0, y0 = W - 260, 68
    h = int(150 * prog)
    if h <= 4:
        return
    rp(d, [x0, y0, W - 26, y0 + h], r=14, fill=(24, 37, 30), outline=LINE)
    items = [("Your profile", False), ("Connectors", False), ("Settings", False)]
    for i, (label, _) in enumerate(items):
        y = y0 + 12 + i * 44
        if y + 30 > y0 + h:
            continue
        if label == "Connectors":
            rp(d, [x0 + 8, y - 6, W - 34, y + 32], r=10, fill=PANEL_HI, outline=ACCENT, width=2)
        d.text((x0 + 24, y), label, font=f_txt, fill=TEXT)
    return (x0, y0)


def connectors_page(d, connected=False, card_hi=0.0):
    d.text((40, 92), "Connectors", font=f_big, fill=TEXT)
    d.text((40, 136), "Connect the apps Lemon Code can work with.", font=f_txt, fill=MUTED)
    cards = [("GitHub", GH, True), ("Google Drive", (40, 46, 44), False), ("Slack", (46, 40, 54), False)]
    y = 186
    for name, col, active in cards:
        box = [40, y, W - 40, y + 96]
        rp(d, box, r=16, fill=PANEL, outline=ACCENT if (active and card_hi > .3) else LINE,
           width=2 + int(2 * card_hi))
        d.rounded_rectangle([60, y + 24, 108, y + 72], radius=12, fill=col, outline=LINE)
        d.text((78 if name == "GitHub" else 70, y + 36), name[0], font=f_mid, fill=TEXT)
        d.text((124, y + 26), name, font=f_mid, fill=TEXT)
        sub = "Connected" if (connected and active) else ("Free browser football game hosting" if active else "Not needed")
        d.text((124, y + 54), sub, font=f_small, fill=ACCENT if (connected and active) else MUTED)
        label = "Reconnect" if (connected and active) else "Connect"
        bx = [W - 210, y + 28, W - 60, y + 70]
        rp(d, bx, r=10, fill=ACCENT if not connected else PANEL_HI,
           outline=ACCENT if not connected else LINE)
        col_t = (9, 26, 17) if not connected else TEXT
        centered(d, label, (bx[0] + bx[2]) / 2, y + 38, f_txt, col_t)
        y += 116
    return (W - 135, 186 + 96 + 0)  # centre of GitHub Connect button row 1


def github_window(d, prog, hi=0.0):
    if prog <= 0:
        return
    h = int(360 * prog)
    box = [W / 2 - 290, 96, W / 2 + 290, 96 + h]
    d.rounded_rectangle(box, radius=18, fill=WHITE, outline=(210, 215, 212), width=2)
    if prog < .9:
        return
    d.ellipse([box[0] + 30, 122, box[0] + 74, 166], fill=(36, 41, 46))
    d.text((box[0] + 44, 134), "GH", font=f_small, fill=WHITE)
    d.text((box[0] + 88, 126), "Sign in to GitHub", font=f_mid, fill=(24, 28, 26))
    for i, lab in enumerate(["Username or email", "Password"]):
        yy = 196 + i * 66
        d.rectangle([box[0] + 30, yy, box[2] - 30, yy + 44], fill=(246, 248, 247), outline=(205, 212, 208), width=2)
        d.text((box[0] + 44, yy + 12), lab, font=f_small, fill=(110, 120, 115))
    d.text((box[0] + 30, 336), "Sign in  ▸  Authorize Lemon Code", font=f_txt, fill=(90, 100, 95))
    ab = [box[2] - 260, 400 - 26, box[2] - 40, 400 + 16]
    d.rounded_rectangle(ab, radius=10, fill=(31, 136, 61) if hi > .4 else (46, 164, 79))
    centered(d, "Authorize", (ab[0] + ab[2]) / 2, 400 - 14, f_txt, WHITE)
    return ((ab[0] + ab[2]) / 2, 388)


def toast(d, prog):
    if prog <= 0:
        return
    w = int(430 * prog)
    box = [W / 2 - w / 2, 452, W / 2 + w / 2, 504]
    d.rounded_rectangle(box, radius=12, fill=(24, 52, 36), outline=ACCENT, width=2)
    if prog > .5:
        centered(d, "✓  GitHub connected", W / 2, 466, f_txt, ACCENT)


def scene(frame):
    """Return (image, caption_step, caption_text)."""
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    app_frame(d)

    if frame < 12:                       # step 1: open the account menu
        t = ease(min(1, frame / 8))
        x = lerp(520, W - 44, t)
        y = lerp(300, 34, t)
        avatar(d, hi=1.0 if frame >= 9 else 0.0)
        menu(d, ease(max(0, (frame - 8) / 4)))
        cursor(d, x, y, pulse=1.0 if frame >= 9 else 0.0)
        cap = (1, "Open the account menu, top right")
    elif frame < 24:                     # step 2: Connectors
        avatar(d, 1.0)
        menu(d, 1.0)
        t = ease(min(1, (frame - 12) / 7))
        x = lerp(W - 44, W - 170, t)
        y = lerp(34, 68 + 12 + 44 * 1 + 10, t)
        cursor(d, x, y, pulse=1.0 if frame >= 20 else 0.0)
        cap = (2, "Tap Connectors")
    elif frame < 38:                     # step 3: GitHub card -> Connect
        hi = min(1, max(0, (frame - 26) / 6))
        bx, by = connectors_page(d, card_hi=hi)
        t = ease(min(1, (frame - 24) / 8))
        x = lerp(W - 170, bx, t)
        y = lerp(168, by - 30, t)
        cursor(d, x, y, pulse=1.0 if frame >= 33 else 0.0)
        cap = (3, "Tap GitHub, then Connect")
    elif frame < 52:                     # step 4: sign in and authorize
        connectors_page(d, card_hi=.4)
        p = ease(min(1, (frame - 38) / 5))
        pos = github_window(d, p, hi=1.0 if frame >= 46 else 0.0)
        if pos and frame >= 41:
            t = ease(min(1, (frame - 41) / 6))
            cursor(d, lerp(600, pos[0], t), lerp(300, pos[1], t), pulse=1.0 if frame >= 47 else 0.0)
        cap = (4, "Sign in to GitHub and tap Authorize")
    else:                                # step 5: connected
        connectors_page(d, connected=True, card_hi=.6)
        toast(d, ease(min(1, (frame - 52) / 5)))
        cap = (5, "Done — GitHub is connected")
    caption(d, *cap)
    # progress dots
    for i in range(5):
        on = i + 1 == cap[0]
        d.ellipse([W - 160 + i * 26, H - 62, W - 148 + i * 26, H - 50],
                  fill=ACCENT if on else LINE)
    return img


def main():
    out = Path("assets/how-to-connect-github.gif")
    frames = [scene(i) for i in range(60)]
    frames[0].save(out, save_all=True, append_images=frames[1:],
                   duration=[150 if i >= 52 else 120 for i in range(60)],
                   loop=0, optimize=True, disposal=2)
    print("wrote", out, out.stat().st_size, "bytes", out.stat().st_size // 1024, "KB")


if __name__ == "__main__":
    main()
