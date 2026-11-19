# ADR-0001: A skill conduz; um script determinístico desenha o banner

- **Data:** 2026-11-15 (registrada em 2026-11-19, retroativa)
- **Status:** `aprovado`
- **Regras afetadas (IDs da constitution):** `ARQ-06`, Regra 6, Regra 10
- **Autor / Responsável:** dono do repositório

## Contexto

Um README comercial tem duas partes de natureza diferente: o texto, que depende de ler o projeto e conversar com a pessoa, e o banner, que precisa caber em 1280x420 sem texto saindo dos cards. Pedir à IA que escreva o SVG inteiro dá tamanhos de fonte errados e XML inválido.

## Opções Consideradas

1. **IA escreve README e SVG:** flexível, mas o texto transborda e o XML quebra.
2. **Skill conduz e escreve o README pelo template; script calcula as fontes e grava o SVG:** a IA só escolhe textos e o desenho da ilustração.

## Decisão

Opção 2, já em uso desde a 0.1.0: `skills/readme-comercial/SKILL.md` conduz, `templates/README.md.tmpl` dá a estrutura e `scripts/gerar_banner.py` desenha o banner, escapando o texto e validando o XML antes de gravar.

## Consequências

- **Positivas:** banner sempre válido e legível; README com estrutura única.
- **Negativas / Trade-offs:** a ilustração própria é um fragmento SVG escrito pela IA, conferido só visualmente.
- **Ações de acompanhamento:** testes automatizados do script (Divergências conhecidas da Constituição).
