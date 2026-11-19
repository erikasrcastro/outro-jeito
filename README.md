# Outro Jeito.

**Existem outras formas de seguir.**

**FIAP — Tecnologia em Agentes Inteligentes | Global Solution 01/2026 — CitizenTech**  
**Turma:** 1TAGOR · **Grupo 24:** projeto individual  
**Autoria:** Érika Francine Silva Rodrigues Castro · **RM:** 574284

O **Outro Jeito** é um agente inteligente acadêmico desenvolvido para ajudar pessoas adultas, especialmente mulheres, a **compreender possibilidades de proteção, moradia, orientação e autonomia** em linguagem simples. Ele não decide pela pessoa, não exige que ela se identifique como vítima e não promete direitos ou resultados individuais.

> **Atenção:** MVP de demonstração, ainda **não homologado para pessoas em situação real de risco**. Utilize exclusivamente cenários inventados, sem nomes, endereços, CPF ou relatos pessoais. Não substitui serviços jurídicos, psicológicos, policiais ou de emergência.

## Assista ao pitch e experimente o MVP

- **Vídeo pitch final (5 minutos):** [Outro Jeito | IA para Ampliar Escolhas e Autonomia Feminina — FIAP Global Solution 2026](https://youtu.be/fTw_Jht3z5c)
- **MVP público para avaliação acadêmica:** https://outro-jeito-staging.erika-srcastro.workers.dev/
- **Código-fonte:** este repositório.
- **Evidências de execução e testes (T01–T06):** [pasta exclusiva de testes](https://drive.google.com/drive/folders/15f47kmXYlfzH6BLP6nBCoKq_1_HHaksU).

A demonstração na Cloudflare depende de conectividade e da disponibilidade dos serviços externos e de seus limites gratuitos. A interface é pública **somente para uso acadêmico com dados fictícios**.

## O que o agente faz

1. A pessoa escolhe um tema geral ou descreve um exemplo inventado.
2. O navegador apresenta palavras gerais identificadas para conferência antes do envio; a frase original não integra o payload previsto do frontend.
3. O **Python** faz nova validação da entrada, controla o fluxo e reduz o contexto a categorias permitidas.
4. A **LLM Groq** interpreta a solicitação e retorna uma estrutura JSON que passa por verificações.
5. Quando há lei mapeada, o backend consulta de fato a **API de dados legislativos do Senado Federal**, valida a referência e a incorpora ao resultado.
6. A interface apresenta **até três caminhos possíveis**, com linguagem acessível, exemplos e limites da informação.

Quando faltam dados, o agente solicita esclarecimento. Quando uma API falha, informa a limitação em vez de inventar uma fonte confirmada. Diante de urgência explícita, pode encaminhar a pessoa para canais oficiais **sem acionar serviços automaticamente**.

### Recursos de cuidado

- **Ajuda imediata:** 180 (atendimento à mulher), 190 (polícia), 192 (emergência médica) e 100 (direitos humanos).
- **Trocar de tela:** substitui visualmente o conteúdo por um jogo da velha; **não apaga histórico, rastros de rede ou monitoramento externo**.
- **Sem decisões impostas:** não incentiva confronto, separação ou denúncia; não fornece aconselhamento jurídico individual.

## Arquitetura

```text
Pessoa → HTML/CSS/JavaScript (web/)
        → triagem e confirmação
        → POST /api/v1/explore
        → Cloudflare Python Worker (src/main.py)
        → validação e minimização pelo Python
        → Groq (interpretação estruturada)
        → Python (validação do JSON e seleção de fonte)
        → Senado Federal (consulta legislativa quando aplicável)
        → validação da referência e resposta contextualizada
        → interface: alternativas e limites
```

**Python controla as ações e integrações; a LLM não pode escolher livremente destinos externos ou atestar a aplicabilidade individual de uma lei.**

| Componente | Responsabilidade |
| --- | --- |
| `web/` | Interface, confirmação do contexto, cartões de resposta, canais de ajuda e troca de tela |
| `src/main.py` | Entrada HTTP do Worker e rotas `/api/v1/explore` e `/api/v1/health` |
| `src/flow_live.py` | Orquestração do fluxo e tratamento de falhas |
| `src/privacy.py`, `src/precheck.py` e módulos correlatos | Triagem, minimização e segurança |
| `src/groq_live.py` | Integração LLM |
| `src/senado_live.py` e `src/evidence.py` | Consulta e validação de referência legislativa |
| `tests/` | Testes automatizados e casos controlados |

**Tecnologias:** Python 3.13+, JavaScript, HTML/CSS, Cloudflare Workers Python, Groq e API do Senado Federal. Nenhum banco de dados é necessário para o MVP demonstrado.

## Como executar os testes no seu computador

Para **visualizar a interface**, não é necessário instalar nada: use o link do MVP acima. Para **reproduzir o conjunto de testes** deste repositório, instale **Python 3.13 ou superior** e **Node.js**.

Clone o repositório e entre na pasta:

```bash
git clone https://github.com/erikasrcastro/outro-jeito.git
cd outro-jeito
```

Execute as verificações:

```bash
python3 scripts/check_lines.py
python3 -m unittest discover -s tests -q
node --test tests/*.mjs
```

No **Windows**, o comando `python3` pode ser substituído por `py -3` ou `python` (desde que seja a versão 3.13+). No **macOS**, use `python3` ou a versão explícita instalada (por exemplo `python3.13`). Esses testes não dependem de uma chave Groq própria porque usam simulações controladas nas integrações.

**Resultado documentado em 16/11/2026:** 48 testes Python e 14 testes JavaScript aprovados, além do verificador de limite de 50 linhas. São **62 testes automatizados**, não uma avaliação de segurança ou eficácia com pessoas em risco. Resultados em novos ambientes dependem das versões e da configuração locais.

### Evidências dos cenários

| Cenário | Comportamento esperado |
| --- | --- |
| **T01 — fluxo real** | LLM + consulta real ao Senado + informação externa incorporada ao resultado |
| **T02 — informação insuficiente** | Solicitar complemento sem inventar possibilidades ou fontes |
| **T03 — falha controlada** | Simular HTTP 503 do Senado e identificar a referência como não verificada |
| **T04 — urgência** | Apresentar canais oficiais sem encaminhamento automático |
| **T05 — troca visual** | Exibir jogo neutro e retirar o conteúdo sensível da visualização |
| **T06 — minimização** | Conferir os dados autorizados para envio e o contrato de saída |

Os testes T03–T06 incluem casos **simulados ou instrumentados**; não são comprovação de indisponibilidade real do Senado nem auditoria de fornecedores. As capturas e os registros estão na [pasta de evidências de testes](https://drive.google.com/drive/folders/15f47kmXYlfzH6BLP6nBCoKq_1_HHaksU).

## Publicar uma instância própria (opcional)

A execução dos testes e a visualização do portal público **não exigem deploy**. O backend utiliza o runtime **Cloudflare Workers Python**; abrir `web/index.html` localmente não inicia automaticamente o backend.

Para implantar outra instância, consulte **[docs/PUBLICACAO_STAGING.md](docs/PUBLICACAO_STAGING.md)**. O processo exige ambiente Cloudflare, Wrangler/`uv` e uma chave Groq própria, armazenada como **segredo** `GROQ_API_KEY` — nunca no repositório. O comando de publicação descrito na documentação é:

```bash
uv run pywrangler deploy
```

A presença da chave indicada por `/api/v1/health` não comprova, por si só, a disponibilidade de ambas as APIs. Não habilite cobrança paga apenas para reproduzir a avaliação acadêmica.

## Resultados, limites e próximos passos

O MVP demonstra um fluxo funcional com interpretação de contexto pela LLM, validação pelo Python e uso de uma fonte legislativa externa. **Não há evidência de redução de violência ou de impacto mensurado sobre decisões reais**. A utilização com relatos reais permanece bloqueada até revisão especializada.

Próximas etapas previstas: revisão jurídica e de segurança, auditoria de privacidade e retenção de dados, testes de acessibilidade e avaliação controlada da compreensão das alternativas. Só depois caberia discutir expansão territorial e novas fontes.

## Identidade visual

Paleta do projeto: roxo profundo `#2A0E3A`, violeta `#7B2FF7`, coral `#FF6B5F`, amarelo `#FFC240` e off-white `#F8F5EE`. Identidade e frontend ativos em `web/`.

---

**Outro Jeito. Existem outras formas de seguir.**  
*Projeto acadêmico · FIAP · Global Solution CitizenTech · Grupo 24 · Érika Francine Silva Rodrigues Castro.*
