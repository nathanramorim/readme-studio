# Fluxos — readme-studio

## Fluxo principal

```
/readme-gerar (ou "gere o README comercial deste projeto")
  ↓
skill lê o projeto (README, manifestos, LICENSE, remote, tags) sem alterar nada
  ↓
descobre a identidade visual -> docs/img/identidade.json + logo.svg.frag (confirma se a confiança for baixa)
  ↓
pergunta só o que falta, uma por vez
  ↓
mostra o plano e espera o "sim"  (README existente -> README.antigo.md)
  ↓
gerar_banner.py --identidade ... --ilustracao-arquivo ... --saida docs/img/banner.svg  (XML validado)
  ↓
conferência visual no Chrome headless (opcional)
  ↓
README.md a partir de templates/README.md.tmpl
  ↓
verificação: links, selos, copy do banner (e a seção Requisitos)
```

## Sem identidade
Sem marca encontrada, o banner usa o tema azul claro (`--cores`) e a skill avisa a pessoa.
