"""Régénère assets/og.png (1200 x 630) à partir de scripts/og.html.

Usage : python3 scripts/og.py
Modifier le texte dans scripts/og.html, puis relancer. Demande Playwright et Chromium.
"""
import os
from playwright.sync_api import sync_playwright

ICI = os.path.dirname(os.path.abspath(__file__))
SORTIE = os.path.join(os.path.dirname(ICI), "assets", "og.png")

with sync_playwright() as p:
    navigateur = p.chromium.launch()
    page = navigateur.new_page(viewport={"width": 1200, "height": 630})
    page.goto("file://" + os.path.join(ICI, "og.html"), wait_until="networkidle")
    page.wait_for_timeout(600)
    page.screenshot(path=SORTIE)
    navigateur.close()
print("assets/og.png régénérée")
