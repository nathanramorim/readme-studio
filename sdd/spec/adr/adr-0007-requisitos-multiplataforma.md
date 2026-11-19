# ADR-0007: Requisitos multiplataforma pelo motor requisitos-para-ia

- **Data:** 2026-11-19
- **Status:** `aprovado`
- **Regras afetadas (IDs da constitution):** Regra 9, `ARQ-06`, `DUP-01`, `FLX-07`
- **Autor / Responsável:** dono do repositório

## Contexto

O 0.5.0 (ADR-0006) trouxe um `scripts/requisitos.py` próprio, escrito e testado só no macOS, e o bloco "Cole isto na sua IA" mandava instalar o `uv` com `brew install uv`. Quem usa Windows ou Linux ficava sem caminho, e o Homebrew virava pré-requisito escondido. Como a skill copia esse script para os projetos que gera, o erro se espalhava.

## Opções Consideradas

1. **Corrigir o script próprio:** mantém um segundo motor, duplicado e sem prova em Windows e Linux.
2. **Vendorizar o motor requisitos-para-ia:** receita declarativa (`requisitos.toml`) por SO, `bootstrap.sh`/`bootstrap.ps1` que instalam o `uv` pelo instalador oficial com o ok da pessoa, trava contra agir pela pessoa e o bloco do README gerado pelo próprio motor (`prompt`).

## Decisão

Opção 2. O readme-studio copia `scripts/requisitos.py`, `scripts/bootstrap.sh` e `scripts/bootstrap.ps1` sem editar, registra origem, commit e sha256 no `skills.lock`, e escreve só o `requisitos.toml`. O exemplo completo do motor vai para `templates/requisitos-exemplo.toml`, de onde a skill parte para criar o `requisitos.toml` dos projetos (nunca inventa comandos). O `verificar_readme.py` falha sem `requisitos.toml` num projeto com dependência, sem o caminho do Windows (`bootstrap.ps1`) ou do macOS/Linux (`bootstrap.sh`) no bloco, ou com o Homebrew no bloco. Um workflow de CI prova a receita em ubuntu-latest, windows-latest e macos-latest.

## Consequências

- **Positivas:** o mesmo bloco em todo projeto, com caminho para os 3 sistemas; uma casa só para o motor (`DUP-01`); prova no CI.
- **Negativas / Trade-offs:** o motor pede Python 3.11+ (`tomllib`); atualizar o motor é trocar as cópias e o `skills.lock` juntos (o teste confere o sha256).
- **Ações de acompanhamento:** fixar o motor numa tag quando o requisitos-para-ia publicar a 0.1.0 na `main`; aplicar nos plugins que já usam o readme-studio.
