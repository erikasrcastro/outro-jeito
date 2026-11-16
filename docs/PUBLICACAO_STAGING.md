# Publicação do MVP — Grupo 24 (staging)

Este repositório é **público**. O clone no Ubuntu receberá todos os **arquivos-fonte do aplicativo** (src/, web/, tests/, scripts/, docs/ e dependências declaradas), excluindo chaves, caches, arquivos temporários e runtimes vendorizados. Nunca versionar `.dev.vars`.

## 1. Importar do Ubuntu sem sobrescrever o branding

```bash
cd ~/projetos
git -C outro-jeito-brand pull --ff-only
python3 outro-jeito-brand/scripts/importar_codigo_seguro.py \
  ~/projetos/citizentech-fase0 ~/projetos/outro-jeito-brand

cd ~/projetos/citizentech-fase0
python3 -m unittest discover -s tests -q
node --test tests/*.mjs

cd ~/projetos/outro-jeito-brand
git add -A -- src web tests scripts docs
git add -- wrangler.jsonc pyproject.toml uv.lock
git diff --cached --check
git diff --cached --stat
git diff --cached --name-only
```

Se os testes e a revisão de arquivos estiverem corretos, publicar:

```bash
git commit -m "feat(mvp): importa codigo funcional validado do Outro Jeito"
git push origin main
```

**Não** executar push se a auditoria revelar chaves, nomes reais, dados de usuários ou `*.har`. O detector automático impede alguns padrões conhecidos de chaves, **mas não é garantia de ausência de segredos**.

## 2. Preparar uma única URL Cloudflare (Worker Python + HTML/CSS/JS)

```bash
cd ~/projetos/citizentech-fase0
python3 ~/projetos/outro-jeito-brand/scripts/preparar_staging_worker.py .
```

Esse script cria `wrangler.staging.jsonc` e `.deploy/outro-jeito/web` (ignorados pelo Git). Na cópia da interface, a URL de API passa de localhost a `/api/v1/explore`. O frontend e o backend são servidos na **mesma origem**, sem Cloudflare Pages separado; a instalação local não é alterada.

Para publicar o Worker com o nome **outro-jeito-staging**:

```bash
uv run pywrangler login
uv run pywrangler deploy --config wrangler.staging.jsonc
uv run pywrangler secret put GROQ_API_KEY --config wrangler.staging.jsonc
```

A Cloudflare solicitará a chave em ambiente local. **Nunca colar a chave no chat nem no repositório**. O deploy deverá mostrar uma URL real `workers.dev`, que deverá ser conferida antes de compartilhar; nenhum endereço de staging é assumido neste documento. Verificar se o segredo foi aplicado e repetir o deploy se necessário.

**Proteção obrigatória de homologação:** no dashboard Cloudflare, **Workers & Pages → outro-jeito-staging → Access → Protect this Worker behind Access → All traffic**; permitir somente contas autorizadas para testes. Sem essa etapa, uma URL `workers.dev` pode ficar pública. Orientação oficial: https://developers.cloudflare.com/workers/configuration/cloudflare-access/

## 3. Smoke test

Em uma sessão autorizada, conferir primeiro a tela inicial, o botão Trocar de tela, o jogo da velha e os telefones 180/100/190. Testar entrada fictícia completa, entrada insuficiente, fallback sem resposta e confirmação do envio de categorias. Conferir no DevTools que a requisição aponta para **`/api/v1/explore`** no domínio Cloudflare e **nunca para `127.0.0.1`**.

Não usar histórias pessoais reais: gates de auditoria de privacidade, retenção Groq, acesso por menores e avaliação especializada continuam pendentes. Proteção visual não apaga histórico nem impede spyware.

Fontes técnicas oficiais: https://developers.cloudflare.com/workers/static-assets/ ; https://developers.cloudflare.com/workers/languages/python/ ; https://developers.cloudflare.com/workers/configuration/secrets/
