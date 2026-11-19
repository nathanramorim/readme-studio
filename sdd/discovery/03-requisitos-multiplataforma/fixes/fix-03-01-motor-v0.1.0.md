# Fix 03-01: motor de requisitos fixo na tag v0.1.0

**Relato:** o motor requisitos-para-ia foi vendorizado do commit `5f63e02` da branch `feat/0001-motor-multiplataforma`, ainda sem versão. O requisitos-para-ia publicou a tag `v0.1.0` (commit `93abe08` na `main`), com a trava mais rígida (ADR-0008 do motor). Dentro do `uv run`, `uv python find` acha o Python do ambiente do próprio script e o item `python` passa mesmo sem Python do sistema.
**Branch:** `fix/03-01-motor-v0.1.0`, a partir de `origin/main`.

## Feature Correlacionada
- **Origem:** `features/feat-03-01-requisitos-multiplataforma.md` (0.6.0), pendência do `status.md`: "fixar o motor numa tag quando o requisitos-para-ia publicar a 0.1.0".
- **Causa-raiz:** `skills.lock` com `ref` de branch e commit pré-release; checagem do Python sem `--system`.
- **Evidência:** `skills.lock` (`"ref": "feat/0001-motor-multiplataforma"`, `"commit": "5f63e02…"`); `requisitos.toml` (`["uv", "python", "find", ">=3.11"]`).

## Modelo do módulo
`enxuto`: troca de cópias exatas (sem editar o motor), ajuste de uma receita e de um teste do verificador.

## Decisões do projeto aplicadas
Regra 7 (`uv`, só biblioteca padrão), Regra 8 (critério executável), Regra 10 (template, skill, comando e README mudam juntos), Regra 12 (versão 0.6.1 no `plugin.json`, selo, tabela de versões e `sdd/releases/history.md`). ADR-0007 (motor vendorizado pelo `skills.lock`, cópia sem edição).

## O que já existe
| Procurei | Onde | Achei | Decisão | Justificativa |
|---|---|---|---|---|
| Cópias do motor | `scripts/`, `templates/requisitos-exemplo.toml` | commit `5f63e02` | reusar | Trocar pelas da tag `v0.1.0`, sem editar. |
| Registro da cópia | `skills.lock` | ref de branch | estender | `ref = v0.1.0`, commit `93abe08`, sha256 novos. |
| Receitas | `requisitos.toml` | 6 itens, validam na v0.1.0 | estender | Só o `python` ganha `--system`. |
| Verificador | `scripts/verificar_readme.py` | aceita `[--arquivo X] instalar …` | reusar | Bloco do `prompt` da v0.1.0 é idêntico; teste novo cobre `instalar --arquivo`. |

## Dependências novas
Nenhuma.

## Rules e IDs da Constituição Aplicáveis
`ARQ-04`, `ARQ-06`, `DUP-01`, `TST-01`, `TST-02`, `SEG-04`, `FLX-07`.

## Critérios de Aceitação Executáveis
1. Para `requisitos.py`, `bootstrap.sh` e `bootstrap.ps1`: `git -C <requisitos-para-ia> show v0.1.0:scripts/<f> | shasum -a 256` = sha256 de `scripts/<f>` = valor no `skills.lock`; idem `exemplos/acme/requisitos.toml` x `templates/requisitos-exemplo.toml`.
2. `skills.lock` tem `"ref": "v0.1.0"` e `"commit": "93abe08895a7e4db3dc032da4ec2ef43bf318766"`.
3. `uv run scripts/requisitos.py validar` sai 0 (macos, linux, windows cobertos).
4. `uv run tests/test_requisitos.py` e `uv run tests/test_verificar_readme.py` saem 0.
5. `uv run scripts/verificar_readme.py README.md` imprime `requisitos: ok`; o bloco do README é igual a `uv run scripts/requisitos.py prompt`.
6. `grep -c '"uv", "python", "find", "--system"' requisitos.toml` = 1.
7. `"version": "0.6.1"` no `plugin.json`, selo 0.6.1 no README, linha 0.6.1 na tabela de versões e em `sdd/releases/history.md`.
8. CI `requisitos` verde em ubuntu-latest, windows-latest e macos-latest.
