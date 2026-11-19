<p align="center">
  <img src="docs/banner.svg" alt="readme-studio: README comercial em um comando" width="100%">
</p>

<p align="center">
  <img alt="versão" src="https://img.shields.io/badge/vers%C3%A3o-0.5.0-2563eb">
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

Testado no **macOS**. Não precisa de conta nem chave. Internet só se o `uv` precisar baixar o Python na primeira vez.

> **Cole isto na sua IA (Claude Code ou agy) antes de instalar:**
>
> "Verifique os requisitos do readme-studio. Se o `uv` não existir, me peça ok e instale com `brew install uv` (sem Homebrew, siga https://docs.astral.sh/uv/). Depois rode `uv run https://raw.githubusercontent.com/nathanramorim/readme-studio/main/scripts/requisitos.py checar`. Se faltar algo, me mostre a lista e, com o meu ok, rode `uv run https://raw.githubusercontent.com/nathanramorim/readme-studio/main/scripts/requisitos.py instalar <item> --sim` para cada item. Não aceite licenças, termos nem declarações por mim: nesses casos, só me diga o que fazer. No fim, instale o plugin com `claude plugin marketplace add nathanramorim/readme-studio` e `claude plugin install readme-studio@readme-studio`."

O script só usa a biblioteca padrão e não guarda nada. Com o repositório já clonado, rode `uv run scripts/requisitos.py checar`.

| | O que precisa | Detalhe |
|---|---|---|
| **Onde roda** | macOS (testado), com **Claude Code** ou **agy (Antigravity)** | A skill é quem conduz; os scripts também rodam sozinhos no terminal. |
| **Programas** | [`uv`](https://docs.astral.sh/uv/) (`brew install uv`) | Roda os scripts com Python 3.9 ou mais novo (o `uv` instala se faltar). Eles só usam a biblioteca padrão: nada de `pip`. `requisitos.py checar` confere. |
| | Google Chrome (opcional) | A skill abre o banner no Chrome, sem janela, para conferir se o texto coube. |
| **Downloads na primeira execução** | Python 3, só se faltar | O `uv` baixa o Python na primeira execução (precisa de internet nessa hora) e o guarda no cache dele. Os scripts e templates já vêm no plugin. |
| **Contas e chaves** | Nenhuma | Ele só lê o projeto e o `git` local. |
| **Máquina** | Um computador comum | |
| **Licenças e limites de uso** | MIT | Sem limites. |
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
uv run scripts/requisitos.py checar            # tabela; sai 1 se faltar algo obrigatório
uv run scripts/requisitos.py checar --json
uv run scripts/requisitos.py instalar          # mostra o que instalaria e pergunta antes de cada item
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
- O `requisitos.py` só instala com o seu ok (ou `--sim`), nunca aceita licenças nem declarações por você e nunca lida com senhas ou tokens.

## Versões

| Versão | Novidades |
|---|---|
| **0.5.0** | **Prompt de instalação para a IA**: todo README de projeto com dependências ganha, em Requisitos, um bloco "Cole isto na sua IA" que usa o script de requisitos do projeto (`checar` e `instalar`), nunca um prompt genérico. Novo `scripts/requisitos.py` (também é a base para outros projetos) e o verificador confere o bloco. |
| **0.4.0** | Seção **Requisitos** obrigatória em todo README (onde roda, programas, downloads, contas, máquina, licenças e o que você fornece), levantada do projeto e nunca inventada, e o `verificar_readme.py`, que confere a seção. |
| **0.3.0** | O banner usa a identidade do projeto (cores, fontes, logo, personagens da landing page); a skill descobre a identidade antes de desenhar. |
| **0.2.0** | O banner agora tem ilustração própria do projeto (ou desenhos prontos: pastas, fluxo, terminal). |
| **0.1.0** | Primeira versão: `/readme-gerar`, skill `readme-comercial`, gerador de banner e template de README. |

## Licença

[MIT](LICENSE)
