# Outro Jeito — homologação pública pela Cloudflare

**Decisão da responsável em 16/11/2026:** disponibilizar o portal para professores e avaliadores sem login ou Cloudflare Access. Usar somente cenários fictícios. Acesso público não significa que o MVP esteja aprovado para histórias reais.

## Configuração publicada no GitHub

O arquivo `wrangler.jsonc` da branch `main` contém:

- `name: outro-jeito-staging`;
- `main: src/main.py`;
- `compatibility_flags: python_workers`;
- `assets.directory: ./web`;
- `assets.run_worker_first: ["/api/*"]`.

O frontend `web/agent.js` consulta `/api/v1/explore` na mesma origem.

## Deploy conectado ao GitHub

No Cloudflare Dashboard → Workers & Pages → Create application → GitHub → `erikasrcastro/outro-jeito` → Create and deploy:

1. Project name: `outro-jeito-staging`.
2. Build command: vazio.
3. Deploy command: `uv run pywrangler deploy`.
4. Preview builds: opcional; desligar para simplificar.
5. Protect with Cloudflare Access: **OFF** para acesso público.
6. Clique **Deploy** e confira o status e URL real do Worker.

O comando Python é o recomendado na documentação oficial: https://developers.cloudflare.com/workers/languages/python/
Workers Builds inclui `uv`: https://developers.cloudflare.com/workers/ci-cd/builds/build-image/

## Configuração da API Groq

Após o primeiro deploy, abra o Worker → Settings → Variables and Secrets → Add secret:

- Nome `GROQ_API_KEY`.
- Valor: chave Groq existente na máquina local; nunca colar no GitHub nem no chat.
- Tipo **Secret**, não variável pública.

Salve e conclua a aplicação da configuração no Worker. Confira `/api/v1/health`; `groq_configured: true` confirma presença da chave. O campo `apis_connected: false` é informativo fixo nesta versão, e NÃO comprova que as APIs estejam desconectadas.

## Testes de aceite público (somente fatos fictícios)

1. Abrir URL pública em janela anônima: não deve exigir login.
2. Testar Trocar de tela → jogo da velha; abrir página novamente.
3. Verificar Ajuda imediata com 180, 100, 190 e 192.
4. T2: escolher assunto e deixar contexto vazio; deve pedir complemento sem consulta externa.
5. T1: perguntar ficticiamente sobre moradia, confirmar o resumo minimizado e observar fonte legislativa e caminhos condicionais.
6. Se a API ficar indisponível, o fallback não deve inventar leis nem prometer benefícios.

Não confundir T3 do relatório, que foi uma **falha simulada do Senado**, com uma indisponibilidade real observada no Worker público.

## Cautelas antes de uso não acadêmico

Ainda pendentes: revisão do tratamento de dados e ZDR da Groq, teste de retenção real, avaliação de falsas interpretações de urgência, acessibilidade e revisão por profissionais da rede de atendimento. O site orienta o uso de contextos fictícios e não faz chamadas automáticas a serviços públicos.

Não ativar cobrança paga apenas para testar.
