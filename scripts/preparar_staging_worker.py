#!/usr/bin/env python3
"""Prepara deploy Worker + assets na mesma URL; não publica."""
from pathlib import Path
import re
import shutil
import sys

project = Path(sys.argv[1] if len(sys.argv) > 1 else "~/projetos/citizentech-fase0").expanduser().resolve()
web, cfg = project / "web", project / "wrangler.jsonc"
if not (web / "agent.js").is_file() or not cfg.is_file():
    raise SystemExit("ABORTADO: web/agent.js ou wrangler.jsonc não encontrado")
source = (web / "agent.js").read_text(encoding="utf-8")
local = "http://127.0.0.1:8787/api/v1/explore"
if source.count(local) != 1:
    raise SystemExit("ABORTADO: endpoint local inesperado; não modificar automaticamente")
raw = cfg.read_text(encoding="utf-8")
if '"assets"' in raw:
    raise SystemExit("ABORTADO: config já tem assets; revisão manual necessária")
updated, count = re.subn(r'("name"\s*:\s*")[^"]+("\s*,)',
    r'\1outro-jeito-staging\2', raw, count=1)
if count != 1 or not updated.strip().endswith("}"):
    raise SystemExit("ABORTADO: configuração Wrangler fora do formato esperado")
stage = project / ".deploy/outro-jeito/web"
if stage.exists():
    shutil.rmtree(stage)
shutil.copytree(web, stage, ignore=shutil.ignore_patterns("*.map", ".DS_Store"))
(stage / "agent.js").write_text(source.replace(local, "/api/v1/explore"), encoding="utf-8")
end = updated.rfind("}")
head = updated[:end].rstrip().rstrip(",")
assets = '\n  "assets": {"directory": "./.deploy/outro-jeito/web", ' \
         '"binding": "ASSETS", "run_worker_first": ["/api/*"]}\n'
output = head + "," + assets + updated[end:]
(project / "wrangler.staging.jsonc").write_text(output, encoding="utf-8")
print("STAGING PREPARADO: frontend usa /api/v1/explore (mesma origem).")
print("CONFIG:", project / "wrangler.staging.jsonc")
print("NÃO ALTERADOS: web original, src, testes, .dev.vars e Worker de produção.")
