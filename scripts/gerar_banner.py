#!/usr/bin/env python3
"""Gera docs/banner.svg (1280x420) com texto que sempre cabe.

Uso:
  python3 -I gerar_banner.py --nome meu-projeto --kicker "PLUGIN PARA X" \
    --linha1 "Frase de valor." --linha2 "Segunda frase." \
    --rotulos "01 · Pasta A|02 · Pasta B|03 · Pasta C" \
    --cores "#1e3a8a,#2563eb,#06b6d4" --saida docs/banner.svg

Os tamanhos de fonte são calculados pelo comprimento do texto, para nada
sair do banner nem dos cards.
"""
import argparse
import os
import xml.dom.minidom
from xml.sax.saxutils import escape

LARGURA, ALTURA = 1280, 420
FONTE = "Segoe UI, Helvetica, Arial, sans-serif"
ESQ = 80            # margem esquerda do texto
CARD_X = 770        # início dos cards
CARD_W = 450
ZONA_TEXTO = CARD_X - ESQ - 40   # largura útil do texto da esquerda
F_REG, F_BOLD = 0.58, 0.66       # largura média de um caractere / tamanho da fonte


def ajusta(texto, maximo, largura, fator):
    """Maior tamanho de fonte (<= maximo) em que o texto cabe na largura."""
    if not texto:
        return maximo
    return max(12, min(maximo, int(largura / (len(texto) * fator))))


def kicker_fonte(texto, maximo, largura):
    # texto em caixa alta, negrito, com letter-spacing de 3px
    if not texto:
        return maximo
    return max(12, min(maximo, int((largura / len(texto) - 3) / 0.7)))


def gerar(a):
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
    f_rot = min(ajusta(r, 20, CARD_W - 90, F_BOLD) for r in rotulos if r) if any(rotulos) else 20

    ponto = [c2, c3, "#f59e0b"]
    ys = [110, 196, 282]
    dx = [0, 30, 0]
    cards, sombras, pontos, textos = [], [], [], []
    for i in range(3):
        x = CARD_X + dx[i]
        y = ys[i]
        sombras.append(f'<rect x="{x}" y="{y + 10}" width="{CARD_W}" height="64" rx="14"/>')
        cards.append(f'<rect x="{x}" y="{y}" width="{CARD_W}" height="64" rx="14"/>')
        pontos.append(f'<circle cx="{x + 32}" cy="{y + 32}" r="12" fill="{ponto[i]}"/>')
        if rotulos[i]:
            textos.append(f'<text x="{x + 56}" y="{y + 39}">{escape(rotulos[i])}</text>')

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

  <g fill="#0b1b4d" opacity="0.28">
    {"".join(sombras)}
  </g>
  <g fill="url(#card)">
    {"".join(cards)}
  </g>
  {"".join(pontos)}
  <g font-family="{FONTE}" font-size="{f_rot}" font-weight="600" fill="{c1}">
    {"".join(textos)}
  </g>
</svg>
'''
    xml.dom.minidom.parseString(svg)  # falha se o XML for inválido
    pasta = os.path.dirname(os.path.abspath(a.saida))
    os.makedirs(pasta, exist_ok=True)
    with open(a.saida, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"ok: {a.saida} (fontes: kicker {f_kick}, nome {f_nome}, linhas {f_l1}/{f_l2}, rótulos {f_rot})")


def main():
    p = argparse.ArgumentParser(description="Gera banner SVG com texto auto-ajustado.")
    p.add_argument("--nome", required=True)
    p.add_argument("--kicker", default="")
    p.add_argument("--linha1", required=True)
    p.add_argument("--linha2", default="")
    p.add_argument("--rotulos", default="", help='até 3 rótulos separados por "|"')
    p.add_argument("--cores", default="#1e3a8a,#2563eb,#06b6d4")
    p.add_argument("--saida", default="docs/banner.svg")
    gerar(p.parse_args())


if __name__ == "__main__":
    main()
