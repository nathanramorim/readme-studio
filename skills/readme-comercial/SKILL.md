---
name: readme-comercial
description: Use para criar ou refazer o README de um projeto em formato comercial (banner, selos de versão, tabelas de instalação e uso, tabela de versões). Gera o banner SVG com texto auto-ajustado.
---

# README comercial

Gera um README amigável para leigos, com banner, selos e versões, a partir do que o projeto já tem.

## Passo a passo
1. **Leia o projeto** (sem alterar nada): README atual, `package.json`/`go.mod`/`pyproject.toml`/`plugin.json`, `LICENSE`, `git remote -v`, `git tag --sort=-v:refname` e pastas principais.
2. **Pergunte só o que faltar**, uma por vez, com padrão sugerido: nome, a frase de valor (duas linhas curtas), público, idioma (padrão pt-BR), cores (padrão azul `#1e3a8a,#2563eb,#06b6d4`), 3 rótulos para o banner (padrão: 3 áreas do projeto) e como se instala.
3. **Mostre o plano** (arquivos que serão criados ou substituídos) e **espere o "sim"**. Se já existir `README.md`, guarde cópia em `README.antigo.md` antes de substituir.
4. **Crie o banner com a cara do projeto.** O banner não pode ser genérico: o desenho da direita deve mostrar o que o projeto faz.
   - Proponha ao usuário 2 ou 3 ideias de desenho (ex.: um terminal com o comando principal; um fluxo de passos; uma tela ou arquivo do resultado; um antes e depois) e deixe-o escolher.
   - Desenhe o fragmento SVG da ilustração (sem a tag `<svg>`), na área x 770-1250 e y 90-370, usando só formas e texto curto. Pode usar os gradientes `#bg` e `#card` do banner. Salve em `docs/ilustracao.svg.frag`.
   - Gere: `python3 -I <plugin>/scripts/gerar_banner.py --nome ... --kicker ... --linha1 ... --linha2 ... --cores "c1,c2,c3" --ilustracao-arquivo docs/ilustracao.svg.frag --saida docs/banner.svg`
   - Só use os desenhos prontos (`--ilustracao pastas|fluxo|terminal` com `--rotulos "a|b|c"`) se o usuário pedir algo rápido.
   - O script calcula o tamanho da fonte do texto da esquerda. Textos dentro da sua ilustração devem caber: estime ~0,6 × tamanho da fonte por caractere.
   - **Confira o resultado renderizado** (ex.: Chrome headless com `--user-data-dir` temporário e `--screenshot`). Corrija texto que saia dos cards.
5. **Gere o README** a partir de `templates/README.md.tmpl`, trocando os `{{PLACEHOLDERS}}`. Remova as seções que não se aplicam.
6. **Verifique:** o SVG é XML válido (o script já checa), os links do README existem, os selos usam o `owner/repo` correto.

## Regras de conteúdo
- Linguagem simples; frases curtas; sem jargão sem explicação.
- Selos: versão (`img.shields.io/github/v/tag/<owner>/<repo>`), licença e 2 a 3 selos do que o projeto é. Só inclua selos verdadeiros.
- Tabela **Versões** a partir das tags do git (mais nova no topo). Se não houver tags, use uma linha `0.1.0` e avise o usuário.
- Instalação: um bloco por forma de uso, com comandos copiáveis. Não invente comandos; se não souber, pergunte.
- **Nunca invente funcionalidades, números ou depoimentos.**
- Não exponha e-mails, caminhos pessoais ou segredos.
- Não faça commit nem push, a menos que o usuário peça.

## Padrão visual
Banner 1280×420, degradê azul, kicker em caixa alta, nome grande, duas linhas de valor e, à direita, uma ilustração própria do projeto. Selos centralizados abaixo do banner, seguidos de uma frase de impacto.
