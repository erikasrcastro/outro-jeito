from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXT = {".py", ".js", ".mjs", ".html", ".css", ".sh", ".jsonc", ".toml"}
SKIP = {".venv", ".git", ".wrangler", "node_modules", "__pycache__"}
bad = []
for path in ROOT.rglob("*"):
    if not path.is_file() or path.suffix not in EXT or SKIP.intersection(path.parts):
        continue
    count = len(path.read_text(encoding="utf-8").splitlines())
    print(f"{count:02d}/50 {path.relative_to(ROOT)}")
    if count > 50:
        bad.append(str(path.relative_to(ROOT)))
if bad:
    raise SystemExit(f"Limite excedido: {', '.join(bad)}")
print("PASS — todos os arquivos de código têm no máximo 50 linhas.")
