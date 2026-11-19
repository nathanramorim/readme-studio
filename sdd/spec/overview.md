# Overview — readme-studio

Plugin (Claude Code e agy) com a skill `readme-comercial` e o comando `/readme-gerar`: o agente lê o projeto consumidor, descobre a identidade visual dele, pergunta só o que falta, mostra o plano e, depois do "sim", gera o `README.md` pelo template e o banner SVG pelo `gerar_banner.py`, com texto que sempre cabe.

## Índice
- `stack.md` — tecnologias
- `modules.md` — componentes
- `flows.md` — fluxos principais
- `decisions.md` — decisões de design

---

## Arquitetura (C4 Model)

### Nível 1: Contexto
```mermaid
graph TB
  Pessoa((Pessoa)) --> Agente[Agente: Claude Code ou agy]
  Agente --> Skill[readme-studio]
  Skill --> Projeto[(Projeto consumidor: código, landing page, logo, tags do git)]
  Skill --> README[README.md + docs/img/banner.svg]
```

### Nível 2: Containers
```mermaid
graph LR
  Cmd[/readme-gerar/] --> Skill[SKILL.md readme-comercial]
  Skill --> Ident[docs/img/identidade.json + fragmentos SVG]
  Ident --> Banner[scripts/gerar_banner.py]
  Banner --> SVG[docs/img/banner.svg]
  Skill --> Tmpl[templates/README.md.tmpl]
  Tmpl --> README[README.md]
```
