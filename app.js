// Návrhy pravidel – zdroj pro sekci Inspirace i pro simulátor
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

const PLAYERS = ['Anička', 'Tomáš', 'Bára', 'Jirka', 'Kuba', 'Verča'];
const LEVELS = ['Pohodička', 'Rozehřívání', 'Už to začíná', 'Soustřeď se', 'Hlava jako pátrací centrála', 'Chaos', 'Legendární', 'Kdo si to ještě pamatuje?'];
const MAX_RULES = 8;

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

// Simulátor
const list = document.getElementById('sim-list');
const status = document.getElementById('sim-status');
const bar = document.getElementById('sim-bar');
const level = document.getElementById('sim-level');
const playBtn = document.getElementById('sim-play');
const form = document.getElementById('sim-form');
const input = document.getElementById('sim-input');
const boardForm = document.getElementById('board-form');
const boardName = document.getElementById('board-name');
const boardSubmit = document.getElementById('board-submit');
const boardHint = document.getElementById('board-hint');
const boardList = document.getElementById('board-list');
const MIN_RULES = 4;

let rules = [];
let pool = [];

function shuffle(a) {
  const arr = a.slice();
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}

function render(winner) {
  list.querySelectorAll('.sim__rule').forEach((n) => n.remove());
  rules.forEach((r, i) => {
    const li = document.createElement('li');
    li.className = 'sim__rule' + (i === rules.length - 1 && winner ? ' is-new' : '');
    for (const [tag, txt] of [['b', r.name], ['span', r.text], ['em', `přidal(a) ${r.by}`]]) {
      const el = document.createElement(tag);
      el.textContent = txt;
      li.appendChild(el);
    }
    list.appendChild(li);
  });

  const n = rules.length;
  bar.style.width = `${Math.min(n / MAX_RULES, 1) * 100}%`;
  level.textContent = LEVELS[Math.min(n, LEVELS.length - 1)];

  if (n === 0) {
    status.textContent = 'Kolo 1 · hrají se jen základní pravidla pomalého prší.';
  } else if (n >= MAX_RULES) {
    status.textContent = `Po ${n} kolech si to už nikdo nepamatuje. Konec hry — příště zase od začátku!`;
  } else {
    status.textContent = `${winner} vyhrál(a) kolo a přidává pravidlo. Před kolem ${n + 1} si připomeňte všech ${n} chytrých pravidel.`;
  }
  playBtn.disabled = n >= MAX_RULES;
  input.disabled = n >= MAX_RULES;
  updateBoardForm();
}

function addRule(rule, by = PLAYERS[Math.floor(Math.random() * PLAYERS.length)]) {
  if (rules.length >= MAX_RULES) return;
  rules.push({ ...rule, by });
  render(by);
}

function reset() {
  rules = [];
  pool = shuffle(IDEAS);
  render();
}

playBtn.addEventListener('click', () => {
  if (!pool.length) pool = shuffle(IDEAS);
  addRule(pool.pop());
});

form.addEventListener('submit', (e) => {
  e.preventDefault();
  const text = input.value.trim();
  if (!text) return;
  addRule({ name: 'Vlastní pravidlo', text, own: true }, boardName.value.trim() || 'Ty');
  input.value = '';
});

// Žebříček – úložiště je oddělené, aby šlo později vyměnit za sdílený backend
const board = {
  key: 'chytre-prsi-zebricek',
  list() {
    try { return JSON.parse(localStorage.getItem(this.key)) || []; } catch { return []; }
  },
  add(entry) {
    const all = [...this.list(), entry];
    try { localStorage.setItem(this.key, JSON.stringify(all)); } catch {}
    return all;
  },
};

const ownCount = () => (rules.every((r) => r.own) ? rules.length : 0);

function updateBoardForm() {
  const own = ownCount();
  const hasName = boardName.value.trim().length > 0;
  boardSubmit.disabled = !(own >= MIN_RULES && hasName);
  if (rules.some((r) => !r.own)) {
    boardHint.textContent = 'Některé pravidlo vybrala hra náhodně. Pro žebříček začni znovu a piš jen vlastní pravidla.';
  } else if (own < MIN_RULES) {
    boardHint.textContent = `Vlastních pravidel: ${own} z ${MIN_RULES} potřebných.`;
  } else if (!hasName) {
    boardHint.textContent = 'Máš dost pravidel! Napiš své jméno a zapiš se.';
  } else {
    boardHint.textContent = own < MAX_RULES ? `Můžeš se zapsat s ${own} koly, nebo vymýšlej dál až do ${MAX_RULES}.` : 'Plný počet kol — zapiš se!';
  }
}

function renderBoard(entries) {
  const sorted = entries.slice().sort((a, b) => b.rules.length - a.rules.length || a.at - b.at).slice(0, 10);
  boardList.replaceChildren();
  if (!sorted.length) {
    const li = document.createElement('li');
    li.className = 'board__empty';
    li.textContent = 'Zatím tu nikdo není. Buď první!';
    boardList.appendChild(li);
    return;
  }
  sorted.forEach((e) => {
    const li = document.createElement('li');
    const details = document.createElement('details');
    const summary = document.createElement('summary');
    const name = document.createElement('b');
    name.textContent = e.name;
    const score = document.createElement('span');
    score.textContent = `${e.rules.length} kol`;
    summary.append(name, score);
    const ol = document.createElement('ol');
    e.rules.forEach((t) => {
      const r = document.createElement('li');
      r.textContent = t;
      ol.appendChild(r);
    });
    details.append(summary, ol);
    li.appendChild(details);
    boardList.appendChild(li);
  });
}

boardName.addEventListener('input', updateBoardForm);
boardForm.addEventListener('submit', (e) => {
  e.preventDefault();
  if (boardSubmit.disabled) return;
  const name = boardName.value.trim();
  renderBoard(board.add({ name, rules: rules.map((r) => r.text), at: Date.now() }));
  reset();
  boardHint.textContent = `${name}, jsi v žebříčku! Zkus to znovu a vymysli ještě víc kol.`;
});

renderBoard(board.list());

document.getElementById('sim-reset').addEventListener('click', reset);
document.querySelectorAll('[data-print]').forEach((b) => b.addEventListener('click', () => window.print()));

reset();
