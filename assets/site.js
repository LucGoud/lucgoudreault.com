/*
  lucgoudreault.com : script partagé, sans dépendance.
  1. Décale l'apparition des rangées du cartouche (le seul mouvement du site).
  2. Met l'année du pied de page à jour.
  3. Retient la langue choisie (sélecteur FR/EN), comme sur junior.coach.
  4. Page Contact : compose le courriel à partir du formulaire, en français ou en anglais.
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

  // 4. Formulaire de contact : ouvre le logiciel de courriel avec la demande rédigée
  var form = document.getElementById("demande");
  if (!form) return;
  var status = document.getElementById("demande-statut");
  var t = anglais ? {
    nom: "Name", courriel: "Email", entreprise: "Company", role: "Role", taille: "Size",
    type: "Looking for", echeance: "Timeline", enjeu: "The issue", vide: "not specified",
    defaut: "Request", ok: "Your email app is opening with the request written. All that is left is to send it."
  } : {
    nom: "Nom", courriel: "Courriel", entreprise: "Entreprise", role: "Rôle", taille: "Taille",
    type: "Offre visée", echeance: "Échéance", enjeu: "L'enjeu", vide: "non précisé",
    defaut: "Demande", ok: "Votre logiciel de courriel s'ouvre avec la demande rédigée. Il ne reste qu'à l'envoyer."
  };

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (!form.reportValidity()) return;

    var data = new FormData(form);
    var get = function (k) { return (data.get(k) || "").toString().trim(); };
    var type = get("type") || t.defaut;
    var entreprise = get("entreprise");

    var lignes = [
      t.nom + " : " + get("nom"),
      t.courriel + " : " + get("courriel"),
      t.entreprise + " : " + entreprise,
      t.role + " : " + (get("role") || t.vide),
      t.taille + " : " + (get("taille") || t.vide),
      t.type + " : " + type,
      t.echeance + " : " + (get("echeance") || t.vide),
      "",
      t.enjeu + " :",
      get("enjeu")
    ];
    if (anglais) lignes = lignes.map(function (l) { return l.replace(" : ", ": ").replace(/ :$/, ":"); });
    var sujet = type + (entreprise ? " (" + entreprise + ")" : "");
    window.location.href = "mailto:" + form.dataset.to +
      "?subject=" + encodeURIComponent(sujet) +
      "&body=" + encodeURIComponent(lignes.join("\n"));
    if (status) status.textContent = t.ok;
  });
})();
