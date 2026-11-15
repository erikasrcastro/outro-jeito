# Identidade visual — Outro Jeito

**Estado:** direção visual aprovada, implementação visual v1 pronta para teste local. O aplicativo e o fluxo Python ainda NÃO foram publicados neste repositório.

## Conceito
*Existem outras formas de seguir.* Símbolo de bifurcação de caminhos, assinatura discreta, sem revelar a natureza potencialmente sensível das perguntas feitas no aplicativo.

| Papel | Cor |
|---|---|
| Roxo profundo | `#2A0E3A` |
| Violeta | `#7B2FF7` |
| Coral | `#FF6B5F` |
| Amarelo | `#FFC240` |
| Off-white | `#F8F5EE` |

Tipografia sugerida: Sora + Inter, com fallback para fontes de sistema. O CSS não busca fontes externas.

## Instalação local em uma cópia do MVP
Após clonar este repositório, execute:

```bash
python3 branding/instalar_identidade.py ~/projetos/citizentech-fase0
```

O instalador salva backup de `index.html`, adiciona CSS e ícones SVG (e os PNGs se existirem no pacote) e não modifica Python nem JavaScript. Não publica nem inicia um deploy.

## Verificação

```bash
cd ~/projetos/citizentech-fase0
python3 -m unittest discover -s tests -q
node --test tests/*.mjs
```

Depois verifique a UI em http://127.0.0.1:5173. Não envie relato real no teste acadêmico.

## Limites
Os SVGs são uma **interpretação vetorial** da referência visual aprovada, e não uma vetorização pixel a pixel. PNGs de ícones e referência visual em alta resolução fazem parte do kit ZIP completo disponibilizado separadamente. A página completa do app só deve ser publicada após auditoria de segredos; `.dev.vars` jamais entra no Git.
