# Catálogo de Conceitos e Contratos (`DUP-01`) — readme-studio

Regra `DUP-01`: **Um conceito = uma casa.** Antes de criar uma nova entidade, módulo ou utilitário, consulte esta tabela para identificar o módulo dono do conceito e reutilizar ou estender seu contrato público (`DUP-02`).

| Conceito | Pacote/Domínio Dono | Entidade/Struct Mestra | Contrato Público | Observação |
| --- | --- | --- | --- | --- |
| Identidade visual | `scripts/gerar_banner.py` | `identidade.json` | `carregar_identidade(caminho)` | Formato no exemplo em `exemplos/`; padrão escuro completa o que falta |
| Banner | `scripts/gerar_banner.py` | SVG 1280x420 | flags da CLI (`--nome`, `--identidade`, `--saida`...) | XML validado antes de gravar |
| Estrutura do README | `templates/README.md.tmpl` | — | `{{PLACEHOLDERS}}` (requisitos: `{{REQUISITOS_RESUMO}}`, `{{PROMPT_IA}}`, `{{REQ_*}}`) | Seções na ordem do template |
| Regras de conteúdo | `skills/readme-comercial/SKILL.md` | — | "Regras de conteúdo" | Sem invenção |
| Verificação do README | `scripts/verificar_readme.py` | — | `problemas(texto, raiz)`; saída 0 ok, 1 falha, 2 uso | Confere a forma de `## Requisitos` e o bloco "Cole isto na sua IA" |
| Requisitos do projeto | `scripts/requisitos.py` | bloco `REQUISITOS` | `checar [--json]`, `instalar [item] [--sim]`; saída 0 ok, 1 falta, 2 uso | Motor igual em todo projeto; a skill copia e troca só `REQUISITOS` |
