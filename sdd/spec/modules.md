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
- [x] `{{PLACEHOLDERS}}` trocados pela skill; seções que não se aplicam são removidas, menos `## Requisitos` (`{{REQUISITOS_RESUMO}}`, `{{PROMPT_IA}}` e `{{REQ_*}}`)

## verificador (`scripts/verificar_readme.py`)
**Responsabilidade:** conferir a forma da seção `## Requisitos` de um README (não a verdade de cada item, que é da skill).
- [x] Falha (código 1) sem `## Requisitos`, com ela depois de `## Instalação`, com `## Antes de começar`, `{{PLACEHOLDER}}`, sem "Onde roda" ou com `pip install`; 2 para uso errado
- [x] Projeto com dependência: exige o bloco "Cole isto na sua IA" com comando real do projeto, trava de licenças e posição antes da instalação (feat-02-01)
- [x] Comando real também por `[project.scripts]` (`uv run <nome>`), `package.json` (`npm run`, `npx`) e `bin/` (fix-02-01)

## requisitos (`scripts/requisitos.py`)
**Responsabilidade:** conferir (`checar`) e instalar com confirmação (`instalar`) os requisitos do readme-studio; base copiada pela skill para outros projetos (troca-se só `REQUISITOS`).
- [x] Só biblioteca padrão; roda por link raw antes de clonar; nunca aceita licença nem lida com segredo (feat-02-01)
