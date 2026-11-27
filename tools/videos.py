import subprocess, os, sys
from style import *

FPS = 30
DAY = "25 NOVEMBER"
FADE = 0.4

def ease(t):
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3

def fade_mul(t, dur):
    return min(1.0, t / FADE, (dur - t) / FADE)

BG = paper().getpixel((540, 640))
def ink(c, a, bg=None):
    bg = bg or BG
    return tuple(int(bg[i] + (c[i] - bg[i]) * a) for i in range(3))

def encode(path, dur, draw_fn):
    tmp = path[:-4] + ".tmp.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo",
        "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", tmp],
        stdin=subprocess.PIPE)
    n = int(round(dur * FPS))
    for i in range(n):
        p.stdin.write(draw_fn(i / FPS, dur).tobytes())
    p.stdin.close()
    if p.wait() == 0:
        os.replace(tmp, path)

def base(section):
    img = paper(); d = ImageDraw.Draw(img); masthead(d, section); footer(d)
    return img

def blend_in(bg, img, m):
    return Image.blend(bg, img, m) if m < 1 else img

def intro(accent, section, title, sub):
    b = base(section)
    def f(t, dur):
        img = b.copy(); d = ImageDraw.Draw(img)
        a = ease(t / 0.7)
        # band wipes open from the centre
        half = (W / 2 - M) * a
        d.rectangle([W / 2 - half, 330, W / 2 + half, 650], fill=accent)
        a2 = ease((t - 0.5) / 0.7)
        if a2 > 0:
            kicker(d, 352, DAY, ink(PAPER, a2, accent))
            y = 392 + (1 - a2) * 30
            for i, line in enumerate(title):
                centred(d, y + i * 118, line, font(P_BLACK, 112), ink(PAPER, a2, accent))
        a3 = ease((t - 1.0) / 0.7)
        centred(d, 680, sub, font(P_ITAL, 38), ink(GREY, a3))
        return blend_in(paper(), img, fade_mul(t, dur))
    return f

def progress(d, idx, total, accent):
    gap = 30; x0 = W / 2 - gap * (total - 1) / 2
    for i in range(total):
        r = 7
        if i == idx:
            d.rectangle([x0 + i * gap - r, H - 108 - r, x0 + i * gap + r, H - 108 + r], fill=accent)
        else:
            d.rectangle([x0 + i * gap - r, H - 108 - r, x0 + i * gap + r, H - 108 + r], outline=HAIR, width=2)

def item(accent, section, year, head, body, idx, total):
    b = base(section)
    def f(t, dur):
        img = b.copy(); d = ImageDraw.Draw(img)
        a = ease(t / 0.6)
        kicker(d, 236, "ON THIS DAY IN", ink(accent, a))
        centred(d, 262 + (1 - a) * 40, year, font(P_BLACK, 200), ink(INK, a))
        a2 = ease((t - 0.45) / 0.7)
        hf = font(P_BOLD, 66); y = 540
        for line in wrap(d, head, hf, 900):
            centred(d, y + (1 - a2) * 20, line, hf, ink(INK, a2)); y += 78
        a3 = ease((t - 0.8) / 0.6)
        d.line([W / 2 - 120 * a3, y + 22, W / 2 + 120 * a3, y + 22], fill=accent, width=3)
        a4 = ease((t - 1.1) / 0.8)
        bf = font(BASK, 40); y += 50
        for line in wrap(d, body, bf, 860):
            centred(d, y, line, bf, ink(GREY, a4)); y += 56
        progress(d, idx, total, accent)
        return blend_in(paper(), img, fade_mul(t, dur))
    return f

def chart_item(accent, section, year, uk, us, idx, total):
    b = base(section)
    def f(t, dur):
        img = b.copy(); d = ImageDraw.Draw(img)
        a = ease(t / 0.6)
        kicker(d, 236, "NUMBER ONE ON THIS DAY IN", ink(accent, a))
        centred(d, 262 + (1 - a) * 40, year, font(P_BLACK, 200), ink(INK, a))
        top = 540
        al = ease((t - 0.4) / 0.6)
        d.line([M, top, M + (W - 2 * M) * al, top], fill=INK, width=2)
        d.line([W / 2, top + 20, W / 2, top + 20 + 300 * al], fill=HAIR, width=1)
        colw = (W - 2 * M - 80) / 2
        for k, (tag, (artist, song)) in enumerate([("UNITED KINGDOM", uk), ("UNITED STATES", us)]):
            ak = ease((t - 0.7 - k * 0.6) / 0.7)
            cx = M + colw / 2 + k * (colw + 80)
            yy = top + 30 + (1 - ak) * 25
            kicker(d, yy, tag, ink(accent, ak), cx=cx, size=17)
            af = font(P_BOLD, 50); yy += 50
            for ln in wrap(d, artist, af, colw):
                centred(d, yy, ln, af, ink(INK, ak), cx=cx); yy += 60
            sf = font(BASK_I, 37); yy += 8
            for ln in wrap(d, "\u201c" + song + "\u201d", sf, colw):
                centred(d, yy, ln, sf, ink(GREY, ak), cx=cx); yy += 44
        progress(d, idx, total, accent)
        return blend_in(paper(), img, fade_mul(t, dur))
    return f

def outro(accent, section, question):
    b = base(section)
    def f(t, dur):
        img = b.copy(); d = ImageDraw.Draw(img)
        a = ease(t / 0.8)
        kicker(d, 380, "YOUR SAY", ink(accent, a))
        qf = font(P_BOLDI, 70); y = 430
        for line in wrap(d, question, qf, 880):
            centred(d, y, line, qf, ink(INK, a)); y += 86
        a2 = ease((t - 0.7) / 0.8)
        centred(d, y + 40, "Tell us in the comments below", font(BASK_I, 34), ink(GREY, a2))
        return blend_in(paper(), img, fade_mul(t, dur))
    return f

# ---------- AI film clips (Higgsfield), stored in clips/ ----------
CLIP_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "clips")
CLIP_FOR = {"HISTORY": "history", "MUSIC": "charts", "SPORT": "sport"}
CREAM = (246, 240, 226)

class ClipReader:
    """Streams 1080x1080 RGB frames from a clip; holds the last frame if the clip runs out."""
    def __init__(self, path):
        self.p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", path, "-vf", f"scale={W}:{H},fps={FPS}",
                                   "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        self.last = None
    def next(self):
        buf = self.p.stdout.read(W * H * 3)
        if len(buf) == W * H * 3:
            self.last = Image.frombytes("RGB", (W, H), buf)
        return self.last.copy()

def _shade(top_dark=False):
    """Dark gradient so cream text reads clearly over the film."""
    g = Image.new("L", (1, H))
    for y in range(H):
        a = max(0.0, (y - H * 0.45) / (H * 0.55)) * 0.82
        if top_dark:
            a = max(a, max(0.0, (H * 0.22 - y) / (H * 0.22)) * 0.55)
        g.putpixel((0, y), int(255 * a))
    g = g.resize((W, H))
    layer = Image.new("RGBA", (W, H), (12, 10, 8, 0)); layer.putalpha(g)
    return layer

_last_clip_frame = {}

def clip_intro(key, accent, title):
    rd = ClipReader(os.path.join(CLIP_DIR, f"{key}.mp4")); shade = _shade(top_dark=True)
    def f(t, dur):
        img = Image.alpha_composite(rd.next().convert("RGBA"), shade).convert("RGB")
        d = ImageDraw.Draw(img)
        a0 = ease(t / 0.8)
        centred(d, 34, "On This Day", font(P_BLACK, 58), ink(CREAM, a0 * 0.95, (40, 34, 30)))
        a = ease((t - 1.0) / 0.9)
        if a > 0:
            kicker(d, 800 + (1 - a) * 20, DAY, ink(CREAM, a, (20, 18, 16)))
            tf = font(P_BLACK, 96)
            line = " ".join(title)
            while d.textlength(line, font=tf) > W - 120: tf = font(P_BLACK, tf.size - 4)
            centred(d, 840 + (1 - a) * 30, line, tf, ink(CREAM, a, (20, 18, 16)))
        if t < 0.35:   # gentle fade up from black
            img = Image.blend(Image.new("RGB", (W, H), (0, 0, 0)), img, t / 0.35)
        _last_clip_frame[key] = img
        return img
    return f

def after_clip(key, fn, xfade=0.6):
    """Cross-fade from the clip's final frame into the paper title card."""
    def f(t, dur):
        img = fn(t, dur)
        if t < xfade and key in _last_clip_frame:
            img = Image.blend(_last_clip_frame[key], img, ease(t / xfade))
        return img
    return f

def clip_outro(question):
    rd = ClipReader(os.path.join(CLIP_DIR, "outro.mp4")); shade = _shade(top_dark=True)
    def f(t, dur):
        img = Image.alpha_composite(rd.next().convert("RGBA"), shade).convert("RGB")
        d = ImageDraw.Draw(img)
        centred(d, 34, "On This Day", font(P_BLACK, 58), CREAM)
        a = ease((t - 0.4) / 0.8)
        if a > 0:
            dk = (20, 18, 16)
            kicker(d, 730, "YOUR SAY", ink(CREAM, a, dk))
            qf = font(P_BOLDI, 62); y = 768
            for line in wrap(d, question, qf, 900):
                centred(d, y, line, qf, ink(CREAM, a, dk)); y += 74
            a2 = ease((t - 1.1) / 0.8)
            centred(d, y + 14, "Tell us in the comments below", font(BASK_I, 36), ink(CREAM, a2, dk))
        if t < 0.5:    # come in from the paper page
            img = Image.blend(paper(), img, ease(t / 0.5))
        if dur - t < 0.6:
            img = Image.blend(Image.new("RGB", (W, H), (0, 0, 0)), img, max(0, (dur - t) / 0.6))
        return img
    return f

def build(name, accent, section, title, sub, scenes, question):
    os.makedirs("scenes", exist_ok=True)
    files = []
    key = CLIP_FOR.get(section)
    have_clips = key and os.path.exists(os.path.join(CLIP_DIR, f"{key}.mp4")) \
        and os.path.exists(os.path.join(CLIP_DIR, "outro.mp4"))
    if have_clips:
        plan = [("film", 4.6, clip_intro(key, accent, title)),
                ("intro", 2.8, after_clip(key, intro(accent, section, title, sub)))]
    else:
        plan = [("intro", 3.2, intro(accent, section, title, sub))]
    for i, s in enumerate(scenes):
        if s[0] == "chart":
            plan.append((f"s{i}", 6.0, chart_item(accent, section, *s[1:], i, len(scenes))))
        else:
            plan.append((f"s{i}", 5.5, item(accent, section, *s, i, len(scenes))))
    if have_clips:
        plan.append(("outro", 4.8, clip_outro(question)))
    else:
        plan.append(("outro", 3.5, outro(accent, section, question)))
    for tag, dur, fn in plan:
        p = f"scenes/{name}_{tag}.mp4"; encode(p, dur, fn); files.append(p)
    with open(f"scenes/{name}.txt", "w") as fh:
        fh.writelines(f"file '{os.path.basename(p)}'\n" for p in files)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
                    "-i", f"scenes/{name}.txt", "-c", "copy", "-movflags", "+faststart",
                    f"out/{name}.mp4"], check=True)

def still(fn, t, dur, path):
    fn(t, dur).save(path)

HIST = ((140, 24, 30), "HISTORY")
CHART = ((28, 62, 104), "MUSIC")
SPORT = ((30, 84, 52), "SPORT")

hist_scenes = [
    ("1783", "Evacuation Day", "The last British troops leave New York at the end of the American Revolutionary War."),
    ("1915", "Einstein's big idea", "Albert Einstein presents the field equations of general relativity in Berlin."),
    ("1952", "Curtain up on The Mousetrap", "Agatha Christie's whodunnit opens in London – now the world's longest-running play."),
    ("1984", "Band Aid", "Britain's biggest pop stars gather in Notting Hill to record “Do They Know It's Christmas?”"),
]
chart_scenes = [
    ("chart", "1963", ("Gerry & the Pacemakers", "You'll Never Walk Alone"), ("Dale & Grace", "I'm Leaving It Up to You")),
    ("chart", "1975", ("Billy Connolly", "D.I.V.O.R.C.E."), ("KC and the Sunshine Band", "That's the Way (I Like It)")),
    ("chart", "1984", ("Chaka Khan", "I Feel for You"), ("Wham!", "Wake Me Up Before You Go-Go")),
]
sport_scenes = [
    ("1953", "Hungary 6–3 England", "Puskás and the Magical Magyars stun Wembley – and English football is never the same."),
    ("1980", "“No más”", "In New Orleans, Roberto Durán quits in round 8 and Sugar Ray Leonard regains his world title."),
    ("2005", "Farewell, Georgie", "Football mourns George Best, the genius from Belfast."),
]

JOBS = {
    "history_25nov": (*HIST, ["Events in", "History"], "Moments that shaped the world", hist_scenes, "Which of these surprised you most?"),
    "charts_25nov": (*CHART, ["Top of", "the Charts"], "Who was Number 1 in Britain and America", chart_scenes, "Which one would you put on first?"),
    "sport_25nov": (*SPORT, ["Sport on", "This Day"], "Great days and famous nights", sport_scenes, "Were you watching any of these?"),
}

if __name__ == "__main__":
    mode = sys.argv[1]
    for name, (acc, sec, title, sub, sc, q) in JOBS.items():
        if mode == "preview":
            if sc[0][0] == "chart":
                still(chart_item(acc, sec, *sc[1][1:], 1, len(sc)), 4, 6, f"prev_{name}.png")
            else:
                longest = max(sc, key=lambda s: len(s[2]))
                still(item(acc, sec, *longest, 0, len(sc)), 4, 5.5, f"prev_{name}.png")
            still(intro(acc, sec, title, sub), 2, 3.2, f"prev_{name}_intro.png")
        else:
            build(name, acc, sec, title, sub, sc, q)
