#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Testes do scripts/verificar_readme.py (bloco "Cole isto na sua IA").
Uso: uv run tests/test_verificar_readme.py"""
from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("verificar_readme", REPO / "scripts" / "verificar_readme.py")
ver = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ver)

TABELA = "| **Onde roda** | macOS | |\n| **Programas** | `uv` (`brew install uv`) | |\n"
BOM = ('> **Cole isto na sua IA antes de instalar:**\n>\n'
       '> "Rode `uv run https://raw.githubusercontent.com/o/acme/main/scripts/requisitos.py checar`. '
       'Com o meu ok, rode `uv run https://raw.githubusercontent.com/o/acme/main/scripts/requisitos.py instalar --sim`. '
       'Não aceite licenças nem declarações por mim. Depois `claude plugin marketplace add o/acme`."\n')


def readme(bloco: str = BOM, tabela: str = TABELA) -> str:
    return f"# acme\n\n## Requisitos\n\nResumo.\n\n{bloco}\n{tabela}\n## Instalação\n\n```\n/plugin marketplace add o/acme\n```\n"


class Base(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.raiz = Path(self._tmp.name)
        (self.raiz / "scripts").mkdir()
        (self.raiz / "scripts" / "requisitos.py").write_text("# /// script\n# ///\n", encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    def erros(self, texto: str) -> list[str]:
        return ver.problemas(texto, self.raiz)


class TestBloco(Base):
    def test_bloco_bom_passa(self):
        self.assertEqual(self.erros(readme()), [])

    def test_sem_bloco_com_dependencia_falha(self):
        e = self.erros(readme(bloco=""))
        self.assertTrue(any("falta o bloco" in x for x in e), e)

    def test_sem_bloco_sem_dependencia_passa(self):
        (self.raiz / "scripts" / "requisitos.py").unlink()
        texto = readme(bloco="", tabela="| **Onde roda** | Claude Code | |\n")
        self.assertEqual(self.erros(texto), [])

    def test_prompt_generico_sem_comando_falha(self):
        bloco = '> **Cole isto na sua IA:**\n> "Verifique se tenho tudo e instale o que faltar. Não aceite licenças por mim."\n'
        e = self.erros(readme(bloco=bloco))
        self.assertTrue(any("comando real" in x for x in e), e)

    def test_comando_de_script_inexistente_falha(self):
        bloco = BOM.replace("scripts/requisitos.py", "scripts/inventado.py")
        e = self.erros(readme(bloco=bloco))
        self.assertTrue(any("comando real" in x for x in e), e)

    def test_sem_trava_de_licenca_falha(self):
        bloco = BOM.replace("Não aceite licenças nem declarações por mim. ", "")
        e = self.erros(readme(bloco=bloco))
        self.assertTrue(any("não aceite licenças" in x for x in e), e)

    def test_bloco_depois_da_instalacao_falha(self):
        texto = readme(bloco="", tabela=TABELA + "\n" + BOM)
        e = self.erros(texto)
        self.assertTrue(any("antes do primeiro passo" in x for x in e), e)

    def test_gh_api_de_repo_privado_passa(self):
        bloco = ('> **Cole isto na sua IA antes de instalar:**\n'
                 '> "Rode `gh api \'repos/o/acme/contents/scripts/requisitos.py?ref=main\' -H \'Accept: application/vnd.github.raw\' > /tmp/r.py` '
                 'e `uv run /tmp/r.py checar`. Não aceite licenças nem declarações por mim; instale só com meu ok."\n')
        self.assertEqual(self.erros(readme(bloco=bloco)), [])

    def test_comando_de_bin_passa(self):
        (self.raiz / "bin").mkdir()
        (self.raiz / "bin" / "acme").write_text("#!/bin/sh\n", encoding="utf-8")
        bloco = '> **Cole isto na sua IA:**\n> "Rode `acme doctor` e me mostre o que falta."\n'
        self.assertEqual(self.erros(readme(bloco=bloco)), [])


class TestAntigos(Base):
    def test_antes_de_comecar_falha(self):
        self.assertTrue(any("Antes de começar" in x for x in ver.problemas("## Antes de começar\n## Instalação\n")))

    def test_main_codigos(self):
        arq = self.raiz / "README.md"
        arq.write_text(readme(), encoding="utf-8")
        self.assertEqual(ver.main([str(arq)]), 0)
        arq.write_text(readme(bloco=""), encoding="utf-8")
        self.assertEqual(ver.main([str(arq)]), 1)
        self.assertEqual(ver.main([str(self.raiz / "nao.md")]), 2)


if __name__ == "__main__":
    sys.exit(unittest.main(verbosity=1, exit=False).result.wasSuccessful() is False)
