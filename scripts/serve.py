"""Aperçu local du site, comme GitHub Pages le sert.

Usage : python3 scripts/serve.py [port]   (port par défaut : 8000)

Reproduit les deux comportements de GitHub Pages qui comptent ici :
- /offres sert offres.html (adresses sans extension, comme sur le site en ligne);
- une adresse inconnue sert 404.html avec le code 404.
Les dossiers exclus de la publication (archive, scripts) restent accessibles en local.
"""
import http.server
import os
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Pages(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=RACINE, **kwargs)

    def send_head(self):
        chemin = self.path.split("?", 1)[0].split("#", 1)[0]
        local = self.translate_path(chemin)
        if not os.path.exists(local) and os.path.exists(local + ".html"):
            self.path = chemin + ".html"
        elif not os.path.exists(local):
            self.send_response(404)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            corps = open(os.path.join(RACINE, "404.html"), "rb").read()
            self.send_header("Content-Length", str(len(corps)))
            self.end_headers()
            return __import__("io").BytesIO(corps)
        return super().send_head()

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    print(f"Aperçu : http://localhost:{port}/")
    http.server.ThreadingHTTPServer(("127.0.0.1", port), Pages).serve_forever()
