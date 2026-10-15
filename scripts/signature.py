"""Régénère l'image de la signature courriel à partir du favicon :
assets/favicon.svg -> assets/signature/marque.png (132 x 132, affichée à 44 x 44, soit 3x pour les écrans haute densité).

Usage : python3 scripts/signature.py
Les signatures elles-mêmes sont dans docs/signature/ (HTML compatible courriel, styles en ligne).
Demande Playwright et Chromium.
"""
import os
from playwright.sync_api import sync_playwright

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
SVG = os.path.join(RACINE, "assets", "favicon.svg")
SORTIE = os.path.join(RACINE, "assets", "signature", "marque.png")
TAILLE = 132

with open(SVG, encoding="utf-8") as f:
    svg = f.read()

page_html = (
    '<!doctype html><html><head><style>html,body{margin:0;background:transparent}'
    'svg{display:block;width:%dpx;height:%dpx}</style></head><body>%s</body></html>'
    % (TAILLE, TAILLE, svg)
)

os.makedirs(os.path.dirname(SORTIE), exist_ok=True)
with sync_playwright() as p:
    navigateur = p.chromium.launch()
    page = navigateur.new_page(viewport={"width": TAILLE, "height": TAILLE})
    page.set_content(page_html)
    page.screenshot(path=SORTIE, omit_background=True)
    navigateur.close()
print("assets/signature/marque.png régénérée")
