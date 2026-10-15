"""Vérifications avant chaque push.

Usage :
  python3 scripts/verifier.py                     vérifications statiques et navigateur
  python3 scripts/verifier.py --publication       idem, et les notes « À confirmer » (.rev) deviennent bloquantes
  python3 scripts/verifier.py --captures DOSSIER  enregistre aussi les captures 375 px et 1440 px

Statique : title, meta description, canonical, og:image, hreflang (paires FR/EN), tiret cadratin,
expressions interdites, liens internes et ancres, images. Navigateur (Playwright + Chromium) :
erreurs console, ressources en échec, débordement horizontal à 375 px et à 1440 px.
Code de sortie 1 s'il y a au moins une erreur.
"""
import glob
import html.parser
import os
import re
import sys
import threading

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOMAINE = "https://www.lucgoudreault.com/"
EXCLUS_PUBLICATION = {"guide-de-style.html"}   # pages de travail, jamais publiées (voir _config.yml)
DOSSIERS_EXCLUS = ("archive", "scripts", "docs", ".git")   # docs : signatures courriel et documents de travail, jamais publiés
CADRATIN = chr(0x2014)

# Expressions interdites dans le texte visible et les métadonnées (minuscules)
INTERDITS = [
    "premier échange gratuit", "échange gratuit", "diagnostic gratuit", "rencontre gratuite",
    "offre de service", "accompagnement sur mesure", "synergie",
    "free consultation", "free call", "free discovery", "free intro",
    # Mandats passés retirés du site (décision du 2026-10-10). Innoptech reste permis :
    # Luc y est aviseur aujourd'hui (rôle actuel, dans le parcours).
    "machitech",
]
# Interdits dans les titres, l'accroche et les métadonnées seulement
INTERDITS_TITRES = ["consultant", "coach"]

erreurs, avertissements = [], []


def err(page, msg):
    erreurs.append(f"{page} : {msg}")


def avert(page, msg):
    avertissements.append(f"{page} : {msg}")


class Lecteur(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title, self.meta, self.links, self.imgs, self.ids = "", {}, [], [], set()
        self.canonical, self.revs, self.texte, self.titres = None, 0, [], []
        self.alternates, self.lang, self.refresh = {}, "", False
        self._pile, self._dans_title, self._ignore = [], False, 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.lang = a.get("lang", "")
        if a.get("id"):
            self.ids.add(a["id"])
        if tag == "title":
            self._dans_title = True
        if tag in ("script", "style"):
            self._ignore += 1
        if tag == "meta":
            cle = a.get("name") or a.get("property")
            if cle:
                self.meta[cle] = a.get("content", "")
            if (a.get("http-equiv") or "").lower() == "refresh":
                self.refresh = True
        if tag == "link" and a.get("rel") == "canonical":
            self.canonical = a.get("href")
        if tag == "link" and a.get("rel") == "alternate" and a.get("hreflang"):
            self.alternates[a["hreflang"]] = a.get("href", "")
        if tag == "a" and a.get("href") is not None:
            self.links.append(a["href"])
        if tag == "img":
            self.imgs.append(a)
        if "rev" in (a.get("class") or "").split():
            self.revs += 1
        self._pile.append((tag, a.get("class") or ""))

    def handle_endtag(self, tag):
        if tag == "title":
            self._dans_title = False
        if tag in ("script", "style"):
            self._ignore -= 1
        while self._pile:
            t, _ = self._pile.pop()
            if t == tag:
                break

    def handle_data(self, data):
        if self._dans_title:
            self.title += data
        if self._ignore:
            return
        self.texte.append(data)
        if any(t == "h1" or "kicker" in c.split() for t, c in self._pile):
            self.titres.append(data)


def pages_html():
    tout = glob.glob(os.path.join(RACINE, "**", "*.html"), recursive=True)
    return sorted(os.path.relpath(p, RACINE) for p in tout
                  if not os.path.relpath(p, RACINE).startswith(DOSSIERS_EXCLUS))


def lire(page):
    lecteur = Lecteur()
    lecteur.feed(open(os.path.join(RACINE, page), encoding="utf-8").read())
    return lecteur


def fichier_de(chemin):
    """Fichier servi pour un chemin relatif à la racine (comme GitHub Pages), ou None."""
    chemin = chemin.lstrip("/")
    if chemin in ("", "."):
        chemin = "index.html"
    elif chemin.endswith("/"):
        chemin += "index.html"
    for essai in (chemin, chemin + ".html", os.path.join(chemin, "index.html")):
        if os.path.isfile(os.path.join(RACINE, essai)):
            return os.path.normpath(essai)
    return None


def cible(page, href):
    """(fichier visé, ancre) pour un lien interne, None si externe, (None, ancre) si brisé."""
    if re.match(r"^(https?:|mailto:|tel:)", href):
        return None
    chemin, _, ancre = href.partition("#")
    chemin = chemin.split("?")[0]
    if chemin == "":
        return page, ancre
    if chemin.startswith("/"):
        base = chemin
    else:
        dossier = os.path.dirname(page)
        base = os.path.normpath(os.path.join(dossier, chemin)) + ("/" if chemin.endswith("/") or chemin in (".", "./") else "")
        if base.startswith(".."):
            return None, ancre
    return fichier_de(base), ancre


def statique(publication):
    pages = pages_html()
    lus = {p: lire(p) for p in pages}
    for page, l in lus.items():
        publiee = page not in EXCLUS_PUBLICATION
        redirection = l.refresh
        if not l.title.strip():
            err(page, "title manquant")
        desc = l.meta.get("description", "")
        if not desc:
            err(page, "meta description manquante")
        elif not 70 <= len(desc) <= 170:
            avert(page, f"meta description de {len(desc)} caractères (viser 70 à 170)")
        if publiee and page != "404.html" and not l.canonical:
            err(page, "canonical manquant")
        if publiee and page != "404.html" and not redirection and "og:image" not in l.meta:
            err(page, "og:image manquant")

        # Pages bilingues : paire hreflang complète, et la page d'en face existe
        if page.startswith(("fr" + os.sep, "en" + os.sep)):
            for code in ("fr-CA", "en", "x-default"):
                if code not in l.alternates:
                    err(page, f"hreflang « {code} » manquant")
            for code, url in l.alternates.items():
                if url.startswith(DOMAINE) and not fichier_de(url[len(DOMAINE):] or "/"):
                    err(page, f"hreflang « {code} » vers une page absente : {url}")
            attendu = "fr" if page.startswith("fr") else "en"
            if not l.lang.startswith(attendu):
                err(page, f"lang « {l.lang} » au lieu de {attendu}")
            if l.canonical and l.canonical.startswith(DOMAINE):
                if fichier_de(l.canonical[len(DOMAINE):] or "/") != os.path.normpath(page):
                    err(page, f"canonical ne pointe pas vers cette page : {l.canonical}")

        visible = " ".join(l.texte).lower()
        meta_txt = (l.title + " " + " ".join(l.meta.values())).lower()
        for mot in INTERDITS:
            if mot in visible or mot in meta_txt:
                err(page, f"expression interdite : « {mot} »")
        tete = (" ".join(l.titres) + " " + meta_txt).lower().replace("junior.coach", "")
        for mot in INTERDITS_TITRES:
            if re.search(rf"\b{mot}", tete):
                err(page, f"« {mot} » dans un titre, l'accroche ou les métadonnées")
        if l.lang.startswith("fr") and re.search(r"\b(tu|toi|ton|tes)\b", visible):
            avert(page, "possible tutoiement, à relire")

        for href in l.links:
            if page != "404.html" and href.startswith("/"):
                err(page, f"chemin absolu « {href} » (les chemins doivent être relatifs)")
            c = cible(page, href)
            if c is None:
                continue
            fichier, ancre = c
            if fichier is None:
                err(page, f"lien interne brisé : {href}")
            elif ancre and fichier in lus and ancre not in lus[fichier].ids:
                err(page, f"ancre introuvable : {href}")
        for img in l.imgs:
            src = img.get("src", "")
            if src.startswith("http"):
                continue
            chemin = src.lstrip("/") if src.startswith("/") else os.path.normpath(os.path.join(os.path.dirname(page), src))
            if not os.path.isfile(os.path.join(RACINE, chemin)):
                err(page, f"image introuvable : {src}")
            if "alt" not in img:
                err(page, f"image sans alt : {src}")

        if l.revs:
            (err if publication and publiee else avert)(page, f"{l.revs} note(s) « À confirmer » (.rev)")

    # Tiret cadratin : partout sauf l'archive, copiée telle quelle
    for chemin in glob.glob(os.path.join(RACINE, "**", "*"), recursive=True):
        rel = os.path.relpath(chemin, RACINE)
        if rel.startswith(("archive" + os.sep, ".git" + os.sep)) or not os.path.isfile(chemin):
            continue
        if os.path.splitext(chemin)[1] not in (".html", ".css", ".js", ".md", ".py", ".xml", ".txt", ".yml", ".svg"):
            continue
        n = open(chemin, encoding="utf-8", errors="ignore").read().count(CADRATIN)
        if n:
            err(rel, f"{n} tiret(s) cadratin")
    return pages, lus


def adresse(page):
    sans = page[:-5]
    if sans == "index":
        return ""
    if sans.endswith(os.sep + "index"):
        return sans[:-5].replace(os.sep, "/")
    return sans.replace(os.sep, "/")


def navigateur(pages, lus, captures):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        avert("navigateur", "Playwright absent : vérifications navigateur sautées")
        return
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import http.server
    from serve import Pages
    serveur = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Pages)
    port = serveur.server_address[1]
    threading.Thread(target=serveur.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{port}/"
    if captures:
        os.makedirs(captures, exist_ok=True)
    # Les pages de redirection et l'aiguillage de langue quittent la page : on les vérifie
    # seulement pour l'arrivée (pas d'erreur console), sans capture.
    with sync_playwright() as p:
        b = p.chromium.launch()
        for largeur, hauteur in ((375, 812), (1440, 900)):
            ctx = b.new_context(viewport={"width": largeur, "height": hauteur}, locale="fr-CA")
            for page in pages:
                url = base + adresse(page)
                pg = ctx.new_page()
                problemes = []
                pg.on("console", lambda m, pr=problemes: m.type == "error" and pr.append("console : " + m.text))
                pg.on("pageerror", lambda e, pr=problemes: pr.append("script : " + str(e)))
                pg.on("requestfailed", lambda r, pr=problemes: r.url.startswith(base) and pr.append("échec : " + r.url))
                pg.on("response", lambda r, pr=problemes: r.url.startswith(base) and r.status >= 400 and not r.url.endswith("/404") and pr.append(f"{r.status} : {r.url}"))
                pg.goto(url, wait_until="networkidle")
                pg.wait_for_timeout(300)
                if page == "404.html":
                    problemes[:] = [x for x in problemes if "404" not in x]
                for pb in problemes:
                    err(f"{page} @{largeur}", pb)
                deb = pg.evaluate("document.documentElement.scrollWidth - window.innerWidth")
                if deb > 1:
                    err(f"{page} @{largeur}", f"débordement horizontal de {deb} px")
                quitte = lus[page].refresh or page == "index.html"
                if captures and not quitte:
                    pg.wait_for_timeout(900)
                    nom = page[:-5].replace(os.sep, "-")
                    pg.screenshot(path=os.path.join(captures, f"{nom}-{largeur}.png"), full_page=True)
                pg.close()
            ctx.close()
        b.close()
    serveur.shutdown()


if __name__ == "__main__":
    args = sys.argv[1:]
    publication = "--publication" in args
    captures = args[args.index("--captures") + 1] if "--captures" in args else None
    pages, lus = statique(publication)
    navigateur(pages, lus, captures)
    for a in avertissements:
        print("  avertissement  " + a)
    for e in erreurs:
        print("  ERREUR         " + e)
    print(f"{len(pages)} pages, {len(erreurs)} erreur(s), {len(avertissements)} avertissement(s)")
    sys.exit(1 if erreurs else 0)
