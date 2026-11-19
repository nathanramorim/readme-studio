# ADR-0003: Python sempre via uv, scripts só com a biblioteca padrão

- **Data:** 2026-11-19
- **Status:** `aprovado`
- **Regras afetadas (IDs da constitution):** `ARQ-04`, `COD-02`, Regra 7
- **Autor / Responsável:** dono do repositório

## Contexto

Os scripts rodam na máquina de quem instala o plugin. Instruções com `pip` e venv quebram e poluem o ambiente. O `gerar_banner.py` já usa só a biblioteca padrão, mas as instruções da skill ainda o chamam com `python3 -I`.

## Opções Consideradas

1. **`python3` do sistema:** depende da versão instalada e abre a porta para `pip`.
2. **`uv run` com cabeçalho PEP 723 em cada script:** o `uv` traz o Python certo; sem dependências externas.

## Decisão

Opção 2 para todo script do repositório. Nunca escrever `pip` em instruções nem no README gerado.

## Consequências

- **Positivas:** um comando roda tudo, em qualquer máquina com `uv`.
- **Negativas / Trade-offs:** exige `uv` instalado (vai para `## Requisitos`).
- **Ações de acompanhamento:** cabeçalho PEP 723 no `gerar_banner.py` e `uv run` no passo 5 da skill (Divergências conhecidas).
