# ADR-0005: Adoção do Forge SDD 4.9.1-beta e regras desta Constituição

- **Data:** 2026-11-19
- **Status:** `aprovado`
- **Regras afetadas (IDs da constitution):** `GOV-01`, `GOV-02`, `FLX-01`, `FLX-07`, Regras 1 a 15
- **Autor / Responsável:** dono do repositório

## Contexto

Toda skill é um produto de TI e segue o processo de desenvolvimento do Forge SDD: repositório próprio e replicável, Constituição alinhada e README pelo readme-studio com `## Requisitos`. Toda feature ou fix precisa mapear as execuções, criar histórico e sequencializar o contexto. O binário disponível é o Forge 4.9.1-beta, e a Regra 11 proíbe mesclar uma versão `-beta` na `main`.

## Opções Consideradas

1. **Esperar uma versão estável do Forge:** mantém a Regra 11 intacta, mas deixa o fix da seção Requisitos (PR #1) sem fluxo.
2. **Adotar a 4.9.1-beta agora, com exceção temporária e com prazo para a Regra 11:** o fluxo começa já e a exceção vence sozinha.

## Decisão

Opção 2. Instalação com `forge init --version 4.9.1-beta --agent claude,gemini --stack python`, Constituição com 15 regras (branch por iniciativa, toda feature ou fix pelo fluxo, replicável, sem invenção, `uv` sempre, critério executável, `## Requisitos` obrigatória, contratos públicos, borda segura) e as divergências atuais registradas. Exceção (`GOV-02`), válida para a estrutura do Forge, não para versões do produto:

```constitution-exception
regra: Regra 11 (FLX-07) — mesclar estrutura Forge SDD 4.9.1-beta na main
motivo: única versão do Forge disponível; o fluxo SDD precisa valer já para features e fixes do readme-studio
prazo: 2026-12-31
responsavel: dono do repositório (nathanramorim)
```

## Consequências

- **Positivas:** toda mudança passa a ter spec, revisão da Governança, `status.md` e telemetria.
- **Negativas / Trade-offs:** a estrutura beta pode mudar; o merge na `main` depende da decisão humana (Camada C) dentro do prazo.
- **Ações de acompanhamento:** `forge update --upgrade` para a versão estável antes de 2026-12-31 (ou renovar a exceção com nova ADR); sessões de telemetria fora do git (`.gitignore`).
