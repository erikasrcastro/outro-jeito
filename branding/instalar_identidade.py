#!/usr/bin/env python3
"""Instala marca Outro Jeito com backup sem editar Python/JS do MVP."""
from pathlib import Path
from datetime import datetime
import re
import shutil
import sys

kit = Path(__file__).resolve().parent
proj = Path(sys.argv[1]).expanduser().resolve() if len(sys.argv) > 1 else Path.cwd()
html_file = next((p for p in (proj / "web/index.html", proj / "index.html") if p.is_file()), None)
if not html_file:
    raise SystemExit("ABORTADO: index.html não encontrado.")
html = html_file.read_text(encoding="utf-8")
if "<!-- OUTRO_JEITO_BRAND_V1 -->" in html:
    raise SystemExit("Marca já instalada. Nada alterado.")
if "</head>" not in html or "CitizenTech" not in html:
    raise SystemExit("ABORTADO: HTML inesperado. Nada alterado.")
css = ["brand-tokens.css", "brand-layout.css", "brand-components.css"]
svg = ["outro-jeito-favicon.svg", "outro-jeito-logo-dark.svg", "outro-jeito-logo-light.svg",
       "outro-jeito-symbol-dark.svg", "outro-jeito-symbol-light.svg"]
optional = ["outro-jeito-favicon-32.png", "outro-jeito-favicon-192.png"]
optional = [name for name in optional if (kit / "assets" / name).is_file()]
files = [(kit / x, html_file.parent / x) for x in css]
files += [(kit / "assets" / x, html_file.parent / "assets" / x) for x in svg + optional]
if any(not src.is_file() or dst.exists() for src, dst in files):
    raise SystemExit("ABORTADO: falta arquivo do kit ou destino já existe. Nada alterado.")
links = ['<!-- OUTRO_JEITO_BRAND_V1 -->', '<meta name="theme-color" content="#2A0E3A">',
         '<meta name="description" content="Outro Jeito. Existem outras formas de seguir.">',
         '<link rel="icon" type="image/svg+xml" href="assets/outro-jeito-favicon.svg">']
if optional:
    links += ['<link rel="icon" type="image/png" sizes="32x32" href="assets/outro-jeito-favicon-32.png">',
              '<link rel="apple-touch-icon" href="assets/outro-jeito-favicon-192.png">']
links += [f'<link rel="stylesheet" href="{name}?v=oj-v1">' for name in css]
updated = html.replace("CitizenTech", "Outro Jeito").replace("</head>", "\n".join(links) + "\n</head>", 1)
updated = re.sub(r'[◇◆◈✧]\s*Outro Jeito(?=\s*</(?:a|strong|span|b|div)>)',
    '<img class="oj-mark" src="assets/outro-jeito-symbol-light.svg" alt="" aria-hidden="true">'
    '<span class="oj-wordmark">Outro Jeito<span class="oj-dot">.</span></span>', updated, count=1)
backup = Path.home() / "CitizenTech_brand_backups" / datetime.now().strftime("%Y%m%d_%H%M%S")
backup.mkdir(parents=True, exist_ok=False)
shutil.copy2(html_file, backup / "index.html")
for src, dst in files:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
html_file.write_text(updated, encoding="utf-8")
print("IDENTIDADE INSTALADA | HTML:", html_file, "| Backup:", backup / "index.html")
print("Código Python/JS do MVP: não alterado. Novos arquivos visuais:", len(files))
