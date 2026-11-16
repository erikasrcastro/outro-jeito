const wins = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6],
              [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]];

function outcome(board) {
  for (const [a, b, c] of wins) {
    if (board[a] && board[a] === board[b] && board[a] === board[c]) return board[a];
  }
  return board.every(Boolean) ? "draw" : null;
}

function minimax(board, computerTurn, depth = 0) {
  const result = outcome(board);
  if (result) return { O: 10 - depth, X: depth - 10, draw: 0 }[result];
  let best = computerTurn ? -Infinity : Infinity;
  for (let i = 0; i < 9; i++) {
    if (board[i]) continue;
    board[i] = computerTurn ? "O" : "X";
    const score = minimax(board, !computerTurn, depth + 1);
    board[i] = "";
    best = computerTurn ? Math.max(best, score) : Math.min(best, score);
  }
  return best;
}

function computerMove(board, level) {
  const free = board.map((value, i) => value ? -1 : i).filter(i => i >= 0);
  if (!free.length) return null;
  if (level === "easy") return free[Math.floor(Math.random() * free.length)];
  let best = -Infinity;
  let move = free[0];
  for (const i of free) {
    board[i] = "O";
    const score = minimax(board, false, 1);
    board[i] = "";
    if (score > best) { best = score; move = i; }
  }
  return move;
}
