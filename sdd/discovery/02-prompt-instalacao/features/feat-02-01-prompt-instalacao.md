# feat-02-01: prompt de instalação para a IA

**Pedido:** "é comum os requisitos terem um prompt que fala com a IA para verificar; nesse prompt ela usa um script para checar se tem os requisitos e, se não tem, já considera fazer a instalação; normalmente esse prompt fica dentro de quote, na instrução inicial antes do plugin add". Generalização: "não pode ser qualquer prompt; se dá para gerar determinístico, gera script e o prompt sabe usar o script como tools".
**Branch:** `feat/02-prompt-instalacao`, a partir da `main` (PR #3, que trazia o fix de Requisitos, já está mesclado).

## Modelo do módulo
`enxuto`: um script novo sem estado (`scripts/requisitos.py`), extensão do verificador, um placeholder novo no template e instruções na skill. Nada de servidor ou banco.

## Decisões do projeto aplicadas
ADR-0001 (skill conduz, script determinístico faz), ADR-0003 (`uv`, PEP 723, só biblioteca padrão), ADR-0006 (nova: prompt apoiado em script). Regra 6 (sem invenção: o bloco só cita comandos que existem), Regra 9 (estendida), Regra 10 (template, skill, comando, README e exemplo no mesmo PR), Regra 12 (0.5.0), Regra 4 (o script nunca lida com segredo).

## O que já existe
| Procurei | Onde | Achei | Decisão | Justificativa |
|---|---|---|---|---|
| Conferência de requisitos | `scripts/` | só `verificar_readme.py` (confere o README, não a máquina) | criar | Responsabilidade diferente (`COD-01`): `requisitos.py` |
| Conferência do README | `scripts/verificar_readme.py` | regras da seção Requisitos | estender | Ganha o bloco "Cole isto na sua IA" e `--raiz` |
| Estrutura de Requisitos | `templates/README.md.tmpl` | `{{REQUISITOS_RESUMO}}` + tabela | estender | `{{PROMPT_IA}}` entre o resumo e a tabela |
| Instrução da skill | `SKILL.md` | "Seção Requisitos" | estender | Nova seção "Prompt de instalação para a IA" |
| Base para outros projetos | — | nada | reusar | A skill copia o próprio `requisitos.py` e troca só `REQUISITOS` (evita script repetido escrito à mão, `DUP-05`) |

## Dependências novas
Nenhuma (biblioteca padrão: `argparse`, `glob`, `json`, `re`, `shlex`, `shutil`, `subprocess`).

## Rules e IDs da Constituição Aplicáveis
`ARQ-04`, `ARQ-06`, `COD-01`, `COD-03`, `SEG-03`, `SEG-04`, `SEG-05`, `TST-01`, `TST-02`, `TST-03`, `DUP-02`, `GOV-01`, `FLX-07`.

## Critérios de Aceitação Executáveis
1. `uv run tests/test_requisitos.py` e `uv run tests/test_verificar_readme.py` saem 0.
2. `uv run scripts/requisitos.py checar` imprime a tabela e sai 0 numa máquina com `uv`; `uv run scripts/requisitos.py instalar </dev/null` não roda nada sem `--sim`.
3. `uv run scripts/verificar_readme.py README.md` imprime `requisitos: ok`.
4. Sem o bloco num projeto com dependência, o verificador sai 1: `cp README.md /tmp/r2/README.md` sem o bloco + `scripts/requisitos.py` → código 1 (coberto por `test_sem_bloco_com_dependencia_falha`); prompt genérico sem comando → código 1 (`test_prompt_generico_sem_comando_falha`).
5. `grep -c '{{PROMPT_IA}}' templates/README.md.tmpl` = 1 e `grep -c 'Prompt de instalação para a IA' skills/readme-comercial/SKILL.md` ≥ 1.
6. `grep -n '"version": "0.5.0"' .claude-plugin/plugin.json` e `grep -n '0.5.0' sdd/releases/history.md README.md` encontram as linhas.
7. `test -f sdd/spec/adr/adr-0006-prompt-de-instalacao-para-ia.md` e a Regra 9 cita ADR-0006.
