"""Tiskový arch karet Chytré prší -> downloads/chytre-prsi-karty.pdf

A4, 3 x 3 karty 57 x 89 mm (mariášky), ořezové značky a vodicí čáry.
Každý list = jedna barva (8 karet) + jedna karta s pravidly. Za každou lícovou stranou
následuje rub zrcadlově (tisk oboustranně, otáčet po delší straně).
Spuštění:  python3 tisk.py   (potřebuje Google Chrome a internet kvůli fontům)
"""
import pathlib, subprocess

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parent.parent
OUT_PDF = ROOT / "downloads" / "chytre-prsi-karty.pdf"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

W, H, COLS, ROWS = 57, 89, 3, 3
SUITS = ["srdce", "kule", "listy", "zaludy"]
RANKS = ["7", "8", "9", "10", "spodek", "svrsek", "kral", "eso"]

RULES = [
    ("Co je chytré prší", "úvod", """
<p>Prší zná každý — jenže každý trochu jinak. Než se parta domluví, jak se vlastně hraje, je po večeru.</p>
<p><b>Chytré prší</b> začíná podle základních pravidel pomalého prší, která jsou pro všechny stejná.</p>
<h4>1. Hrajte pomalé prší</h4><p>První kolo podle základních pravidel.</p>
<h4>2. Vítěz vymyslí pravidlo</h4><p>Kdo se první zbaví karet, přidá nové chytré pravidlo. Ostatní ho musí schválit.</p>
<h4>3. Pamatujte si všechno</h4><p>Všechna pravidla platí dál. Kdo zapomene, líže.</p>
"""),
    ("Základní pravidla", "pomalé prší", """
<p>Každý dostane <b>4 karty</b>, zbytek je balíček, vrchní karta se otočí. Začíná nejmladší, hraje se po směru hodin.</p>
<p><b>Cíl:</b> zbavit se všech karet.</p>
<p>Na vyloženou kartu dáte kartu <b>stejné barvy</b> nebo <b>stejné hodnoty</b>. Když nemůžete, líznete si jednu.</p>
<h4>Sedmička</h4><p>Další hráč líže 2. Lze přebít sedmičkou — pak líže 2 za každou zahranou.</p>
<h4>Svršek</h4><p>Jde na cokoli kromě sedmičky a esa. Kdo ho zahraje, určí barvu.</p>
<h4>Eso</h4><p>Další hráč stojí. Lze přebít esem.</p>
"""),
    ("Chytrá pravidla", "co z prší dělá chytré prší", """
<p><b>Vítěz určuje.</b> Po každém kole přidá ten, kdo vyhrál, jedno nové pravidlo.</p>
<p><b>Všichni souhlasí.</b> Nové pravidlo musí schválit všichni u stolu.</p>
<p><b>Nedohrává se.</b> Jakmile někdo vyhraje, kolo končí.</p>
<p><b>Připomínejte.</b> Před každým kolem se nahlas zopakují všechna pravidla.</p>
<p><b>Nepozornost se trestá.</b> Kdo neví, že je na tahu, nebo pravidlo nezná či nesplní, líže kartu.</p>
<p><b>Nepodvádějte.</b> Do karet se nekouká.</p>
<p class="muted">Hraje se, dokud si pravidla pamatujete — obvykle 4–8. Hru kazí pravidla, kvůli kterým se líže moc často.</p>
"""),
    ("Inspirace", "návrhy chytrých pravidel", """
<p><b>Zelený král</b> přebije sedmičku, za krále líže 4.</p>
<p><b>Uno:</b> s poslední kartou řekni „Uno“, jinak líznutí.</p>
<p><b>Spodek</b> mění hodnotu karty.</p>
<p><b>Rychlé prší:</b> víc karet stejné hodnoty naráz.</p>
<p><b>Změna směru:</b> vybraná karta otáčí směr hry.</p>
<p><b>Červená sedmička</b> vrací do hry, má-li ji hráč po vítězi.</p>
<p><b>Výměna karet</b> s jiným hráčem za vybranou kartu.</p>
<p><b>Vyrušení:</b> vybraná karta ruší efekt právě zahrané.</p>
<p><b>Nelze vyhrát svrškem.</b> Kdo dohraje svrškem, líže.</p>
<p><b>Tichá osmička:</b> po osmičce se mlčí do další osmičky, kdo promluví, líže.</p>
<p class="muted">Nejlepší pravidla si ale vymyslíte sami.</p>
"""),
]

def front(name):
    return f'<div class="card"><img src="tisk/{name}.jpg"></div>'

def rule_card(title, sub, body):
    tight = " rule--tight" if body.count("<p") > 8 else ""
    return (f'<div class="card rule{tight}"><img src="tisk/pravidla-ramec.jpg"><div class="rule__in">'
            f'<h3>{title}</h3><p class="sub">{sub}</p>{body}<p class="foot">chytryprsi.cz</p></div></div>')

BACK = ('<div class="card back"><img src="tisk/zadni-strana.jpg">'
        '<div class="logo"><span>Chytré</span><span>prší</span></div></div>')
EMPTY = '<div class="card empty"></div>'

def lines():
    gx, gy = (210 - COLS * W) / 2, (297 - ROWS * H) / 2
    gw, gh = COLS * W, ROWS * H
    out = []
    def box(cls, x, y, w, h):
        out.append(f'<i class="ln ln--{cls}" style="left:{x:.3f}mm;top:{y:.3f}mm;width:{w:.3f}mm;height:{h:.3f}mm"></i>')
    for c in range(COLS + 1):
        x = gx + c * W
        box("guide", x - .1, gy, .2, gh)                 # vodicí čára přes celou výšku
        box("mark", x - .1, gy - 10, .2, 7)                 # značka nahoře
        box("mark", x - .1, gy + gh + 3, .2, 7)             # značka dole
    for r in range(ROWS + 1):
        y = gy + r * H
        box("guide", gx, y - .1, gw, .2)
        box("mark", gx - 10, y - .1, 7, .2)
        box("mark", gx + gw + 3, y - .1, 7, .2)
    return "".join(out)

def page(cells, cls=""):
    return f'<section class="sheet {cls}"><div class="grid">{"".join(cells)}</div>{lines()}</section>'

def main():
    # Na každém listu jedna barva (8 karet) a jako devátá jedna karta s pravidly.
    per = COLS * ROWS
    pages = []
    for suit, rule in zip(SUITS, RULES):
        chunk = [front(f"{suit}-{r}") for r in RANKS] + [rule_card(*rule)]
        chunk += [EMPTY] * (per - len(chunk))
        pages.append(page(chunk))
        # Rub: v každém řádku obrácené pořadí, aby po otočení listu po delší straně seděl pod lícem.
        backs = [BACK if chunk[r * COLS + c] != EMPTY else EMPTY
                 for r in range(ROWS) for c in reversed(range(COLS))]
        pages.append(page(backs, "sheet--back"))

    gw, gh = COLS * W, ROWS * H
    html = f"""<!doctype html><html lang="cs"><head><meta charset="utf-8"><title>Chytré prší – karty k tisku</title>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,800;9..144,900&family=Work+Sans:wght@400;600;700&display=swap&subset=latin-ext" rel="stylesheet">
<style>
@page {{ size: A4; margin: 0; }}
* {{ box-sizing: border-box; margin: 0; }}
body {{ font-family: 'Work Sans', sans-serif; color: #1d1a17; }}
.sheet {{ width: 210mm; height: 297mm; position: relative; page-break-after: always; overflow: hidden; }}
.grid {{ position: absolute; left: {(210 - gw) / 2}mm; top: {(297 - gh) / 2}mm;
  display: grid; grid-template-columns: repeat({COLS}, {W}mm); grid-template-rows: repeat({ROWS}, {H}mm); }}
/* Čáry jako samostatné prvky: opakovaný gradient se v PDF dlaždicuje a prohlížeče z něj
   některé čáry zahodí. Ořezové značky černé v okraji, vodicí čáry světlé přes karty. */
.ln {{ position: absolute; z-index: 2; }}
.ln--mark {{ background: #000; }}
.ln--guide {{ background: #9a8f7d; }}
.card {{ position: relative; width: {W}mm; height: {H}mm; overflow: hidden; }}
.card img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
.back .logo {{ position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center;
  font: 900 9.5mm/0.95 'Fraunces', serif; letter-spacing: -.02em; color: #1d1a17; }}
.back .logo span + span {{ color: #c8322b; }}
.rule__in {{ position: absolute; inset: 7mm 6.5mm 6.5mm; display: flex; flex-direction: column; font-size: 6.6pt; line-height: 1.28; }}
.rule h3 {{ font: 900 13pt/1 'Fraunces', serif; text-align: center; }}
.rule .sub {{ text-align: center; text-transform: uppercase; letter-spacing: .12em; font-size: 5pt; font-weight: 700; color: #c8322b; margin: 1mm 0 2mm; }}
.rule p {{ margin-bottom: 1.1mm; }}
.rule h4 {{ font: 800 8pt/1 'Fraunces', serif; margin: 1.4mm 0 .5mm; }}
.rule .muted {{ color: #6b5f52; font-style: italic; }}
.rule--tight .rule__in {{ font-size: 6.1pt; line-height: 1.22; }}
.rule--tight p {{ margin-bottom: .8mm; }}
.rule .foot {{ margin-top: auto; text-align: center; font-size: 5pt; letter-spacing: .1em; color: #6b5f52; }}
</style></head><body>{''.join(pages)}</body></html>"""
    (HERE / "tisk.html").write_text(html)
    OUT_PDF.parent.mkdir(exist_ok=True)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=15000",
                    f"--print-to-pdf={OUT_PDF}", (HERE / "tisk.html").as_uri()], check=True, capture_output=True)
    print(OUT_PDF)

if __name__ == "__main__":
    main()
