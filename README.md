<p align="center">
  <img src="docs/banner.svg" alt="readme-studio: README comercial em um comando" width="100%">
</p>

<p align="center">
  <img alt="versão" src="https://img.shields.io/badge/vers%C3%A3o-0.6.1-2563eb">
  <img alt="licença" src="https://img.shields.io/badge/licen%C3%A7a-MIT-16a34a">
  <img alt="Claude Code" src="https://img.shields.io/badge/Claude%20Code-plugin-7c3aed">
  <img alt="agy" src="https://img.shields.io/badge/agy-skill-06b6d4">
</p>

<h3 align="center">README comercial em um comando.<br>Banner, selos e versões prontos.</h3>

---

## O que é

O **readme-studio** cria o README de um projeto com cara de produto: banner bonito no topo, selos de versão e licença, tabelas de instalação e uso e uma lista de versões.

Ele lê o seu projeto, pergunta só o que faltar, mostra o plano e só grava depois do seu "sim".

## Por que usar

| | |
|---|---|
| 🎨 **Banner com a marca do projeto** | Usa as cores, fontes, logo e personagens da landing page, e a ilustração mostra o que o projeto faz. O texto sempre cabe. |
| 🏷️ **Selos e versões** | Versão, licença e a tabela de versões a partir das tags do git. |
| 🗣️ **Linguagem simples** | Texto para leigos, com comandos copiáveis. |
| 🛡️ **Sem invenção** | Não inventa funcionalidades, números nem depoimentos. |
| 📋 **Requisitos completos** | Diz onde roda, o que instalar, o que é baixado, contas, máquina, licenças e o que você precisa fornecer, tirado do próprio projeto. |

## Requisitos

Roda no **macOS**, no **Linux** e no **Windows**, com **Claude Code** ou **agy**. Não precisa de conta nem chave. Internet só para baixar o `uv` e o Python na primeira vez. O Homebrew não é necessário.

> **Cole isto na sua IA antes de instalar:**
>
> "Confira os requisitos do readme-studio. Se o repositório ainda não estiver clonado, clone com o GitHub CLI: `gh repo clone nathanramorim/readme-studio` (instale o gh com `winget install --id GitHub.cli -e` no Windows, pelo https://cli.github.com no macOS e pelo pacote `gh` da sua distro no Linux; o `gh auth login` é comigo). No Windows, rode `powershell -ExecutionPolicy Bypass -File scripts/bootstrap.ps1`; no macOS ou Linux, rode `sh scripts/bootstrap.sh`. Ele confere e, com o meu ok, instala o uv, e depois mostra o que falta. Para cada item, peça meu ok e rode `uv run scripts/requisitos.py instalar --sim <item>`. Itens marcados como é com você (licença, consentimento ou voz, login, permissões do sistema, senha de administrador): me explique e espere eu fazer. Não aceite licenças nem declarações por mim e não mexa em senhas, chaves ou tokens."

A receita de tudo isso está em [`requisitos.toml`](requisitos.toml) e o `scripts/requisitos.py` (do [requisitos-para-ia](https://github.com/nathanramorim/requisitos-para-ia), copiado pelo [`skills.lock`](skills.lock)) confere, instala com o seu ok e nunca aceita licenças por você. Com o repositório clonado e o `uv` instalado, rode `uv run scripts/requisitos.py checar`.

| | O que precisa | Detalhe |
|---|---|---|
| **Onde roda** | macOS, Linux e Windows, com **Claude Code** ou **agy (Antigravity)** | A skill é quem conduz; os scripts também rodam sozinhos no terminal. Testado em macOS Apple Silicon e no CI em Ubuntu, Windows e macOS. |
| **Programas** | [`uv`](https://docs.astral.sh/uv/) e Python 3.11 ou mais novo (o `uv` instala) | Os scripts só usam a biblioteca padrão: nada de `pip`. O `git` (opcional) dá a tabela de versões; o Chrome ou Chromium (opcional) confere o banner. |
| ↳ macOS | `sh scripts/bootstrap.sh` | Instala o `uv` pelo instalador oficial em `~/.local/bin`, sem senha. `git` vem com `xcode-select --install` (você aceita a licença da Apple); o Chrome é baixado por você. |
| ↳ Linux | `sh scripts/bootstrap.sh` | Mesmo instalador oficial, sem `sudo`. `git` e Chromium pelo `apt`, `dnf`, `pacman` ou `zypper` (o motor só mostra o `sudo ...`: quem roda é você); no Ubuntu o Chromium vem pelo `snap`. Google Chrome não tem versão Linux arm64: use o Chromium. |
| ↳ Windows | `powershell -ExecutionPolicy Bypass -File scripts/bootstrap.ps1` | Instala o `uv` pelo `winget` (que pede o seu aceite) ou pelo instalador oficial, sem administrador; `scoop` e `choco` também servem. `git` e Chrome pelo `winget`. A política de execução só muda nessa execução. |
| **Downloads na primeira execução** | `uv` e Python (cerca de 60 MB), só se faltarem | O Python fica na pasta do `uv` (`uv python dir`): `~/.local/share/uv/python` no macOS e no Linux, `%APPDATA%\uv\python` no Windows. O navegador (cerca de 500 MB) só se você quiser a conferência visual. |
| **Contas e chaves** | Nenhuma | Ele só lê o projeto e o `git` local. O login do seu agente de IA é seu. |
| **Máquina** | Um computador comum, com cerca de 1 GB livre | |
| **Licenças e limites de uso** | MIT | Sem limites. Termos do Chrome, do Git for Windows e da Apple são aceitos por você, nunca pela IA. |
| **O que você fornece** | O projeto e algumas respostas | Ele lê o que existe (código, landing page, logo) e pergunta o que faltar, como a frase de valor e, se não estiver no projeto, o sistema testado. |

## Instalação

### No Claude Code

```
/plugin marketplace add nathanramorim/readme-studio
/plugin install readme-studio@readme-studio
```

### No agy (Antigravity)

```bash
git clone https://github.com/nathanramorim/readme-studio.git
mkdir -p .agents/skills
cp -R readme-studio/skills/readme-comercial .agents/skills/
cp -R readme-studio/scripts readme-studio/templates .agents/skills/readme-comercial/
```

> Teste no seu agy: o plugin usa a pasta `.agents/skills/` do projeto. Se o seu agy usar outro local, copie para lá. Neste caso, o script e os templates ficam dentro da pasta da skill.

## Como usar

| Claude Code | agy |
|---|---|
| `/readme-gerar` | "Gere o README comercial deste projeto" |

Para conferir a seção Requisitos de um README pronto (inclusive o bloco "Cole isto na sua IA"):

```bash
uv run scripts/verificar_readme.py README.md
```

Para conferir os requisitos do próprio readme-studio:

```bash
sh scripts/bootstrap.sh                        # macOS e Linux: confere o uv (instala com o seu ok) e roda o checar
powershell -ExecutionPolicy Bypass -File scripts/bootstrap.ps1   # o mesmo no Windows
uv run scripts/requisitos.py checar            # tabela; sai 1 se faltar algo obrigatório
uv run scripts/requisitos.py checar --json
uv run scripts/requisitos.py instalar          # mostra o que instalaria e pergunta antes de cada item
uv run scripts/requisitos.py validar           # confere o requisitos.toml nas 3 plataformas
uv run scripts/requisitos.py prompt            # imprime o bloco "Cole isto na sua IA"
```

Primeiro ele **procura a identidade visual do projeto** (landing page, CSS, logo, mascote) e confirma com você o que achou. Depois pergunta o que faltar, propõe ideias de desenho para o banner a partir do que o projeto faz, mostra o que vai criar e espera a confirmação.

### Identidade do projeto

Se o projeto já tem marca (landing page, logo, paleta), o banner a usa. A skill extrai as cores, as fontes e o logo para um `docs/img/identidade.json`. Um exemplo completo, o do forge-sdd, está em [`exemplos/forge-sdd/`](exemplos/forge-sdd/).

```json
{
  "fundo": "#0d0f14", "brilho": "#1e2a4a", "texto": "#e9ecf4", "suave": "#99a2b8",
  "acento": ["#4f8ef7", "#8aa4ff", "#3ecf8e"],
  "painel": "#12151d", "borda": "#252d40",
  "fonte": "Montserrat, system-ui, sans-serif", "logo": "logo.svg.frag"
}
```

O que não for informado cai no tema escuro padrão. Sem identidade nenhuma, o banner usa o tema azul claro.

> O GitHub mostra o SVG como imagem e não carrega fontes da web: as fontes da marca caem para a fonte do sistema.

### Só o banner

```bash
# com a identidade do projeto
uv run scripts/gerar_banner.py \
  --identidade docs/img/identidade.json \
  --ilustracao-arquivo docs/img/ilustracao.svg.frag \
  --nome meu-projeto --kicker "Frase curta de contexto" \
  --titulo1 "Primeira linha," --titulo2 "segunda em degradê." \
  --linha1 "Frase de apoio." --linha2 "Segunda frase." \
  --comando "$ npm i -g meu-projeto" --saida docs/img/banner.svg

# sem identidade (tema azul claro)
uv run scripts/gerar_banner.py \
  --nome meu-projeto --kicker "Plugin para X" \
  --linha1 "Frase de valor." --linha2 "Segunda frase." \
  --ilustracao-arquivo docs/ilustracao.svg.frag \
  --cores "#1e3a8a,#2563eb,#06b6d4" --saida docs/banner.svg
```

Com tema claro, também há desenhos prontos: `--ilustracao pastas|fluxo|terminal` com `--rotulos "a|b|c"`.

## Segurança e privacidade

- Não faz commit nem push sozinho.
- Guarda o README antigo em `README.antigo.md` antes de substituir.
- Não coloca e-mails, caminhos pessoais nem segredos no texto.
- O `requisitos.py` só instala com o seu ok (ou `--sim`), nunca usa `sudo` nem roda shell, nunca aceita licenças nem declarações por você e nunca lida com senhas ou tokens. Os bootstraps só instalam o `uv` pelo instalador oficial depois do seu ok.

## Versões

| Versão | Novidades |
|---|---|
| **0.6.1** | O motor de requisitos fica fixo na tag **v0.1.0** do requisitos-para-ia (trava mais rígida, instruções do Windows em PowerShell e cmd, `--arquivo` depois do subcomando) e o Python é conferido com `uv python find --system`, para não confundir com o Python do próprio `uv run`. |
| **0.6.0** | **Requisitos multiplataforma**: o readme-studio usa o motor [requisitos-para-ia](https://github.com/nathanramorim/requisitos-para-ia) (`requisitos.toml` + `bootstrap.sh`/`bootstrap.ps1`) e todo README gerado também: o bloco "Cole isto na sua IA" é o que `requisitos.py prompt` imprime, com caminho para Windows e para macOS/Linux, e o Homebrew deixa de ser pré-requisito. O verificador falha sem esses caminhos, com Homebrew no bloco ou sem `requisitos.toml`. CI em Ubuntu, Windows e macOS. |
| **0.5.0** | **Prompt de instalação para a IA**: todo README de projeto com dependências ganha, em Requisitos, um bloco "Cole isto na sua IA" que usa o script de requisitos do projeto (`checar` e `instalar`), nunca um prompt genérico. Novo `scripts/requisitos.py` (também é a base para outros projetos) e o verificador confere o bloco. |
| **0.4.0** | Seção **Requisitos** obrigatória em todo README (onde roda, programas, downloads, contas, máquina, licenças e o que você fornece), levantada do projeto e nunca inventada, e o `verificar_readme.py`, que confere a seção. |
| **0.3.0** | O banner usa a identidade do projeto (cores, fontes, logo, personagens da landing page); a skill descobre a identidade antes de desenhar. |
| **0.2.0** | O banner agora tem ilustração própria do projeto (ou desenhos prontos: pastas, fluxo, terminal). |
| **0.1.0** | Primeira versão: `/readme-gerar`, skill `readme-comercial`, gerador de banner e template de README. |

## Licença

[MIT](LICENSE)
