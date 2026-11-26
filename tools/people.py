from style import *
from dates import life

RED = (140, 24, 30)

# Photo frame position, so a photo can be dropped in later (x, y, w, h)
PX, PY, PW, PH = M, 272, 400, 600

def person_page(fname, section, kick, accent, name, role, bio, n, total, dark=False):
    img = paper(); d = ImageDraw.Draw(img)
    masthead(d, section)
    kicker(d, 232, kick, accent)
    nf = font(P_BLACK, 84)
    while d.textlength(name, font=nf) > W - 2 * M - 40:
        nf = font(P_BLACK, nf.size - 4)
    centred(d, 262 + (84 - nf.size) // 2, name, nf, INK)
    centred(d, 364, role, font(P_ITAL, 34), accent)
    spaced(d, W / 2, 420, life(name), font(OLD_B, 20), GREY, 3, "c")
    d.line([W / 2 - 60, 464, W / 2 + 60, 464], fill=accent, width=3)
    # body column with a drop cap on the first paragraph
    x0, colw = 130, W - 260
    bf = font(BASK, 28); lh = 42
    y = 494
    for pi, para in enumerate(bio):
        if pi == 0:
            cap, rest = para[0], para[1:]
            cf = font(P_BLACK, 150)
            # baseline of the cap sits on the baseline of the third line
            d.text((x0 - 2, y + 2 * lh + 24), cap, font=cf, fill=accent, anchor="ls")
            indent = d.textlength(cap, font=cf) + 14
            words = rest.split(); lines = []; cur = ""
            first = True
            for w_ in words:
                maxw = colw - indent if len(lines) < 3 else colw
                t = (cur + " " + w_) if cur else w_
                if d.textlength(t, font=bf) <= maxw: cur = t
                else: lines.append(cur); cur = w_
            if cur: lines.append(cur)
            y_cap = y + 3 * lh
            for li, ln in enumerate(lines):
                d.text((x0 + (indent if li < 3 else 0), y), ln, font=bf, fill=INK); y += lh
            y = max(y, y_cap)
        else:
            for ln in wrap(d, para, bf, colw):
                d.text((x0, y), ln, font=bf, fill=INK); y += lh
        y += 18
    if y > H - 120:
        print("OVERFLOW", fname, y)
    spaced(d, W - M, H - 104, f"{n} OF {total}", font(OLD_B, 16), GREY, 3, "r")
    if n < total:
        w = spaced(d, M, H - 104, "SWIPE FOR MORE", font(OLD_B, 16), GREY, 3)
        ax = M + w + 14; ay = H - 95
        d.line([ax, ay, ax + 34, ay], fill=GREY, width=2)
        d.polygon([(ax + 34, ay - 6), (ax + 44, ay), (ax + 34, ay + 6)], fill=GREY)
    footer(d)
    img.save(fname)

born = [
    ("1835", "Andrew Carnegie", "Industrialist and philanthropist", [
        "Born in Dunfermline, Scotland, he emigrated to America as a boy and started work in a cotton mill.",
        "He built Carnegie Steel into a giant, sold it in 1901, and gave most of his fortune away – funding more than 2,500 public libraries and New York's Carnegie Hall.",
        "He famously wrote that a man who dies rich dies disgraced \u2013 and he lived by his word."]),
    ("1844", "Karl Benz", "Engineer and motoring pioneer", [
        "In 1886 the German engineer patented the Benz Patent-Motorwagen, widely seen as the first practical petrol-powered car.",
        "Two years later his wife Bertha drove it more than 100km to prove it worked. His company later merged with Daimler – the start of Mercedes-Benz.",
        "He died in 1929, aged 84, having lived to see the motor car transform the world."]),
    ("1914", "Joe DiMaggio", "Baseball legend", [
        "Nicknamed “Joltin’ Joe”, he spent his whole 13-season career with the New York Yankees, winning nine World Series and three MVP awards.",
        "His 56-game hitting streak in 1941 still stands as a record. In 1954 he married Marilyn Monroe.",
        "He entered baseball\u2019s Hall of Fame in 1955 and died in 1999, aged 84."]),
    ("1960", "John F. Kennedy Jr.", "Lawyer and publisher", [
        "Son of President Kennedy, he was photographed saluting his father’s coffin in 1963 – on his third birthday.",
        "He later worked as a New York prosecutor and founded George magazine in 1995. He died in a plane crash in 1999.",
        "In 1988 People magazine named him the \u201cSexiest Man Alive\u201d."]),
    ("1971", "Christina Applegate", "Actress", [
        "She found fame as Kelly Bundy in the long-running sitcom Married… with Children.",
        "She went on to win an Emmy for Friends, starred in Anchorman, and earned acclaim for Netflix’s dark comedy Dead to Me.",
        "She also earned a Tony nomination for the Broadway revival of Sweet Charity in 2005."]),
    ("1981", "Xabi Alonso", "Footballer and manager", [
        "The Basque midfielder won the Champions League with Liverpool in 2005 and Real Madrid in 2014, plus the World Cup and two Euros with Spain.",
        "As a manager he led Bayer Leverkusen to an unbeaten Bundesliga title in 2024.",
        "After a short spell in charge of Real Madrid, he became Chelsea manager in July 2026."]),
]

remembered = [
    ("1974", "Nick Drake", "Singer-songwriter", [
        "The English folk singer released three albums – Five Leaves Left, Bryter Layter and Pink Moon – which sold poorly in his lifetime.",
        "He died aged just 26. Decades later his gentle, haunting songs found the audience they deserved.",
        "In 1999 his song Pink Moon reached a new generation when it featured in a Volkswagen advert."]),
    ("2005", "George Best", "Footballer", [
        "Born in Belfast, he became Manchester United’s brightest star, winning the European Cup and the Ballon d’Or in 1968.",
        "Dazzling, daring and impossible to tackle, he is still remembered as one of the most gifted players of all time. He died aged 59.",
        "He won 37 caps for Northern Ireland and later played in the United States and Scotland."]),
    ("2016", "Fidel Castro", "Cuban leader", [
        "He led the revolution that took power in Cuba in 1959 and ruled the island for almost half a century.",
        "One of the most divisive figures of the Cold War, he handed power to his brother Raúl in 2008. He died aged 90.",
        "His death brought mourning in Havana and celebrations among Cuban exiles in Miami."]),
    ("2020", "Diego Maradona", "Footballer", [
        "He captained Argentina to the 1986 World Cup – scoring both the “Hand of God” and the “Goal of the Century” against England in a single match.",
        "He also led Napoli to two Serie A titles. He died aged 60, fifteen years to the day after George Best.",
        "In 2000 he was named joint FIFA Player of the Century alongside Pel\u00e9."]),
]

if __name__ == "__main__":
    for i, (yr, name, role, bio) in enumerate(born, 1):
        person_page(f"out/born_{i+1:02d}_{name.split()[-1].lower().strip('.')}.png", "BIRTHDAYS",
                    "BORN ON THIS DAY", RED, name, role, bio, i + 1, len(born) + 1)
    for i, (yr, name, role, bio) in enumerate(remembered, 1):
        person_page(f"out/remembered_{i+1:02d}_{name.split()[-1].lower()}.png", "REMEMBRANCE",
                    "DIED ON THIS DAY", INK, name, role, bio, i + 1, len(remembered) + 1)
