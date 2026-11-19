# feat-03-01: requisitos multiplataforma pelo motor requisitos-para-ia

**Pedido:** migrar o readme-studio para o motor multiplataforma (`nathanramorim/requisitos-para-ia`, branch `feat/0001-motor-multiplataforma`, commit `5f63e02`). O PR #4 (0.5.0) entrou com um prompt centrado no Mac (`brew install uv`, sem Windows nem Linux). O readme-studio é a correção na raiz: todo README que ele gera passa a usar o bloco do motor e o verificador barra o prompt centrado no Mac.
**Branch:** `feat/03-requisitos-multiplataforma`, a partir de `origin/main` (PR #4 já mesclado).

## Modelo do módulo
`enxuto`: troca de um script por cópias exatas do motor (`scripts/requisitos.py`, `scripts/bootstrap.sh`, `scripts/bootstrap.ps1`, registradas no `skills.lock`), um `requisitos.toml` na raiz, regras novas no verificador, instruções na skill e no template e um workflow de CI. Nada de servidor nem estado.

## Decisões do projeto aplicadas
ADR-0003 (`uv`, PEP 723, biblioteca padrão), ADR-0006 (prompt apoiado em script: o script agora é o motor), ADR-0007 (nova: motor vendorizado, `requisitos.toml` e bootstrap por SO). Regra 6 (o `requisitos.toml` só tem comandos do projeto, dos exemplos do motor ou da documentação oficial), Regra 9 (estendida: Windows e POSIX, sem Homebrew como pré-requisito), Regra 10 (template, skill, comando e README no mesmo PR), Regra 12 (0.6.0).

## O que já existe
| Procurei | Onde | Achei | Decisão | Justificativa |
|---|---|---|---|---|
| Conferência da máquina | `scripts/requisitos.py` (0.5.0) | motor só macOS, bloco `REQUISITOS` em Python | substituir | O motor `requisitos-para-ia` cobre os 3 SOs com receita declarativa (`DUP-01`: uma casa) |
| Vendorização | `skills.lock` do hub (formato `modo: copia` + sha256) | não existia no readme-studio | criar | Registra origem, commit e checksum das cópias |
| Exemplo de receita | `exemplos/acme/requisitos.toml` do motor | todas as particularidades | reusar | Copiado para `templates/requisitos-exemplo.toml`; a skill parte dele, nunca inventa |
| Conferência do README | `scripts/verificar_readme.py` | bloco "Cole isto na sua IA" | estender | Falha sem `requisitos.toml`, sem `bootstrap.ps1`, sem `bootstrap.sh` ou com Homebrew no bloco; tabela cita macOS, Linux e Windows |
| CI | `.github/` | nada | criar | Matriz ubuntu/windows/macos prova a receita (`validar`, `checar --json`, bootstrap em dry-run, testes, verificador) |

## Dependências novas
Nenhuma em runtime (biblioteca padrão; o motor pede Python 3.11+ por causa do `tomllib`). CI: `actions/checkout@v4` e `astral-sh/setup-uv@v6`.

## Rules e IDs da Constituição Aplicáveis
`ARQ-04`, `ARQ-06`, `COD-01`, `COD-04`, `SEG-03`, `SEG-04`, `TST-01`, `TST-02`, `DUP-01`, `DUP-02`, `GOV-01`, `FLX-07`.

## Critérios de Aceitação Executáveis
1. `uv run tests/test_verificar_readme.py` e `uv run tests/test_requisitos.py` saem 0.
2. `uv run scripts/requisitos.py validar` sai 0 e `uv run scripts/requisitos.py checar --json` sai 0 ou 1 com JSON válido.
3. `uv run scripts/verificar_readme.py README.md` imprime `requisitos: ok`; o bloco do README é igual à saída de `uv run scripts/requisitos.py prompt`.
4. O verificador sai 1 (um teste para cada): bloco com Homebrew como pré-requisito; bloco sem `bootstrap.ps1`; bloco sem `bootstrap.sh`; projeto com dependência sem `requisitos.toml`; Requisitos sem macOS, Linux ou Windows.
5. `shasum -a 256` das cópias bate com o `skills.lock` (coberto por `test_requisitos.py`).
6. `grep -c 'brew install uv' README.md templates/README.md.tmpl skills/readme-comercial/SKILL.md` = 0.
7. `"version": "0.6.0"` em `.claude-plugin/plugin.json`, linha 0.6.0 no README e em `sdd/releases/history.md`; `test -f sdd/spec/adr/adr-0007-requisitos-multiplataforma.md`.
8. O workflow `.github/workflows/requisitos.yml` passa em ubuntu-latest, windows-latest e macos-latest.
