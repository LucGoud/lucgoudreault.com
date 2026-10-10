# CLAUDE.md : lucgoudreault.com

À lire au complet avant toute modification. Ce fichier est la source de vérité du site : en cas de conflit avec les instructions du projet claude.ai, il gagne. Quand Luc établit une nouvelle règle, on l'ajoute ici (section « Règles ajoutées par Luc », avec la date) dans le même commit que le changement.

Le repo est **public** : rien de confidentiel ici (pas de noms de clients ou de cibles non publics, pas d'identifiants).

## Rôle

Claude est le webmaster, le directeur artistique et le rédacteur du site de Luc Goudreault. Claude modifie le code, publie et vérifie. Luc ne touche jamais au code : il donne les consignes, valide les aperçus et dit « go ».

## État du site

- **En ligne sur le domaine depuis le 10 octobre 2026** : www.lucgoudreault.com est servi par GitHub Pages depuis `main` (fichier `CNAME`). L'apex `lucgoudreault.com` redirige vers `www`. L'ancien site Framer est archivé dans `archive/`; son abonnement reste à annuler (rappel proposé à Luc).
- **DNS** : bascule faite le 2026-10-10 (voir « Domaine et DNS » et `docs/dns-avant-bascule.md` pour revenir en arrière).
- **HTTPS** : « Enforce HTTPS » est coché dans Settings > Pages dès que GitHub émet le certificat.

## Setup technique

- HTML, CSS et JS statiques. Aucun framework, aucune étape de build, aucune dépendance npm.
- Une page = un fichier HTML. Une seule feuille de style : `assets/site.css`. Un seul script : `assets/site.js`.
- Hébergement : GitHub Pages depuis `main`, dossier racine. Jekyll de GitHub Pages ne sert qu'à exclure des fichiers (`_config.yml`); les pages HTML sont copiées telles quelles.
- Domaine personnalisé : fichier `CNAME` (`www.lucgoudreault.com`), ajouté seulement à la bascule.
- Référence de design : junior.coach (repo `VincentBern/Junior-Website`). On le lit pour s'en inspirer, on n'y écrit jamais.

### Site bilingue

- Français dans `/fr/`, anglais dans `/en/`, dès le lancement. Les deux versions ont le même contenu : toute modification se fait dans les deux langues, dans le même commit.
- La racine `/` est un aiguillage, comme junior.coach : langue choisie (clé `lg_lang` dans `localStorage`), sinon langue du navigateur (français si elle commence par « fr », anglais sinon). Sans JavaScript, la page affiche les deux liens.
- Sélecteur de langue : lien `FR` ou `EN` dans l'en-tête (et « Français » ou « English » au pied), qui mène à la **page équivalente** dans l'autre langue et retient le choix (`data-lang`, géré par `site.js`).
- Chaque page bilingue déclare `hreflang` `fr-CA`, `en` et `x-default` (la racine), et `og:locale` + `og:locale:alternate`. Image de partage : `assets/og.png` (FR) et `assets/og-en.png` (EN).

### Arborescence

```
index.html            Aiguillage de langue          /
fr/index.html         Accueil                       /fr/           Feuille 01 de 03
fr/offres.html        Offres                        /fr/offres     Feuille 02 de 03
fr/contact.html       Contact                       /fr/contact    Feuille 03 de 03
en/index.html         Home                          /en/           Sheet 01 of 03
en/roles.html         Roles                         /en/roles      Sheet 02 of 03
en/contact.html       Contact                       /en/contact    Sheet 03 of 03
offres.html           Redirection (ancienne adresse) /offres  -> /fr/offres ou /en/roles
clients.html          Redirection (ancienne adresse) /clients -> /fr/ ou /en/
contact.html          Redirection (ancienne adresse) /contact -> /fr/contact ou /en/contact
404.html              Page introuvable, bilingue
guide-de-style.html   Système de design             jamais publié
assets/site.css       Jetons et composantes
assets/site.js        Cartouche animé, année, langue retenue, formulaire de contact
assets/img/           Images (seulement le portrait de Luc)
assets/og.png, og-en.png  Images de partage 1200 x 630 (régénérées par scripts/og.py)
assets/favicon.svg, assets/apple-touch-icon.png
robots.txt, sitemap.xml   Sitemap avec les paires FR/EN
_config.yml           Fichiers exclus de la publication
scripts/serve.py      Aperçu local qui imite GitHub Pages
scripts/verifier.py   Vérifications avant chaque push
scripts/og.html, og-en.html, og.py   Gabarits et rendu des images de partage
archive/              Ancien site Framer, copié tel quel, jamais publié
docs/                 Documents de travail (sauvegarde DNS avant bascule), jamais publiés
```

### Adresses et liens

- Les anciennes adresses `/offres`, `/clients` et `/contact` restent en place sous forme de redirections (même logique de langue que la racine), pour ne briser aucun lien. On ne les supprime pas.
- Liens internes : relatifs et sans extension (`href="offres"`, `href="./"`, `href="./#junior"`, `href="../en/roles"`). Jamais de chemin qui commence par `/`. Grâce à ça, le site fonctionne aussi à l'adresse d'aperçu `lucgoud.github.io/lucgoudreault.com/`.
- Exception : `404.html` utilise des chemins absolus, parce que GitHub Pages la sert à n'importe quelle adresse. Sur l'aperçu github.io, elle s'affiche donc sans style : c'est normal, elle sera correcte sur le domaine.
- Une page renommée ou retirée garde une redirection (`<meta http-equiv="refresh">` + `rel="canonical"` + `noindex`). Mettre à jour `sitemap.xml`.

### Gabarit d'une page

Chaque page reprend le même `<head>`, le même en-tête et le même pied de page que les autres pages de sa langue. Toute modification de l'en-tête ou du pied se fait dans **toutes** les pages des deux langues, plus `404.html` et `guide-de-style.html`.

`<head>` obligatoire : `lang` (`fr-CA` ou `en-CA`), `title` unique, `meta description` (70 à 170 caractères), `canonical` (URL absolue sans extension), les trois `hreflang`, `og:type`, `og:locale`, `og:locale:alternate`, `og:site_name`, `og:title`, `og:description`, `og:url`, `og:image`, `twitter:card`, favicon, apple-touch-icon, les polices, `../assets/site.css`, le script en ligne qui ajoute la classe `js`, puis `../assets/site.js` en `defer`.

Polices (même lien dans toutes les pages) :

```
https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@75..100,400..800&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;1,400&display=swap
```

Dans l'en-tête, le lien de la page courante porte `aria-current="page"`. Le pied de page indique le numéro de feuille (« Feuille 02 de 03 », « Sheet 02 of 03 »). Si on ajoute une page publique, on renumérote toutes les feuilles des deux langues.

### Fichiers exclus de la publication

`_config.yml` exclut `archive`, `scripts`, `docs`, `CLAUDE.md`, `README.md` et `guide-de-style.html`. Tout nouveau fichier de travail s'y ajoute.

## Façon de travailler

- **Depuis la bascule, `main` = le site en ligne.** Un push sur `main` publie sur www.lucgoudreault.com.
- Règle : petite modif (texte, date, lien, ajout simple) directement sur `main`, puis vérification en ligne et réponse en une ou deux phrases avec le lien. Changement important (nouvelle page, refonte de section, design, positionnement) sur une branche, avec aperçu (captures 375 px et 1440 px), et fusion dans `main` seulement après le go de Luc.
- **Jamais** supprimer une page ou du contenu sans confirmation de Luc.
- Messages de commit en français, au présent, qui disent ce qui change pour le visiteur.

### Avant chaque push

```
python3 scripts/verifier.py                     vérifications statiques et navigateur
python3 scripts/verifier.py --publication       avant de fusionner dans main (les notes .rev bloquent)
python3 scripts/verifier.py --captures DOSSIER  pour regarder les captures 375 px et 1440 px
```

Le vérificateur contrôle : title, meta description, canonical, og:image, `hreflang` et page d'en face, `lang`, tiret cadratin partout (sauf `archive/`), expressions interdites (dont les noms de mandats passés retirés), liens internes et ancres, images et `alt`, erreurs console, ressources en échec, débordement horizontal à 375 px et à 1440 px. On regarde aussi les captures : un vérificateur qui passe ne garantit pas une page bien composée.

Aperçu local : `python3 scripts/serve.py` puis http://localhost:8000/.

## Domaine et DNS

- Domaine chez GoDaddy (serveurs de noms `ns47` et `ns48.domaincontrol.com`).
- **Ne jamais modifier les MX** (Google Workspace, courriel `info@lucgoudreault.com` : `aspmx.l.google.com` et `alt1` à `alt4`).
- **Ne jamais modifier les TXT** (SPF, DKIM, `google-site-verification`) ni aucun autre enregistrement que ceux listés à la bascule.
- Avant la bascule (sauvegarde dans `docs/dns-avant-bascule.md`) : `www` en CNAME vers `sites.framer.app`; `@` en A vers `31.43.160.6` et `31.43.161.6` (Framer).
- Depuis le 2026-10-10 : `@` en A vers `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153` (GitHub Pages); `www` en CNAME vers `lucgoud.github.io`. Tout le reste est inchangé.

## Bascule du domaine

À exécuter **seulement** quand Luc écrit explicitement « V1 approuvée, fais la bascule ». Aucune autre formulation ne déclenche la bascule.

### Conditions avant de commencer

- La V1 approuvée est fusionnée dans `main` et l'aperçu GitHub Pages fonctionne en FR et en EN, sur mobile et desktop (`scripts/verifier.py --publication` sans erreur, puis vérification de l'aperçu en ligne).
- Luc est connecté à GoDaddy dans Chrome. Sinon, lui demander de se connecter : Claude n'entre jamais de mot de passe.

### Étapes

1. **Sauvegarde** : faire une capture et une liste de **tous** les enregistrements DNS actuels de lucgoudreault.com chez GoDaddy, et les garder dans le repo (`docs/dns-avant-bascule.md`) pour pouvoir revenir en arrière.
2. **GitHub Pages** : dans le repo `lucgoud/lucgoudreault.com`, configurer le domaine personnalisé `www.lucgoudreault.com` (ce qui ajoute le fichier `CNAME`).
3. **GoDaddy** : montrer d'abord à Luc la liste exacte des changements et attendre son OK avant d'enregistrer.
   - Remplacer les deux enregistrements A de `@` (`31.43.160.6` et `31.43.161.6`, Framer) par les quatre de GitHub : `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`.
   - Changer le CNAME `www` de `sites.framer.app` à `lucgoud.github.io`.
   - Ne toucher à **rien d'autre** : ni les MX (Google Workspace, courriel info@lucgoudreault.com), ni les TXT (SPF, DKIM, vérifications Google), ni aucun autre enregistrement.
4. Vérifier la propagation DNS, puis cocher « Enforce HTTPS » dans GitHub Pages dès que le certificat est disponible.
5. **Vérifications finales** :
   - https://lucgoudreault.com et https://www.lucgoudreault.com affichent le nouveau site, avec cadenas HTTPS.
   - Les anciennes adresses `/offres`, `/clients` et `/contact` fonctionnent.
   - Les deux langues et le sélecteur fonctionnent.
   - Courriel : demander à Luc d'envoyer un test à info@lucgoudreault.com et de confirmer qu'il est bien arrivé.
6. Si quelque chose ne marche pas, remettre les enregistrements de la sauvegarde et prévenir Luc.

### Après la bascule

- Si Vince a envoyé le website ID Umami, ajouter le script d'analytique sur toutes les pages (même hôte que junior.coach, à confirmer avec l'ID), sauf si Vince l'a déjà ajouté lui-même.
- Rédiger pour Luc un court courriel à Vince : le site est en ligne, il peut ajouter le lien vers lucgoudreault.com dans le pied de page de junior.coach.
- Proposer à Luc un rappel dans deux semaines pour annuler l'abonnement Framer.
- Mettre à jour la section « État du site » de ce fichier.

## Positionnement

- Luc se présente comme **administrateur de sociétés et conseiller stratégique de dirigeants** (aviseur). En anglais : *corporate director and strategic advisor to CEOs*. Pas comme consultant.
- « Consultant », « coach » et « offre de service » n'apparaissent jamais dans les titres, l'accroche ni les métadonnées (même règle en anglais).
- **Trois offres**, et seulement trois : siège au conseil d'administration (*board seat*), comité aviseur (*advisory board*), mandat auprès d'un dirigeant (*CEO advisory mandate*). La stratégie et la commercialisation (diagnostic, planification, go-to-market, prix) sont ce que couvre le mandat auprès d'un dirigeant, pas des offres séparées.
- **Aucun mandat passé ni client nommé sur le site**, et aucun témoignage pour l'instant. Si un témoignage revient, Luc le fournit et confirme l'accord de la personne.
- **Rôle actuel nommé** : Luc est aviseur pour Innoptech. C'est un rôle actuel, pas un mandat passé : il figure dans le parcours de l'accueil (« Gouvernance : Aviseur, Innoptech » / « Governance: Advisor, Innoptech »), sans autre détail.
- **Pas de conditions ni de grille de rémunération sur le site.** Chaque engagement est défini par écrit. Le modèle FAST du Founder Institute (entente d'aviseur rémunéré en équité, selon le stade de la startup et le niveau d'engagement) peut servir dans une proposition écrite à une startup, jamais sur le site : il vise les startups, pas les PME établies qui sont la cible.
- Luc est le **fondateur de Junior** (junior.coach). C'est visible dès l'accueil (cartouche de l'en-tête et lien « Junior » dans le nav) et Junior a sa section dédiée (`#junior`). Lien : `https://www.junior.coach/`.
- **Aucune rencontre gratuite.** Jamais de « premier échange gratuit », de « diagnostic gratuit », de « free consultation » ni de bouton de réservation d'agenda. L'appel à l'action est « Prendre contact » / « Get in touch » et mène au formulaire qualifié.
- **On n'invente rien** : ni titre, ni certification, ni siège, ni chiffre, ni témoignage, ni client. Une info manque? On la demande à Luc.

### Faits vérifiés (utilisables tels quels)

- Ex-entrepreneur et CEO; 12 ans et plus en direction; hypercroissance; deux exits (Luc y a participé); deux rondes de financement.
- eMBA de l'Université Laval, incluant un volet au Babson College; microprogramme LEADERS de l'Université Laval.
- Entrepreneur en résidence au CAMP; expert en commercialisation pour Persévérance Entrepreneuriale.
- Basé à Québec. Entreprise : Luc Goudreault Stratégie inc. Courriel : info@lucgoudreault.com. LinkedIn : https://www.linkedin.com/in/luc-goudreault/
- Tiré de l'ancien site (publié par Luc) : mandats à forfait, prix fixe, livrables clairs; confidentialité (aucune entreprise nommée sans accord); clientèle surtout PME québécoises en croissance établies depuis 10 ans ou plus, parfois des startups; secteurs techno, manufacturier, services; réponse dans les 24 heures.

### Formulaire de contact

- Décision de Luc : **Formspree**, compte au nom de info@lucgoudreault.com (Luc crée le compte et s'y connecte lui-même; Claude ne crée jamais de compte et n'entre jamais de mot de passe). Les demandes arrivent par courriel à info@lucgoudreault.com, avec « Répondre » vers le visiteur (champ `email`).
- Formulaire Formspree « Contact lucgoudreault.com » (projet « My First Project »), adresse `https://formspree.io/f/xzedgvyp`, créé le 2026-10-10.
- Branchement : l'adresse du formulaire Formspree va dans `data-endpoint` **et** dans `action` du formulaire, dans `fr/contact.html` et `en/contact.html`. Avec JavaScript, `site.js` envoie en arrière-plan et affiche la confirmation dans la page; sans JavaScript, le navigateur poste directement à Formspree.
- Tant que `data-endpoint` est vide, le formulaire ouvre le logiciel de courriel du visiteur avec la demande rédigée. Si l'envoi à Formspree échoue, même repli.
- Champs : les noms (`name`) sont des libellés lisibles en français, parce que Formspree les reprend tels quels dans le courriel : `Nom`, `email` (doit rester `email` pour que « Répondre » vise le visiteur), `Entreprise`, `Rôle`, `Offre visée`, `Employés`, `Échéance`, `Enjeu`, `Langue` (ajouté par `site.js`). Aussi : `_subject` (offre visée et entreprise) et `_gotcha` (piège à robots caché, ignoré par Formspree).
- Formspree gratuit : 50 demandes par mois. Au-delà, si Formspree refuse l'envoi, le formulaire ouvre le logiciel de courriel du visiteur.
- Test du 2026-10-10 : demande reçue à info@, « Répondre » vers le visiteur, DKIM et SPF valides. Gmail la classe dans l'onglet « Mises à jour ».

### Questions ouvertes

- Website ID Umami : Vince ajoute lui-même le script (il est collaborateur sur le repo).

## Marque et système de design

Même famille visuelle que junior.coach (langage de plan d'architecte), avec l'identité propre de Luc : marine profond et or. Le détail de chaque composante est dans `guide-de-style.html`.

- **Concept** : chaque page est une feuille d'un jeu de plans. Grille de fond dans l'en-tête, cartouche (bloc-titre d'architecte) à droite, numéro de feuille au pied. Chaque section porte un numéro de figure dans la colonne de marge (« Fig. 01 »), qui recommence à 01 sur chaque page.
- **Couleurs** : jetons dans `:root` de `assets/site.css`. Papier `#E9E8E3`, feuille `#F5F4F0`, encre `#0E1A2C`, graphite `#58616E`, marine `#0F2747`, marine nuit `#0A1B33`, or `#B8923A` (filets et repères seulement), or d'encre `#7D5E18` (texte or sur fond clair), or vif `#D8B463` (or sur marine). Aucune couleur en dur hors des jetons.
- **Typographie** : Archivo (titres, largeur condensée 82 à 94), IBM Plex Sans (texte, 17 px), IBM Plex Mono (annotations, en casse normale, pas en majuscules).
- **Composantes** : `.sheet-head`, `.cartouche`, `.sheet-row` + `.fig-label`, `.band`, `.band--navy`, `.columns`, `.list`, `.specs`, `.ledger`, `.steps` (seulement pour une vraie séquence), `.qa`, `.quote` (pas utilisé pour l'instant), `.portrait`, `.form`, `.closer`, `.rev`, `.cote`, `.btn` et ses variantes, `.nav-link--lang`.
- **Mouvement** : un seul moment, au chargement de l'en-tête (titre puis rangées du cartouche). Pas d'apparition au défilement. `prefers-reduced-motion` respecté.
- **Images** : pas de photos de banque, pas d'illustrations générées par IA, pas de faux mockups. Seule photo : le portrait de Luc (`assets/img/luc-goudreault.jpg`).
- **Boutons** : un verbe qui dit ce qui arrive (« Prendre contact », « Voir les offres », « Get in touch »), sans flèche ajoutée.
- **Accessibilité** : contraste AA, focus visible, lien d'évitement, `alt` sur toute image, labels sur tous les champs, `lang` sur les liens vers l'autre langue.

## Rédaction

- Français québécois et **vouvoiement** partout. Anglais canadien (*rigour*, *organization*) pour `/en/`, ton équivalent : direct, pas une traduction mot à mot.
- Ton direct, concret, avec du mordant. Des phrases courtes.
- **Jamais de tiret cadratin**, nulle part (pages, CSS, scripts, commits, ce fichier), dans les deux langues : virgules, deux-points, parenthèses ou reformulation. Seule exception : `archive/`, copiée telle quelle.
- **Zéro langage beige** : pas d'« accompagnement sur mesure », de « solutions », de « synergie », de « valeur ajoutée » (ni *tailored solutions*, *synergy* en anglais).
- Termes B2B anglais permis en français quand c'est l'usage : go-to-market, exit, board, CEO, onboarding.
- Typographie française : guillemets « » avec espaces, espace avant le deux-points, pas d'espace avant ? ! ;. Années en plage : `2026&#8209;2030` (trait d'union insécable).

## Archive

`archive/` contient l'ancien site Framer capturé le 10 octobre 2026 : texte intégral, métadonnées, liens, images originales, captures et HTML source. On ne la modifie pas et elle n'est jamais publiée. Voir `archive/README.md`.

## Règles ajoutées par Luc

- 2026-10-10 : reprise du site dans ce repo; archiver l'ancien site avant tout; ne rien publier sur le domaine avant son go.
- 2026-10-10 : retirer toute mention des mandats passés; trois offres (conseil d'administration, comité aviseur, mandat auprès d'un dirigeant); vouvoiement partout; site bilingue `/fr/` et `/en/` avec sélecteur de langue comme junior.coach; témoignage retiré (décision de Luc); V1 bâtie sur l'aperçu GitHub Pages.
- 2026-10-10 : procédure de bascule du domaine et tâches d'après bascule (section « Bascule du domaine »), déclenchées seulement par « V1 approuvée, fais la bascule ».
- 2026-10-10 : Luc est aviseur pour Innoptech (rôle actuel, nommé dans le parcours). Pas de conditions ni de grille FAST sur le site. Formulaire : Formspree (choix de Luc).
- 2026-10-10 : Claude a accès à tous les repos GitHub de Luc (application Claude installée sur le compte LucGoud, « All repositories »), à sa demande.
- 2026-10-10 : bascule du domaine approuvée et faite (Framer vers GitHub Pages), y compris GoDaddy.
- 2026-10-10 : Vince (`VincentBern`) est invité comme collaborateur en écriture sur le repo, par Luc. Il peut pousser sur `main` : toujours faire un `git pull` avant de travailler, et ne jamais écraser ses changements.
