
DATES = {
    "Andrew Carnegie": ("25 November 1835", "11 August 1919"),
    "Karl Benz": ("25 November 1844", "4 April 1929"),
    "Joe DiMaggio": ("25 November 1914", "8 March 1999"),
    "John F. Kennedy Jr.": ("25 November 1960", "16 July 1999"),
    "Christina Applegate": ("25 November 1971", None),
    "Xabi Alonso": ("25 November 1981", None),
    "Nick Drake": ("19 June 1948", "25 November 1974"),
    "George Best": ("22 May 1946", "25 November 2005"),
    "Fidel Castro": ("13 August 1926", "25 November 2016"),
    "Diego Maradona": ("30 October 1960", "25 November 2020"),
    "Willis Carrier": ("26 November 1876", "7 October 1950"),
    "Charles M. Schulz": ("26 November 1922", "12 February 2000"),
    "Tina Turner": ("26 November 1939", "24 May 2023"),
    "John McVie": ("26 November 1945", None),
    "Rita Ora": ("26 November 1990", None),
    "Danny Welbeck": ("26 November 1990", None),
    "John Loudon McAdam": ("21 September 1756", "26 November 1836"),
    "Sojourner Truth": ("c. 1797", "26 November 1883"),
    "Michael Bentine": ("26 January 1922", "26 November 1996"),
    "Stephen Sondheim": ("22 March 1930", "26 November 2021"),
}
def life(name, short=False):
    b, d = DATES[name]
    if short:
        f = lambda s: " ".join(w[:3] if i == 1 and w.isalpha() else w for i, w in enumerate(s.split()))
        b = f(b); d = f(d) if d else None
    return f"BORN {b}".upper() if not d else f"{b} \u2013 {d}".upper()
