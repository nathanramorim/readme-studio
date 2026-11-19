#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Confere e instala os requisitos do readme-studio, para você ou para a sua IA.

Uso:
  uv run requisitos.py checar [--json]
  uv run requisitos.py instalar [item ...] [--sim]

checar    mostra cada requisito (ok, faltando ou aviso) e sai com 1 se faltar algo obrigatório.
instalar  mostra o comando de cada item que falta e pergunta antes de rodar; com --sim, roda sem
          perguntar. Sem terminal para perguntar (ex.: rodado pela IA), só mostra: nada é instalado.

Nunca aceita licenças, termos ou declarações por você e nunca lida com senhas ou tokens: nesses
itens ele só explica o que você precisa fazer. Rodar de novo não refaz o que já está ok.

Base para outros projetos: o motor abaixo é o mesmo em todo projeto; troque só o bloco
REQUISITOS (cada item com fonte no próprio projeto) e o PROJETO.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

OK, FALTA, AVISO = "ok", "faltando", "aviso"
# Trechos que nunca podem aparecer num comando de instalação (aceitar licença ou termos por alguém).
PROIBIDO = ("--accept", "--agree", "--yes", "yes |", "licen")


def proibido(argv: list[str]) -> bool:
    """O comando aceitaria algo por alguém? Cada argumento é partido em espaços e `=`;
    só os pedaços que são caminho ou link (com `/`) ficam de fora."""
    partes = [t for x in argv for t in re.split(r"[\s=]+", x) if t and "/" not in t]
    texto = " " + " ".join(partes).lower() + " "
    return any(p in texto for p in PROIBIDO) or " -y " in texto


# ---------- conferências (cada uma devolve: achou, versão, detalhe) ----------

def _rodar(argv: list[str]) -> str:
    try:
        r = subprocess.run(argv, check=False, capture_output=True, text=True, timeout=20)
    except (OSError, subprocess.SubprocessError):
        return ""
    return (r.stdout or r.stderr or "") if r.returncode == 0 else ""


def _versao(texto: str) -> str:
    m = re.search(r"\d+(?:\.\d+)+", texto)
    return m.group(0) if m else ""


def menor(versao: str, minimo: str) -> bool:
    """True se `versao` for mais velha que `minimo` (compara só números)."""
    def num(v: str) -> tuple[int, ...]:
        return tuple(int(x) for x in re.findall(r"\d+", v)[:3])
    return num(versao) < num(minimo)


def programa(cmd: str, *args: str):
    """Programa no PATH; a versão vem de `cmd --version` (ou dos args dados)."""
    def conferir():
        caminho = shutil.which(cmd)
        if not caminho:
            return False, "", f"`{cmd}` não está no PATH"
        return True, _versao(_rodar([caminho, *(args or ("--version",))])), ""
    return conferir


def python_pelo_uv(minimo: str):
    """Python que o `uv` acha (ou o que roda este script, se não houver uv)."""
    def conferir():
        uv = shutil.which("uv")
        if uv:
            caminho = _rodar([uv, "python", "find", f">={minimo}"]).strip()
            if not caminho:
                return False, "", f"o uv não achou Python {minimo} ou mais novo"
            return True, _versao(_rodar([caminho, "--version"])), ""
        v = ".".join(str(x) for x in sys.version_info[:3])
        return (not menor(v, minimo)), v, "sem uv: conferido o Python atual"
    return conferir


def algum_caminho(*padroes: str, nome: str = ""):
    """Algum destes caminhos existe (aceita ~, $VAR e curingas)."""
    def conferir():
        for p in padroes:
            achados = sorted(glob.glob(os.path.expandvars(os.path.expanduser(p))))
            if achados:
                return True, "", nome or Path(achados[-1]).name
        return False, "", ""
    return conferir


def se_tiver(cmd: str, argv: list[str]):
    """Comando de instalação que só vale se `cmd` existir (ex.: brew)."""
    return lambda: [argv] if shutil.which(cmd) else []


# ---------- REQUISITOS do readme-studio (fonte: README, ADR-0003, SKILL.md passo 5) ----------

PROJETO = "readme-studio"
REQUISITOS = [
    {
        "id": "uv", "nome": "uv", "obrigatorio": True,
        "conferir": programa("uv"),
        "instalar": se_tiver("brew", ["brew", "install", "uv"]),
        "voce_faz": "sem Homebrew, instale o uv pelo site oficial: https://docs.astral.sh/uv/",
    },
    {
        "id": "python", "nome": "Python 3.9+", "obrigatorio": True,
        "conferir": python_pelo_uv("3.9"),
        "instalar": se_tiver("uv", ["uv", "python", "install"]),
        "voce_faz": "instale o uv primeiro; ele baixa o Python",
    },
    {
        "id": "chrome", "nome": "Google Chrome (opcional)", "obrigatorio": False,
        "conferir": algum_caminho("/Applications/Google Chrome.app", "~/Applications/Google Chrome.app",
                                  nome="Google Chrome"),
        "voce_faz": "opcional: só para conferir o banner. Baixe em https://www.google.com/chrome/ "
                    "(a instalação pede que você aceite os termos do Google: faça você mesmo)",
    },
]


# ---------- motor (igual em todo projeto) ----------

def _cmd_texto(argv: list[str]) -> str:
    return " ".join(shlex.quote(x) for x in argv)


def avaliar(item: dict) -> dict:
    try:
        achou, versao, detalhe = item["conferir"]()
    except Exception as e:  # noqa: BLE001 — conferência nunca derruba o relatório
        achou, versao, detalhe = False, "", f"erro ao conferir: {e}"
    obrig = bool(item.get("obrigatorio"))
    minimo = item.get("minimo")
    if achou and minimo and versao and menor(versao, minimo):
        achou, detalhe = False, f"versão {versao}; precisa {minimo} ou mais nova"
    estado = OK if achou else (FALTA if obrig else AVISO)
    cmds = [] if achou else (item["instalar"]() if item.get("instalar") else [])
    return {"id": item["id"], "nome": item["nome"], "obrigatorio": obrig, "estado": estado,
            "versao": versao, "detalhe": detalhe if achou else (detalhe or item.get("voce_faz", "")),
            "instalar": [_cmd_texto(c) for c in cmds], "_argv": cmds,
            "voce_faz": "" if achou else item.get("voce_faz", "")}


def relatorio(itens: list[dict]) -> str:
    linhas = [f"{'requisito':<28} {'estado':<9} {'versão':<9} detalhe"]
    for r in itens:
        linhas.append(f"{r['nome']:<28} {r['estado']:<9} {r['versao'] or '-':<9} {r['detalhe']}".rstrip())
    return "\n".join(linhas)


def tudo_ok(itens: list[dict]) -> bool:
    return not any(r["estado"] == FALTA for r in itens)


def cmd_checar(a) -> int:
    itens = [avaliar(i) for i in REQUISITOS]
    if a.json:
        limpo = [{k: v for k, v in r.items() if not k.startswith("_")} for r in itens]
        print(json.dumps({"projeto": PROJETO, "ok": tudo_ok(itens), "itens": limpo}, ensure_ascii=False, indent=2))
    else:
        print(relatorio(itens))
        print("\ntudo pronto." if tudo_ok(itens) else
              "\nfalta algo obrigatório: rode `requisitos.py instalar` (ou instale você mesmo).")
    return 0 if tudo_ok(itens) else 1


def perguntar(texto: str) -> bool:
    try:
        return input(texto).strip().lower() in ("s", "sim", "y")
    except EOFError:
        return False


def cmd_instalar(a) -> int:
    ids = {i["id"] for i in REQUISITOS}
    desconhecidos = [x for x in a.itens if x not in ids]
    if desconhecidos:
        print(f"item desconhecido: {', '.join(desconhecidos)} (use: {', '.join(sorted(ids))})", file=sys.stderr)
        return 2
    alvo = [i for i in REQUISITOS if not a.itens or i["id"] in a.itens]
    pendentes = [(i, r) for i in alvo if (r := avaliar(i))["estado"] != OK]
    if not pendentes:
        print("nada a instalar: tudo ok.")
        return 0
    falhou = False
    for item, r in pendentes:
        print(f"\n- {r['nome']} ({r['estado']})")
        if not r["_argv"]:
            print(f"  você faz: {r['voce_faz'] or r['detalhe']}")
            continue
        if any(proibido(c) for c in r["_argv"]):
            print("  recusei: o comando aceitaria algo por você. Rode você mesmo, se concordar.")
            falhou = True
            continue
        for c in r["instalar"]:
            print(f"  $ {c}")
        if not a.sim and not perguntar("  Rodar agora? [s/N] "):
            print("  não rodei (para rodar sem perguntar, use --sim).")
            continue
        for argv in r["_argv"]:
            if subprocess.run(argv, check=False).returncode != 0:  # argv fixo, sem shell
                print(f"  falhou: {_cmd_texto(argv)}")
                falhou = True
                break
        else:
            print("  ok." if avaliar(item)["estado"] == OK else "  rodou, mas ainda não aparece como ok.")
    finais = [avaliar(i) for i in alvo]
    return 1 if falhou or not tudo_ok(finais) else 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=f"Requisitos do {PROJETO}: conferir e instalar.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("checar", help="confere cada requisito; sai 1 se faltar algo obrigatório")
    c.add_argument("--json", action="store_true", help="resposta em JSON")
    i = sub.add_parser("instalar", help="mostra e (com sua confirmação ou --sim) roda a instalação do que falta")
    i.add_argument("itens", nargs="*", help="só estes itens (padrão: tudo que falta)")
    i.add_argument("--sim", action="store_true", help="roda sem perguntar")
    a = ap.parse_args(argv)
    return cmd_checar(a) if a.cmd == "checar" else cmd_instalar(a)


if __name__ == "__main__":
    sys.exit(main())
