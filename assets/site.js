/*
  lucgoudreault.com : script partagé, sans dépendance.
  1. Décale l'apparition des rangées du cartouche (le seul mouvement du site).
  2. Met l'année du pied de page à jour.
  3. Retient la langue choisie (sélecteur FR/EN), comme sur junior.coach.
  4. Page Contact : envoie la demande au point de réception (Google Apps Script) si
     data-endpoint est rempli, sinon ouvre le logiciel de courriel avec la demande rédigée.
*/
(function () {
  "use strict";

  var anglais = (document.documentElement.lang || "").slice(0, 2) === "en";

  // 1. Cartouche : chaque rangée reçoit son rang pour l'animation CSS
  document.querySelectorAll(".sheet-head .cartouche").forEach(function (c) {
    c.querySelectorAll(".cartouche-row, .cartouche-foot").forEach(function (row, i) {
      row.style.setProperty("--i", i);
    });
  });

  // 2. Année courante
  var year = String(new Date().getFullYear());
  document.querySelectorAll("[data-year]").forEach(function (el) { el.textContent = year; });

  // 3. Langue choisie : lue par l'aiguillage de la page racine et par les anciennes adresses
  document.querySelectorAll("[data-lang]").forEach(function (lien) {
    lien.addEventListener("click", function () {
      try { localStorage.setItem("lg_lang", lien.dataset.lang); } catch (e) {}
    });
  });

  // 4. Formulaire de contact
  var form = document.getElementById("demande");
  if (!form) return;
  var status = document.getElementById("demande-statut");
  var bouton = form.querySelector('button[type="submit"]');
  var endpoint = (form.dataset.endpoint || "").trim();

  var t = anglais ? {
    nom: "Name", courriel: "Email", entreprise: "Company", role: "Role", taille: "Employees",
    type: "Looking for", echeance: "Timeline", enjeu: "The issue", vide: "not specified",
    sep: ": ", defaut: "Request",
    mailto: "Your email app is opening with your request filled in. All that's left is to hit send.",
    envoi: "Sending…",
    ok: "Request sent. I will reply within 24 hours.",
    echec: "Sending failed. Your email app is opening with your request filled in instead."
  } : {
    nom: "Nom", courriel: "Courriel", entreprise: "Entreprise", role: "Rôle", taille: "Employés",
    type: "Offre visée", echeance: "Échéance", enjeu: "L'enjeu", vide: "à préciser",
    sep: " : ", defaut: "Demande",
    mailto: "Votre logiciel de courriel s'ouvre avec la demande rédigée. Il ne reste qu'à l'envoyer.",
    envoi: "Envoi en cours…",
    ok: "Demande envoyée. Je vous réponds dans les 24 heures.",
    echec: "L'envoi n'a pas fonctionné. Votre logiciel de courriel s'ouvre plutôt avec la demande rédigée."
  };

  // Avec un point de réception, le texte sous le bouton n'annonce plus le logiciel de courriel
  if (endpoint && status) status.textContent = "";

  function dire(texte) { if (status) status.textContent = texte; }

  function parCourriel(data) {
    var get = function (k) { return (data.get(k) || "").toString().trim(); };
    var type = get("type") || t.defaut;
    var entreprise = get("entreprise");
    var lignes = [
      t.nom + t.sep + get("nom"),
      t.courriel + t.sep + get("courriel"),
      t.entreprise + t.sep + entreprise,
      t.role + t.sep + (get("role") || t.vide),
      t.taille + t.sep + (get("taille") || t.vide),
      t.type + t.sep + type,
      t.echeance + t.sep + (get("echeance") || t.vide),
      "",
      t.enjeu + t.sep.trimEnd(),
      get("enjeu")
    ];
    var sujet = type + (entreprise ? " (" + entreprise + ")" : "");
    window.location.href = "mailto:" + form.dataset.to +
      "?subject=" + encodeURIComponent(sujet) +
      "&body=" + encodeURIComponent(lignes.join("\n"));
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (!form.reportValidity()) return;
    var data = new FormData(form);

    // Piège à robots : un humain ne voit pas ce champ
    if ((data.get("site_web") || "").toString().trim()) { form.reset(); dire(t.ok); return; }

    if (!endpoint) { parCourriel(data); dire(t.mailto); return; }

    data.append("langue", anglais ? "en" : "fr");
    if (bouton) bouton.disabled = true;
    dire(t.envoi);
    fetch(endpoint, { method: "POST", body: new URLSearchParams(data) })
      .then(function (r) { return r.json(); })
      .then(function (rep) {
        if (!rep || !rep.ok) throw new Error("refus");
        form.reset();
        dire(t.ok);
      })
      .catch(function () {
        parCourriel(data);
        dire(t.echec);
      })
      .then(function () { if (bouton) bouton.disabled = false; });
  });
})();
