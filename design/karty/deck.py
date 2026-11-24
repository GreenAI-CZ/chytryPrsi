"""Balíček Chytré prší přes Codex CLI (ChatGPT předplatné). usage: python3 deck.py OUTDIR [card ...]"""
import base64, json, os, sys, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor

STYLE = """Design ONE playing-card face for an original Czech single-headed "mariášky" deck (32 German-suited cards)
made for the party card game "Chytré prší" (Clever Prší). Portrait card face filling the whole canvas edge to edge.
NO outer border line, NO rounded corners, NO drop shadow, NO mockup, NO table, nothing outside the card.
Keep everything important inside the central 88% width (the sides may be cropped slightly).

Layout rules of Czech single-headed mariášky (follow strictly):
- The card is SINGLE-HEADED (one upright picture, NOT mirrored, NOT double-ended, no center dividing line).
- There are NO corner indices: NO letters, NO numbers, NO words anywhere on the card
  (the only exception: the ten has a Roman numeral "X" at the top center).
- The rank is recognised only from the layout of the suit symbols and the picture, as described for this card below.
- Number cards (7, 8, 9, 10) have a small illustrated vignette at the bottom standing on a strip of green grass ground.

Art direction (must match the website and the whole deck):
- Flat vector illustration with bold confident black ink outlines (#1d1a17), mid-century folk-poster feel,
  crisp, flat colour fills, at most a tiny bit of hatching. Friendly, witty, characterful.
- Background: SOLID FLAT warm cream #fffaf0. NO glow, NO gradient, NO vignette, NO dark background, NO texture.
- Limited palette only: ink #1d1a17, cream #fffaf0, paper #f4ead5, red #c8322b, green #2f7a3a,
  acorn brown #8a5a22, ochre/gold #d99a1e, dark green #1f4d33, skin tone peach.
- Suit symbols (identical style on every card of the deck):
  hearts = bold red heart; leaves = green linden-like leaf with cream veins and short stem;
  acorns = brown acorn with darker cross-hatched cap; bells = round ochre/gold sleigh bell with a cream band and a
  black slit, small loop on top.
- Theme of the deck: every card hides one small witty detail about inventing new rules (round spectacles, a pencil,
  a folded rule note, a lightbulb spark). Any notes, scrolls, books or papers show ONLY wavy scribble lines,
  NEVER readable letters or words. Characters and scenes are ORIGINAL, not copied from any existing deck.
"""

SUITS = {
    "srdce": ("hearts", "red hearts"),
    "kule": ("bells", "ochre/gold bells"),
    "listy": ("leaves", "green leaves"),
    "zaludy": ("acorns", "brown acorns"),
}

PIPS = {
    7: "EXACTLY 7 {sym}: one centered at the top, then a left column of 3 and a right column of 3. Count: 1+3+3 = 7.",
    8: "EXACTLY 8 {sym}: a left column of 4 and a right column of 4. Count: 4+4 = 8.",
    9: "EXACTLY 9 {sym}: three columns of 3 (a 3x3 grid). Count: 3+3+3 = 9.",
    10: "A bold black serif Roman numeral \"X\" at the top center, then EXACTLY 10 {sym}: left column of 4, "
        "middle column of 2, right column of 4. Count: 4+2+4 = 10.",
}
PLANT = (" For leaves and acorns the symbols grow on a stylised folk plant: a central green stem with short branches, "
         "each branch ending in one symbol, still in the described column arrangement.")

VIGNETTES = {
    ("srdce", 7): "a heart-shaped potted rosebush; one of the hearts above wears tiny round spectacles",
    ("srdce", 8): "a little fountain with a small owl in spectacles perched on its rim",
    ("srdce", 9): "a striped market tent with a folded rule note pinned to it",
    ("srdce", 10): "a cheeky cupid shooting an arrow that carries a folded rule note",
    ("kule", 7): "a potted sunflower with a lightbulb spark doodle above it",
    ("kule", 8): "a dog running with a rolled rule note in its mouth",
    ("kule", 9): "a small horse next to a fence, a pencil tucked behind its ear",
    ("kule", 10): "two village musicians, one with a trumpet, one with a drum, reading notes",
    ("listy", 7): "a juggler balancing a pencil on his nose",
    ("listy", 8): "a small elephant wearing round spectacles",
    ("listy", 9): "a goat nibbling a page of rules",
    ("listy", 10): "a fox asleep on an open book",
    ("zaludy", 7): "an old man smoking a pipe while reading a rule note",
    ("zaludy", 8): "a hunter blowing a horn, a pencil in his hat band",
    ("zaludy", 9): "a pheasant pecking at a crumpled rule note",
    ("zaludy", 10): "a squirrel writing with a pencil on a tiny scroll",
}

COURTS = {
    "spodek": ("SPODEK (Unter, the lower knave)",
        "One full-length STANDING figure, single-headed. The suit symbol appears ONLY ONCE, SMALL, at the BOTTOM of the card "
        "near the figure's feet on the green ground (this low position is what marks the spodek). Nothing in the top corners."),
    "svrsek": ("SVRŠEK (Ober, the upper knave)",
        "One full-length STANDING figure, single-headed. The suit symbol appears ONLY ONCE, at the TOP-LEFT corner of the card "
        "above the figure (this high position is what marks the svršek). No symbol at the bottom."),
    "kral": ("KRÁL (King)",
        "A king SEATED on an ornate throne, full figure, single-headed, wearing a crown. The suit symbol appears TWICE, "
        "once in the TOP-LEFT and once in the TOP-RIGHT corner. No symbol at the bottom."),
}
CHARACTERS = {
    ("srdce", "spodek"): "a young troubadour in red and cream playing a lute, a pencil tucked behind his ear",
    ("srdce", "svrsek"): "a romantic poet in a red doublet writing with a big quill on a rule note",
    ("srdce", "kral"): "a kind, cheerful king in red robes reading a rule note through round spectacles",
    ("kule", "spodek"): "a merchant apprentice in ochre and green counting coins into a pouch",
    ("kule", "svrsek"): "an eccentric inventor in an ochre coat holding up a glowing lightbulb, goggles on his hat",
    ("kule", "kral"): "a YOUNG clean-shaven, slim king with short black hair and a thin moustache, ochre and gold robes, "
        "sitting on a simple ochre wooden bench-throne, an abacus on his lap and a money pouch at his side",
    ("listy", "spodek"): "a young gardener in green with a watering can and a pencil behind his ear",
    ("listy", "svrsek"): "a lanky hunter in green with a feathered hat, round spectacles, holding a pencil and a leaf banner",
    ("listy", "kral"): "a tall lean middle-aged king with a long braided red-brown beard and a crown made of twigs and leaves "
        "(no gold), green hooded cloak, sitting on a throne grown from a tree stump with roots, a sprouting staff in hand",
    ("zaludy", "spodek"): "a sturdy woodcutter in brown and red with an axe on his shoulder and a rule note in his belt",
    ("zaludy", "svrsek"): "a scholar in a brown gown with round spectacles holding a thick book of rules",
    ("zaludy", "kral"): "a very stout, bald king with a short dark-brown beard and big rosy cheeks, a small brown fur hat with a "
        "gold crown band, brown and red robes, sitting on a heavy dark-brown carved oak throne, holding an unrolled scroll "
        "of scribbled rules and an acorn scepter",
}
ACES = {
    "srdce": "spring: blossoming tree, swallows and a little cottage",
    "kule": "summer: golden wheat field, sun and a haystack",
    "listy": "autumn: orchard with falling leaves and a basket of apples",
    "zaludy": "winter: small snowy village with a church tower and a sledge",
}

def cards():
    out = {}
    for s, (en, sym) in SUITS.items():
        for n in (7, 8, 9, 10):
            d = f"CARD: number card {n} of {en}. " + PIPS[n].format(sym=sym)
            if s in ("listy", "zaludy"):
                d += PLANT
            d += f" Bottom vignette under the symbols: {VIGNETTES[(s, n)]}."
            out[f"{s}-{n}"] = d
        for r, (name, rule) in COURTS.items():
            out[f"{s}-{r}"] = f"CARD: {name} of {en}. {rule} The figure: {CHARACTERS[(s, r)]}. Each king of the deck looks clearly different (face, age, beard, throne). Suit symbol = {sym[:-1]}."
        out[f"{s}-eso"] = (f"CARD: ACE (eso) of {en}. TWO LARGE {sym} at the top, one in the top-left and one in the top-right. "
            f"Below them a decorative folk-ornament cartouche/crest with flowers and an EMPTY ribbon banner (no text). "
            f"Inside the cartouche a small seasonal scene of {ACES[s]}. A tiny lightbulb spark doodle hidden in the ornament.")
    return out

import glob, shutil, subprocess, time
CODEX = shutil.which("codex") or "/Applications/ChatGPT.app/Contents/Resources/codex-cli/bin/codex"
CODEX_IMAGES = os.path.expanduser("~/.codex/generated_images")
HERE = os.path.dirname(os.path.abspath(__file__))
# Generuje se přes Codex CLI z aplikace ChatGPT = z ChatGPT předplatného. Placené API se nevolá.
# Reference drží styl balíčku jednotný: dvorní karty podle srdcového krále, číselné podle srdcové osmy.
REF_COURT = os.path.join(HERE, "balicek", "srdce-kral.png")
REF_PIP = os.path.join(HERE, "balicek", "srdce-8.png")

def gen(item):
    name, desc, out = item
    # Králové bez srdcového krále jako reference, jinak se propíše jeho tvář i trůn.
    ref = REF_PIP if name.split("-")[1].isdigit() or name in ("kule-kral", "listy-kral", "zaludy-kral") else REF_COURT
    task = ("Use your image generation tool exactly once and do nothing else. "
            "Pass the text between <prompt> tags to it verbatim as the prompt. "
            "Use the attached image only as a STYLE reference (same line work, palette, cream background, "
            "same suit-symbol drawing style); the content must follow the prompt, not copy the reference. "
            "Aspect ratio 2:3 portrait. Reply only with DONE.\n\n<prompt>\n" + STYLE + "\n" + desc + "\n</prompt>")
    err = ""
    for attempt in range(3):
        cmd = [CODEX, "exec", "--skip-git-repo-check", "--json", "-s", "read-only",
               "-c", "model_reasoning_effort=low", "-i", ref]
        p = subprocess.run(cmd, input=task, capture_output=True, text=True, timeout=900)
        thread = None
        for line in p.stdout.splitlines():
            try: ev = json.loads(line)
            except ValueError: continue
            if ev.get("type") == "thread.started": thread = ev["thread_id"]
        pngs = sorted(glob.glob(os.path.join(CODEX_IMAGES, thread or "-", "*.png")), key=os.path.getmtime)
        if pngs:
            shutil.copyfile(pngs[-1], os.path.join(out, name + ".png"))
            return f"ok {name}"
        err = (p.stdout[-400:] + p.stderr[-400:]).replace("\n", " ")
        time.sleep(10)
    return f"FAIL {name}: {err}"


if __name__ == "__main__":
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    allc = cards()
    names = sys.argv[2:] or list(allc)
    with ThreadPoolExecutor(int(os.environ.get("PAR", "6"))) as ex:
        for line in ex.map(gen, [(n, allc[n], out) for n in names]):
            print(line, flush=True)
