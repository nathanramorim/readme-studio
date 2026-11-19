# ADR-0002: O banner usa a identidade do projeto e nunca inventa marca

- **Data:** 2026-11-15 (registrada em 2026-11-19, retroativa)
- **Status:** `aprovado`
- **Regras afetadas (IDs da constitution):** Regra 3, Regra 6
- **Autor / Responsável:** dono do repositório

## Contexto

Um banner genérico não lembra o produto. Projetos com landing page já têm cores, fontes, logo e personagens. Inventar uma marca, por outro lado, cria algo que o dono do projeto não aprovou.

## Opções Consideradas

1. **Tema fixo para todos:** simples, mas todo README fica igual.
2. **Descobrir a identidade no projeto e gravá-la em `docs/img/identidade.json`; sem identidade, tema azul claro:** o banner segue a marca existente.

## Decisão

Opção 2 (versão 0.3.0). A skill procura a identidade na landing, no CSS e nos logos do projeto consumidor, confirma quando a confiança é baixa e nunca cria logo, mascote ou paleta que o projeto não tenha. O script completa o que faltar com o tema escuro padrão.

## Consequências

- **Positivas:** banner com a cara do produto, reaproveitável pelo próprio projeto.
- **Negativas / Trade-offs:** o GitHub não carrega webfonts no SVG; as fontes caem para a do sistema (avisado).
- **Ações de acompanhamento:** trocar o exemplo de identidade por um projeto fictício (Regra 3).
