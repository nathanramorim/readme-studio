#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Gera docs/banner.svg (1280x420) com texto que sempre cabe.

Com --identidade, o banner usa o tema do projeto (fundo, cores, fontes, logo), como a
landing page dele. Sem ela, usa o tema azul claro padrão.

O banner deve lembrar o que o projeto faz. Há duas formas de escolher o
desenho da direita:
  --ilustracao pastas|fluxo|terminal   desenhos prontos
  --ilustracao-arquivo desenho.svg     fragmento SVG próprio do projeto
                                       (sem a tag <svg>), desenhado na área
                                       x 770-1250, y 90-370. Recomendado.

Uso:
  uv run gerar_banner.py --nome meu-projeto --kicker "PLUGIN PARA X" \\
    --linha1 "Frase de valor." --linha2 "Segunda frase." \\
    --rotulos "Passo 1|Passo 2|Passo 3" --ilustracao fluxo \\
    --cores "#1e3a8a,#2563eb,#06b6d4" --saida docs/banner.svg

Os tamanhos de fonte são calculados pelo comprimento do texto, para nada
sair do banner nem dos cards.
"""
import argparse
import json
import os
import xml.dom.minidom
from xml.sax.saxutils import escape

LARGURA, ALTURA = 1280, 420
FONTE = "Segoe UI, Helvetica, Arial, sans-serif"
MONO = "SF Mono, Menlo, Consolas, monospace"
ESQ = 80
CARD_X = 770
CARD_W = 450
ZONA_TEXTO = CARD_X - ESQ - 40
F_REG, F_BOLD = 0.58, 0.66


def ajusta(texto, maximo, largura, fator):
    """Maior tamanho de fonte (<= maximo) em que o texto cabe na largura."""
    if not texto:
        return maximo
    return max(12, min(maximo, int(largura / (len(texto) * fator))))


def kicker_fonte(texto, maximo, largura):
    if not texto:
        return maximo
    return max(12, min(maximo, int((largura / len(texto) - 3) / 0.7)))


def _fonte_rotulos(rotulos, maximo, largura, fator=F_BOLD):
    usados = [r for r in rotulos if r]
    return min(ajusta(r, maximo, largura, fator) for r in usados) if usados else maximo


def _pastas(rotulos, c1, c2, c3):
    f = _fonte_rotulos(rotulos, 20, CARD_W - 90)
    ponto = [c2, c3, "#f59e0b"]
    ys, dx = [110, 196, 282], [0, 30, 0]
    out = ['<g fill="#0b1b4d" opacity="0.28">']
    out += [f'<rect x="{CARD_X + dx[i]}" y="{ys[i] + 10}" width="{CARD_W}" height="64" rx="14"/>' for i in range(3)]
    out.append('</g><g fill="url(#card)">')
    out += [f'<rect x="{CARD_X + dx[i]}" y="{ys[i]}" width="{CARD_W}" height="64" rx="14"/>' for i in range(3)]
    out.append('</g>')
    out += [f'<circle cx="{CARD_X + dx[i] + 32}" cy="{ys[i] + 32}" r="12" fill="{ponto[i]}"/>' for i in range(3)]
    out.append(f'<g font-family="{FONTE}" font-size="{f}" font-weight="600" fill="{c1}">')
    out += [f'<text x="{CARD_X + dx[i] + 56}" y="{ys[i] + 39}">{escape(rotulos[i])}</text>' for i in range(3) if rotulos[i]]
    out.append('</g>')
    return "".join(out)


def _fluxo(rotulos, c1, c2, c3):
    f = _fonte_rotulos(rotulos, 20, CARD_W - 90)
    ys = [104, 190, 276]
    out = ['<g stroke="#ffffff" stroke-width="3" opacity="0.7">']
    out += [f'<line x1="{CARD_X + 32}" y1="{y + 64}" x2="{CARD_X + 32}" y2="{y + 86}"/>' for y in ys[:2]]
    out.append('</g><g fill="url(#card)">')
    out += [f'<rect x="{CARD_X}" y="{y}" width="{CARD_W}" height="64" rx="14"/>' for y in ys]
    out.append('</g>')
    for i, y in enumerate(ys):
        out.append(f'<circle cx="{CARD_X + 32}" cy="{y + 32}" r="16" fill="{c2}"/>')
        out.append(f'<text x="{CARD_X + 32}" y="{y + 39}" text-anchor="middle" font-family="{FONTE}" font-size="20" font-weight="800" fill="#ffffff">{i + 1}</text>')
        if rotulos[i]:
            out.append(f'<text x="{CARD_X + 62}" y="{y + 39}" font-family="{FONTE}" font-size="{f}" font-weight="600" fill="{c1}">{escape(rotulos[i])}</text>')
    return "".join(out)


def _terminal(rotulos, c1, c2, c3):
    largura = CARD_W + 30
    f = _fonte_rotulos(rotulos, 22, largura - 90, 0.62)
    out = [f'<rect x="{CARD_X}" y="110" width="{largura}" height="236" rx="16" fill="#0b1220"/>',
           f'<rect x="{CARD_X}" y="110" width="{largura}" height="40" rx="16" fill="#1e293b"/>',
           f'<rect x="{CARD_X}" y="134" width="{largura}" height="16" fill="#1e293b"/>',
           f'<circle cx="{CARD_X + 24}" cy="130" r="7" fill="#ef4444"/>',
           f'<circle cx="{CARD_X + 48}" cy="130" r="7" fill="#f59e0b"/>',
           f'<circle cx="{CARD_X + 72}" cy="130" r="7" fill="#22c55e"/>']
    for i, r in enumerate(rotulos):
        if r:
            out.append(f'<text x="{CARD_X + 28}" y="{194 + i * 52}" font-family="{MONO}" font-size="{f}" fill="#e2e8f0"><tspan fill="#22c55e">$ </tspan>{escape(r)}</text>')
    return "".join(out)


def montar_ilustracao(a, rotulos, c1, c2, c3):
    if a.ilustracao_arquivo:
        with open(a.ilustracao_arquivo, encoding="utf-8") as f:
            return f.read()
    return {"pastas": _pastas, "fluxo": _fluxo, "terminal": _terminal}[a.ilustracao](rotulos, c1, c2, c3)


IDENTIDADE_PADRAO = {
    "fundo": "#0d0f14", "brilho": "#1e2a4a", "texto": "#e9ecf4", "suave": "#99a2b8",
    "acento": ["#4f8ef7", "#8aa4ff", "#3ecf8e"],
    "painel": "#12151d", "borda": "#252d40",
    "terminal_fundo": "#090b10", "terminal_borda": "#363e52", "ok": "#3ecf8e",
    "fonte": "system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif",
    "fonte_mono": "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace",
    "logo": "",
}


def carregar_identidade(caminho):
    """Lê o JSON de identidade e completa o que faltar com o padrão escuro."""
    with open(caminho, encoding="utf-8") as f:
        dados = json.load(f)
    ident = dict(IDENTIDADE_PADRAO)
    ident.update({k: v for k, v in dados.items() if v not in (None, "")})
    ac = list(ident["acento"])
    while len(ac) < 3:
        ac.append(ac[-1])
    ident["acento"] = ac[:3]
    base = os.path.dirname(os.path.abspath(caminho))
    logo = ident.get("logo") or ""
    if logo and not os.path.isabs(logo):
        logo = os.path.join(base, logo)
    ident["logo"] = logo
    return ident


def gerar_escuro(a, ident):
    """Layout com a identidade do projeto: fundo escuro, logo, título em degradê,
    terminal e painel para a ilustração própria (--ilustracao-arquivo, obrigatória)."""
    if not a.ilustracao_arquivo:
        raise SystemExit("erro: com --identidade, informe --ilustracao-arquivo (desenho do painel da direita)")
    with open(a.ilustracao_arquivo, encoding="utf-8") as f:
        ilustracao = f.read()
    logo = ""
    if ident["logo"]:
        with open(ident["logo"], encoding="utf-8") as f:
            logo = f.read()

    c1, c2, c3 = ident["acento"]
    sans, mono = ident["fonte"], ident["fonte_mono"]
    zona = ZONA_TEXTO - 20            # o texto fica à esquerda do painel
    t1, t2 = a.titulo1 or a.nome, a.titulo2
    f_t = min(ajusta(t, 56, zona, 0.64) for t in (t1, t2) if t) if (t1 or t2) else 56
    f_s1 = ajusta(a.linha1, 19, zona, 0.56)
    f_s2 = ajusta(a.linha2, 19, zona, 0.56)
    f_nome = ajusta(a.nome, 34, 400, F_BOLD)
    f_eye = max(11, min(14, int((zona - 20) / max(1, len(a.kicker)) / 0.78 - 1.4))) if a.kicker else 14
    f_cmd = ajusta(a.comando, 16, 460, 0.62) if a.comando else 16
    w_cmd = min(560, int(len(a.comando) * f_cmd * 0.62) + 44) if a.comando else 0

    partes = []
    if logo:
        partes.append(f'<g transform="translate(80 44) scale(1.9)">{logo}</g>')
        partes.append(f'<text x="152" y="88" font-family="{sans}" font-weight="800" font-size="{f_nome}" fill="{ident["texto"]}" letter-spacing="-0.5">{escape(a.nome)}</text>')
    else:
        partes.append(f'<text x="80" y="88" font-family="{sans}" font-weight="800" font-size="{f_nome}" fill="{ident["texto"]}" letter-spacing="-0.5">{escape(a.nome)}</text>')
    if a.kicker:
        partes.append(f'<circle cx="86" cy="140" r="5" fill="{ident["ok"]}"/>')
        partes.append(f'<text x="100" y="145" font-family="{sans}" font-weight="600" font-size="{f_eye}" fill="{ident["suave"]}" letter-spacing="1.4">{escape(a.kicker.upper())}</text>')
    if t1 and t1 != a.nome or t2:
        partes.append(f'<text x="80" y="205" font-family="{sans}" font-weight="800" font-size="{f_t}" fill="#ffffff" letter-spacing="-1.2">{escape(t1)}</text>')
        if t2:
            partes.append(f'<text x="80" y="265" font-family="{sans}" font-weight="800" font-size="{f_t}" fill="url(#acc)" letter-spacing="-1.2">{escape(t2)}</text>')
    if a.linha1:
        partes.append(f'<text x="80" y="305" font-family="{sans}" font-weight="500" font-size="{f_s1}" fill="{ident["suave"]}">{escape(a.linha1)}</text>')
    if a.linha2:
        partes.append(f'<text x="80" y="331" font-family="{sans}" font-weight="500" font-size="{f_s2}" fill="{ident["suave"]}">{escape(a.linha2)}</text>')
    if a.comando:
        partes.append(f'<rect x="80" y="352" width="{w_cmd}" height="40" rx="12" fill="{ident["terminal_fundo"]}" stroke="{ident["terminal_borda"]}" stroke-width="1.2"/>')
        partes.append(f'<text x="100" y="377" font-family="{mono}" font-weight="600" font-size="{f_cmd}" fill="{ident["ok"]}">{escape(a.comando)}</text>')

    texto = "\n  ".join(partes)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{LARGURA}" height="{ALTURA}" viewBox="0 0 {LARGURA} {ALTURA}" role="img" aria-label="{escape(a.nome)}: {escape(a.titulo1)} {escape(a.titulo2)}">
  <defs>
    <radialGradient id="glow" cx="50%" cy="25%" r="75%">
      <stop offset="0" stop-color="{ident["brilho"]}" stop-opacity="0.85"/>
      <stop offset="1" stop-color="{ident["fundo"]}"/>
    </radialGradient>
    <linearGradient id="acc" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{c1}"/><stop offset="0.5" stop-color="{c2}"/><stop offset="1" stop-color="{c3}"/>
    </linearGradient>
    <linearGradient id="hex" x1="2" y1="4" x2="30" y2="28" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{c1}"/><stop offset="0.5" stop-color="{c2}"/><stop offset="1" stop-color="{c3}"/>
    </linearGradient>
    <marker id="seta" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
      <path d="M0 0 L7 4 L0 8 Z" fill="{c2}"/>
    </marker>
  </defs>

  <rect width="{LARGURA}" height="{ALTURA}" fill="{ident["fundo"]}"/>
  <rect width="{LARGURA}" height="{ALTURA}" fill="url(#glow)"/>

  {texto}

  <rect x="760" y="62" width="480" height="318" rx="18" fill="{ident["painel"]}" stroke="{ident["borda"]}" stroke-width="1.5"/>
  {ilustracao}
</svg>
'''
    xml.dom.minidom.parseString(svg)  # falha se o XML for inválido
    os.makedirs(os.path.dirname(os.path.abspath(a.saida)), exist_ok=True)
    with open(a.saida, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"ok: {a.saida} (tema escuro; fontes: título {f_t}, subtítulo {f_s1}/{f_s2}, eyebrow {f_eye}, comando {f_cmd})")


def gerar(a):
    if a.identidade:
        return gerar_escuro(a, carregar_identidade(a.identidade))
    cores = [c.strip() for c in a.cores.split(",")]
    while len(cores) < 3:
        cores.append(cores[-1])
    c1, c2, c3 = cores[:3]
    rotulos = [r.strip() for r in a.rotulos.split("|") if r.strip()][:3]
    while len(rotulos) < 3:
        rotulos.append("")

    f_kick = kicker_fonte(a.kicker.upper(), 26, ZONA_TEXTO)
    f_nome = ajusta(a.nome, 78, ZONA_TEXTO, F_BOLD)
    f_l1 = ajusta(a.linha1, 30, ZONA_TEXTO, F_REG)
    f_l2 = ajusta(a.linha2, 30, ZONA_TEXTO, F_REG)
    ilustracao = montar_ilustracao(a, rotulos, c1, c2, c3)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{LARGURA}" height="{ALTURA}" viewBox="0 0 {LARGURA} {ALTURA}" role="img" aria-label="{escape(a.nome)}: {escape(a.linha1)}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{c1}"/>
      <stop offset="0.6" stop-color="{c2}"/>
      <stop offset="1" stop-color="{c3}"/>
    </linearGradient>
    <linearGradient id="card" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#ffffff"/>
      <stop offset="1" stop-color="#e8f0ff"/>
    </linearGradient>
  </defs>

  <rect width="{LARGURA}" height="{ALTURA}" fill="url(#bg)"/>
  <circle cx="1120" cy="-20" r="220" fill="#ffffff" opacity="0.07"/>
  <circle cx="1220" cy="380" r="160" fill="#ffffff" opacity="0.08"/>
  <circle cx="60" cy="420" r="140" fill="#ffffff" opacity="0.06"/>

  <text x="{ESQ}" y="150" font-family="{FONTE}" font-size="{f_kick}" font-weight="600" fill="#bfdbfe" letter-spacing="3">{escape(a.kicker.upper())}</text>
  <text x="{ESQ}" y="228" font-family="{FONTE}" font-size="{f_nome}" font-weight="800" fill="#ffffff">{escape(a.nome)}</text>
  <text x="{ESQ}" y="285" font-family="{FONTE}" font-size="{f_l1}" fill="#e0ecff">{escape(a.linha1)}</text>
  <text x="{ESQ}" y="330" font-family="{FONTE}" font-size="{f_l2}" fill="#e0ecff">{escape(a.linha2)}</text>

  {ilustracao}
</svg>
'''
    xml.dom.minidom.parseString(svg)  # falha se o XML for inválido
    os.makedirs(os.path.dirname(os.path.abspath(a.saida)), exist_ok=True)
    with open(a.saida, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"ok: {a.saida} (fontes: kicker {f_kick}, nome {f_nome}, linhas {f_l1}/{f_l2})")


def main():
    p = argparse.ArgumentParser(description="Gera banner SVG com texto auto-ajustado.")
    p.add_argument("--nome", required=True)
    p.add_argument("--kicker", default="")
    p.add_argument("--linha1", required=True)
    p.add_argument("--linha2", default="")
    p.add_argument("--rotulos", default="", help='até 3 rótulos separados por "|"')
    p.add_argument("--ilustracao", choices=["pastas", "fluxo", "terminal"], default="pastas")
    p.add_argument("--ilustracao-arquivo", default="",
                   help="fragmento SVG próprio do projeto (x 770-1250, y 90-370)")
    p.add_argument("--identidade", default="",
                   help="JSON com a identidade do projeto (tema escuro: cores, fontes, logo); exige --ilustracao-arquivo")
    p.add_argument("--titulo1", default="", help="(tema escuro) 1ª linha do título, em branco")
    p.add_argument("--titulo2", default="", help="(tema escuro) 2ª linha do título, em degradê")
    p.add_argument("--comando", default="", help="(tema escuro) comando de instalação, no terminal")
    p.add_argument("--cores", default="#1e3a8a,#2563eb,#06b6d4")
    p.add_argument("--saida", default="docs/banner.svg")
    gerar(p.parse_args())


if __name__ == "__main__":
    main()
