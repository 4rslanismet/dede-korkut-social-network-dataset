(function () {
  "use strict";

  var NETWORK_DEFS = {
    G0_full: "All nodes and all relations, no filtering. See docs/network_models.md.",
    G1_person_only: "Only actors of node_type == 'kişi' on both endpoints.",
    G2_core_social: "All relations except the SEMANTIC family (identity/title/epithet).",
  };

  var cy = null;
  var currentNetwork = "G0_full";

  function setDefText(name) {
    var el = document.getElementById("network-def-text");
    if (el) el.textContent = NETWORK_DEFS[name] || "";
  }

  function safeFilename(nodeId) {
    // Mirrors src/build_site.py::safe_filename - a handful of node_ids are
    // pathologically long (concatenated multi-actor entries); truncate
    // deterministically so the link matches the generated page's filename.
    var maxlen = 60;
    if (nodeId.length <= maxlen) return nodeId;
    return nodeId.slice(0, maxlen) + "_" + nodeId.length;
  }

  function showNodeDetail(data) {
    var panel = document.getElementById("detail-panel");
    panel.innerHTML =
      '<strong>' + escapeHtml(data.label || data.id) + '</strong>' +
      field("Type", data.node_type) +
      field("Story count", data.story_count) +
      '<p style="margin-top:10px"><a href="characters/' + encodeURIComponent(safeFilename(data.id)) + '.html">Full character profile &rarr;</a></p>';
  }

  function showEdgeDetail(data) {
    var panel = document.getElementById("detail-panel");
    panel.innerHTML =
      '<strong>Relation</strong>' +
      field("Source", data.source) +
      field("Target", data.target) +
      field("Weight", data.weight) +
      field("Interaction count", data.interaction_count);
  }

  function field(k, v) {
    return '<div class="field"><span class="k">' + k + '</span><span class="v">' + escapeHtml(String(v == null ? "—" : v)) + '</span></div>';
  }

  function escapeHtml(s) {
    return s.replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function layoutOptions(name) {
    if (name === "concentric") {
      return {
        name: "concentric",
        concentric: function (node) { return node.degree(); },
        levelWidth: function () { return 2; },
        animate: false,
      };
    }
    if (name === "circle") return { name: "circle", animate: false };
    return { name: "cose", animate: false, nodeRepulsion: 8000, idealEdgeLength: 60 };
  }

  function loadNetwork(name) {
    currentNetwork = name;
    setDefText(name);
    fetch("data/networks/" + name + ".json")
      .then(function (r) { return r.json(); })
      .then(function (data) {
        if (cy) cy.destroy();
        cy = cytoscape({
          container: document.getElementById("cy"),
          elements: data.elements,
          style: [
            { selector: "node", style: {
                "background-color": "#7a4b2a",
                "label": "data(label)",
                "font-size": 7,
                "color": "#2a2622",
                "text-valign": "bottom",
                "text-margin-y": 3,
                "width": "mapData(degreeVal, 0, 40, 6, 34)",
                "height": "mapData(degreeVal, 0, 40, 6, 34)",
                "text-opacity": 0,
              } },
            { selector: "edge", style: {
                "width": 1,
                "line-color": "#ccc4b3",
                "curve-style": "haystack",
                "opacity": 0.6,
              } },
            { selector: ".highlighted", style: { "background-color": "#c0392b", "text-opacity": 1, "font-size": 9, "font-weight": "bold" } },
            { selector: ".dimmed", style: { "opacity": 0.12 } },
          ],
          layout: layoutOptions(document.getElementById("layout-select").value),
        });

        cy.nodes().forEach(function (n) { n.data("degreeVal", n.degree()); });
        // show labels for the top 15 nodes by degree so it doesn't turn into a hairball of text
        cy.nodes().sort(function (a, b) { return b.data("degreeVal") - a.data("degreeVal"); })
          .slice(0, 15).style("text-opacity", 1);

        // Cytoscape can initialize before the container has its final CSS size
        // (fit-to-container then locks onto a near-zero box). Force a resize +
        // fit once the layout has actually settled.
        cy.resize();
        cy.one("layoutstop", function () { cy.resize(); cy.fit(undefined, 30); });
        cy.fit(undefined, 30);

        cy.on("tap", "node", function (evt) { showNodeDetail(evt.target.data()); });
        cy.on("tap", "edge", function (evt) { showEdgeDetail(evt.target.data()); });
      })
      .catch(function (err) {
        document.getElementById("cy").innerHTML = "<p style='padding:20px;color:#8a3b32'>Could not load network data: " + err + "</p>";
      });
  }

  function applySearch(term) {
    if (!cy) return;
    cy.elements().removeClass("highlighted dimmed");
    if (!term) return;
    var lower = term.toLowerCase();
    var matched = cy.nodes().filter(function (n) {
      return (n.data("label") || "").toLowerCase().indexOf(lower) !== -1;
    });
    if (matched.length === 0) return;
    cy.elements().addClass("dimmed");
    matched.removeClass("dimmed").addClass("highlighted");
    cy.animate({ fit: { eles: matched, padding: 80 } }, { duration: 300 });
  }

  document.addEventListener("DOMContentLoaded", function () {
    loadNetwork(currentNetwork);

    document.getElementById("network-select").addEventListener("change", function (e) {
      loadNetwork(e.target.value);
    });
    document.getElementById("layout-select").addEventListener("change", function () {
      if (cy) cy.layout(layoutOptions(document.getElementById("layout-select").value)).run();
    });
    document.getElementById("search-box").addEventListener("input", function (e) {
      applySearch(e.target.value.trim());
    });
  });
})();
