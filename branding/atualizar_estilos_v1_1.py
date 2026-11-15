#!/usr/bin/env python3
"""Aplica CSS v1.1 sem modificar JS, Python do MVP ou fluxos."""
from pathlib import Path
from datetime import datetime
import shutil
import sys

kit = Path(__file__).resolve().parent
project = Path(sys.argv[1] if len(sys.argv) > 1 else "~/projetos/citizentech-fase0").expanduser()
project = project.resolve()
page = next((p for p in (project / "web/index.html", project / "index.html") if p.is_file()), None)
if page is None:
    raise SystemExit("ABORTADO: index.html não encontrado.")
names = ("brand-tokens.css", "brand-layout.css", "brand-components.css")
text = page.read_text(encoding="utf-8")
for name in names:
    old = f"{name}?v=oj-v1"
    if text.count(old) != 1 or not (kit / name).is_file():
        raise SystemExit(f"ABORTADO: arquivo ou referência inesperada: {name}")
    if not (page.parent / name).is_file():
        raise SystemExit(f"ABORTADO: CSS instalado não encontrado: {name}")
    text = text.replace(old, f"{name}?v=oj-v1-1", 1)
if "OUTRO_JEITO_BRAND_V1" not in text:
    raise SystemExit("ABORTADO: o kit visual original não está instalado.")
backup = Path.home() / "CitizenTech_brand_backups" / ("css_v1_1_" + datetime.now().strftime("%Y%m%d_%H%M%S"))
backup.mkdir(parents=True, exist_ok=False)
shutil.copy2(page, backup / "index.html")
for name in names:
    shutil.copy2(page.parent / name, backup / name)
for name in names:
    shutil.copy2(kit / name, page.parent / name)
page.write_text(text, encoding="utf-8")
print("CSS 1.1 INSTALADO: PASS")
print("BACKUP:", backup)
print("ALTERADOS: 3 arquivos CSS e referências de versão no HTML")
print("NÃO ALTERADOS: JS, Python, dados e integração das APIs")
