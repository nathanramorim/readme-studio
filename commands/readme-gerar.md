---
description: Gera (ou refaz) o README comercial do projeto atual, com banner SVG, selos e tabela de versões.
argument-hint: "[nome do projeto]"
---

Gere o README comercial deste projeto seguindo a skill `readme-comercial`.

- Nome sugerido: `$ARGUMENTS` (vazio = nome da pasta do repositório).
- O script do banner está em `${CLAUDE_PLUGIN_ROOT}/scripts/gerar_banner.py` e os templates em `${CLAUDE_PLUGIN_ROOT}/templates/`.
- Mostre o plano e espere a confirmação antes de gravar. Não faça commit.
- A seção `## Requisitos` é obrigatória (veja "Seção Requisitos" na skill). Se o projeto tiver dependências, ela abre com o bloco "Cole isto na sua IA", que usa o script de requisitos do projeto (base em `${CLAUDE_PLUGIN_ROOT}/scripts/requisitos.py`; veja "Prompt de instalação para a IA"). Antes de entregar, rode `uv run ${CLAUDE_PLUGIN_ROOT}/scripts/verificar_readme.py README.md`.
