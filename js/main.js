(function () {
  "use strict";

  var body = document.body;
  var header = document.querySelector(".site-header");
  var toggle = document.querySelector(".menu-toggle");
  var menu = document.getElementById("mobile-menu");

  function setMenu(open) {
    body.classList.toggle("menu-open", open);
    if (toggle) {
      toggle.setAttribute("aria-expanded", String(open));
      toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    }
  }

  if (toggle && menu) {
    toggle.addEventListener("click", function () {
      setMenu(!body.classList.contains("menu-open"));
    });
    menu.addEventListener("click", function (e) {
      if (e.target.closest("a")) setMenu(false);
    });
    window.addEventListener("resize", function () {
      if (window.innerWidth > 1024) setMenu(false);
    });
  }

  document.querySelectorAll(".nav__item").forEach(function (item) {
    var btn = item.querySelector("button");
    if (!btn) return;
    btn.addEventListener("click", function () {
      var open = !item.classList.contains("is-open");
      item.classList.toggle("is-open", open);
      btn.setAttribute("aria-expanded", String(open));
    });
    document.addEventListener("click", function (e) {
      if (!item.contains(e.target)) {
        item.classList.remove("is-open");
        btn.setAttribute("aria-expanded", "false");
      }
    });
  });

  document.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    setMenu(false);
    document.querySelectorAll(".nav__item.is-open").forEach(function (item) {
      item.classList.remove("is-open");
      item.querySelector("button").setAttribute("aria-expanded", "false");
    });
  });

  if (header) {
    var onScroll = function () {
      header.classList.toggle("is-scrolled", window.scrollY > 8);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  document.querySelectorAll("[data-year]").forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });
})();
