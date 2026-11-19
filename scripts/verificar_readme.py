#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Confere a seção Requisitos de um README gerado pelo readme-studio.

Uso: uv run verificar_readme.py README.md [--raiz <pasta do projeto>]

A raiz do projeto é, por padrão, a pasta do README. Falha (código 1) se:
- faltar `## Requisitos`, se ela vier depois de `## Instalação`, se sobrar `## Antes de começar`
  ou um `{{PLACEHOLDER}}`, se faltar a linha "Onde roda" ou se o README mandar usar `pip install`;
- o projeto tiver dependência além do agente de IA (cabeçalho PEP 723, pyproject.toml,
  package.json, Brewfile... ou `brew install`/`npx`/`uv run` no README) e a seção Requisitos não
  tiver o bloco de citação "Cole isto na sua IA";
- o bloco existir e: não usar nenhum comando real do projeto (um script que existe no repositório,
  por caminho, link raw do GitHub ou `gh api .../contents/<caminho>`; um entry point de
  `[project.scripts]` com `uv run <nome>`; um `npm run <script>` ou `npx <bin>` do package.json; ou
  um executável de uma pasta `bin/` do projeto); mandar instalar algo sem a trava "não aceite
  licenças ... por mim"; ou vier depois do primeiro passo de instalação fora dele.
Não confere se cada requisito é verdadeiro: isso é da skill, que só escreve o que tem fonte no projeto.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

MARCA = "Cole isto na sua IA"
ARQ_DEPENDENCIA = ("pyproject.toml", "package.json", "Brewfile", "requirements.txt", "go.mod",
                   "Cargo.toml", "Gemfile", "Dockerfile", "uv.lock")
CMD_DEPENDENCIA = re.compile(r"\b(brew install|npx |uvx |uv run|npm (i|install)\b|pnpm |playwright install)")
PASSO_INSTALACAO = re.compile(r"(plugin marketplace add|plugin install|git clone|brew install|npm (i|install)\b)")
IGNORAR = {"node_modules", "sdd", "vendor", "dist", "build", "__pycache__", "venv", "site-packages"}
EXT_SCRIPT = r"\.(?:py|sh|js|mjs|cjs|ts)"


def secao_requisitos(texto: str) -> str | None:
    m = re.search(r"^## Requisitos\s*$(.*?)(?=^## |\Z)", texto, flags=re.MULTILINE | re.DOTALL)
    return m.group(1) if m else None


def arquivos(raiz: Path):
    """Arquivos do projeto, sem pastas ocultas, dependências nem `sdd/`."""
    for p in raiz.rglob("*"):
        rel = p.relative_to(raiz).parts
        if p.is_file() and not any(x.startswith(".") or x in IGNORAR for x in rel[:-1]):
            yield p


def dependencias(raiz: Path, texto: str) -> list[str]:
    """Motivos pelos quais o projeto depende de algo além do agente de IA."""
    motivos = [n for n in ARQ_DEPENDENCIA if (raiz / n).is_file()]
    for p in arquivos(raiz):
        if p.suffix == ".py":
            try:
                cabeca = p.read_text(encoding="utf-8", errors="ignore")[:600]
            except OSError:
                continue
            if "# /// script" in cabeca:
                motivos.append(f"script PEP 723 ({p.relative_to(raiz)})")
                break
    m = CMD_DEPENDENCIA.search(texto)
    if m:
        motivos.append(f"o README usa `{m.group(1).strip()}`")
    return motivos


def bloco_prompt(texto: str) -> str | None:
    """O bloco de citação (linhas `>` seguidas) que contém a MARCA."""
    linhas = texto.splitlines()
    i = 0
    while i < len(linhas):
        if linhas[i].lstrip().startswith(">"):
            j = i
            while j < len(linhas) and linhas[j].lstrip().startswith(">"):
                j += 1
            bloco = "\n".join(linhas[i:j])
            if MARCA.lower() in bloco.lower():
                return bloco
            i = j
        else:
            i += 1
    return None


def caminhos_citados(comando: str) -> list[str]:
    """Caminhos de script dentro de um comando (link raw, gh api ou caminho direto)."""
    achados = re.findall(r"raw\.githubusercontent\.com/[^/\s]+/[^/\s]+/[^/\s]+/([^\s?'\"]+)", comando)
    achados += re.findall(r"/contents/([^\s?'\"]+)", comando)
    if not achados:
        achados = re.findall(rf"([\w.${{}}/-]+{EXT_SCRIPT})\b", comando)
    return [re.sub(r"^\$\{?\w+\}?/", "", a) for a in achados]


def _scripts_pyproject(raiz: Path) -> set[str]:
    """Nomes de `[project.scripts]` do pyproject.toml (entry points: `uv run <nome>`)."""
    arq = raiz / "pyproject.toml"
    if not arq.is_file():
        return set()
    texto = arq.read_text(encoding="utf-8", errors="ignore")
    try:
        import tomllib
        projeto = tomllib.loads(texto).get("project")
        scripts = projeto.get("scripts") if isinstance(projeto, dict) else None
        return set(scripts) if isinstance(scripts, dict) else set()
    except ImportError:  # Python < 3.11: lê só a seção
        m = re.search(r"^\[project\.scripts\]\s*$(.*?)(?=^\[|\Z)", texto, flags=re.MULTILINE | re.DOTALL)
        return set(re.findall(r"^\s*\"?([\w.-]+)\"?\s*=", m.group(1), flags=re.MULTILINE)) if m else set()
    except ValueError:
        return set()


def _package_json(raiz: Path) -> tuple[set[str], set[str]]:
    """(scripts, bins) do package.json: `npm run <script>` e `npx <bin>`."""
    arq = raiz / "package.json"
    if not arq.is_file():
        return set(), set()
    try:
        dados = json.loads(arq.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return set(), set()
    if not isinstance(dados, dict):
        return set(), set()
    scripts = set((dados.get("scripts") or {}).keys()) if isinstance(dados.get("scripts"), dict) else set()
    b = dados.get("bin")
    bins = set(b.keys()) if isinstance(b, dict) else ({str(dados.get("name", "")).split("/")[-1]} if b else set())
    return scripts, bins - {""}


def comandos_declarados(raiz: Path, todos: list[Path]) -> dict[str, set[str]]:
    """Nomes que o projeto declara como comando: entry points, package.json e executáveis de bin/."""
    npm_scripts, npm_bins = _package_json(raiz)
    return {"py": _scripts_pyproject(raiz), "npm_scripts": npm_scripts, "npm_bins": npm_bins,
            "bin": {p.name for p in todos if p.parent.name == "bin"}}


def _depois_das_opcoes(partes: list[str]) -> str:
    """Primeiro argumento que não é opção (pula `--with x`, `--from x`, `-q`...)."""
    i = 0
    while i < len(partes):
        if partes[i] in ("--with", "--from", "--project", "--directory", "--python", "-p", "-w"):
            i += 2
        elif partes[i].startswith("-"):
            i += 1
        else:
            return partes[i]
    return ""


def comando_real(comando: str, raiz: Path, todos: list[Path], nomes: dict[str, set[str]] | None = None) -> bool:
    """O comando aponta para algo que existe no projeto: script do repositório, entry point de
    `[project.scripts]` (`uv run <nome>`), `package.json` (`npm run <script>`, `npx <bin>`) ou `bin/`."""
    for c in caminhos_citados(comando):
        if "/" in c and ((raiz / c).is_file() or any(p.relative_to(raiz).as_posix().endswith(c) for p in todos)):
            return True
        if "/" not in c and any(p.name == c for p in todos):
            return True
    nomes = nomes if nomes is not None else comandos_declarados(raiz, todos)
    partes = comando.split()
    if not partes:
        return False
    executaveis = nomes["py"] | nomes["bin"] | nomes["npm_bins"]
    if partes[:2] == ["uv", "run"]:
        return _depois_das_opcoes(partes[2:]) in executaveis
    if partes[0] == "uvx":  # sem --from local, o uvx busca um pacote de mesmo nome no PyPI
        nome = _depois_das_opcoes(partes[1:])
        antes = partes[1:partes.index(nome)] if nome else []  # só opções antes do nome valem para o uvx
        local = any(a == "--from" and i + 1 < len(antes) and antes[i + 1].startswith((".", "/", "~"))
                    for i, a in enumerate(antes))
        return local and nome in executaveis
    if partes[0] == "npm":  # o npm só roda script do projeto com run (ou os embutidos test/start)
        if len(partes) > 1 and partes[1] in ("run", "run-script"):
            return _depois_das_opcoes(partes[2:]) in nomes["npm_scripts"]
        return len(partes) > 1 and partes[1] in ("test", "start", "stop", "restart") and partes[1] in nomes["npm_scripts"]
    if partes[0] in ("pnpm", "yarn", "bun"):
        resto = partes[2:] if len(partes) > 1 and partes[1] in ("run", "run-script") else partes[1:]
        alvo = _depois_das_opcoes(resto)
        return alvo in nomes["npm_scripts"] or alvo in nomes["npm_bins"]
    if partes[0] == "npx":
        return _depois_das_opcoes(partes[1:]) in nomes["npm_bins"]
    return partes[0] in executaveis


def problemas_prompt(texto: str, raiz: Path) -> list[str]:
    out = []
    secao = secao_requisitos(texto)
    if secao is None:
        return out
    bloco = bloco_prompt(secao)
    if bloco is None:
        motivos = dependencias(raiz, texto)
        if motivos:
            out.append(f"falta o bloco '> **{MARCA} ...**' na seção Requisitos "
                       f"(o projeto tem dependências: {', '.join(motivos[:3])})")
        return out
    comandos = re.findall(r"`([^`\n]+)`", bloco)
    todos = list(arquivos(raiz))
    nomes = comandos_declarados(raiz, todos)
    if not any(comando_real(c, raiz, todos, nomes) for c in comandos):
        out.append("o bloco 'Cole isto na sua IA' não usa nenhum comando real do projeto (script do "
                   "repositório, [project.scripts], package.json ou bin/)")
    if re.search(r"instal", bloco, flags=re.IGNORECASE) and not (
            re.search(r"n[ãa]o aceite", bloco, flags=re.IGNORECASE) and "licen" in bloco.lower()):
        out.append("o bloco manda instalar, mas não diz 'não aceite licenças nem declarações por mim'")
    inicio = texto.find(bloco)
    for m in PASSO_INSTALACAO.finditer(texto):
        linha = texto[texto.rfind("\n", 0, m.start()) + 1:m.start()]
        if m.start() < inicio and not linha.lstrip().startswith(">"):
            out.append("o bloco 'Cole isto na sua IA' deve vir antes do primeiro passo de instalação")
            break
    return out


def problemas(texto: str, raiz: Path | None = None) -> list[str]:
    out = []
    titulos = re.findall(r"^## (.+?)\s*$", texto, flags=re.MULTILINE)
    if "Requisitos" not in titulos:
        out.append("falta a seção '## Requisitos'")
    elif "Instalação" in titulos and titulos.index("Requisitos") > titulos.index("Instalação"):
        out.append("'## Requisitos' deve vir antes de '## Instalação'")
    if "Antes de começar" in titulos:
        out.append("sobrou '## Antes de começar': troque por '## Requisitos'")
    if re.search(r"\{\{[A-Z0-9_]+\}\}", texto):
        out.append("sobrou placeholder {{...}} do template")
    secao = secao_requisitos(texto)
    if secao is not None and "Onde roda" not in secao:
        out.append("a seção Requisitos não diz onde roda (sistema testado e agente)")
    if re.search(r"\bpip3? install\b", texto):
        out.append("o README manda usar 'pip install': use o uv")
    if raiz is not None:
        out += problemas_prompt(texto, raiz)
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Confere a seção Requisitos de um README.")
    ap.add_argument("readme")
    ap.add_argument("--raiz", help="pasta do projeto (padrão: a pasta do README)")
    try:
        a = ap.parse_args(argv)
    except SystemExit:
        return 2
    arq = Path(a.readme)
    if not arq.is_file():
        print(f"não achei {arq}", file=sys.stderr)
        return 2
    raiz = Path(a.raiz) if a.raiz else arq.resolve().parent
    erros = problemas(arq.read_text(encoding="utf-8"), raiz)
    for e in erros:
        print(f"[falha] {e}")
    if not erros:
        print("requisitos: ok")
    return 1 if erros else 0


if __name__ == "__main__":
    sys.exit(main())
