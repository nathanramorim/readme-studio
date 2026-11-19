# Fix 02-01: verificador não reconhece CLIs declaradas do projeto

**Relato:** o `verificar_readme.py` (feat-02-01) recusou o README do gerador-videos (PR nathanramorim/gerador-videos#6) com "não usa nenhum comando real", embora o bloco use `uv run gv requisitos checar`, e `gv` esteja declarado em `[project.scripts]` do `pyproject.toml`.
**Branch:** `feat/02-prompt-instalacao` (mesmo PR #4).

## Feature Correlacionada
- **Origem:** feat-02-01, módulo `verificador` (`scripts/verificar_readme.py`, `comando_real`).
- **Causa-raiz:** `comando_real` só aceitava caminho de script no repositório ou executável em `bin/`; CLIs declaradas por entry point (`[project.scripts]`) e por `package.json` (`bin`, `scripts`) não contavam.
- **Evidência:** `uv run scripts/verificar_readme.py` no README e no `pyproject.toml` da branch `feat/aa40-prompt-instalacao` do gerador-videos → `[falha] o bloco 'Cole isto na sua IA' não usa nenhum comando real do projeto`.

## Modelo do módulo
`enxuto`: o verificador continua sem estado. Ganha a leitura dos nomes declarados no projeto (`[project.scripts]`, `package.json` `bin` e `scripts`, executáveis de `bin/`) e o reconhecimento de `uv run <nome>`, `uvx --from <pasta local> <nome>` (sem `--from` local o uvx busca no PyPI, então não conta), `npm run <script>` (ou os embutidos `npm test`/`npm start`), `npx <bin>`, `pnpm`/`yarn`/`bun` e `<nome>` direto. O `--from` só vale antes do nome do comando. Manifesto com tipo errado é ignorado, sem traceback. A busca de executáveis e de scripts ignora `venv/` e `site-packages/` (ambientes Python não ocultos, cujos `bin/python`/`pip` não são comandos do projeto).

## Decisões do projeto aplicadas
ADR-0006 (o bloco usa um comando real do projeto), ADR-0003 (só biblioteca padrão: `tomllib` quando houver, senão leitura simples da seção), Regra 6 (nome inventado continua falhando), Regra 8.

## O que já existe
| Procurei | Onde | Achei | Decisão | Justificativa |
|---|---|---|---|---|
| Reconhecer comando real | `verificar_readme.py` (`comando_real`) | caminho de script e `bin/` | estender | Mesma responsabilidade; só amplia as fontes de nomes |

## Dependências novas
Nenhuma (`tomllib` e `json` da biblioteca padrão).

## Rules e IDs da Constituição Aplicáveis
`ARQ-04`, `ARQ-06`, `TST-01`, `TST-02`, `TST-03`.

## Critérios de Aceitação Executáveis
1. `uv run tests/test_verificar_readme.py` sai 0, com casos positivos para `[project.scripts]` (`uv run gv ...`), `package.json` `scripts` (`npm run x`) e `bin` (`npx y`), `bin/` do plugin e caminho de script, e negativo para um nome inventado.
2. `uv run scripts/verificar_readme.py <README do gerador-videos> --raiz <pasta com o pyproject dele>` imprime `requisitos: ok`.
3. `uv run scripts/verificar_readme.py README.md` continua `requisitos: ok`.
