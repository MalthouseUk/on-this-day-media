"""Build one day's On This Day set from data/YYYY-MM-DD.json.

Usage:  python3 tools/build_day.py 2026-11-27
Writes: YYYY-MM-DD/  (cover + person pages, 3 videos, captions.txt)

JSON format (see data/2026-11-26.json for a full example):
{
  "dateline": "FRIDAY, 27 NOVEMBER 2026",      # masthead line
  "day": "27 November",                        # used in standfirsts and video kicker
  "born":       [{"name", "role", "short", "born", "died" (or null), "bio": [p1, p2, p3]}],  # 6 people
  "remembered": [{... same ...}],                                                         # 4 people
  "history": [{"year", "head", "body"}],       # 3-4 items
  "charts":  [{"year", "uk": [artist, song], "us": [artist, song]}],  # 3 items
  "sport":   [{"year", "head", "body"}],       # 3-4 items
  "questions": {"history", "charts", "sport"}, # closing question on each video
  "captions":  {"born", "remembered", "history", "charts", "sport"}   # Facebook caption text
}
"""
import json, os, re, sys, shutil, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import style, dates
date = sys.argv[1]
data = json.load(open(os.path.join(ROOT, "data", f"{date}.json")))
style.DATELINE = data["dateline"]
import datetime
# Edition No. 1 was 25 November 2026; the number goes up by one each day
style.EDITION = (datetime.date.fromisoformat(date) - datetime.date(2026, 11, 25)).days + 1
import pictures, people, videos
videos.DAY = data["day"].upper()

OUT = os.path.join(ROOT, date)
os.makedirs(OUT, exist_ok=True)
RED = (140, 24, 30)

def slug(n):
    return re.sub(r"[^a-z]", "", n.lower().replace("jr.", "").split()[-1]) or "person"

for p in data["born"] + data["remembered"]:
    dates.DATES[p["name"]] = (p["born"], p.get("died"))

born, rem = data["born"], data["remembered"]
pictures.page(f"{OUT}/born_01_cover.png", "BIRTHDAYS", "BORN ON THIS DAY", "Happy Birthday",
              f"{['', 'One', 'Two', 'Three', 'Four', 'Five', 'Six'][len(born)]} remarkable lives that began on {data['day']}",
              [(None, p["name"], p["short"]) for p in born], band=RED, accent=RED)
pictures.page(f"{OUT}/remembered_01_cover.png", "REMEMBRANCE", "DIED ON THIS DAY", "We Remember",
              f"Those we lost on {data['day']}", [(None, p["name"], p["short"]) for p in rem], band=style.INK)
for i, p in enumerate(born, 2):
    people.person_page(f"{OUT}/born_{i:02d}_{slug(p['name'])}.png", "BIRTHDAYS", "BORN ON THIS DAY",
                       RED, p["name"], p["role"], p["bio"], i, len(born) + 1)
for i, p in enumerate(rem, 2):
    people.person_page(f"{OUT}/remembered_{i:02d}_{slug(p['name'])}.png", "REMEMBRANCE", "DIED ON THIS DAY",
                       style.INK, p["name"], p["role"], p["bio"], i, len(rem) + 1)

work = tempfile.mkdtemp()
os.makedirs(os.path.join(work, "out"))
cwd = os.getcwd(); os.chdir(work)
tag = data["day"].split()[0] + data["day"].split()[1][:3].lower()   # e.g. 27nov
q = data["questions"]
jobs = [
    (f"history_{tag}", videos.HIST, ["Events in", "History"], "Moments that shaped the world",
     [(h["year"], h["head"], h["body"]) for h in data["history"]], q["history"]),
    (f"charts_{tag}", videos.CHART, ["Top of", "the Charts"], "Who was Number 1 in Britain and America",
     [("chart", c["year"], tuple(c["uk"]), tuple(c["us"])) for c in data["charts"]], q["charts"]),
    (f"sport_{tag}", videos.SPORT, ["Sport on", "This Day"], "Great days and famous nights",
     [(s["year"], s["head"], s["body"]) for s in data["sport"]], q["sport"]),
]
for name, (acc, sec), title, sub, sc, question in jobs:
    videos.build(name, acc, sec, title, sub, sc, question)
    shutil.move(f"out/{name}.mp4", f"{OUT}/{name}.mp4")
os.chdir(cwd); shutil.rmtree(work)

c = data["captions"]
with open(f"{OUT}/captions.txt", "w") as fh:
    for k in ["born", "remembered", "history", "charts", "sport"]:
        fh.write(f"===== {k.upper()} =====\n{c[k]}\n\n")
print("\n".join(sorted(os.listdir(OUT))))
