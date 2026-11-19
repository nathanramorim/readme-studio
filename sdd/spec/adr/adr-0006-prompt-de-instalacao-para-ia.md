# ADR-0006: Prompt de instalação para a IA, apoiado em script de requisitos

- **Data:** 2026-11-19
- **Status:** `aprovado`
- **Regras afetadas (IDs da constitution):** Regra 9, `ARQ-06`, `FLX-07`
- **Autor / Responsável:** dono do repositório

## Contexto

Quem instala um plugin quase sempre pede ajuda à IA. A seção `## Requisitos` (0.4.0) diz o que é preciso, mas a IA ainda adivinha como conferir e como instalar, e um prompt genérico ("veja se tenho tudo") produz respostas diferentes em cada máquina e pode aceitar licenças sem a pessoa ver.

## Opções Consideradas

1. **Só a tabela de requisitos:** a IA interpreta o texto; nada determinístico.
2. **Prompt livre no README:** fácil de escrever, mas genérico e impossível de conferir.
3. **Script de requisitos (`checar`/`instalar`) + bloco "Cole isto na sua IA" que o usa:** o que é determinístico vira script; o prompt só orquestra e pede o ok da pessoa.

## Decisão

Opção 3. O readme-studio traz `scripts/requisitos.py` (motor igual em todo projeto; troca-se só o bloco `REQUISITOS`) e torna o bloco obrigatório quando o projeto tem dependência além do agente. O `verificar_readme.py` confere que o bloco existe, usa um comando real do projeto, tem a trava "não aceite licenças nem declarações por mim" e vem antes do primeiro passo de instalação. A Regra 9 ganha essa exigência (no lugar de uma regra nova, pelo limite de 15).

## Consequências

- **Positivas:** instalação guiada e igual em qualquer IA; nada é aceito em nome da pessoa; prompt conferível.
- **Negativas / Trade-offs:** cada projeto mantém um script a mais; repositórios privados precisam de `gh` autenticado para rodar o script antes de clonar.
- **Ações de acompanhamento:** aplicar nos plugins que já usam o readme-studio.
