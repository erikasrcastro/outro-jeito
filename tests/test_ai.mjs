import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { runInNewContext } from "node:vm";

const code = readFileSync(new URL("../web/ai.js", import.meta.url), "utf8");
const ai = runInNewContext(`${code}; ({ computerMove, outcome })`, { Math });
const blank = () => Array(9).fill("");

assert.equal(ai.outcome(["X", "X", "X", "", "", "", "", "", ""]), "X");
assert.equal(ai.outcome(["X", "O", "X", "X", "O", "O", "O", "X", "X"]), "draw");
for (const level of ["easy", "hard"]) {
  const board = ["X", "", "", "", "O", "", "", "", ""];
  const next = ai.computerMove(board, level);
  assert.equal(board[next], "");
  assert.equal(board[0], "X");
}
assert.equal(ai.computerMove(["O", "O", "", "X", "X", "", "", "", ""], "hard"), 2);
assert.equal(ai.computerMove(["X", "X", "", "", "O", "", "", "", ""], "hard"), 2);

let leaves = 0;
function allHumanChoices(board = blank()) {
  const state = ai.outcome(board);
  assert.notEqual(state, "X", "A IA difícil deixou o jogador vencer");
  if (state) { leaves++; return; }
  for (let i = 0; i < 9; i++) {
    if (board[i]) continue;
    const next = board.slice();
    next[i] = "X";
    if (!ai.outcome(next)) {
      const reply = ai.computerMove(next, "hard");
      assert.equal(next[reply], "");
      next[reply] = "O";
    }
    allHumanChoices(next);
  }
}
allHumanChoices();
console.log(`PASS — fácil válido, difícil vence/bloqueia e não perde (${leaves} finais).`);
