# Módulos — readme-studio

Dependências apontam para dentro: `commands/readme-gerar.md` (borda) -> `skills/readme-comercial/SKILL.md` -> `templates/` e `scripts/` (`ARQ-02`). Modelo: **enxuto** (skill em Markdown e um script sem estado; tudo vira arquivo no projeto consumidor).

## comando (`commands/readme-gerar.md`)
**Responsabilidade:** ponto de entrada no Claude Code; aponta para a skill, o script e os templates pelo `${CLAUDE_PLUGIN_ROOT}`.
- [x] `/readme-gerar [nome]` (vazio = nome da pasta)
- [x] Mostra o plano e espera a confirmação; não faz commit

## skill (`skills/readme-comercial/SKILL.md`)
**Responsabilidade:** conduzir a geração: ler o projeto, descobrir a identidade, perguntar o que falta, mostrar o plano, gerar banner e README e verificar.
- [x] Descoberta de identidade (landing, CSS, logo, mascote) para `docs/img/identidade.json`
- [x] Cópia `README.antigo.md` antes de substituir
- [x] Regras de conteúdo: sem invenção, selos verdadeiros, versões pelas tags

## banner (`scripts/gerar_banner.py`)
**Responsabilidade:** desenhar o banner SVG 1280x420 com fontes calculadas pelo comprimento do texto.
- [x] Tema escuro com `--identidade` (exige `--ilustracao-arquivo`); tema claro com `--cores`
- [x] Desenhos prontos `--ilustracao pastas|fluxo|terminal` (tema claro)
- [x] Texto escapado; XML validado antes de gravar em `--saida`

## template (`templates/README.md.tmpl`)
**Responsabilidade:** estrutura única do README (banner, selos, benefícios, requisitos, instalação, uso, versões, licença).
- [x] `{{PLACEHOLDERS}}` trocados pela skill; seções que não se aplicam são removidas
