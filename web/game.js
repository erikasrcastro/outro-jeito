const board = document.getElementById("board");
const statusText = document.getElementById("game-status");
const levels = document.querySelector(".levels");
let cells = Array(9).fill("");
let thinking = false;
let timer;

function draw() {
  const result = outcome(cells);
  statusText.textContent = result === "X" ? "Você venceu! 🎉" :
    result === "O" ? "Computador venceu. Tente outra!" :
    result === "draw" ? "Empate! Que tal outra?" :
    thinking ? "Computador pensando..." : "Sua vez: X";
  board.replaceChildren();
  cells.forEach((value, i) => {
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = value;
    button.disabled = thinking || Boolean(result) || Boolean(value);
    button.setAttribute("aria-label", `Casa ${i + 1}: ${value || "vazia"}`);
    button.addEventListener("click", () => play(i));
    board.append(button);
  });
}

function play(i) {
  if (thinking || outcome(cells) || cells[i]) return;
  cells[i] = "X";
  if (outcome(cells)) return draw();
  thinking = true;
  draw();
  timer = setTimeout(() => {
    const chosen = computerMove(cells, document.querySelector('input[name="difficulty"]:checked').value);
    if (chosen !== null) cells[chosen] = "O";
    thinking = false;
    draw();
  }, 220);
}

function reset() {
  clearTimeout(timer);
  cells = Array(9).fill("");
  thinking = false;
  draw();
}

document.getElementById("reset").addEventListener("click", reset);
levels.addEventListener("change", reset);
draw();
