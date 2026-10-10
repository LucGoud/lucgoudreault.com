/*
  Point de réception du formulaire de contact de lucgoudreault.com (Google Apps Script).

  À installer une seule fois, dans le Google Workspace de Luc (info@lucgoudreault.com) :
  1. Créer une feuille Google « Demandes lucgoudreault.com ».
  2. Extensions > Apps Script, coller ce fichier, enregistrer.
  3. Déployer > Nouveau déploiement > Application Web.
     Exécuter en tant que : moi. Qui a accès : tout le monde.
  4. Autoriser l'accès (Luc clique lui-même), copier l'URL de l'application Web.
  5. Coller cette URL dans data-endpoint du formulaire, dans fr/contact.html et en/contact.html.

  Chaque demande ajoute une ligne dans la feuille et envoie un avis à info@lucgoudreault.com,
  avec « Répondre » qui va directement au visiteur.
*/
var DESTINATAIRE = "info@lucgoudreault.com";
var CHAMPS = ["nom", "courriel", "entreprise", "role", "type", "taille", "echeance", "enjeu", "langue"];

function doPost(e) {
  var p = (e && e.parameter) || {};
  if (p.site_web) return reponse({ ok: true });                       // piège à robots
  if (!p.nom || !p.courriel || !p.enjeu) return reponse({ ok: false, erreur: "champs manquants" });
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(p.courriel)) return reponse({ ok: false, erreur: "courriel invalide" });

  var valeurs = CHAMPS.map(function (c) { return String(p[c] || "").slice(0, 5000); });
  var feuille = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
  if (feuille.getLastRow() === 0) feuille.appendRow(["Reçue le"].concat(CHAMPS));
  feuille.appendRow([new Date()].concat(valeurs));

  var lignes = CHAMPS.map(function (c, i) { return c + " : " + (valeurs[i] || "à préciser"); });
  MailApp.sendEmail({
    to: DESTINATAIRE,
    replyTo: p.courriel,
    subject: "Demande du site : " + (p.type || "contact") + (p.entreprise ? " (" + p.entreprise + ")" : ""),
    body: lignes.join("\n")
  });
  return reponse({ ok: true });
}

function reponse(objet) {
  return ContentService.createTextOutput(JSON.stringify(objet)).setMimeType(ContentService.MimeType.JSON);
}
