#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Testes do scripts/requisitos.py (sem rede, sem brew: which, subprocess e input simulados).
Uso: uv run tests/test_requisitos.py"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import sys
import unittest
from pathlib import Path
from unittest import mock

REPO = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("requisitos", REPO / "scripts" / "requisitos.py")
req = importlib.util.module_from_spec(spec)
spec.loader.exec_module(req)


def rodar(*args: str) -> tuple[int, str]:
    out = io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
        code = req.main(list(args))
    return code, out.getvalue()


class Processo:
    def __init__(self, stdout: str = "", code: int = 0):
        self.stdout, self.stderr, self.returncode = stdout, "", code


def sem_nada():
    """Máquina vazia: nenhum programa, nenhum caminho."""
    return [mock.patch.object(req.shutil, "which", return_value=None),
            mock.patch.object(req.glob, "glob", return_value=[]),
            mock.patch.object(req.sys, "version_info", (3, 8, 0))]


class TestChecar(unittest.TestCase):
    def test_maquina_pronta_sai_0(self):
        with mock.patch.object(req.shutil, "which", side_effect=lambda c: f"/bin/{c}"), \
             mock.patch.object(req.subprocess, "run", side_effect=lambda argv, **k: Processo(
                 "/py/python3" if "find" in argv else "uv 0.9.7" if argv[0].endswith("uv") else "Python 3.12.1")), \
             mock.patch.object(req.glob, "glob", return_value=["/Applications/Google Chrome.app"]):
            code, out = rodar("checar")
        self.assertEqual(code, 0, out)
        self.assertIn("tudo pronto", out)

    def test_faltando_obrigatorio_sai_1_e_json(self):
        with contextlib.ExitStack() as st:
            for p in sem_nada():
                st.enter_context(p)
            code, out = rodar("checar", "--json")
        dados = json.loads(out)
        self.assertEqual(code, 1)
        self.assertFalse(dados["ok"])
        estados = {i["id"]: i["estado"] for i in dados["itens"]}
        self.assertEqual(estados["uv"], "faltando")
        self.assertEqual(estados["chrome"], "aviso")  # opcional nunca derruba

    def test_opcional_faltando_nao_derruba(self):
        with mock.patch.object(req.shutil, "which", side_effect=lambda c: f"/bin/{c}"), \
             mock.patch.object(req.subprocess, "run", side_effect=lambda argv, **k: Processo("3.12.1")), \
             mock.patch.object(req.glob, "glob", return_value=[]):
            code, out = rodar("checar")
        self.assertEqual(code, 0, out)
        self.assertIn("aviso", out)

    def test_versao_antiga(self):
        self.assertTrue(req.menor("3.8.10", "3.9"))
        self.assertFalse(req.menor("3.12.0", "3.9"))


class TestInstalar(unittest.TestCase):
    def test_sem_terminal_nao_roda_nada(self):
        chamadas = []
        with contextlib.ExitStack() as st:
            st.enter_context(mock.patch.object(req.shutil, "which", side_effect=lambda c: "/bin/brew" if c == "brew" else None))
            st.enter_context(mock.patch.object(req.glob, "glob", return_value=[]))
            st.enter_context(mock.patch.object(req.sys, "version_info", (3, 8, 0)))
            st.enter_context(mock.patch.object(req.subprocess, "run", side_effect=lambda argv, **k: chamadas.append(argv) or Processo(code=1)))
            st.enter_context(mock.patch("builtins.input", side_effect=EOFError))
            code, out = rodar("instalar")
        self.assertEqual(code, 1)
        self.assertIn("$ brew install uv", out)
        self.assertIn("não rodei", out)
        self.assertNotIn(["brew", "install", "uv"], chamadas)

    def test_sim_roda_so_o_que_falta(self):
        chamadas = []
        with contextlib.ExitStack() as st:
            st.enter_context(mock.patch.object(req.shutil, "which", side_effect=lambda c: "/bin/brew" if c == "brew" else None))
            st.enter_context(mock.patch.object(req.glob, "glob", return_value=[]))
            st.enter_context(mock.patch.object(req.sys, "version_info", (3, 8, 0)))
            st.enter_context(mock.patch.object(req.subprocess, "run", side_effect=lambda argv, **k: chamadas.append(argv) or Processo()))
            rodar("instalar", "uv", "--sim")
        self.assertIn(["brew", "install", "uv"], chamadas)

    def test_tudo_ok_nada_a_instalar(self):
        with mock.patch.object(req, "avaliar", side_effect=lambda i: {"estado": "ok"}):
            code, out = rodar("instalar")
        self.assertEqual(code, 0)
        self.assertIn("nada a instalar", out)

    def test_item_desconhecido_sai_2(self):
        self.assertEqual(rodar("instalar", "nao-existe")[0], 2)

    def test_nenhum_comando_aceita_licenca(self):
        with mock.patch.object(req.shutil, "which", side_effect=lambda c: f"/bin/{c}"):
            for item in req.REQUISITOS:
                for argv in (item["instalar"]() if item.get("instalar") else []):
                    self.assertFalse(req.proibido(argv), argv)
        self.assertTrue(req.proibido(["xcodebuild", "-license", "accept"]))
        self.assertTrue(req.proibido(["apt-get", "install", "-y", "x"]))

    def test_comando_proibido_e_recusado(self):
        item = {"id": "x", "nome": "X", "obrigatorio": True, "conferir": lambda: (False, "", ""),
                "instalar": lambda: [["tool", "--accept-license"]]}
        chamadas = []
        with mock.patch.object(req, "REQUISITOS", [item]), \
             mock.patch.object(req.subprocess, "run", side_effect=lambda argv, **k: chamadas.append(argv)):
            code, out = rodar("instalar", "--sim")
        self.assertEqual(code, 1)
        self.assertIn("recusei", out)
        self.assertEqual(chamadas, [])


if __name__ == "__main__":
    sys.exit(unittest.main(verbosity=1, exit=False).result.wasSuccessful() is False)
