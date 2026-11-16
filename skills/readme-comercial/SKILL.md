---
name: readme-comercial
description: Use para criar ou refazer o README de um projeto em formato comercial (banner, selos de versão, tabelas de instalação e uso, tabela de versões). Descobre a identidade visual do projeto (landing page, logo, cores, mascote) e gera o banner SVG com ela, com texto auto-ajustado.
---

# README comercial

Gera um README amigável para leigos, com banner, selos e versões, a partir do que o projeto já tem, **inclusive a identidade visual dele**.

## Passo a passo
1. **Leia o projeto** (sem alterar nada): README atual, `package.json`/`go.mod`/`pyproject.toml`/`plugin.json`, `LICENSE`, `git remote -v`, `git tag --sort=-v:refname` e pastas principais.
2. **Descubra a identidade visual** (sem alterar nada). O banner de um projeto que já tem marca deve parecer com essa marca:
   - **Onde procurar:** landing page e site (`site/`, `web/`, `landing/`, `docs/index.html`, `public/`), CSS com variáveis em `:root { --... }` (fundo, texto, destaque, borda), `tailwind.config.*`, `theme.*`, logo e ícone (`favicon.svg`, `logo.*`, `icon.*`), cartão social (`og-image.*`), mascotes e ilustrações (componentes `.astro`, `.svelte`, `.tsx` com SVG), fontes (`@font-face` ou link do Google Fonts) e o texto do topo da página (eyebrow, título e subtítulo).
   - **Extraia:** cores (fundo, brilho, texto, texto suave, 3 cores de destaque, painel, borda, sucesso), fontes (sans e mono), logo (SVG em viewBox 32×32) e personagens ou ícones que possam entrar na ilustração.
   - **Registre** em `docs/img/identidade.json`, no formato de `exemplos/forge-sdd/identidade.json`, e o logo em `docs/img/logo.svg.frag` (só as formas, sem `<svg>`; para o traço em degradê use `stroke="url(#hex)"`).
   - **Confirme com o usuário** o que encontrou ("achei fundo escuro, destaque azul-verde, logo em hexágono; uso isso?") quando a confiança for baixa ou houver mais de uma marca. Sem identidade encontrada, use o tema padrão (azul claro) e avise.
   - **Nunca invente marca:** não crie logo, mascote nem paleta que o projeto não tenha. Reaproveite o que existe.
3. **Pergunte só o que faltar**, uma por vez, com padrão sugerido: nome, a frase de valor, público, idioma (padrão pt-BR), 3 rótulos ou personagens para a ilustração e como se instala. **Prefira o texto da própria landing** (título e subtítulo) à frase inventada.
4. **Mostre o plano** (arquivos que serão criados ou substituídos) e **espere o "sim"**. Se já existir `README.md`, guarde cópia em `README.antigo.md` antes de substituir.
5. **Crie o banner com a cara do projeto.** O desenho da direita deve mostrar o que o projeto faz, e o visual deve seguir a identidade.
   - Proponha 2 ou 3 ideias de desenho (ex.: personagens da marca em fluxo; um terminal com o comando principal; uma tela do resultado) e deixe o usuário escolher.
   - Desenhe o fragmento SVG da ilustração (sem `<svg>`), na área x 770-1250 e y 70-370, com formas e texto curto. Salve em `docs/img/ilustracao.svg.frag`. Com identidade, o script já desenha o painel de fundo (x 760-1240, y 62-380) e disponibiliza o gradiente `url(#acc)` e o marcador `url(#seta)` para setas.
   - **Com identidade (recomendado):**
     `python3 -I <plugin>/scripts/gerar_banner.py --identidade docs/img/identidade.json --ilustracao-arquivo docs/img/ilustracao.svg.frag --nome ... --kicker ... --titulo1 ... --titulo2 ... --linha1 ... --linha2 ... --comando "$ npm i -g ..." --saida docs/img/banner.svg`
   - **Sem identidade:** `... --nome ... --kicker ... --linha1 ... --linha2 ... --cores "c1,c2,c3" --ilustracao-arquivo ... --saida ...` (tema azul claro). Os desenhos prontos (`--ilustracao pastas|fluxo|terminal`) só valem para o tema claro e para pedidos rápidos.
   - O script calcula o tamanho da fonte dos textos da esquerda. Textos dentro da sua ilustração devem caber: estime ~0,6 × tamanho da fonte por caractere.
   - **Confira o resultado renderizado.** Chrome headless com `--user-data-dir` temporário e `--screenshot`. No macOS não existe `timeout`; use `perl -e 'alarm 40; exec @ARGV' <comando>` para não travar. Corrija texto que saia dos cards ou linhas que não apareçam (um degradê `objectBoundingBox` em linha horizontal some: use cor sólida).
   - O GitHub mostra SVG como imagem e **não carrega webfonts**: avise que as fontes da marca caem para a fonte do sistema.
6. **Gere o README** a partir de `templates/README.md.tmpl`, trocando os `{{PLACEHOLDERS}}`. Remova as seções que não se aplicam. Com identidade, ponha os selos na mesma paleta (`?color=<destaque>&labelColor=<fundo>`).
7. **Verifique:** o SVG é XML válido (o script já checa), os links do README existem, os selos usam o `owner/repo` correto e a copy do banner vem do projeto.

## Regras de conteúdo
- Linguagem simples; frases curtas; sem jargão sem explicação.
- Selos: versão (`img.shields.io/github/v/tag/<owner>/<repo>`), licença e 2 a 3 selos do que o projeto é. Só inclua selos verdadeiros.
- Tabela **Versões** a partir das tags do git (mais nova no topo). Se não houver tags, use uma linha `0.1.0` e avise o usuário.
- Instalação: um bloco por forma de uso, com comandos copiáveis. Não invente comandos; se não souber, pergunte.
- **Nunca invente funcionalidades, números, depoimentos nem identidade visual.**
- Não exponha e-mails, caminhos pessoais ou segredos.
- Não faça commit nem push, a menos que o usuário peça.

## Padrão visual
Banner 1280×420. **Com identidade:** fundo, brilho, cores, fontes e logo do projeto; nome com logo, eyebrow, título em duas linhas (a segunda em degradê), subtítulo, comando de instalação num terminal e, à direita, um painel com a ilustração. **Sem identidade:** degradê azul, kicker em caixa alta, nome grande, duas linhas de valor e ilustração própria. Selos centralizados abaixo do banner, seguidos de uma frase de impacto.
