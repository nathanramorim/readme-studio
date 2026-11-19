---
description: Gera (ou refaz) o README comercial do projeto atual, com banner SVG, selos e tabela de versões.
argument-hint: "[nome do projeto]"
---

Gere o README comercial deste projeto seguindo a skill `readme-comercial`.

- Nome sugerido: `$ARGUMENTS` (vazio = nome da pasta do repositório).
- O script do banner está em `${CLAUDE_PLUGIN_ROOT}/scripts/gerar_banner.py` e os templates em `${CLAUDE_PLUGIN_ROOT}/templates/`.
- Mostre o plano e espere a confirmação antes de gravar. Não faça commit.
- A seção `## Requisitos` é obrigatória (veja "Seção Requisitos" na skill). Se o projeto tiver dependências, ele ganha o motor multiplataforma (`${CLAUDE_PLUGIN_ROOT}/scripts/requisitos.py`, `bootstrap.sh` e `bootstrap.ps1`, copiados sem editar) e um `requisitos.toml` feito a partir de `${CLAUDE_PLUGIN_ROOT}/templates/requisitos-exemplo.toml`, e a seção abre com o bloco que `uv run scripts/requisitos.py prompt` imprime (veja "Prompt de instalação para a IA"). O Homebrew nunca é pré-requisito. Antes de entregar, rode `uv run ${CLAUDE_PLUGIN_ROOT}/scripts/verificar_readme.py README.md`.
