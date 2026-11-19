# Decisões — readme-studio

## Resolvidas

| # | Decisão | Resolução | Motivo |
|---|---------|-----------|--------|
| 1 | Quem escreve o quê | Skill conduz e escreve o README; script desenha o banner | Texto que sempre cabe e SVG válido (ADR-0001) |
| 2 | Visual do banner | Identidade do projeto; sem ela, tema azul claro; nunca inventar marca | O README parece o produto (ADR-0002) |
| 3 | Python | `uv` sempre; scripts só com a biblioteca padrão | Nada de pip nem venv manual (ADR-0003) |
| 4 | Distribuição | Plugin na raiz + cópia para o agy; Forge SDD fora do plugin | Instalação direta do GitHub (ADR-0004) |
| 5 | Adoção do Forge SDD | 4.9.1-beta com exceção temporária da Regra 11 | Toda feature ou fix com histórico (ADR-0005) |
| 7 | Prompt de instalação para a IA | Script de requisitos (`checar`/`instalar`) + bloco "Cole isto na sua IA" que o usa, conferido pelo verificador | O que é determinístico vira script; o prompt só orquestra (ADR-0006) |
| 6 | Layout x `ARQ-01` | `commands/` é a borda (equivale a `cmd/`); skill, template e script são o domínio (equivale a `internal/`) | Projeto de skill, sem pacotes Go |

## Abertas

| # | Questão |
|---|---------|
| D1 | Promover o Forge para uma versão estável antes do prazo da exceção (ADR-0005) |
