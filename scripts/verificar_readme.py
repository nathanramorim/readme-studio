#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Confere a seção Requisitos de um README gerado pelo readme-studio.

Uso: uv run verificar_readme.py README.md

Falha (código 1) se faltar `## Requisitos`, se ela vier depois de `## Instalação`, se sobrar
`## Antes de começar` ou um `{{PLACEHOLDER}}`, se faltar a linha "Onde roda" ou se o README
mandar instalar com `pip install`. Não confere se cada requisito é verdadeiro: isso é da skill,
que só escreve o que tem fonte no projeto.
"""
import re
import sys
from pathlib import Path


def problemas(texto: str) -> list[str]:
    out = []
    titulos = re.findall(r"^## (.+?)\s*$", texto, flags=re.M)
    if "Requisitos" not in titulos:
        out.append("falta a seção '## Requisitos'")
    elif "Instalação" in titulos and titulos.index("Requisitos") > titulos.index("Instalação"):
        out.append("'## Requisitos' deve vir antes de '## Instalação'")
    if "Antes de começar" in titulos:
        out.append("sobrou '## Antes de começar': troque por '## Requisitos'")
    if re.search(r"\{\{[A-Z0-9_]+\}\}", texto):
        out.append("sobrou placeholder {{...}} do template")
    m = re.search(r"^## Requisitos\s*$(.*?)(?=^## |\Z)", texto, flags=re.M | re.S)
    if m and "Onde roda" not in m.group(1):
        out.append("a seção Requisitos não diz onde roda (sistema testado e agente)")
    if re.search(r"\bpip3? install\b", texto):
        out.append("o README manda usar 'pip install': use o uv")
    return out


def main() -> int:
    if len(sys.argv) != 2:
        print("uso: verificar_readme.py README.md", file=sys.stderr)
        return 2
    arq = Path(sys.argv[1])
    if not arq.is_file():
        print(f"não achei {arq}", file=sys.stderr)
        return 2
    erros = problemas(arq.read_text(encoding="utf-8"))
    for e in erros:
        print(f"[falha] {e}")
    if not erros:
        print("requisitos: ok")
    return 1 if erros else 0


if __name__ == "__main__":
    sys.exit(main())
