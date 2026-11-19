# Release Notes — readme-studio

Este arquivo registra o histórico de entregas de produto deste projeto.

## Entregas

### 0.4.0 — 2026-11-19 — seção Requisitos obrigatória (fix-01-01)
- Todo README ganha `## Requisitos` antes de `## Instalação`, com sete pontos (onde roda, programas, downloads, contas, máquina, licenças e o que você fornece), levantados do projeto e nunca inventados.
- `scripts/verificar_readme.py` confere a seção; o banner passa a rodar com `uv run` (cabeçalho PEP 723).

### 0.3.0 — 2026-11-15 — banner com a identidade do projeto
- O banner usa as cores, fontes, logo e personagens da landing page (`--identidade`, `identidade.json`).

### 0.2.0 — 2026-11-15 — ilustração própria
- Ilustração do projeto (`--ilustracao-arquivo`) ou desenhos prontos (pastas, fluxo, terminal).

### 0.1.0 — 2026-11-15 — primeira versão
- `/readme-gerar`, skill `readme-comercial`, gerador de banner e template de README.
