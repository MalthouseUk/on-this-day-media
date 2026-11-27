from style import *
H = PAGE_H   # 4:5 portrait pages
from dates import life

def page(fname, section, kick, headline, standfirst, people, band=False, accent=INK):
    img = paper(H); d = ImageDraw.Draw(img)
    masthead(d, section)
    # headline block
    if band:
        d.rectangle([M, 212, W - M, 396], fill=band)
        kicker(d, 226, kick, PAPER)
        centred(d, 246, headline, font(P_BLACK, 104), PAPER)
    else:
        kicker(d, 226, kick, accent)
        centred(d, 246, headline, font(P_BLACK, 104), INK)
    centred(d, 406, standfirst, font(P_ITAL, 30), GREY)
    d.line([M, 456, W - M, 456], fill=INK, width=2)
    # two-column grid with column rule
    rows = (len(people) + 1) // 2
    top, bottom = 470, H - 86
    rh = (bottom - top) / rows
    colw = (W - 2 * M - 48) / 2
    d.line([W / 2, top + 6, W / 2, bottom - 10], fill=HAIR, width=1)
    for i, (yr, name, note) in enumerate(people):
        r, c = i // 2, i % 2
        x = M + c * (colw + 48)
        y = top + r * rh + 8
        big = rows <= 2
        ys, ns, bs = (30, 62, 36) if big else (26, 50, 31)
        if big: y += 20
        spaced(d, x, y + 2, life(name, short=True), font(OLD_B, ys - 4), accent, 2)
        nf = font(P_BOLD, ns)
        while d.textlength(name, font=nf) > colw - 24:
            nf = font(P_BOLD, nf.size - 2)
        d.text((x, y + ys + 6), name, font=nf, fill=INK)
        ny = y + ys + ns + 22
        for ln in wrap(d, note, font(BASK, bs), colw):
            d.text((x, ny), ln, font=font(BASK, bs), fill=GREY); ny += bs * 1.45
        if r < rows - 1:
            d.line([x, top + (r + 1) * rh - 6, x + colw, top + (r + 1) * rh - 6], fill=HAIR, width=1)
    footer(d, H)
    img.save(fname)

if __name__ == "__main__":
    page("out/born_25nov.png", "BIRTHDAYS", "BORN ON THIS DAY", "Happy Birthday",
         "Six remarkable lives that began on 25 November", [
        ("1835", "Andrew Carnegie", "The Scottish-born steel magnate who gave away a fortune"),
        ("1844", "Karl Benz", "Built what is widely seen as the first true motor car"),
        ("1914", "Joe DiMaggio", "Yankees legend, famed for his 56-game hitting streak"),
        ("1960", "John F. Kennedy Jr.", "Lawyer, magazine publisher and son of a president"),
        ("1971", "Christina Applegate", "Star of Married… with Children and Dead to Me"),
        ("1981", "Xabi Alonso", "Champions League winner with Liverpool and Real Madrid"),
    ], band=(140, 24, 30), accent=(150, 28, 32))

    page("out/remembered_25nov.png", "REMEMBRANCE", "DIED ON THIS DAY", "We Remember",
         "Those we lost on 25 November", [
        ("1974", "Nick Drake", "The singer-songwriter whose music found its audience after his death"),
        ("2005", "George Best", "The Belfast boy who lit up Old Trafford"),
        ("2016", "Fidel Castro", "Revolutionary who led Cuba for nearly fifty years"),
        ("2020", "Diego Maradona", "Died fifteen years to the day after George Best"),
    ], band=INK)
