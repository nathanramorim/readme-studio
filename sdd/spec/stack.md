# Stack — readme-studio

## Dependências

| Camada | Escolha | Versão | Motivo |
|--------|---------|--------|--------|
| Runtime | Python via `uv` | >= 3.9 | Scripts só com a biblioteca padrão; nunca pip |
| Banner | `argparse`, `json`, `xml.dom.minidom`, `xml.sax.saxutils` (stdlib) | — | SVG com texto escapado e XML validado |
| Conferência visual | Google Chrome headless (opcional) | — | A skill confere o banner renderizado |
| Testes | nenhum automatizado ainda | — | Critérios por comando (Regra 8); ver Divergências |
| DB | none | — | — |

## Layout do projeto
```
.claude-plugin/plugin.json, marketplace.json   o plugin (source ./)
commands/readme-gerar.md                       /readme-gerar
skills/readme-comercial/SKILL.md               a skill (passo a passo e regras de conteúdo)
scripts/gerar_banner.py                        banner SVG 1280x420, texto auto-ajustado
templates/README.md.tmpl                       estrutura do README com {{PLACEHOLDERS}}
exemplos/                                      identidade de exemplo
docs/                                          banner do próprio README
sdd/, .agents/, .claude/, .gemini/, .forge/    Forge SDD (fora do plugin)
```
