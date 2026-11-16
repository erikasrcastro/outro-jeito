# Outro Jeito.

**Existem outras formas de seguir.**

Protótipo acadêmico do Grupo 24 da Global Solution (CitizenTech), FIAP — Agentes Inteligentes. A proposta é ajudar pessoas a explorar possibilidades de orientação, proteção e autonomia, sem impor decisões.

## Demonstração pública

O código completo do MVP está neste repositório. O Cloudflare Worker chama-se `outro-jeito-staging`, com interface HTML/CSS/JS estática e backend Python sob a mesma origem, usando a rota `/api/v1/explore`.

O portal está destinado a **testes acadêmicos públicos**, sem login, exclusivamente com situações fictícias. Ele não está homologado para acompanhamento de casos reais ou intervenções de emergência. Não envia ligações, denúncias ou mensagens automaticamente.

A implantação pública de testes está disponível em https://outro-jeito-staging.erika-srcastro.workers.dev/ e foi verificada em 16/11/2026. A chave `GROQ_API_KEY` é armazenada somente como segredo da Cloudflare.

## Identidade visual

Identidade aprovada: roxo profundo `#2A0E3A`, violeta `#7B2FF7`, coral `#FF6B5F`, amarelo `#FFC240` e off-white `#F8F5EE`. Assinatura: *Existem outras formas de seguir.* Arquivos ativos exclusivamente em `web/`; o kit histórico está arquivado no Drive.

## Arquitetura

- **Frontend:** `web/` servido como Workers Static Assets.
- **Backend:** `src/main.py` e módulos Python sob a rota `/api/v1/explore`.
- **Groq:** interpretação estruturada do contexto minimizado.
- **Senado Federal:** fonte oficial para referências legislativas.
- **Segurança de interface:** ajuda imediata 180, 100, 190 e troca rápida para jogo da velha. A troca de tela não apaga histórico nem impede monitoramento.

## Cloudflare — conexão com GitHub

Ao criar o aplicativo a partir deste repositório na Cloudflare Workers & Pages:

- Project name: `outro-jeito-staging` (mesmo nome que em `wrangler.jsonc`).
- Build command: **vazio**.
- Deploy command: `uv run pywrangler deploy`.
- Preview builds: opcionais; podem ficar desligadas.
- Cloudflare Access: **desligado para permitir testes públicos**.
- Depois do primeiro deploy, configure o segredo `GROQ_API_KEY` no Worker, em **Settings → Variables and Secrets**.

A Cloudflare cria a URL real `*.workers.dev` após a implantação. Veja também `docs/PUBLICACAO_STAGING.md`.

## Segurança e avaliação

Nunca publicar `.dev.vars`, `.env`, tokens, dados pessoais ou históricos de conversa. Somente testar com cenários fictícios. A aplicação é um MVP e não presta aconselhamento jurídico individual nem substitui profissionais ou serviços de emergência.

Executar regressão local antes de mudanças funcionais:

```bash
python3 -m unittest discover -s tests -q
node --test tests/*.mjs
```
