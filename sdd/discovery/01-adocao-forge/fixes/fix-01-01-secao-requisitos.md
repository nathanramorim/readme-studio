# Fix 01-01: README sem requisitos completos

**Relato:** os requisitos dos READMEs gerados (e o deste repositório) estavam incompletos: quem instala não sabia em que sistema foi testado, o que é baixado na primeira vez, onde fica, que conta precisa nem o que deve fornecer.
**Branch:** `fix/secao-requisitos` (PR #1), empilhada em `chore/forge-sdd`.

## Feature Correlacionada
- **Origem:** módulos `skill` e `template` de `sdd/spec/modules.md` (`skills/readme-comercial/SKILL.md` e `templates/README.md.tmpl`, entregues na 0.1.0 e retro-documentados na iniciativa 01).
- **Causa-raiz:** o template só tinha `## Antes de começar` com `{{REQUISITOS}}`, uma lista solta, e a skill não dizia quais pontos levantar nem onde procurar. Nada conferia a seção.
- **Evidência:** `templates/README.md.tmpl` na `main` (`## Antes de começar` / `{{REQUISITOS}}`) e o `README.md` deste repositório, com dois itens ("Claude Code ou agy", "Python 3 instalado"), sem sistema testado, sem `uv` e sem licenças.

## Modelo do módulo
`enxuto`: skill (Markdown), template e um script verificador sem estado. Após a Camada B, o banner passa a rodar com `uv run` (cabeçalho PEP 723 no `gerar_banner.py`), para o README não contradizer a própria seção Requisitos; isso fecha a divergência da Regra 7. A seção vira `## Requisitos`, obrigatória, com sete pontos fixos; o `verificar_readme.py` confere a forma (não a verdade de cada item, que é da skill).

## Decisões do projeto aplicadas
Regra 6 (sem invenção: requisito sem fonte é perguntado), Regra 7 (`uv`, PEP 723, só biblioteca padrão), Regra 8 (critério executável), Regra 9 (`## Requisitos` antes de `## Instalação`), Regra 10 (template, skill, comando e README mudam juntos), Regra 12 (versão 0.4.0 no `plugin.json`, selo, tabela de versões e `sdd/releases/history.md`). ADR-0001 e ADR-0003.

## O que já existe
| Procurei | Onde | Achei | Decisão | Justificativa |
|---|---|---|---|---|
| Seção de requisitos | `templates/README.md.tmpl` | `## Antes de começar` + `{{REQUISITOS}}` | estender | Vira `## Requisitos` com tabela de sete pontos. |
| Passo de verificação | `SKILL.md`, passo 7 | conferência manual de links e selos | estender | Ganha a chamada ao verificador e a conferência da fonte de cada requisito. |
| Verificador de README | `scripts/` | só `gerar_banner.py` (desenha, não confere) | criar | Responsabilidade diferente (`COD-01`); script novo, só biblioteca padrão. |

## Dependências novas
Nenhuma (só biblioteca padrão: `re`, `sys`, `pathlib`).

## Rules e IDs da Constituição Aplicáveis
`FLX-07`, `ARQ-06`, `TST-01`, `TST-02`, `ARQ-04`, `DUP-01`.

## Critérios de Aceitação Executáveis
1. `uv run scripts/verificar_readme.py README.md` imprime `requisitos: ok` e sai 0.
2. O verificador falha (código 1) num README com `## Antes de começar`: `printf '## Antes de começar\n## Instalação\n' > /tmp/r.md; uv run scripts/verificar_readme.py /tmp/r.md; test $? -eq 1`.
3. `grep -c '^## Requisitos' templates/README.md.tmpl` = 1 e `grep -c 'Antes de começar' templates/README.md.tmpl` = 0.
4. `grep -n '"version": "0.4.0"' .claude-plugin/plugin.json` encontra a linha.
5. `grep -c 'python3' README.md skills/readme-comercial/SKILL.md` = 0 em ambos e `head -5 scripts/gerar_banner.py | grep -c '# /// script'` = 1.
6. `uv run scripts/gerar_banner.py --nome acme --linha1 "Frase." --saida /tmp/rs-banner/banner.svg` sai 0 (XML validado pelo script).
7. `grep -n '0.4.0' sdd/releases/history.md` encontra a entrada.
