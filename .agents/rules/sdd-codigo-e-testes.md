---
description: Como manter os scripts Python do readme-studio limpos, pendências rastreáveis e critérios executáveis com uv.
globs: ["**/*.py", "tests/**", "templates/**", "skills/**"]
regras: [COD-01, COD-02, COD-04, COD-06, TST-01, TST-02, TST-05]
---

# Guia Prático — Código Limpo e Critérios Executáveis

Rotina para atender `COD-01`, `COD-02`, `COD-04`, `COD-06`, `TST-01`, `TST-02` e `TST-05` de `sdd/memory/constitution.md` (`GOV-04`).

## 1. Higiene (`COD-01`, `COD-02`, `COD-04`, `COD-06`)
- Um script, uma responsabilidade (`gerar_banner.py` desenha; um verificador só confere).
- Scripts com cabeçalho PEP 723 e rodados com `uv run`; nunca `pip`. Se houver `ruff`, `uv run ruff check` passa.
- Ao trocar uma flag, placeholder ou seção, remova o antigo e as referências órfãs na mesma entrega.
- Pendência só como `# TODO(feat-XX): descrição`.

## 2. Critérios (`TST-01`, `TST-02`, `TST-05`)
- Cada critério da spec é um comando que sai 0: gerar o banner de exemplo em pasta temporária (o script valida o XML), `uv run scripts/verificar_readme.py README.md`, `grep` de seções.
- Mudou o template ou a skill: confira o README deste repositório com o verificador no mesmo PR.
- Testes automatizados (pytest via `uv`) entram com a próxima feature (Divergências conhecidas).
