#!/usr/bin/env python3
"""Copia somente código e configuração pública do MVP para um clone Git."""
from pathlib import Path
import re
import shutil
import sys

if len(sys.argv) != 3:
    raise SystemExit("Uso: python3 importar_codigo_seguro.py <fonte-MVP> <clone-Git>")
source, repo = (Path(x).expanduser().resolve() for x in sys.argv[1:])
if not (repo / ".git").exists() or not (source / "src").is_dir():
    raise SystemExit("ABORTADO: clone Git ou projeto fonte inválido")
roots = ("src", "web", "tests", "scripts", "docs")
rootfiles = ("wrangler.jsonc", "pyproject.toml", "pylock.toml", "uv.lock", ".dev.vars.example")
allowed = {".py", ".js", ".mjs", ".css", ".html", ".json", ".jsonc", ".toml",
           ".lock", ".md", ".sh", ".txt", ".svg", ".webp", ".png", ".ico"}
excluded = {".git", ".venv", "node_modules", "__pycache__", ".wrangler", ".deploy", "dist", "build"}
secrets = re.compile(rb"gsk_[A-Za-z0-9_-]{12,}|github_pat_[A-Za-z0-9_]{15,}|ghp_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9_-]{28,}")
files = [source / n for n in rootfiles if (source / n).is_file()]
for root in roots:
    if (source / root).is_dir():
        files.extend(p for p in (source / root).rglob("*") if p.is_file())
checked = []
for path in files:
    rel = path.relative_to(source)
    if path.is_symlink() or any(part in excluded or part.startswith(".dev.vars") or
            part.startswith(".env") for part in rel.parts) or path.suffix not in allowed:
        continue
    data = path.read_bytes()
    if len(data) > 3_000_000 or secrets.search(data):
        raise SystemExit(f"ABORTADO: arquivo grande ou aparente segredo em {rel}")
    checked.append((rel, data))
if len(checked) < 10 or not any(str(rel).startswith("src/") for rel, _ in checked):
    raise SystemExit("ABORTADO: faltam fontes do MVP; nada copiado")
for rel, data in checked:
    dest = repo / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
if (source / "README.md").is_file():
    p = repo / "docs/README_MVP_ORIGINAL.md"
    p.parent.mkdir(exist_ok=True)
    shutil.copy2(source / "README.md", p)
print(f"COPIADOS {len(checked)} arquivos do MVP; Git e Cloudflare não foram acionados.")
print("ATENÇÃO: revisar arquivos, testar e auditar segredos ANTES de publicar.")
