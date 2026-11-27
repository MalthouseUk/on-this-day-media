from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

W = H = 1080      # videos are square
PAGE_H = 1350     # picture posts are 4:5 portrait (1080 x 1350)
import os
FD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts") + "/"
FRAKTUR = FD + "Fraktur.ttf"
P_BLACK = FD + "PlayfairBlack.ttf"
P_BOLD = FD + "PlayfairBold.ttf"
P_BOLDI = FD + "PlayfairBoldItalic.ttf"
P_ITAL = FD + "PlayfairItalic.ttf"
BASK = FD + "Bask.ttf"
BASK_I = FD + "BaskItalic.ttf"
BASK_B = FD + "BaskBold.ttf"
OLD_B = FD + "OldStdBold.ttf"

PAPER = (246, 242, 233)
INK = (22, 20, 18)
GREY = (72, 67, 60)   # secondary text: kept dark for easy reading
HAIR = (170, 162, 150)

DATELINE = "WEDNESDAY, 25 NOVEMBER 2026"
EDITION = 1  # edition number shown in the right-hand ear box

_cache = {}
def font(path, size):
    k = (path, size)
    if k not in _cache:
        _cache[k] = ImageFont.truetype(path, size)
    return _cache[k]

_papers = {}
def paper(h=1080):
    """Newsprint: fine grain, faint vignette (cached per height)."""
    if h not in _papers:
        H = h
        img = Image.new("RGB", (W, H), PAPER)
        n = np.asarray(Image.effect_noise((W, H), 22).convert("L"), dtype=np.int16) - 128
        a = np.asarray(img, dtype=np.int16) + (n[..., None] * 0.07).astype(np.int16)
        img = Image.fromarray(np.clip(a, 0, 255).astype("uint8"))
        vig = Image.new("L", (W, H), 0)
        d = ImageDraw.Draw(vig)
        for i in range(50):
            d.rectangle([i * 5, i * 5, W - i * 5, H - i * 5], outline=int(255 * i / 50))
        vig = vig.filter(ImageFilter.GaussianBlur(50))
        dark = Image.new("RGB", (W, H), tuple(int(c * 0.94) for c in PAPER))
        _papers[h] = Image.composite(img, dark, vig)
    return _papers[h].copy()

def spaced_len(d, text, fnt, track):
    return sum(d.textlength(c, font=fnt) for c in text) + track * (len(text) - 1)

def spaced(d, x, y, text, fnt, fill, track=0, anchor="l"):
    w = spaced_len(d, text, fnt, track)
    if anchor == "c": x -= w / 2
    elif anchor == "r": x -= w
    for c in text:
        d.text((x, y), c, font=fnt, fill=fill)
        x += d.textlength(c, font=fnt) + track
    return w

def centred(d, y, text, fnt, fill, cx=W / 2):
    d.text((cx - d.textlength(text, font=fnt) / 2, y), text, font=fnt, fill=fill)

def wrap(d, text, fnt, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= maxw: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

M = 56  # page margin

def masthead(d, section):
    """Broadsheet masthead: ears, blackletter title, double rule, dateline."""
    d.line([M, 44, W - M, 44], fill=INK, width=1)
    # ears
    ef = font(BASK_I, 17); eb = font(OLD_B, 15)
    for x0, top, l1, l2 in [(M, 58, "THE DAILY", "History Edition"),
                            (W - M - 150, 58, f"No. {EDITION}", "Every day · Free")]:
        d.rectangle([x0, top, x0 + 150, top + 76], outline=INK, width=1)
        spaced(d, x0 + 75, top + 14, l1, eb, INK, 2, "c")
        centred(d, top + 40, l2, ef, GREY, cx=x0 + 75)
    centred(d, 44, "On This Day", font(P_BLACK, 80), INK)
    # double rule
    d.line([M, 156, W - M, 156], fill=INK, width=4)
    d.line([M, 163, W - M, 163], fill=INK, width=1)
    df = font(OLD_B, 16)
    spaced(d, M, 172, DATELINE, df, INK, 1.5)
    spaced(d, W - M, 172, "ESTABLISHED 2026", df, INK, 1.5, "r")
    spaced(d, W / 2, 172, section, df, INK, 3, "c")
    d.line([M, 198, W - M, 198], fill=INK, width=1)

def footer(d, H=1080):
    d.line([M, H - 70, W - M, H - 70], fill=INK, width=1)
    d.line([M, H - 66, W - M, H - 66], fill=INK, width=1)
    centred(d, H - 56, "Follow On This Day for your daily edition of history",
            font(BASK_I, 20), GREY)

def kicker(d, y, text, fill, cx=W / 2, size=18):
    f = font(OLD_B, size)
    w = spaced_len(d, text, f, 4)
    spaced(d, cx, y, text, f, fill, 4, "c")
    d.line([cx - w / 2 - 70, y + size * 0.6, cx - w / 2 - 16, y + size * 0.6], fill=fill, width=1)
    d.line([cx + w / 2 + 16, y + size * 0.6, cx + w / 2 + 70, y + size * 0.6], fill=fill, width=1)
