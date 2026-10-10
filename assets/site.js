/*
  lucgoudreault.com : script partagé, sans dépendance.
  1. Décale l'apparition des rangées du cartouche (le seul mouvement du site).
  2. Met l'année du pied de page à jour.
  3. Page Contact : compose le courriel à partir du formulaire.
*/
(function () {
  "use strict";

  // 1. Cartouche : chaque rangée reçoit son rang pour l'animation CSS
  document.querySelectorAll(".sheet-head .cartouche").forEach(function (c) {
    c.querySelectorAll(".cartouche-row, .cartouche-foot").forEach(function (row, i) {
      row.style.setProperty("--i", i);
    });
  });

  // 2. Année courante
  var year = String(new Date().getFullYear());
  document.querySelectorAll("[data-year]").forEach(function (el) { el.textContent = year; });

  // 3. Formulaire de contact : ouvre le logiciel de courriel avec la demande rédigée
  var form = document.getElementById("demande");
  if (!form) return;
  var status = document.getElementById("demande-statut");

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (!form.reportValidity()) return;

    var data = new FormData(form);
    var get = function (k) { return (data.get(k) || "").toString().trim(); };
    var type = get("type") || "Demande";
    var entreprise = get("entreprise");

    var lignes = [
      "Nom : " + get("nom"),
      "Courriel : " + get("courriel"),
      "Entreprise : " + entreprise,
      "Rôle : " + (get("role") || "non précisé"),
      "Taille : " + (get("taille") || "non précisée"),
      "Type de demande : " + type,
      "Échéance : " + (get("echeance") || "non précisée"),
      "",
      "L'enjeu :",
      get("enjeu")
    ];
    var sujet = type + (entreprise ? " (" + entreprise + ")" : "");
    var href = "mailto:" + form.dataset.to +
      "?subject=" + encodeURIComponent(sujet) +
      "&body=" + encodeURIComponent(lignes.join("\n"));

    window.location.href = href;
    if (status) {
      status.textContent = "Votre logiciel de courriel s'ouvre avec la demande rédigée. Il ne reste qu'à l'envoyer.";
    }
  });
})();
