# ADR-0004: Plugin na raiz, cópia para o agy, Forge SDD fora do plugin

- **Data:** 2026-11-15 (registrada em 2026-11-19, retroativa)
- **Status:** `aprovado`
- **Regras afetadas (IDs da constitution):** `DUP-10`, Regra 3
- **Autor / Responsável:** dono do repositório

## Contexto

O plugin é instalado direto do GitHub (`/plugin marketplace add`), com `source: ./` no `marketplace.json`. Com a adoção do Forge SDD, a raiz passou a ter também `sdd/`, `.agents/`, `.claude/`, `.gemini/`, `.forge/`, `CLAUDE.md` e `GEMINI.md`.

## Opções Consideradas

1. **Mover o plugin para `plugins/readme-studio/`:** isola totalmente, mas muda o caminho de instalação de quem já usa.
2. **Manter o plugin na raiz:** o Claude Code só carrega `commands/`, `skills/` e o manifesto do plugin; os arquivos do Forge ficam em pastas ocultas que o plugin não usa. O agy recebe só a cópia de `skills/`, `scripts/` e `templates/`.

## Decisão

Opção 2. Nada do Forge SDD entra em `commands/`, `skills/`, `scripts/` ou `templates/`.

## Consequências

- **Positivas:** quem já instalou não precisa mudar nada.
- **Negativas / Trade-offs:** a instalação pelo marketplace baixa também as pastas do Forge (pequenas, só Markdown).
- **Ações de acompanhamento:** se surgir conflito de comandos entre `.claude/commands/` e `commands/`, migrar para a opção 1 com nova ADR.
