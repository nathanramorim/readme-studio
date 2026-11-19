---
description: Como organizar comando, skill, template e script do readme-studio, recursos estáticos e o modelo de módulo.
globs: ["commands/**", "skills/**", "scripts/**", "templates/**", "sdd/spec/**"]
regras: [ARQ-01, ARQ-02, ARQ-03, ARQ-04, ARQ-05, ARQ-06, ARQ-11]
---

# Guia Prático — Arquitetura da skill

Instruções para aplicar `ARQ-01` a `ARQ-06` e `ARQ-11` de `sdd/memory/constitution.md` (`GOV-04`).

## 1. Camadas (`ARQ-01`, `ARQ-02`, `ARQ-06`)
- **Borda:** `commands/readme-gerar.md` só aponta para a skill, o script e os templates via `${CLAUDE_PLUGIN_ROOT}`; a lógica fica na skill.
- Dependências: comando -> `skills/readme-comercial/SKILL.md` -> `templates/` e `scripts/`; nenhum script lê a skill.
- Contratos públicos (flags do `gerar_banner.py`, formato do `identidade.json`, placeholders do template) mudam junto com a skill, o exemplo e o README.

## 2. Recursos, dependências e simulação (`ARQ-03`, `ARQ-04`, `ARQ-05`)
- Tudo que a skill usa vem do próprio plugin (`${CLAUDE_PLUGIN_ROOT}` ou a pasta copiada no agy); nenhum caminho de projeto consumidor fixo.
- Nenhum nome de empresa, pessoa ou perfil na skill, no comando, no template nem no script (Regra 3); exemplos com projeto fictício.
- Scripts só com a biblioteca padrão; dependência nova segue `sdd-seguranca.md`.
- A skill só grava depois do "sim" da pessoa; antes disso, apenas lê.

## 3. Modelo de módulo na spec (`ARQ-11`)
Toda spec declara `completo` ou `enxuto` com justificativa. A skill hoje é `enxuto` (Markdown e um script sem estado).
