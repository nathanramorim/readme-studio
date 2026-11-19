# Release Notes — readme-studio

Este arquivo registra o histórico de entregas de produto deste projeto.

## Entregas

### 0.6.0 — 2026-11-19 — requisitos multiplataforma (feat-03-01)
- O `scripts/requisitos.py` passa a ser o motor requisitos-para-ia (cópia exata do commit `5f63e02`, registrada no novo `skills.lock`), com `bootstrap.sh` (macOS e Linux) e `bootstrap.ps1` (Windows), que instalam o `uv` pelo instalador oficial só com o ok da pessoa. A receita do readme-studio fica em `requisitos.toml`.
- O README abre Requisitos com o bloco de `requisitos.py prompt` e uma linha por sistema; o Homebrew deixa de ser pré-requisito.
- `verificar_readme.py` falha sem `requisitos.toml` (projeto com dependência), sem `bootstrap.ps1` ou `bootstrap.sh` no bloco, com Homebrew no bloco, sem `requisitos.py instalar` ou sem macOS, Linux e Windows na seção. A skill cria o `requisitos.toml` a partir dos exemplos do motor (`templates/requisitos-exemplo.toml`).
- CI (`.github/workflows/requisitos.yml`) em ubuntu-latest, windows-latest e macos-latest.

### 0.5.0 — 2026-11-19 — prompt de instalação para a IA (feat-02-01)
- Novo `scripts/requisitos.py` (`checar [--json]` e `instalar [item] [--sim]`): confere e instala os requisitos, pergunta antes de cada item e nunca aceita licenças nem lida com senhas. É também a base que a skill copia para outros projetos.
- Template ganha `{{PROMPT_IA}}`: o bloco "Cole isto na sua IA" abre a seção Requisitos quando o projeto tem dependências.
- `verificar_readme.py` confere o bloco: existe, usa um comando real do projeto, tem a trava de licenças e vem antes da instalação.

### 0.4.0 — 2026-11-19 — seção Requisitos obrigatória (fix-01-01)
- Todo README ganha `## Requisitos` antes de `## Instalação`, com sete pontos (onde roda, programas, downloads, contas, máquina, licenças e o que você fornece), levantados do projeto e nunca inventados.
- `scripts/verificar_readme.py` confere a seção; o banner passa a rodar com `uv run` (cabeçalho PEP 723).

### 0.3.0 — 2026-11-15 — banner com a identidade do projeto
- O banner usa as cores, fontes, logo e personagens da landing page (`--identidade`, `identidade.json`).

### 0.2.0 — 2026-11-15 — ilustração própria
- Ilustração do projeto (`--ilustracao-arquivo`) ou desenhos prontos (pastas, fluxo, terminal).

### 0.1.0 — 2026-11-15 — primeira versão
- `/readme-gerar`, skill `readme-comercial`, gerador de banner e template de README.
