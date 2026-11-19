---
name: readme-comercial
description: Use para criar ou refazer o README de um projeto em formato comercial (banner, selos de versão, tabelas de instalação e uso, tabela de versões). Descobre a identidade visual do projeto (landing page, logo, cores, mascote) e gera o banner SVG com ela, com texto auto-ajustado.
---

# README comercial

Gera um README amigável para leigos, com banner, selos e versões, a partir do que o projeto já tem, **inclusive a identidade visual dele**.

## Passo a passo
1. **Leia o projeto** (sem alterar nada): README atual, `package.json`/`go.mod`/`pyproject.toml`/`plugin.json`, `LICENSE`, `git remote -v`, `git tag --sort=-v:refname` e pastas principais. Levante também os **requisitos** (seção abaixo, "Seção Requisitos"): é obrigatória em todo README.
2. **Descubra a identidade visual** (sem alterar nada). O banner de um projeto que já tem marca deve parecer com essa marca:
   - **Onde procurar:** landing page e site (`site/`, `web/`, `landing/`, `docs/index.html`, `public/`), CSS com variáveis em `:root { --... }` (fundo, texto, destaque, borda), `tailwind.config.*`, `theme.*`, logo e ícone (`favicon.svg`, `logo.*`, `icon.*`), cartão social (`og-image.*`), mascotes e ilustrações (componentes `.astro`, `.svelte`, `.tsx` com SVG), fontes (`@font-face` ou link do Google Fonts) e o texto do topo da página (eyebrow, título e subtítulo).
   - **Extraia:** cores (fundo, brilho, texto, texto suave, 3 cores de destaque, painel, borda, sucesso), fontes (sans e mono), logo (SVG em viewBox 32×32) e personagens ou ícones que possam entrar na ilustração.
   - **Registre** em `docs/img/identidade.json`, no formato de `exemplos/forge-sdd/identidade.json`, e o logo em `docs/img/logo.svg.frag` (só as formas, sem `<svg>`; para o traço em degradê use `stroke="url(#hex)"`).
   - **Confirme com o usuário** o que encontrou ("achei fundo escuro, destaque azul-verde, logo em hexágono; uso isso?") quando a confiança for baixa ou houver mais de uma marca. Sem identidade encontrada, use o tema padrão (azul claro) e avise.
   - **Nunca invente marca:** não crie logo, mascote nem paleta que o projeto não tenha. Reaproveite o que existe.
3. **Pergunte só o que faltar**, uma por vez, com padrão sugerido: nome, a frase de valor, público, idioma (padrão pt-BR), 3 rótulos ou personagens para a ilustração e como se instala. Requisito que o projeto não mostra (sistema testado, tamanho de um download, conta necessária) é **perguntado, nunca chutado**. **Prefira o texto da própria landing** (título e subtítulo) à frase inventada.
4. **Mostre o plano** (arquivos que serão criados ou substituídos) e **espere o "sim"**. Se já existir `README.md`, guarde cópia em `README.antigo.md` antes de substituir.
5. **Crie o banner com a cara do projeto.** O desenho da direita deve mostrar o que o projeto faz, e o visual deve seguir a identidade.
   - Proponha 2 ou 3 ideias de desenho (ex.: personagens da marca em fluxo; um terminal com o comando principal; uma tela do resultado) e deixe o usuário escolher.
   - Desenhe o fragmento SVG da ilustração (sem `<svg>`), na área x 770-1250 e y 70-370, com formas e texto curto. Salve em `docs/img/ilustracao.svg.frag`. Com identidade, o script já desenha o painel de fundo (x 760-1240, y 62-380) e disponibiliza o gradiente `url(#acc)` e o marcador `url(#seta)` para setas.
   - **Com identidade (recomendado):**
     `uv run <plugin>/scripts/gerar_banner.py --identidade docs/img/identidade.json --ilustracao-arquivo docs/img/ilustracao.svg.frag --nome ... --kicker ... --titulo1 ... --titulo2 ... --linha1 ... --linha2 ... --comando "$ npm i -g ..." --saida docs/img/banner.svg`
   - **Sem identidade:** `... --nome ... --kicker ... --linha1 ... --linha2 ... --cores "c1,c2,c3" --ilustracao-arquivo ... --saida ...` (tema azul claro). Os desenhos prontos (`--ilustracao pastas|fluxo|terminal`) só valem para o tema claro e para pedidos rápidos.
   - O script calcula o tamanho da fonte dos textos da esquerda. Textos dentro da sua ilustração devem caber: estime ~0,6 × tamanho da fonte por caractere.
   - **Confira o resultado renderizado.** Chrome headless com `--user-data-dir` temporário e `--screenshot`. No macOS não existe `timeout`; use `perl -e 'alarm 40; exec @ARGV' <comando>` para não travar. Corrija texto que saia dos cards ou linhas que não apareçam (um degradê `objectBoundingBox` em linha horizontal some: use cor sólida).
   - O GitHub mostra SVG como imagem e **não carrega webfonts**: avise que as fontes da marca caem para a fonte do sistema.
6. **Gere o README** a partir de `templates/README.md.tmpl`, trocando os `{{PLACEHOLDERS}}`. Remova as seções que não se aplicam, **menos `## Requisitos`, que é obrigatória**: nela, remova só as linhas da tabela que não se aplicam. O `{{PROMPT_IA}}` é o bloco "Cole isto na sua IA" (seção "Prompt de instalação para a IA"); só sai se o projeto não depender de nada além do agente. Com identidade, ponha os selos na mesma paleta (`?color=<destaque>&labelColor=<fundo>`).
7. **Verifique:** o SVG é XML válido (o script já checa), os links do README existem, os selos usam o `owner/repo` correto e a copy do banner vem do projeto. Rode `uv run <plugin>/scripts/verificar_readme.py README.md`: ele falha se faltar `## Requisitos`, se sobrar `## Antes de começar` ou `{{PLACEHOLDER}}`, se faltar a linha **Onde roda**, se aparecer `pip install` ou se o bloco "Cole isto na sua IA" faltar (projeto com dependências), não usar um comando real do projeto, não tiver a trava de licenças ou vier depois do primeiro passo de instalação. Rode também o `checar` do script de requisitos do projeto e confira que a saída bate com a tabela. Confira também, à mão, que cada requisito tem fonte no projeto (a lista da seção abaixo).

## Seção Requisitos (obrigatória)
Todo README tem `## Requisitos`, logo antes de `## Instalação`. Ela substitui o antigo "Antes de começar". É curta, em linguagem simples, com comandos copiáveis, e o detalhe longo vai para um link. Cubra só o que se aplica, nesta ordem:

1. **Onde roda:** sistema testado de verdade (ex.: macOS Apple Silicon) e com qual agente (Claude Code, agy). Não diga "funciona em tudo" sem prova.
2. **Programas:** cada programa com a versão mínima (ou fixa), o comando de instalação (`brew install …`, link do `uv`) e como o projeto confere (ex.: `doctor`, `--validar`). Python sempre pelo [`uv`](https://docs.astral.sh/uv/), nunca `pip`.
3. **Downloads na primeira execução:** modelos, navegadores, fontes e pacotes, com tamanho aproximado e onde ficam guardados. Diga se precisa de internet e quando.
4. **Contas e chaves:** contas externas, permissões e tokens, e onde o segredo fica (Keychain, `.env` fora do git). Nunca no git. Repositório privado também entra aqui.
5. **Máquina:** memória, disco e se o computador precisa ficar ligado (ex.: agendamento).
6. **Licenças e limites de uso:** licença de terceiros que restringe o uso (ex.: modelo só para uso não comercial) e limites de API.
7. **O que você fornece:** o que a pessoa precisa trazer (amostra de voz com consentimento, arquivo de marca, foto, pasta de dados).

**Onde descobrir (nunca invente):** comando de diagnóstico (`doctor`, `check`, `--validar`) e o que ele confere; `pyproject.toml` (`requires-python`, extras), cabeçalho PEP 723 dos scripts (`# /// script`), `package.json` (`engines`), `.nvmrc`, `.python-version`, `.tool-versions`, `go.mod`; `Dockerfile` e `docker-compose.*`; menções a `brew install`, `apt` e `npx`; variáveis de ambiente lidas no código (`os.environ`, `process.env`) e `.env.example`; caminhos de cache e de modelos no código; `LICENSE`, `NOTICE.md` e licença dos modelos e das dependências; e o `README` e as `references/` atuais. Tamanho só se estiver no projeto ou for medido na máquina; se não souber, pergunte. Funcionalidade em construção (ex.: publicar numa API) ganha um bloco próprio marcado "(em construção)".

## Prompt de instalação para a IA (obrigatório se houver dependência)
Se o projeto depende de algo além do agente de IA (cabeçalho PEP 723, `pyproject.toml`, `package.json`, `Brewfile`, ou `brew install`/`npx`/`uv run` nas instruções), a seção Requisitos abre, logo depois do resumo e antes da tabela e de qualquer passo de instalação, com um bloco de citação que a pessoa cola na IA dela. **Não pode ser um prompt qualquer:** o que dá para conferir de forma determinística vira script, e o prompt manda a IA usar esse script como ferramenta.

1. **Localize o script de requisitos do projeto** (sem alterar nada): `scripts/requisitos.py`, comando `doctor`/`check`/`--validar`, `bin/<cli> doctor`, alvo `make check`. Use o que existe, com o comando exato.
2. **Se não existir, proponha criar** `scripts/requisitos.py` (ou dentro da pasta da skill do projeto, se ela for copiada sozinha) a partir de `${CLAUDE_PLUGIN_ROOT}/scripts/requisitos.py`: copie o arquivo e troque **só** o bloco `REQUISITOS` e o `PROJETO`. Cada item tem fonte no projeto (a mesma da tabela); o comando de instalação vem do projeto ou da documentação oficial da ferramenta e, se você não tiver certeza, pergunte. Itens que a pessoa precisa fazer (conta, token, licença, consentimento, arquivo que ela fornece) não têm `instalar`: só `voce_faz`, explicando o que fazer. Mostre o plano e espere o "sim", como no passo 4.
3. **Escreva o bloco** com o caminho que funciona **antes de clonar**:
   - repositório público: `uv run https://raw.githubusercontent.com/<owner>/<repo>/main/<caminho>/requisitos.py checar`;
   - repositório privado (o link raw não funciona): `gh auth login` com acesso ao repositório e `gh api 'repos/<owner>/<repo>/contents/<caminho>/requisitos.py?ref=main' -H 'Accept: application/vnd.github.raw' > "${TMPDIR:-/tmp}/requisitos-<repo>.py"`, depois `uv run` nesse arquivo; diga também como rodar com o repositório clonado.
4. **Conteúdo do bloco**, em linguagem simples: (a) se faltar `uv` (ou o programa que roda o script), pedir o ok e instalar primeiro; (b) rodar `… checar`; (c) se faltar algo, mostrar a lista e, com o ok da pessoa, rodar `… instalar <item> --sim` item a item; (d) **"Não aceite licenças, termos nem declarações por mim"**; (e) no fim, instalar o plugin com os comandos reais da seção Instalação. Exemplo:

   > **Cole isto na sua IA antes de instalar:**
   >
   > "Verifique os requisitos do acme. Se o `uv` não existir, me peça ok e instale com `brew install uv`. Depois rode `uv run https://raw.githubusercontent.com/exemplo/acme/main/scripts/requisitos.py checar`. Se faltar algo, me mostre a lista e, com o meu ok, rode `uv run https://raw.githubusercontent.com/exemplo/acme/main/scripts/requisitos.py instalar <item> --sim` para cada item. Não aceite licenças, termos nem declarações por mim. No fim, instale o plugin com `claude plugin marketplace add exemplo/acme` e `claude plugin install acme@acme`."

**Nunca invente comandos:** o bloco só cita scripts e comandos que existem no projeto (o verificador confere o caminho).

## Regras de conteúdo
- Linguagem simples; frases curtas; sem jargão sem explicação.
- Selos: versão (`img.shields.io/github/v/tag/<owner>/<repo>`), licença e 2 a 3 selos do que o projeto é. Só inclua selos verdadeiros.
- Tabela **Versões** a partir das tags do git (mais nova no topo). Se não houver tags, use uma linha `0.1.0` e avise o usuário.
- Instalação: um bloco por forma de uso, com comandos copiáveis. Não invente comandos; se não souber, pergunte.
- Requisitos: a seção `## Requisitos` nunca falta e nunca tem requisito sem fonte no projeto (veja "Seção Requisitos").
- **Nunca invente funcionalidades, números, depoimentos nem identidade visual.**
- Não exponha e-mails, caminhos pessoais ou segredos.
- Não faça commit nem push, a menos que o usuário peça.

## Padrão visual
Banner 1280×420. **Com identidade:** fundo, brilho, cores, fontes e logo do projeto; nome com logo, eyebrow, título em duas linhas (a segunda em degradê), subtítulo, comando de instalação num terminal e, à direita, um painel com a ilustração. **Sem identidade:** degradê azul, kicker em caixa alta, nome grande, duas linhas de valor e ilustração própria. Selos centralizados abaixo do banner, seguidos de uma frase de impacto.
