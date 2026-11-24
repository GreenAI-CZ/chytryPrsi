"""Zadní strana a rámeček karet s pravidly přes Codex (ChatGPT předplatné). usage: python3 extra.py [zadni-strana] [pravidla-ramec]"""
import os, sys
from concurrent.futures import ThreadPoolExecutor
import deck

COMMON = """Design for the original Czech card deck "Chytré prší" (Clever Prší). Portrait 2:3, filling the whole canvas edge to edge.
NO outer border shadow, NO rounded corners, NO mockup, nothing outside the card. NO letters, NO words, NO numbers anywhere.
Flat vector illustration with bold black ink outlines (#1d1a17), mid-century folk-poster feel, flat colour fills.
Limited palette only: ink #1d1a17, cream #fffaf0, red #c8322b, green #2f7a3a, acorn brown #8a5a22, ochre/gold #d99a1e,
dark green #1f4d33. NO glow, NO gradient, NO texture.
Suit symbols in the deck style: red heart, green linden leaf with cream veins, brown acorn with cross-hatched cap,
round ochre sleigh bell with cream band and black slit.
"""
ITEMS = {
    "zadni-strana": COMMON + """CARD BACK. A dense, regular all-over folk ornament pattern in deep red #c8322b and cream with thin ink lines:
small repeated motifs of the four suit symbols (heart, leaf, acorn, bell) alternating with tiny flowers and little lightbulb
sparks, arranged in a tidy diamond lattice. The design must look IDENTICAL when rotated 180 degrees (point-symmetric),
so every card back looks the same in both orientations. A cream margin frame about 5% wide with a thin red double line
runs around the edge. In the exact center a large EMPTY plain cream oval cartouche (about 60% of the card width) with a
thin ink and gold double outline and small ornaments around it; the inside of the oval stays completely blank.""",
    "pravidla-ramec": COMMON + """A RULE CARD FRAME. Plain cream #fffaf0 card with a narrow decorative folk border (about 6% of the width)
made of a thin ink double line with small leaves and flowers. In the four corners one suit symbol each: heart top-left,
leaf top-right, acorn bottom-left, bell bottom-right, small. The whole inside (about 85% of the card) stays COMPLETELY
EMPTY plain cream for printed text later: no drawings, no lines, no lightbulbs inside the frame.""",
}

def gen(name):
    # Stejné volání jako u balíčku, jen s vlastním zadáním místo karty.
    deck.STYLE = ""
    return deck.gen((name, ITEMS[name], os.path.join(deck.HERE, "balicek")))

if __name__ == "__main__":
    names = sys.argv[1:] or list(ITEMS)
    with ThreadPoolExecutor(len(names)) as ex:
        for line in ex.map(gen, names):
            print(line, flush=True)
