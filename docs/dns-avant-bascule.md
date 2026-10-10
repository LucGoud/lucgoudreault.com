# DNS de lucgoudreault.com avant la bascule

Sauvegarde faite le 10 octobre 2026 à 12 h 32 (heure de Québec), dans GoDaddy (Domain Portfolio, lucgoudreault.com, DNS, DNS Records), juste avant la bascule de Framer vers GitHub Pages. Elle sert à revenir en arrière si quelque chose ne marche pas.

Captures : `dns-avant-bascule/godaddy-page-1.jpg` (enregistrements 1 à 10), `dns-avant-bascule/godaddy-page-2.jpg` et `dns-avant-bascule/godaddy-page-2-fin.jpg` (enregistrements 11 à 18).

Serveurs de noms : `ns47.domaincontrol.com` et `ns48.domaincontrol.com` (GoDaddy).

## Les 18 enregistrements

| # | Type | Nom | Valeur | TTL |
|---|---|---|---|---|
| 1 | A | @ | 31.43.160.6 | 600 secondes |
| 2 | A | @ | 31.43.161.6 | 600 secondes |
| 3 | NS | @ | ns47.domaincontrol.com. | 1 heure |
| 4 | NS | @ | ns48.domaincontrol.com. | 1 heure |
| 5 | CNAME | ftp | lucgoudreault.com. | 1 heure |
| 6 | CNAME | www | sites.framer.app. | 1 heure |
| 7 | CNAME | _domainconnect | _domainconnect.gd.domaincontrol.com. | 1 heure |
| 8 | SOA | @ | Primary nameserver: ns47.domaincontrol.com. | 600 secondes |
| 9 | MX | @ | aspmx.l.google.com. (priorité 1) | 1 heure |
| 10 | MX | @ | alt3.aspmx.l.google.com. (priorité 10) | 1 heure |
| 11 | MX | @ | alt4.aspmx.l.google.com. (priorité 10) | 1 heure |
| 12 | MX | @ | alt1.aspmx.l.google.com. (priorité 5) | 1 heure |
| 13 | MX | @ | alt2.aspmx.l.google.com. (priorité 5) | 1 heure |
| 14 | TXT | @ | google-site-verification=evCPGAjYHf37p7WWHMZhEOUwksCvhS0vEWFBLgK0IxY | 1 heure |
| 15 | TXT | @ | google-site-verification=XSC14_ArBCVPvlJPldD-TTlwCSpxqQYqPRguspLCepM | 1 heure |
| 16 | TXT | dc-aa8e722993._spfm | v=spf1 include:_spf.google.com ~all | 1 heure |
| 17 | TXT | google._domainkey | v=DKIM1; k=rsa; p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAtoKetDvFDcIJh496vA/r9oOZDD/zPUPOsu8BxX9LssE6EcjmCwF2ckjJN/NKcuydMOozFI9BYQ5QfFzFbJ+nYvGZoMF5JgLGeKKIRVYGckPt274WXLnYtdMtpLE62IcRWe22I506EUYO/RJ5ZBOjnoi8BIfAXare1ln6nUEGhlql6glWsQIpx1llGhKjZa3J9lQAjTTfGZ88Qcj3F0nHA4TUZZKaqdb5AcqUA6hg9GsFHM4Ey+3ceiUecY6dJlKVFDEK9r0YS8m4H2AG+ncbxI3om1hWaGgQRAnPTMdLgtkD2tYkqEs0bkiLDaAao4cH5v52LPll2Cr8x0eaeMhewwIDAQAB | 1 heure |
| 18 | TXT | _dmarc | v=DMARC1; p=quarantine; rua=mailto:postmaster@lucgoudreault.com; ruf=mailto:postmaster@lucgoudreault.com; fo=1 | 1 heure |

## Ce que la bascule change (et rien d'autre)

| Enregistrement | Avant | Après |
|---|---|---|
| A @ | 31.43.160.6 | 185.199.108.153 |
| A @ | 31.43.161.6 | 185.199.109.153 |
| A @ | (aucun) | 185.199.110.153 |
| A @ | (aucun) | 185.199.111.153 |
| CNAME www | sites.framer.app. | lucgoud.github.io. |

Les MX (9 à 13), les TXT (14 à 18), les NS, le SOA et les CNAME `ftp` et `_domainconnect` ne bougent pas.

## Retour en arrière

1. Dans GoDaddy, supprimer les quatre A de `@` vers 185.199.108.153 à 185.199.111.153.
2. Recréer les deux A de `@` : `31.43.160.6` et `31.43.161.6`, TTL 600 secondes.
3. Remettre le CNAME `www` à `sites.framer.app.`, TTL 1 heure.
4. Dans GitHub, Settings > Pages : retirer le domaine personnalisé (ce qui retire le fichier `CNAME` du repo).
5. Vérifier que www.lucgoudreault.com affiche de nouveau le site Framer, puis prévenir Luc.
