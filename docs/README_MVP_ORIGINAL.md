# CitizenTech · Fase 0 local

Protótipo local de **interface estática**, jogo da velha e Worker Python com rota de saúde.
Não consulta Groq ou Senado; **não usar relatos reais**. Nenhum deploy nem GitHub neste estágio.

## Dependências no Ubuntu

- Python 3.13+, `uv` e Node.js (requisitos do `pywrangler`).
- O primeiro `uv run` poderá baixar dependências para o seu computador.

## Validar arquivos e testes

```bash
python3 scripts/check_lines.py
python3 -m unittest discover -s tests -v
```

## Terminal 1: Worker (porta 8787)

```bash
uv run pywrangler dev
```

## Terminal 2: site estático (porta 5173)

```bash
python3 -m http.server 5173 --bind 127.0.0.1 --directory web
```

Abrir http://127.0.0.1:5173 no navegador.
Testar API com `curl http://127.0.0.1:8787/api/v1/health`.
Esperado: `{"status":"ok","phase":"F0","apis_connected":false}`.

**Próximo passo:** validar as duas telas, os três assuntos, a ajuda e o jogo.
Quando algo falhar, envie o erro do terminal sem tokens. Não publique o repositório.
