"""QR platba (SPAYD) na příspěvek -> img/qr-platba.svg

Potřebuje knihovnu segno (pip install segno), na web jde jen hotové SVG.
Spuštění:  python3 qr_platba.py
"""
import pathlib
import segno

ROOT = pathlib.Path(__file__).resolve().parents[2]

ACCOUNT = "6761768329/0800"
AMOUNT = "1.00"
VS = "111222333"
# Bez diakritiky: ne každá bankovní aplikace ji ve zprávě z QR přečte.
MESSAGE = "Mam napad na nove pravidlo chytreho prsi"

def iban(account: str) -> str:
    number, bank = account.split("/")
    prefix, _, base = number.rpartition("-")
    bban = bank + prefix.zfill(6) + base.zfill(10)
    check = 98 - int(bban + "123500") % 97   # "CZ00" -> C=12, Z=35
    return f"CZ{check:02d}{bban}"

def spayd() -> str:
    return f"SPD*1.0*ACC:{iban(ACCOUNT)}*AM:{AMOUNT}*CC:CZK*MSG:{MESSAGE}*X-VS:{VS}"

if __name__ == "__main__":
    data = spayd()
    print(data)
    qr = segno.make(data, error="m", micro=False)
    out = ROOT / "img" / "qr-platba.svg"
    qr.save(out, kind="svg", scale=1, border=2, dark="#1d1a17", light="#fffaf0", xmldecl=False, svgclass=None, lineclass=None)
    # Pevnou velikost nahradit viewBoxem, aby se SVG dalo na webu libovolně zvětšit.
    n = qr.symbol_size(scale=1, border=2)[0]
    svg = out.read_text().replace(f'width="{n}" height="{n}"',
        f'viewBox="0 0 {n} {n}" shape-rendering="crispEdges" role="img" aria-label="QR platba"', 1)
    out.write_text(svg)
    print(out, qr.version, qr.error)
