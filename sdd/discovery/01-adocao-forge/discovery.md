# Discovery 01 — adoção do Forge SDD

**Pedido:** toda skill é produto de TI e segue o Forge SDD (repositório próprio e replicável, Constituição alinhada, README pelo readme-studio com `## Requisitos`); toda feature ou fix passa pelo fluxo para mapear execuções, criar histórico e sequencializar contexto.
**Branch:** `chore/forge-sdd` (a partir de `main`).

## Modelo do módulo
`enxuto`: só estrutura e documentação (`sdd/`, `.agents/`, `.claude/`, `.gemini/`, `.forge/`, `CLAUDE.md`, `GEMINI.md`). Nenhum arquivo do plugin (`.claude-plugin/`, `commands/`, `skills/`, `scripts/`, `templates/`, `exemplos/`, `README.md`) muda.

## O que já existe
| Procurei | Onde | Achei | Decisão | Justificativa |
|---|---|---|---|---|
| Decisões do produto | código e histórico (0.1.0 a 0.3.0) | skill conduz e script desenha; identidade do projeto; plugin na raiz | reusar | Viram ADR-0001, 0002 e 0004 (retroativas, `aprovado`). |
| Padrão de adoção | outros repositórios de skill já no Forge | Constituição com regra de replicabilidade, fluxo Forge e `uv` | estender | Mesmas regras, adaptadas ao readme-studio. |

## Dependências novas
Nenhuma.

## Decisões do projeto aplicadas
ADR-0001 a ADR-0005; Regras 1 a 15 da Constituição.

## Exceção temporária (`GOV-02`)
```constitution-exception
regra: Regra 11 (FLX-07) — mesclar estrutura Forge SDD 4.9.1-beta na main
motivo: única versão do Forge disponível; o fluxo SDD precisa valer já para features e fixes do readme-studio
prazo: 2026-12-31
responsavel: dono do repositório (nathanramorim)
```

## Critérios de Aceitação Executáveis
1. `forge brief --check` sai 0 (`pronta`).
2. `forge gate` sem falha bloqueante (avisos documentados no `status.md`).
3. `git diff --stat main -- .claude-plugin commands skills scripts templates exemplos README.md` vazio.
