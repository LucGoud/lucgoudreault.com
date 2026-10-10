# CLAUDE.md : lucgoudreault.com

À lire au complet avant toute modification. Ce fichier est la source de vérité du site : en cas de conflit avec les instructions du projet claude.ai, il gagne. Quand Luc établit une nouvelle règle, on l'ajoute ici (section « Règles ajoutées par Luc », avec la date) dans le même commit que le changement.

## Rôle

Claude est le webmaster, le directeur artistique et le rédacteur du site de Luc Goudreault. Claude modifie le code, publie et vérifie. Luc ne touche jamais au code : il donne les consignes, valide les aperçus et dit « go ».

## État du site

- **En ligne aujourd'hui** : l'ancien site Framer (`www` pointe vers `sites.framer.app`). Son contenu est archivé dans `archive/`.
- **Dans ce repo** : la refonte, sur la branche `refonte/fondations`. Rien n'est publié tant que Luc n'a pas donné son go et que la bascule DNS (plus bas) n'est pas faite.
- **Notes « À confirmer »** : les informations manquantes sont marquées dans les pages par un bloc `.rev`. Il n'en reste aucun au moment de fusionner dans `main` (le vérificateur bloque).

## Setup technique

- HTML, CSS et JS statiques. Aucun framework, aucune étape de build, aucune dépendance npm.
- Une page = un fichier HTML à la racine. Une seule feuille de style : `assets/site.css`. Un seul script : `assets/site.js`.
- Hébergement : GitHub Pages depuis la branche `main`, dossier racine. Un push sur `main` publie le site (une fois la bascule faite).
- Domaine personnalisé : fichier `CNAME` contenant `www.lucgoudreault.com`. Il n'est pas encore dans le repo : on l'ajoute à la bascule.
- Référence de design : junior.coach (repo `VincentBern/Junior-Website`). On le lit pour s'en inspirer, on n'y écrit jamais.

### Arborescence

```
index.html            Accueil              /            Feuille 01
offres.html           Mandats              /offres      Feuille 02
clients.html          Clients              /clients     Feuille 03
contact.html          Contact              /contact     Feuille 04
404.html              Page introuvable     (toute adresse inconnue)
guide-de-style.html   Système de design    jamais publié
assets/site.css       Jetons et composantes
assets/site.js        Cartouche animé, année, formulaire de contact
assets/img/           Images (seulement le portrait de Luc)
assets/og.png         Image de partage 1200 x 630 (régénérée par scripts/og.py)
assets/favicon.svg, assets/apple-touch-icon.png
robots.txt, sitemap.xml
_config.yml           Fichiers exclus de la publication
scripts/serve.py      Aperçu local qui imite GitHub Pages
scripts/verifier.py   Vérifications avant chaque push
scripts/og.html, og.py  Gabarit et rendu de l'image de partage
archive/              Ancien site Framer, copié tel quel, jamais publié
```

### Adresses et liens

- Les URL existantes sont conservées : `/`, `/offres`, `/clients`, `/contact`. GitHub Pages sert `offres.html` à l'adresse `/offres`.
- Liens internes : relatifs et sans extension (`href="offres"`, `href="./"` pour l'accueil, `href="./#junior"` depuis une autre page). Jamais de chemin qui commence par `/`.
- Exception : `404.html` utilise des chemins absolus (`/assets/site.css`, `/offres`), parce que GitHub Pages la sert à n'importe quelle adresse.
- Une page renommée ou retirée garde une redirection (petite page HTML avec `<meta http-equiv="refresh">` et `rel="canonical"`) pour ne briser aucun lien. Mettre à jour `sitemap.xml`.
- Le nav affiche « Mandats » pour l'adresse `/offres` : on garde l'adresse, pas le mot « offres ».

### Gabarit d'une page

Chaque page reprend le même `<head>`, le même en-tête et le même pied de page. Toute modification de l'en-tête ou du pied se fait dans **toutes** les pages (index, offres, clients, contact, 404, guide-de-style).

`<head>` obligatoire : `lang="fr-CA"`, `title` unique, `meta description` (70 à 170 caractères), `link rel="canonical"` (URL absolue sans extension), `og:type`, `og:locale` (`fr_CA`), `og:site_name`, `og:title`, `og:description`, `og:url`, `og:image` (`https://www.lucgoudreault.com/assets/og.png`), `twitter:card`, favicon, apple-touch-icon, les polices, `assets/site.css`, le script en ligne qui ajoute la classe `js`, puis `assets/site.js` en `defer`.

Polices (même lien dans toutes les pages) :

```
https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@75..100,400..800&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;1,400&display=swap
```

Dans l'en-tête, le lien de la page courante porte `aria-current="page"`. Le pied de page indique le numéro de feuille de la page (« Feuille 02 de 04 »). Si on ajoute une page publique, on renumérote toutes les feuilles.

### Fichiers exclus de la publication

`_config.yml` exclut `archive`, `scripts`, `CLAUDE.md`, `README.md` et `guide-de-style.html`. Tout nouveau fichier de travail s'y ajoute.

## Façon de travailler

- **Petite modif** (texte, date, lien, ajout simple) : faire la modif sur `main`, lancer le vérificateur, commit avec un message clair en français, push, vérifier la page en ligne, puis répondre à Luc en une ou deux phrases avec le lien.
- **Changement important** (nouvelle page, refonte de section, design, positionnement) : travailler sur une branche, montrer un aperçu (captures 375 px et 1440 px, ou page d'aperçu), attendre le go de Luc avant de fusionner dans `main`.
- **Jamais** supprimer une page ou du contenu sans confirmation de Luc.
- Messages de commit en français, au présent, qui disent ce qui change pour le visiteur (« Ajouter la fiche Machitech », pas « update clients.html »).

### Avant chaque push

```
python3 scripts/verifier.py                     sur une branche
python3 scripts/verifier.py --publication       avant de fusionner dans main
python3 scripts/verifier.py --captures DOSSIER  pour regarder les captures
```

Le vérificateur contrôle : title, meta description, canonical, og:image, tiret cadratin partout (sauf `archive/`), expressions interdites, liens internes et ancres, images et `alt`, erreurs console, ressources en échec, débordement horizontal à 375 px et à 1440 px. Avec `--publication`, toute note `.rev` est une erreur. On regarde aussi les captures : un vérificateur qui passe ne garantit pas une page bien composée.

Aperçu local : `python3 scripts/serve.py` puis http://localhost:8000/.

## Domaine et DNS

- Domaine chez GoDaddy (serveurs de noms `ns47` et `ns48.domaincontrol.com`).
- **Ne jamais modifier les enregistrements MX** (Google Workspace, courriel `info@lucgoudreault.com` : `aspmx.l.google.com` et `alt1` à `alt4`).
- **Ne jamais modifier les TXT `google-site-verification`.**
- État relevé le 10 octobre 2026 : `www` en CNAME vers `sites.framer.app`; apex en A vers `31.43.160.6` et `31.43.161.6` (Framer).

### Bascule de Framer vers GitHub Pages (une seule fois, avec le go de Luc)

1. Fusionner la branche de refonte dans `main` (vérificateur `--publication` sans erreur).
2. Ajouter le fichier `CNAME` (`www.lucgoudreault.com`) sur `main`.
3. Dans GitHub, Settings > Pages : source `main`, dossier `/ (root)`, domaine `www.lucgoudreault.com`.
4. Chez GoDaddy, changer **seulement** : le CNAME `www` vers `lucgoud.github.io`, et les A de l'apex vers `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`. Rien d'autre.
5. Attendre le certificat, puis cocher « Enforce HTTPS » dans Settings > Pages.
6. Vérifier les quatre adresses en ligne, l'apex qui redirige vers `www`, et un courriel test vers `info@lucgoudreault.com`.
7. Ensuite seulement, dépublier le site Framer.

## Positionnement

- Luc se présente comme **administrateur de sociétés et conseiller stratégique de dirigeants** (aviseur). Pas comme consultant.
- « Consultant », « coach » et « offre de service » n'apparaissent jamais dans les titres, l'accroche ni les métadonnées.
- Luc est le **fondateur de Junior** (junior.coach). C'est visible dès l'accueil (cartouche de l'en-tête et lien dans le nav) et Junior a sa section dédiée (`#junior`, Fig. 03 de l'accueil). Lien : `https://www.junior.coach/`.
- **Aucune rencontre gratuite.** Jamais de « premier échange gratuit », de « diagnostic gratuit » ni de bouton de réservation d'agenda. L'appel à l'action est « Prendre contact » et mène au formulaire qualifié de `/contact`.
- **On n'invente rien** : ni titre, ni certification, ni siège, ni chiffre, ni témoignage, ni client. Une info manque? On la demande à Luc et on met un bloc `.rev` en attendant.

### Faits vérifiés (utilisables tels quels)

- Ex-entrepreneur et CEO; 12 ans et plus en direction; hypercroissance; deux exits (Luc y a participé); deux rondes de financement.
- eMBA de l'Université Laval, incluant un volet au Babson College; microprogramme LEADERS de l'Université Laval.
- Entrepreneur en résidence au CAMP; expert en commercialisation pour Persévérance Entrepreneuriale.
- Basé à Québec. Entreprise : Luc Goudreault Stratégie inc. Courriel : info@lucgoudreault.com. LinkedIn : https://www.linkedin.com/in/luc-goudreault/
- Tiré de l'ancien site (publié par Luc) : mandats à forfait, prix fixe, livrables clairs; confidentialité (aucun client nommé sans accord); clientèle surtout PME québécoises en croissance établies depuis 10 ans ou plus, parfois des startups; secteurs techno, manufacturier, services; réponse dans les 24 heures.
- Mandats et témoignages de l'ancien site : Machitech (planification stratégique 2026-2030, témoignage de Terry Savoie), Innoptech (fondations opérationnelles, deux témoignages de Jean-Christophe Ruel), une PME confidentielle (structuration pour exit). Témoignages reproduits mot pour mot.

### À confirmer avec Luc (blocs `.rev` en place)

- Conseils d'administration et comités consultatifs à nommer; entreprises derrière les exits, si on peut les nommer.
- Formats « Au conseil » et « Aux côtés du dirigeant » : cadence, durée, engagement.
- Liste des mandats présentés sur `/clients` et accord de chaque client.
- Service d'envoi du formulaire de contact (aujourd'hui : il ouvre le logiciel de courriel du visiteur, sans service tiers).

## Marque et système de design

Même famille visuelle que junior.coach (langage de plan d'architecte), avec l'identité propre de Luc : marine profond et or. Le détail de chaque composante est dans `guide-de-style.html`.

- **Concept** : chaque page est une feuille d'un jeu de plans. Grille de fond dans l'en-tête, cartouche (bloc-titre d'architecte) à droite, numéro de feuille au pied. Chaque section porte un numéro de figure dans la colonne de marge (« Fig. 01 »), qui recommence à 01 sur chaque page.
- **Couleurs** : jetons dans `:root` de `assets/site.css`. Papier `#E9E8E3`, feuille `#F5F4F0`, encre `#0E1A2C`, graphite `#58616E`, marine `#0F2747`, marine nuit `#0A1B33`, or `#B8923A` (filets et repères seulement), or d'encre `#7D5E18` (texte or sur fond clair), or vif `#D8B463` (or sur marine). Aucune couleur en dur hors des jetons.
- **Typographie** : Archivo (titres, largeur condensée 82 à 94), IBM Plex Sans (texte, 17 px), IBM Plex Mono (annotations, en casse normale, pas en majuscules).
- **Composantes** : `.sheet-head`, `.cartouche`, `.sheet-row` + `.fig-label`, `.band`, `.band--navy`, `.columns`, `.list`, `.specs`, `.ledger`, `.steps` (seulement pour une vraie séquence), `.qa`, `.case`, `.quote`, `.portrait`, `.form`, `.closer`, `.rev`, `.cote`, `.btn` et ses variantes.
- **Mouvement** : un seul moment, au chargement de l'en-tête (titre puis rangées du cartouche). Pas d'apparition au défilement. `prefers-reduced-motion` respecté.
- **Images** : pas de photos de banque, pas d'illustrations générées par IA, pas de faux mockups. Seule photo : le portrait de Luc (`assets/img/luc-goudreault.jpg`). Les clients sont nommés en texte dans un cartouche, sans logo.
- **Boutons** : un verbe qui dit ce qui arrive (« Prendre contact », « Voir les mandats »), sans flèche ajoutée.
- **Accessibilité** : contraste AA, focus visible, lien d'évitement, `alt` sur toute image, labels sur tous les champs.

## Rédaction

- Français québécois, **vouvoiement** partout sur le site.
- Ton direct, concret, avec du mordant. Des phrases courtes.
- **Jamais de tiret cadratin**, nulle part (pages, CSS, scripts, commits, ce fichier) : virgules, deux-points, parenthèses ou reformulation. Seule exception : `archive/`, copiée telle quelle.
- **Zéro langage beige** : pas d'« accompagnement sur mesure », de « solutions », de « synergie », de « valeur ajoutée ».
- Termes B2B anglais permis quand c'est l'usage : go-to-market, exit, board, CEO, onboarding.
- Typographie : guillemets « » avec espaces, espace avant le deux-points, pas d'espace avant ? ! ;. Nombres : « 12+ », « 24 heures ». Années en plage : `2026&#8209;2030` (trait d'union insécable) pour éviter la coupure.

## Archive

`archive/` contient l'ancien site Framer capturé le 10 octobre 2026 : texte intégral, métadonnées, liens, images originales, captures et HTML source. On ne la modifie pas et elle n'est jamais publiée. Voir `archive/README.md`.

## Règles ajoutées par Luc

- 2026-10-10 : reprise du site dans ce repo; archiver l'ancien site avant tout; ne rien publier sur le domaine avant son go.
