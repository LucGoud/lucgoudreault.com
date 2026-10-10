"""Régénère les images de partage 1200 x 630 à partir des gabarits :
scripts/og.html -> assets/og.png (français), scripts/og-en.html -> assets/og-en.png (anglais).

Usage : python3 scripts/og.py
Modifier le texte dans les gabarits, puis relancer. Demande Playwright et Chromium.
"""
import os
from playwright.sync_api import sync_playwright

ICI = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(os.path.dirname(ICI), "assets")

with sync_playwright() as p:
    navigateur = p.chromium.launch()
    page = navigateur.new_page(viewport={"width": 1200, "height": 630})
    for gabarit, sortie in (("og.html", "og.png"), ("og-en.html", "og-en.png")):
        page.goto("file://" + os.path.join(ICI, gabarit), wait_until="networkidle")
        page.wait_for_timeout(600)
        page.screenshot(path=os.path.join(ASSETS, sortie))
        print("assets/" + sortie + " régénérée")
    navigateur.close()
