"""Pravidla Chytrého prší na jedné A4 -> downloads/chytre-prsi-pravidla.pdf

Texty vycházejí z karet s pravidly (design/karty/tisk.py) a z webu.
Spuštění:  python3 pravidla.py   (potřebuje Google Chrome a internet kvůli fontům)
"""
import pathlib, subprocess

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parent.parent
OUT_PDF = ROOT / "downloads" / "chytre-prsi-pravidla.pdf"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

SYMBOLS = """<svg width="0" height="0" style="position:absolute"><defs>
<symbol id="s-srdce" viewBox="0 0 32 32"><path d="M16 28C6 20 2 15 2 10a7 7 0 0 1 14-2 7 7 0 0 1 14 2c0 5-4 10-14 18z" fill="currentColor"/></symbol>
<symbol id="s-listy" viewBox="0 0 32 32"><path d="M16 2c8 6 12 12 10 20-2 5-6 7-10 8-4-1-8-3-10-8C4 14 8 8 16 2z" fill="currentColor"/>
<path d="M16 7v23M16 14l-5 4M16 14l5 4M16 21l-6 3M16 21l6 3" stroke="#fffaf0" stroke-width="1.6" fill="none" stroke-linecap="round"/></symbol>
<symbol id="s-zaludy" viewBox="0 0 32 32"><path d="M15 1h2v4h-2z" fill="currentColor"/><path d="M5 14c0-6 5-10 11-10s11 4 11 10z" fill="currentColor"/>
<path d="M8 15h16c0 8-4 13-8 15-4-2-8-7-8-15z" fill="currentColor" opacity=".75"/></symbol>
<symbol id="s-kule" viewBox="0 0 32 32"><circle cx="16" cy="16" r="13" fill="currentColor"/><path d="M4 14h24" stroke="#fffaf0" stroke-width="2"/>
<circle cx="16" cy="22" r="2.5" fill="#fffaf0"/></symbol></defs></svg>"""

IDEAS = [
    ("listy", "Zelený král", "Přebije sedmičku, sedmička ho ne. Za krále se líže 4."),
    ("srdce", "Uno", "S poslední kartou v ruce řekni „Uno“. Kdo zapomene, líže."),
    ("zaludy", "Spodek", "Spodek mění hodnotu karty."),
    ("kule", "Rychlé prší", "Víc karet stejné hodnoty se smí vyložit naráz."),
    ("listy", "Změna směru", "Vybraná karta otáčí směr hry."),
    ("srdce", "Červená sedmička", "Vrací do hry, má-li ji hráč po vítězi."),
    ("zaludy", "Výměna karet", "Vybraná karta dovolí vyměnit si karty s jiným hráčem."),
    ("kule", "Duha", "Máš od každé barvy jednu? Řekni „Duha“ a vylož všechny čtyři."),
    ("listy", "Vyrušení", "Vybraná karta ruší efekt právě zahrané karty."),
]

SMART = [
    ("Vítěz určuje", "Po každém kole přidá ten, kdo vyhrál, jedno nové pravidlo."),
    ("Všichni souhlasí", "Nové pravidlo musí schválit všichni u stolu, aby nezkazilo hru."),
    ("Nedohrává se", "Jakmile jeden hráč vyhraje, kolo končí. O druhé místo se nehraje."),
    ("Připomínejte", "Před každým kolem se nahlas zopakují všechna dosavadní pravidla."),
    ("Nepozornost se trestá", "Kdo neví, že je na tahu, nebo pravidlo nezná či nesplní, líže kartu. Napoprvé může být varování."),
    ("Nepodvádějte", "Koukat do karet je snadné. Ale o tom tahle hra není."),
]

def sym(s):
    return f'<svg class="sym sym--{s}"><use href="#s-{s}"/></svg>'

def main():
    smart = "".join(f'<li><b>{t}.</b> {d}</li>' for t, d in SMART)
    ideas = "".join(f'<div class="idea">{sym(s)}<div><b>{t}</b><br>{d}</div></div>' for s, t, d in IDEAS)
    html = f"""<!doctype html><html lang="cs"><head><meta charset="utf-8"><title>Chytré prší – pravidla</title>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,800;9..144,900&family=Work+Sans:wght@400;600;700&display=swap&subset=latin-ext" rel="stylesheet">
<style>
@page {{ size: A4; margin: 0; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font: 9.4pt/1.38 'Work Sans', sans-serif; color: #1d1a17; }}
.page {{ width: 210mm; height: 297mm; padding: 12mm 14mm 10mm; display: flex; flex-direction: column; gap: 4.2mm; overflow: hidden; }}
h1, h2 {{ font-family: 'Fraunces', serif; font-weight: 900; line-height: 1; letter-spacing: -.01em; }}
h1 {{ font-size: 40pt; letter-spacing: -.02em; }}
h2 {{ font-size: 15pt; margin-bottom: 2mm; display: flex; align-items: baseline; gap: 2.5mm; }}
h2 small {{ font: 700 6.8pt 'Work Sans', sans-serif; letter-spacing: .14em; text-transform: uppercase; color: #c8322b; }}
.eyebrow {{ font-weight: 700; font-size: 7pt; letter-spacing: .16em; text-transform: uppercase; color: #c8322b; margin-bottom: 2mm; }}
.head {{ display: grid; grid-template-columns: 1fr 62mm; gap: 6mm; align-items: center; border-bottom: .5mm solid #1d1a17; padding-bottom: 4mm; }}
.lead {{ font-size: 10.5pt; margin-top: 2.5mm; max-width: 112mm; }}
.fan {{ position: relative; height: 40mm; }}
.fan img {{ position: absolute; width: 22mm; top: 4mm; left: 20mm; border: .35mm solid #1d1a17; border-radius: 1.6mm;
  box-shadow: .8mm .8mm 0 #1d1a17; transform-origin: 50% 120%; }}
.fan img:nth-child(1) {{ transform: rotate(-22deg) translateX(-6mm); }}
.fan img:nth-child(2) {{ transform: rotate(-7deg) translateX(-2mm); }}
.fan img:nth-child(3) {{ transform: rotate(8deg) translateX(2mm); }}
.fan img:nth-child(4) {{ transform: rotate(23deg) translateX(6mm); }}
.cols {{ display: grid; grid-template-columns: 1fr 1fr; gap: 7mm; }}
.box {{ background: #f4ead5; border-radius: 2.5mm; padding: 3.2mm 4mm; }}
ul, ol {{ list-style: none; }}
.dots li {{ padding-left: 4mm; position: relative; margin-bottom: .9mm; }}
.dots li::before {{ content: ""; position: absolute; left: .5mm; top: 1.9mm; width: 1.4mm; height: 1.4mm; border-radius: 50%; background: #c8322b; }}
.facts {{ display: grid; grid-template-columns: auto 1fr; gap: .8mm 3mm; }}
.facts dt {{ font-weight: 700; }}
.sym {{ width: 3.6mm; height: 3.6mm; flex: none; }}
.sym--srdce {{ color: #c8322b; }} .sym--listy {{ color: #2f7a3a; }} .sym--zaludy {{ color: #8a5a22; }} .sym--kule {{ color: #d99a1e; }}
.suits {{ display: flex; flex-wrap: wrap; gap: 1mm 3mm; align-items: center; }}
.suits span {{ display: inline-flex; align-items: center; gap: 1mm; }}
.special {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 4mm; }}
.sp {{ display: flex; gap: 3mm; align-items: flex-start; }}
.sp img {{ width: 15mm; border: .3mm solid #1d1a17; border-radius: 1.2mm; flex: none; }}
.sp b {{ font: 800 11pt/1.1 'Fraunces', serif; display: block; margin-bottom: .6mm; }}
.smart {{ counter-reset: n; display: grid; grid-template-columns: 1fr 1fr; gap: 1.6mm 7mm; }}
.smart li {{ counter-increment: n; padding-left: 7mm; position: relative; }}
.smart li::before {{ content: counter(n); position: absolute; left: 0; top: -.2mm; width: 5mm; height: 5mm; border-radius: 50%;
  background: #1d1a17; color: #fffaf0; font: 800 8pt/5mm 'Fraunces', serif; text-align: center; }}
.note {{ display: grid; grid-template-columns: 1fr 1fr; gap: 7mm; margin-top: 2.5mm; }}
.note p {{ border-left: .8mm solid #c8322b; padding-left: 2.5mm; }}
.ideas {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 2.4mm 5mm; font-size: 8.6pt; line-height: 1.3; }}
.idea {{ display: flex; gap: 2mm; align-items: flex-start; }}
.idea .sym {{ margin-top: .4mm; }}
.own {{ margin-top: 2.4mm; font-style: italic; color: #6b5f52; }}
.foot {{ margin-top: auto; border-top: .3mm solid #1d1a17; padding-top: 2mm; display: flex; justify-content: space-between; font-size: 7.4pt; color: #6b5f52; }}
.foot b {{ color: #1d1a17; }}
</style></head><body>{SYMBOLS}
<div class="page">
  <header class="head">
    <div>
      <p class="eyebrow">Karetní hra pro partu kamarádů</p>
      <h1>Chytré prší</h1>
      <p class="lead">Klasické prší, které si pamatuje. Začíná se podle základních pravidel pomalého prší, po každém kole ale
      vítěz přidá jedno nové pravidlo. Všechna pravidla platí dál — a kdo zapomene, líže.</p>
    </div>
    <div class="fan"><img src="img/srdce-7.jpg"><img src="img/listy-svrsek.jpg"><img src="img/zaludy-kral.jpg"><img src="img/kule-eso.jpg"></div>
  </header>

  <section class="cols">
    <div class="box">
      <h2>Co potřebujete</h2>
      <dl class="facts">
        <dt>Karty</dt><dd>Jeden balíček mariášek, 32 karet, jednohlavé i dvouhlavé. Pro 5 a více hráčů dva balíčky.</dd>
        <dt>Barvy</dt><dd class="suits"><span>{sym('srdce')}srdce</span><span>{sym('listy')}listy</span><span>{sym('zaludy')}žaludy</span><span>{sym('kule')}kule</span></dd>
        <dt>Hodnoty</dt><dd>7, 8, 9, 10, spodek, svršek, král, eso</dd>
      </dl>
    </div>
    <div>
      <h2>Jak se hraje <small>pomalé prší</small></h2>
      <ul class="dots">
        <li>Každý dostane <b>4 karty</b>, zbytek je balíček a vrchní karta se otočí.</li>
        <li>Začíná nejmladší hráč (nebo los), hraje se <b>po směru hodin</b>.</li>
        <li>Na vyloženou kartu dáte kartu <b>stejné barvy</b> nebo <b>stejné hodnoty</b>.</li>
        <li>Když nemůžete, líznete si jednu kartu z balíčku.</li>
        <li><b>Cíl:</b> zbavit se všech karet.</li>
      </ul>
    </div>
  </section>

  <section>
    <h2>Speciální karty</h2>
    <div class="special">
      <div class="sp"><img src="img/srdce-7.jpg"><div><b>Sedmička</b>Další hráč líže 2 karty. Lze ji přebít sedmičkou — pak se líže 2 za každou zahranou.</div></div>
      <div class="sp"><img src="img/listy-svrsek.jpg"><div><b>Svršek</b>Jde na cokoli kromě sedmičky a esa. Kdo ho zahraje, určí novou barvu.</div></div>
      <div class="sp"><img src="img/kule-eso.jpg"><div><b>Eso</b>Další hráč jedno kolo stojí (přeskočí tah). Lze ho přebít dalším esem.</div></div>
    </div>
  </section>

  <section class="box">
    <h2>Chytrá pravidla <small>co z prší dělá chytré prší</small></h2>
    <ol class="smart">{smart}</ol>
    <div class="note">
      <p><b>Kdy hra končí?</b> Hraje se, dokud si všichni pravidla pamatují. Obvykle to bývá 4–8 chytrých pravidel.</p>
      <p><b>Co kazí hru:</b> pravidla, která vracejí do hry víc než jednou kartou, a pravidla, kvůli kterým se líže moc často.</p>
    </div>
  </section>

  <section>
    <h2>Inspirace <small>návrhy chytrých pravidel</small></h2>
    <div class="ideas">{ideas}</div>
    <p class="own">Nejlepší pravidla jsou ale ta, která si vymyslíte sami. Hlavně ať je schválí všichni u stolu.</p>
  </section>

  <footer class="foot">
    <span><b>chytryprsi.cz</b> · karty k tisku a další inspirace na webu</span>
    <span>Text pravidel: CC BY-SA 4.0</span>
  </footer>
</div></body></html>"""
    (HERE / "pravidla.html").write_text(html)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=15000",
                    f"--print-to-pdf={OUT_PDF}", (HERE / "pravidla.html").as_uri()], check=True, capture_output=True)
    print(OUT_PDF)

if __name__ == "__main__":
    main()
