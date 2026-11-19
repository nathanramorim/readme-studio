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


class TestComandosDeclarados(Base):
    def bloco(self, cmd: str) -> str:
        return f'> **Cole isto na sua IA:**\n> "Rode `{cmd}` e me mostre o que falta. Não aceite licenças nem declarações por mim; instale só com meu ok."\n'

    def test_entry_point_do_pyproject(self):
        (self.raiz / "pyproject.toml").write_text('[project]\nname = "acme"\n\n[project.scripts]\ngv = "acme.cli:main"\n', encoding="utf-8")
        self.assertEqual(self.erros(readme(bloco=self.bloco("uv run gv requisitos checar"))), [])
        self.assertEqual(self.erros(readme(bloco=self.bloco("uv run --with x==1 gv requisitos checar"))), [])

    def test_entry_point_sem_tomllib(self):  # Python 3.9/3.10: lê a seção à mão
        from unittest import mock
        (self.raiz / "pyproject.toml").write_text('[project.scripts]\ngv = "a:main"\n"gr" = "b:main"\n\n[build-system]\nx = 1\n', encoding="utf-8")
        with mock.patch.dict(sys.modules, {"tomllib": None}):
            self.assertEqual(ver._scripts_pyproject(self.raiz), {"gv", "gr"})

    def test_uvx_so_com_from_local(self):
        (self.raiz / "pyproject.toml").write_text('[project.scripts]\ngv = "a:main"\n', encoding="utf-8")
        self.assertEqual(self.erros(readme(bloco=self.bloco("uvx --from . gv checar"))), [])

    def test_manifesto_com_tipo_errado_nao_quebra(self):
        (self.raiz / "pyproject.toml").write_text('[project]\nscripts = "ruim"\n', encoding="utf-8")
        (self.raiz / "package.json").write_text('["lista"]', encoding="utf-8")
        e = self.erros(readme(bloco=self.bloco("uv run gv checar")))
        self.assertTrue(any("comando real" in x for x in e), e)

    def test_npm_run_script(self):
        (self.raiz / "package.json").write_text('{"name": "acme", "scripts": {"requisitos": "node r.js"}}', encoding="utf-8")
        self.assertEqual(self.erros(readme(bloco=self.bloco("npm run requisitos -- checar"))), [])

    def test_npx_bin(self):
        (self.raiz / "package.json").write_text('{"name": "acme", "bin": {"acme-check": "cli.js"}}', encoding="utf-8")
        self.assertEqual(self.erros(readme(bloco=self.bloco("npx acme-check checar"))), [])

    def test_npx_bin_texto_usa_o_nome_do_pacote(self):
        (self.raiz / "package.json").write_text('{"name": "@o/acme", "bin": "cli.js"}', encoding="utf-8")
        self.assertEqual(self.erros(readme(bloco=self.bloco("npx acme checar"))), [])

    def test_bin_do_plugin(self):
        (self.raiz / "plugins" / "acme" / "bin").mkdir(parents=True)
        (self.raiz / "plugins" / "acme" / "bin" / "acme").write_text("#!/bin/sh\n", encoding="utf-8")
        self.assertEqual(self.erros(readme(bloco=self.bloco("acme requisitos checar"))), [])

    def test_caminho_de_script(self):
        self.assertEqual(self.erros(readme(bloco=self.bloco("uv run scripts/requisitos.py checar"))), [])

    def test_nome_inventado_falha(self):
        (self.raiz / "pyproject.toml").write_text('[project.scripts]\ngv = "acme.cli:main"\n', encoding="utf-8")
        (self.raiz / "package.json").write_text('{"name": "acme", "scripts": {"a": "x"}, "bin": {"b": "c.js"}}', encoding="utf-8")
        for cmd in ("uv run inventado checar", "npm run inventado", "npx inventado", "inventado checar", "uvx inventado",
                    "uvx gv checar", "npm a"):
            e = self.erros(readme(bloco=self.bloco(cmd)))
            self.assertTrue(any("comando real" in x for x in e), (cmd, e))


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
