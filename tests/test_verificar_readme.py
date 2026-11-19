#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Testes do scripts/verificar_readme.py (bloco "Cole isto na sua IA" do motor requisitos-para-ia).
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

TABELA = ("| **Onde roda** | macOS, Linux e Windows | |\n| **Programas** | `uv` | |\n"
          "| ↳ macOS | instalador oficial | |\n| ↳ Linux | instalador oficial | |\n| ↳ Windows | winget ou oficial | |\n")
BOM = ('> **Cole isto na sua IA antes de instalar:**\n>\n'
       '> "Confira os requisitos do acme. No Windows, rode `powershell -ExecutionPolicy Bypass -File scripts/bootstrap.ps1`; '
       'no macOS ou Linux, rode `sh scripts/bootstrap.sh`. Ele confere e, com o meu ok, instala o uv, e depois mostra o que falta. '
       'Para cada item, peça meu ok e rode `uv run scripts/requisitos.py instalar --sim <item>`. '
       'Não aceite licenças nem declarações por mim e não mexa em senhas, chaves ou tokens."\n')
MOTOR = REPO / "scripts" / "requisitos.py"


def readme(bloco: str = BOM, tabela: str = TABELA) -> str:
    return f"# acme\n\n## Requisitos\n\nResumo.\n\n{bloco}\n{tabela}\n## Instalação\n\n```\n/plugin marketplace add o/acme\n```\n"


class Base(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.raiz = Path(self._tmp.name)
        (self.raiz / "scripts").mkdir()
        (self.raiz / "scripts" / "requisitos.py").write_text("# /// script\n# ///\n", encoding="utf-8")
        (self.raiz / "scripts" / "bootstrap.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        (self.raiz / "scripts" / "bootstrap.ps1").write_text("# ps\n", encoding="utf-8")
        (self.raiz / "requisitos.toml").write_text('versao = 1\n[projeto]\nnome = "acme"\n', encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    def erros(self, texto: str) -> list[str]:
        return ver.problemas(texto, self.raiz)

    def erros_de_comando(self, texto: str) -> list[str]:
        """Só os erros de 'comando real' (os blocos destes testes não trazem o bootstrap de propósito)."""
        return [x for x in self.erros(texto) if "comando real" in x]


class TestBloco(Base):
    def test_bloco_bom_passa(self):
        self.assertEqual(self.erros(readme()), [])

    def test_sem_bloco_com_dependencia_falha(self):
        e = self.erros(readme(bloco=""))
        self.assertTrue(any("falta o bloco" in x for x in e), e)

    def test_sem_bloco_sem_dependencia_passa(self):
        (self.raiz / "scripts" / "requisitos.py").unlink()
        (self.raiz / "requisitos.toml").unlink()
        texto = readme(bloco="", tabela="| **Onde roda** | Claude Code no macOS, Linux e Windows | |\n")
        self.assertEqual(self.erros(texto), [])

    def test_prompt_generico_sem_comando_falha(self):
        bloco = '> **Cole isto na sua IA:**\n> "Verifique se tenho tudo e instale o que faltar. Não aceite licenças por mim."\n'
        e = self.erros(readme(bloco=bloco))
        self.assertTrue(any("comando real" in x for x in e), e)

    def test_comando_de_script_inexistente_falha(self):
        bloco = BOM.replace("scripts/", "inventado/")
        e = self.erros(readme(bloco=bloco))
        self.assertTrue(any("comando real" in x for x in e), e)

    def test_sem_trava_de_licenca_falha(self):
        bloco = BOM.replace("Não aceite licenças nem declarações por mim e não mexa em senhas, chaves ou tokens.", "")
        e = self.erros(readme(bloco=bloco))
        self.assertTrue(any("não aceite licenças" in x for x in e), e)

    def test_bloco_depois_da_instalacao_falha(self):
        texto = readme(bloco="", tabela=TABELA + "\n```\ngit clone https://github.com/o/acme\n```\n\n" + BOM)
        e = self.erros(texto)
        self.assertTrue(any("antes do primeiro passo" in x for x in e), e)

    def test_gh_api_de_repo_privado_passa(self):
        bloco = ('> **Cole isto na sua IA antes de instalar:**\n'
                 '> "Rode `gh api \'repos/o/acme/contents/scripts/requisitos.py?ref=main\' -H \'Accept: application/vnd.github.raw\' > /tmp/r.py` '
                 'e `uv run /tmp/r.py checar`. Não aceite licenças nem declarações por mim; instale só com meu ok."\n')
        self.assertEqual(self.erros_de_comando(readme(bloco=bloco)), [])

    def test_comando_de_bin_passa(self):
        (self.raiz / "bin").mkdir()
        (self.raiz / "bin" / "acme").write_text("#!/bin/sh\n", encoding="utf-8")
        bloco = '> **Cole isto na sua IA:**\n> "Rode `acme doctor` e me mostre o que falta."\n'
        self.assertEqual(self.erros_de_comando(readme(bloco=bloco)), [])


class TestComandosDeclarados(Base):
    def bloco(self, cmd: str) -> str:
        return f'> **Cole isto na sua IA:**\n> "Rode `{cmd}` e me mostre o que falta. Não aceite licenças nem declarações por mim; instale só com meu ok."\n'

    def test_entry_point_do_pyproject(self):
        (self.raiz / "pyproject.toml").write_text('[project]\nname = "acme"\n\n[project.scripts]\ngv = "acme.cli:main"\n', encoding="utf-8")
        self.assertEqual(self.erros_de_comando(readme(bloco=self.bloco("uv run gv requisitos checar"))), [])
        self.assertEqual(self.erros_de_comando(readme(bloco=self.bloco("uv run --with x==1 gv requisitos checar"))), [])

    def test_entry_point_sem_tomllib(self):  # Python 3.9/3.10: lê a seção à mão
        from unittest import mock
        (self.raiz / "pyproject.toml").write_text('[project.scripts]\ngv = "a:main"\n"gr" = "b:main"\n\n[build-system]\nx = 1\n', encoding="utf-8")
        with mock.patch.dict(sys.modules, {"tomllib": None}):
            self.assertEqual(ver._scripts_pyproject(self.raiz), {"gv", "gr"})

    def test_uvx_so_com_from_local(self):
        (self.raiz / "pyproject.toml").write_text('[project.scripts]\ngv = "a:main"\n', encoding="utf-8")
        self.assertEqual(self.erros_de_comando(readme(bloco=self.bloco("uvx --from . gv checar"))), [])

    def test_venv_nao_conta_mas_env_conta(self):
        (self.raiz / "venv" / "bin").mkdir(parents=True)
        (self.raiz / "venv" / "bin" / "pip").write_text("x", encoding="utf-8")
        self.assertTrue(any("comando real" in x for x in self.erros(readme(bloco=self.bloco("pip checar")))))
        (self.raiz / "env" / "bin").mkdir(parents=True)
        (self.raiz / "env" / "bin" / "acme").write_text("x", encoding="utf-8")
        self.assertEqual(self.erros_de_comando(readme(bloco=self.bloco("acme checar"))), [])

    def test_manifesto_com_tipo_errado_nao_quebra(self):
        (self.raiz / "pyproject.toml").write_text('[project]\nscripts = "ruim"\n', encoding="utf-8")
        (self.raiz / "package.json").write_text('["lista"]', encoding="utf-8")
        e = self.erros(readme(bloco=self.bloco("uv run gv checar")))
        self.assertTrue(any("comando real" in x for x in e), e)

    def test_npm_run_script(self):
        (self.raiz / "package.json").write_text('{"name": "acme", "scripts": {"requisitos": "node r.js"}}', encoding="utf-8")
        self.assertEqual(self.erros_de_comando(readme(bloco=self.bloco("npm run requisitos -- checar"))), [])

    def test_npx_bin(self):
        (self.raiz / "package.json").write_text('{"name": "acme", "bin": {"acme-check": "cli.js"}}', encoding="utf-8")
        self.assertEqual(self.erros_de_comando(readme(bloco=self.bloco("npx acme-check checar"))), [])

    def test_npx_bin_texto_usa_o_nome_do_pacote(self):
        (self.raiz / "package.json").write_text('{"name": "@o/acme", "bin": "cli.js"}', encoding="utf-8")
        self.assertEqual(self.erros_de_comando(readme(bloco=self.bloco("npx acme checar"))), [])

    def test_bin_do_plugin(self):
        (self.raiz / "plugins" / "acme" / "bin").mkdir(parents=True)
        (self.raiz / "plugins" / "acme" / "bin" / "acme").write_text("#!/bin/sh\n", encoding="utf-8")
        self.assertEqual(self.erros_de_comando(readme(bloco=self.bloco("acme requisitos checar"))), [])

    def test_caminho_de_script(self):
        self.assertEqual(self.erros_de_comando(readme(bloco=self.bloco("uv run scripts/requisitos.py checar"))), [])

    def test_nome_inventado_falha(self):
        (self.raiz / "pyproject.toml").write_text('[project.scripts]\ngv = "acme.cli:main"\n', encoding="utf-8")
        (self.raiz / "package.json").write_text('{"name": "acme", "scripts": {"a": "x"}, "bin": {"b": "c.js"}}', encoding="utf-8")
        for cmd in ("uv run inventado checar", "npm run inventado", "npx inventado", "inventado checar", "uvx inventado",
                    "uvx gv checar", "npm a", "uvx gv --from .", "uvx gv checar --from ./x"):
            e = self.erros(readme(bloco=self.bloco(cmd)))
            self.assertTrue(any("comando real" in x for x in e), (cmd, e))


class TestMultiplataforma(Base):
    def test_bloco_do_motor_passa(self):
        spec_m = importlib.util.spec_from_file_location("motor", MOTOR)
        motor = importlib.util.module_from_spec(spec_m)
        sys.modules["motor"] = motor  # o motor usa dataclass, que procura o módulo em sys.modules
        spec_m.loader.exec_module(motor)
        for projeto in ({"nome": "acme"}, {"nome": "acme", "repo": "o/acme"}):
            bloco = motor.bloco_prompt(projeto) + "\n"
            self.assertEqual(self.erros(readme(bloco=bloco)), [], projeto)

    def test_homebrew_como_pre_requisito_falha(self):
        for troca in (("instala o uv", "instala o uv com `brew install uv`"), ("Ele confere", "Instale o Homebrew. Ele confere"),
                      ("instala o uv", "instala o uv com `brew upgrade uv`"), ("instala o uv", "instala o uv com `brew reinstall uv`"),
                      ("instala o uv", "instala o uv com `brew tap astral-sh/uv`"), ("Ele confere", "Antes, tenha o brew. Ele confere")):
            e = self.erros(readme(bloco=BOM.replace(*troca)))
            self.assertTrue(any("Homebrew" in x for x in e), (troca, e))

    def test_sem_caminho_do_windows_falha(self):
        bloco = BOM.replace("No Windows, rode `powershell -ExecutionPolicy Bypass -File scripts/bootstrap.ps1`; no", "No")
        e = self.erros(readme(bloco=bloco))
        self.assertTrue(any("bootstrap.ps1" in x and "Windows" in x for x in e), e)

    def test_sem_caminho_posix_falha(self):
        bloco = BOM.replace("no macOS ou Linux, rode `sh scripts/bootstrap.sh`. ", "")
        e = self.erros(readme(bloco=bloco))
        self.assertTrue(any("bootstrap.sh" in x and "Linux" in x for x in e), e)

    def test_bootstrap_que_nao_existe_falha(self):
        (self.raiz / "scripts" / "bootstrap.ps1").unlink()
        e = self.erros(readme())
        self.assertTrue(any("bootstrap.ps1" in x and "não existe" in x for x in e), e)

    def test_bootstrap_de_fachada_falha(self):
        """Citar o bootstrap como argumento de outro comando real não conta como rodar o bootstrap."""
        (self.raiz / "scripts" / "bootstrap.ps1").unlink()
        bloco = BOM.replace("`powershell -ExecutionPolicy Bypass -File scripts/bootstrap.ps1`",
                            "`uv run scripts/requisitos.py checar --x scripts/bootstrap.ps1`")
        e = self.erros(readme(bloco=bloco))
        self.assertTrue(any("bootstrap.ps1" in x and "Windows" in x for x in e), e)
        bloco = BOM.replace("`sh scripts/bootstrap.sh`", "`uv run scripts/requisitos.py checar # bootstrap.sh`")
        e = self.erros(readme(bloco=bloco))
        self.assertTrue(any("bootstrap.sh" in x and "Linux" in x for x in e), e)

    def test_bootstrap_ausente_ao_lado_do_motor_falha(self):
        (self.raiz / "scripts" / "bootstrap.sh").unlink()
        e = self.erros(readme())
        self.assertTrue(any("bootstrap.sh" in x and "não existe" in x for x in e), e)

    def test_dependencia_sem_requisitos_toml_falha(self):
        (self.raiz / "requisitos.toml").unlink()
        e = self.erros(readme())
        self.assertTrue(any("falta o requisitos.toml" in x for x in e), e)
        e = self.erros(readme(bloco=""))
        self.assertTrue(any("falta o requisitos.toml" in x for x in e), e)

    def test_sem_instalar_pelo_motor_falha(self):
        for troca in ("instale", "rode `echo requisitos.py instalar`", "rode `uv run scripts/inventado/requisitos.py instalar`",
                      "rode `uv run scripts/requisitos.py checar instalar`"):
            bloco = BOM.replace("rode `uv run scripts/requisitos.py instalar --sim <item>`", troca)
            e = self.erros(readme(bloco=bloco))
            self.assertTrue(any("requisitos.py instalar" in x for x in e), (troca, e))

    def test_requisitos_sem_um_sistema_falha(self):
        for sistema in ("Windows", "Linux", "macOS"):
            tabela = TABELA.replace(f"| ↳ {sistema} |", "| ↳ outro |").replace(sistema, "x")
            e = self.erros(readme(tabela=tabela))  # o bloco do motor, intacto, cita os 3 e não conta
            self.assertTrue(any(f"não fala de {sistema}" in x for x in e), (sistema, e))


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
