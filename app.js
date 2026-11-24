// Návrhy pravidel – zdroj pro sekci Inspirace
const IDEAS = [
  { name: 'Zelený král', suit: 'listy', text: 'Přebije sedmičku, ale sedmička nepřebije krále. Za krále líže hráč 4 karty.' },
  { name: 'Uno', suit: 'srdce', text: 'Kdo má v ruce poslední kartu, musí říct „Uno“. Když zapomene a někdo ho upozorní, líže si kartu.' },
  { name: 'Spodek', suit: 'zaludy', text: 'Spodek mění hodnotu karty.' },
  { name: 'Rychlé prší', suit: 'kule', text: 'Hráč může vyložit více karet se stejnou hodnotou najednou.' },
  { name: 'Změna směru', suit: 'listy', text: 'Vybraná karta otáčí směr hry.' },
  { name: 'Červená sedmička', suit: 'srdce', text: 'Vrací do hry, pokud ji má hráč, který následuje po vítězi.' },
  { name: 'Výměna karet', suit: 'zaludy', text: 'Vybraná karta umožní vyměnit si karty s jiným hráčem.' },
  { name: 'Duha', suit: 'kule', text: 'Kdo má od každé barvy jednu kartu, může říct „Duha“ a vyložit všechny čtyři najednou.' },
  { name: 'Vyrušení', suit: 'listy', text: 'Vybraná karta ruší efekt právě zahrané karty.' },
];

const suitIcon = (suit) => `<svg><use href="#s-${suit}"/></svg>`;

// Inspirace
const ideasEl = document.getElementById('ideas');
ideasEl.innerHTML = IDEAS.map((r) => `
  <article class="idea" data-suit="${r.suit}">
    <div class="idea__head">${suitIcon(r.suit)}<h3>${r.name}</h3></div>
    <p>${r.text}</p>
  </article>`).join('') + `
  <article class="idea idea--own">
    <h3>Vaše pravidlo</h3>
    <p>Každý si může vymyslet úplně vlastní pravidla. Hlavně ať je schválí všichni u stolu.</p>
  </article>`;

document.querySelectorAll('[data-print]').forEach((b) => b.addEventListener('click', () => window.print()));

