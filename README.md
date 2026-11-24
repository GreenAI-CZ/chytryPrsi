# Chytré prší

Seznamovací web karetní hry Chytré prší — klasické prší, do kterého vítěz každého kola přidá nové pravidlo.

Čistě statický web bez buildu: `index.html`, `styles.css`, `app.js`.

## Spuštění

```bash
python3 -m http.server 8123
```

Pak otevřete http://localhost:8123.

## Úpravy

- Návrhy pravidel (sekce Inspirace) jsou v poli `IDEAS` v `app.js`.
- Soubory ke stažení jsou ve složce `downloads/` (`chytre-prsi-pravidla.pdf`, `chytre-prsi-karty.pdf`). Karty k tisku se generují z `design/karty/` (`deck.py` a `extra.py` kreslí přes Codex z ChatGPT předplatného, `tisk.py` skládá PDF).
- Tlačítko „Vytisknout pravidla“ používá tiskový styl v `styles.css` (`@media print`).

## Licence

Text pravidel: CC BY-SA 4.0.

## Nasazení (GitHub Pages)

Web běží na GitHub Pages s doménou `chytryprsi.cz` (soubor `CNAME`).

1. V repozitáři: Settings → Pages → Source: „Deploy from a branch“, větev `main`, složka `/ (root)`.
2. Custom domain: `chytryprsi.cz`, po ověření zapnout „Enforce HTTPS“.
3. DNS u WEDOSu (doména `chytryprsi.cz`):

| Typ | Název | Hodnota |
|---|---|---|
| A | (prázdné) | 185.199.108.153 |
| A | (prázdné) | 185.199.109.153 |
| A | (prázdné) | 185.199.110.153 |
| A | (prázdné) | 185.199.111.153 |
| AAAA | (prázdné) | 2606:50c0:8000::153 |
| AAAA | (prázdné) | 2606:50c0:8001::153 |
| AAAA | (prázdné) | 2606:50c0:8002::153 |
| AAAA | (prázdné) | 2606:50c0:8003::153 |
| CNAME | www | `greenai-cz.github.io` |

Původní A záznam (185.8.237.22) je potřeba smazat.
