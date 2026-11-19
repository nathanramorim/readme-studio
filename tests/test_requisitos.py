#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Testes da adoção do motor requisitos-para-ia: cópias iguais ao skills.lock, receita válida nas 3
plataformas, Homebrew nunca pré-requisito e o README com o bloco que o motor imprime.
Uso: uv run tests/test_requisitos.py"""
from __future__ import annotations

import contextlib
import hashlib
import importlib.util
import io
import json
import sys
import tomllib
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("requisitos", REPO / "scripts" / "requisitos.py")
req = importlib.util.module_from_spec(spec)
sys.modules["requisitos"] = req  # o motor usa dataclass, que procura o módulo em sys.modules
spec.loader.exec_module(req)
TOML = REPO / "requisitos.toml"


def rodar(*args: str) -> tuple[int, str]:
    out = io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
        code = req.main(["--arquivo", str(TOML), *args])
    return code, out.getvalue()


class TestVendorizado(unittest.TestCase):
    def test_copias_batem_com_o_skills_lock(self):
        lock = json.loads((REPO / "skills.lock").read_text(encoding="utf-8"))
        motor = next(s for s in lock["skills"] if s["nome"] == "requisitos-para-ia")
        self.assertEqual(motor["modo"], "copia")
        self.assertRegex(motor["commit"], r"^[0-9a-f]{40}$")
        destinos = {d["destino"] for d in motor["destinos"]}
        self.assertEqual(destinos, set(motor["arquivos"]))
        for rel, sha in motor["arquivos"].items():
            self.assertEqual(hashlib.sha256((REPO / rel).read_bytes()).hexdigest(), sha, rel)


class TestReceita(unittest.TestCase):
    def test_valida_nas_tres_plataformas(self):
        code, out = rodar("validar")
        self.assertEqual(code, 0, out)
        self.assertIn("macos, linux, windows", out)

    def test_homebrew_nunca_e_pre_requisito(self):
        """Toda receita com brew tem, depois dela, outra para o mesmo sistema que não depende do brew."""
        dados = tomllib.loads(TOML.read_text(encoding="utf-8"))
        for item in dados["requisito"]:
            receitas = item.get("receita", [])
            for i, r in enumerate(receitas):
                q = r.get("quando", {})
                if q.get("gerenciador") != "brew":
                    continue
                sistema = q.get("sistema")
                resto = [x for x in receitas[i + 1:] if x.get("quando", {}).get("sistema", sistema) == sistema
                         and "gerenciador" not in x.get("quando", {})]
                self.assertTrue(resto, f"{item['id']}: sem alternativa ao Homebrew")

    def test_checar_json_nao_quebra(self):
        code, out = rodar("checar", "--json")
        self.assertIn(code, (0, 1), out)
        dados = json.loads(out)
        self.assertEqual({r["id"] for r in dados["requisitos"]},
                         {"uv", "python", "git", "navegador", "agente", "disco"})


class TestReadme(unittest.TestCase):
    def test_readme_usa_o_bloco_do_motor(self):
        code, bloco = rodar("prompt")
        self.assertEqual(code, 0)
        self.assertIn(bloco.strip(), (REPO / "README.md").read_text(encoding="utf-8"))

    def test_sem_brew_install_uv(self):
        for rel in ("README.md", "templates/README.md.tmpl", "skills/readme-comercial/SKILL.md"):
            self.assertNotIn("brew install uv", (REPO / rel).read_text(encoding="utf-8"), rel)


if __name__ == "__main__":
    sys.exit(unittest.main(verbosity=1, exit=False).result.wasSuccessful() is False)
