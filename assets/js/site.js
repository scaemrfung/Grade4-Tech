(function () {
  "use strict";

  var PREFIX = "g4tech-v1";
  var STAMPS = PREFIX + "-stamps";
  var CURRENT = PREFIX + "-current";
  var VIEW = PREFIX + "-view";

  function readJSON(key, fallback) {
    try {
      var raw = localStorage.getItem(key);
      return raw ? JSON.parse(raw) : fallback;
    } catch (err) {
      return fallback;
    }
  }

  function writeJSON(key, value) {
    localStorage.setItem(key, JSON.stringify(value));
  }

  function stamps() {
    return readJSON(STAMPS, {});
  }

  function setStamp(id, on) {
    var all = stamps();
    if (on) all[id] = true;
    else delete all[id];
    writeJSON(STAMPS, all);
    refreshStamps();
  }

  function refreshStamps() {
    var all = stamps();
    var count = Object.keys(all).length;
    document.querySelectorAll("[data-stamp-count]").forEach(function (el) {
      el.textContent = count + " of 18 stamped on this device";
    });
    document.querySelectorAll("[data-stamp]").forEach(function (btn) {
      var id = btn.getAttribute("data-stamp");
      var on = !!all[id];
      btn.setAttribute("aria-pressed", on ? "true" : "false");
      btn.textContent = on ? "Stamped on this device" : "Stamp this lesson";
    });
    document.querySelectorAll("[data-stamped]").forEach(function (el) {
      var on = !!all[el.getAttribute("data-stamped")];
      el.hidden = !on;
    });
  }

  function applyView(mode) {
    var student = mode === "student";
    document.body.classList.toggle("mode-student", student);
    document.body.classList.toggle("mode-teacher", !student);
    document.querySelectorAll("[data-view]").forEach(function (btn) {
      var active = (btn.getAttribute("data-view") === "student") === student;
      btn.setAttribute("aria-pressed", String(active));
      btn.classList.toggle("primary", active);
      btn.classList.toggle("ghost", !active);
    });
    var status = document.getElementById("view-status");
    if (status) {
      status.textContent = student
        ? "Student view. Teaching notes are hidden on this screen only. This is not a lock."
        : "Teacher view. Students can still open this public page.";
    }
  }

  function initView() {
    var params = new URLSearchParams(location.search);
    var query = params.get("view");
    var mode = query === "student" || query === "teacher" ? query : sessionStorage.getItem(VIEW) || "teacher";
    applyView(mode);
    document.querySelectorAll("[data-view]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var next = btn.getAttribute("data-view");
        sessionStorage.setItem(VIEW, next);
        applyView(next);
      });
    });
  }

  function initStamps() {
    document.querySelectorAll("[data-stamp]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var id = btn.getAttribute("data-stamp");
        setStamp(id, btn.getAttribute("aria-pressed") !== "true");
      });
    });
    var clear = document.getElementById("clear-device-data");
    if (clear) {
      clear.addEventListener("click", function () {
        localStorage.removeItem(STAMPS);
        localStorage.removeItem(CURRENT);
        Object.keys(localStorage).forEach(function (key) {
          if (key.indexOf(PREFIX + "-chalkie-") === 0) localStorage.removeItem(key);
        });
        refreshStamps();
        renderCurrent();
        document.querySelectorAll("[data-chalkie-url]").forEach(function (input) {
          input.value = "";
          updateChalkieLink(input);
        });
        var note = document.getElementById("clear-status");
        if (note) note.textContent = "Device-only stamps, current lesson, and Chalkie links were cleared.";
      });
    }
    refreshStamps();
  }

  function renderCurrent() {
    var id = localStorage.getItem(CURRENT) || "01";
    document.querySelectorAll("[data-current-lesson]").forEach(function (el) {
      var match = el.getAttribute("data-current-lesson") === id;
      el.hidden = !match;
    });
    var label = document.getElementById("current-label");
    var link = document.querySelector("[data-lesson-link='" + id + "']");
    if (label && link) {
      label.textContent = link.getAttribute("data-lesson-title") || "Lesson " + id;
      var go = document.getElementById("current-link");
      if (go) go.setAttribute("href", link.getAttribute("href"));
    }
  }

  function initCurrent() {
    document.querySelectorAll("[data-make-current]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        localStorage.setItem(CURRENT, btn.getAttribute("data-make-current"));
        renderCurrent();
        var status = document.getElementById("current-status");
        if (status) status.textContent = "Current lesson saved on this device.";
      });
    });
    renderCurrent();
  }

  function initFilters() {
    var search = document.getElementById("lesson-search");
    var unit = document.getElementById("unit-filter");
    var kind = document.getElementById("kind-filter");
    if (!search && !unit && !kind) return;
    var cards = Array.prototype.slice.call(document.querySelectorAll("[data-filter-card]"));
    var units = Array.prototype.slice.call(document.querySelectorAll("[data-filter-unit]"));
    function apply() {
      var q = (search && search.value || "").trim().toLowerCase();
      var u = unit ? unit.value : "all";
      var k = kind ? kind.value : "all";
      var shown = 0;
      cards.forEach(function (card) {
        var hay = (card.getAttribute("data-text") || "").toLowerCase();
        var ok = (!q || hay.indexOf(q) !== -1) &&
          (u === "all" || card.getAttribute("data-unit") === u) &&
          (k === "all" || card.getAttribute("data-kind") === k);
        card.hidden = !ok;
        if (ok) shown += 1;
      });
      units.forEach(function (block) {
        var visible = block.querySelectorAll("[data-filter-card]:not([hidden])").length;
        block.hidden = visible === 0;
      });
      var status = document.getElementById("filter-status");
      if (status) status.textContent = shown + (shown === 1 ? " lesson shown." : " lessons shown.");
    }
    [search, unit, kind].forEach(function (el) {
      if (el) el.addEventListener("input", apply);
    });
  }

  function chalkieKey(id) {
    return PREFIX + "-chalkie-" + id;
  }

  function updateChalkieLink(input) {
    var id = input.getAttribute("data-chalkie-url");
    var link = document.querySelector("[data-chalkie-open='" + id + "']");
    var msg = document.querySelector("[data-chalkie-msg='" + id + "']");
    var value = input.value.trim();
    if (!link || !msg) return;
    if (!value) {
      link.hidden = true;
      link.removeAttribute("href");
      msg.textContent = "No Chalkie share link has been added on this device.";
      return;
    }
    var ok = /^https:\/\/\S+$/i.test(value);
    if (!ok) {
      link.hidden = true;
      link.removeAttribute("href");
      msg.textContent = "That is not a full https link yet. Nothing was opened.";
      return;
    }
    link.hidden = false;
    link.href = value;
    msg.textContent = "Saved on this device only. Open it when you are ready.";
  }

  function initChalkie() {
    document.querySelectorAll("[data-copy-brief]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var id = btn.getAttribute("data-copy-brief");
        var node = document.getElementById("brief-" + id);
        var text = node ? node.innerText : "";
        var status = document.querySelector("[data-copy-status='" + id + "']");
        function done(ok) {
          if (status) status.textContent = ok ? "Brief copied." : "Select the brief and copy it manually.";
        }
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(text).then(function () { done(true); }, function () { done(false); });
        } else {
          done(false);
        }
      });
    });
    document.querySelectorAll("[data-chalkie-url]").forEach(function (input) {
      var id = input.getAttribute("data-chalkie-url");
      input.value = localStorage.getItem(chalkieKey(id)) || "";
      updateChalkieLink(input);
      input.addEventListener("change", function () {
        var value = input.value.trim();
        if (!value) localStorage.removeItem(chalkieKey(id));
        else localStorage.setItem(chalkieKey(id), value);
        updateChalkieLink(input);
      });
    });
  }

  function initPrint() {
    var btn = document.getElementById("print-student");
    if (!btn) return;
    btn.addEventListener("click", function () {
      document.body.classList.add("print-student");
      window.print();
      document.body.classList.remove("print-student");
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    initView();
    initStamps();
    initCurrent();
    initFilters();
    initChalkie();
    initPrint();
  });
})();
