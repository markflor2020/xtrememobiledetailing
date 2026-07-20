/* Xtreme Mobile Detailing — interactions */
(function () {
  "use strict";

  /* ---- current year ---- */
  var yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  /* ---- hero slideshow ---- */
  var heroSlideshow = document.getElementById("heroSlideshow");
  if (heroSlideshow) {
    var slides = heroSlideshow.querySelectorAll(".hero__slide");
    var dots = heroSlideshow.querySelectorAll(".hero__dot");
    var current = 0;
    var timer = null;

    var goTo = function (index) {
      slides[current].classList.remove("is-active");
      dots[current].classList.remove("is-active");
      current = index;
      slides[current].classList.add("is-active");
      dots[current].classList.add("is-active");
    };

    var next = function () { goTo((current + 1) % slides.length); };

    var start = function () {
      if (slides.length < 2) return;
      timer = setInterval(next, 5000);
    };
    var stop = function () { clearInterval(timer); };

    dots.forEach(function (dot, i) {
      dot.addEventListener("click", function () { goTo(i); stop(); start(); });
    });
    heroSlideshow.addEventListener("mouseenter", stop);
    heroSlideshow.addEventListener("mouseleave", start);

    if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) start();
  }

  /* ---- Google Analytics ---- */
  // Create a GA4 property at analytics.google.com, then paste its Measurement
  // ID (looks like "G-XXXXXXXXXX") below. Loads on every page once set — this
  // site is US-only (no EU/UK audience) and uses plain GA4 with no ad pixels,
  // so no cookie-consent gate is needed (see privacy.html). If Meta Pixel,
  // Google Ads conversion tracking, or remarketing ever get added, revisit
  // this — those count as "selling/sharing" data under CA/state privacy laws
  // and need an opt-out mechanism + updated policy.
  var GA_MEASUREMENT_ID = "";
  if (GA_MEASUREMENT_ID) {
    var s = document.createElement("script");
    s.async = true;
    s.src = "https://www.googletagmanager.com/gtag/js?id=" + GA_MEASUREMENT_ID;
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag("js", new Date());
    window.gtag("config", GA_MEASUREMENT_ID);
  }

  /* ---- header shrink on scroll ---- */
  var header = document.querySelector(".header");
  var onScroll = function () {
    if (header) {
      if (window.scrollY > 24) header.classList.add("shrink");
      else header.classList.remove("shrink");
    }
  };
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ---- mobile drawer ---- */
  var burger = document.getElementById("burger");
  var drawer = document.getElementById("drawer");
  var toggleDrawer = function (open) {
    var isOpen = open === undefined ? !drawer.classList.contains("open") : open;
    drawer.classList.toggle("open", isOpen);
    drawer.setAttribute("aria-hidden", String(!isOpen));
    burger.setAttribute("aria-expanded", String(isOpen));
    document.body.style.overflow = isOpen ? "hidden" : "";
  };
  if (burger) burger.addEventListener("click", function () { toggleDrawer(); });
  if (drawer) {
    drawer.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () { toggleDrawer(false); });
    });
  }
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") toggleDrawer(false);
  });

  /* ---- scroll reveal ---- */
  var reveals = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("in");
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -8% 0px" });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("in"); });
  }

  /* ---- quote form: email Xtreme (Web3Forms) + pre-filled text fallback ---- */
  // Get a FREE access key at https://web3forms.com (enter Xtreme's email —
  // submissions are emailed there). Paste it below to turn on email delivery.
  // Until then, the form falls back to opening a pre-filled text, so it
  // always works.
  var WEB3FORMS_KEY = "";
  var XTREME_PHONE = "+14023013243";

  var form = document.getElementById("qform");
  if (form) {
    var val = function (id) {
      var el = document.getElementById(id);
      return el ? el.value.trim() : "";
    };
    var fields = function () {
      return {
        name: val("f-name"), phone: val("f-phone"), vehicle: val("f-vehicle"),
        service: val("f-service"), notes: val("f-notes")
      };
    };
    var openText = function (f) {
      var lines = ["Hi Xtreme, I'd like a detailing quote."];
      if (f.name) lines.push("Name: " + f.name);
      if (f.phone) lines.push("Phone: " + f.phone);
      if (f.vehicle) lines.push("Vehicle: " + f.vehicle);
      if (f.service) lines.push("Service: " + f.service);
      if (f.notes) lines.push("Details: " + f.notes);
      var body = encodeURIComponent(lines.join("\n"));
      var ua = navigator.userAgent || "";
      var sep = /iPhone|iPad|Macintosh/i.test(ua) ? "&" : "?";
      window.location.href = "sms:" + XTREME_PHONE + sep + "body=" + body;
    };
    var showDone = function () {
      var done = document.getElementById("qformDone");
      if (done) { form.hidden = true; done.hidden = false; done.scrollIntoView({ block: "center" }); }
    };

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      // honeypot — bots fill this hidden field
      if (form.botcheck && form.botcheck.checked) return;
      var f = fields();

      // No key yet → just open a pre-filled text (works immediately).
      if (!WEB3FORMS_KEY || WEB3FORMS_KEY.indexOf("YOUR_") === 0) {
        openText(f);
        return;
      }

      var btn = form.querySelector('button[type="submit"]');
      var orig = btn ? btn.innerHTML : "";
      if (btn) { btn.disabled = true; btn.textContent = "Sending…"; }

      fetch("https://api.web3forms.com/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json", "Accept": "application/json" },
        body: JSON.stringify({
          access_key: WEB3FORMS_KEY,
          subject: "New quote request" + (f.name ? " — " + f.name : ""),
          from_name: "Xtreme Mobile Detailing website",
          name: f.name, phone: f.phone, vehicle: f.vehicle,
          service: f.service, message: f.notes
        })
      })
        .then(function (r) { return r.json(); })
        .then(function (data) {
          if (data && data.success) { showDone(); }
          else { openText(f); } // delivery failed → fall back to text
        })
        .catch(function () { openText(f); })
        .finally(function () { if (btn) { btn.disabled = false; btn.innerHTML = orig; } });
    });
  }
})();
