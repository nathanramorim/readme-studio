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
  por caminho, link raw do GitHub ou `gh api .../contents/<caminho>`, ou um comando de uma pasta
  `bin/` do projeto); mandar instalar algo sem a trava "não aceite licenças ... por mim"; ou vier
  depois do primeiro passo de instalação fora dele.
Não confere se cada requisito é verdadeiro: isso é da skill, que só escreve o que tem fonte no projeto.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

MARCA = "Cole isto na sua IA"
ARQ_DEPENDENCIA = ("pyproject.toml", "package.json", "Brewfile", "requirements.txt", "go.mod",
                   "Cargo.toml", "Gemfile", "Dockerfile", "uv.lock")
CMD_DEPENDENCIA = re.compile(r"\b(brew install|npx |uvx |uv run|npm (i|install)\b|pnpm |playwright install)")
PASSO_INSTALACAO = re.compile(r"(plugin marketplace add|plugin install|git clone|brew install|npm (i|install)\b)")
IGNORAR = {"node_modules", "sdd", "vendor", "dist", "build", "__pycache__"}
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


def comando_real(comando: str, raiz: Path, todos: list[Path]) -> bool:
    """O comando aponta para algo que existe no projeto (script ou comando de bin/)."""
    for c in caminhos_citados(comando):
        if "/" in c and ((raiz / c).is_file() or any(p.relative_to(raiz).as_posix().endswith(c) for p in todos)):
            return True
        if "/" not in c and any(p.name == c for p in todos):
            return True
    partes = comando.split()
    return bool(partes) and any(p.parent.name == "bin" and p.name == partes[0] for p in todos)


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
    if not any(comando_real(c, raiz, todos) for c in comandos):
        out.append("o bloco 'Cole isto na sua IA' não usa nenhum comando real do projeto "
                   "(script de requisitos que exista no repositório ou comando de bin/)")
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
