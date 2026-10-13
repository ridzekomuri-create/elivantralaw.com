document.addEventListener("DOMContentLoaded", function () {
  var header = document.querySelector(".site-header");
  var toggle = document.querySelector(".nav-toggle");
  var links = document.querySelector(".nav-links");

  if (location.hash) {
    var target = document.getElementById(location.hash.slice(1));
    if (target) {
      setTimeout(function () {
        target.scrollIntoView({ block: "start" });
      }, 50);
    }
  }

  window.addEventListener("scroll", function () {
    if (window.scrollY > 12) header.classList.add("is-scrolled");
    else header.classList.remove("is-scrolled");
  });

  if (toggle && links) {
    toggle.addEventListener("click", function () {
      links.classList.toggle("open");
    });
    links.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () { links.classList.remove("open"); });
    });
  }

  var homeLink = document.querySelector("[data-home-link]");
  if (homeLink) {
    homeLink.addEventListener("click", function (e) {
      if (location.pathname === homeLink.pathname) {
        e.preventDefault();
        window.scrollTo({ top: 0, behavior: "smooth" });
        if (location.hash) history.replaceState(null, "", location.pathname);
      }
    });
  }

  var revealEls = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.15 }
    );
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add("is-visible"); });
  }

  document.querySelectorAll("[data-cookie-reset]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      document.cookie = "cookie_consent=; Max-Age=0; path=/";
      location.reload();
    });
  });

  document.querySelectorAll("[data-cookie-choice]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var banner = document.getElementById("cookieBanner");
      fetch("/cookie-consent", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ choice: btn.dataset.cookieChoice }),
      }).then(function () {
        if (banner) banner.remove();
      });
    });
  });

  var topicSelect = document.getElementById("topic");
  var presetSlug = new URLSearchParams(location.search).get("service");
  if (topicSelect && presetSlug) {
    var match = topicSelect.querySelector('option[data-slug="' + presetSlug + '"]');
    if (match) topicSelect.value = match.value;
  }

  var form = document.getElementById("contactForm");
  if (form) {
    var statusEl = document.getElementById("formStatus");
    var btn = form.querySelector(".btn");
    var btnLabel = btn.querySelector("span:not([hidden])");
    var btnOriginal = btnLabel ? btnLabel.textContent : btn.textContent;

    var MESSAGES = {
      sending: { ru: "Отправка…", en: "Sending…" },
      sent: { ru: "Отправлено", en: "Sent" },
      success: { ru: "Спасибо! Мы свяжемся с вами в ближайшее время.", en: "Thank you! We'll get back to you shortly." },
      invalid: { ru: "Проверьте, пожалуйста, имя и email.", en: "Please check your name and email." },
      error: { ru: "Не удалось отправить. Напишите нам на elivantralaw@gmail.com.", en: "Couldn't send. Please email us at elivantralaw@gmail.com." },
    };

    function currentLang() {
      return document.documentElement.getAttribute("data-lang") === "en" ? "en" : "ru";
    }
    function setBtnLabel(text) {
      if (btnLabel) btnLabel.textContent = text;
      else btn.textContent = text;
    }
    function showStatus(kind, cls) {
      var lang = currentLang();
      statusEl.textContent = MESSAGES[kind][lang];
      statusEl.className = "form-status" + (cls ? " " + cls : "");
    }

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.checkValidity()) {
        showStatus("invalid", "is-error");
        return;
      }

      var lang = currentLang();
      var payload = {
        name: form.elements["name"].value.trim(),
        email: form.elements["email"].value.trim(),
        topic: form.elements["topic"].value,
        message: form.elements["message"].value.trim(),
      };

      btn.disabled = true;
      setBtnLabel(MESSAGES.sending[lang]);
      statusEl.className = "form-status";
      statusEl.textContent = "";

      fetch("/contact", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      })
        .then(function (res) { return res.json().then(function (data) { return { ok: res.ok, data: data }; }); })
        .then(function (result) {
          if (result.ok && result.data.ok) {
            setBtnLabel(MESSAGES.sent[lang]);
            showStatus("success", "is-success");
            form.reset();
          } else {
            setBtnLabel(btnOriginal);
            showStatus("error", "is-error");
          }
        })
        .catch(function () {
          setBtnLabel(btnOriginal);
          showStatus("error", "is-error");
        })
        .finally(function () {
          btn.disabled = false;
          setTimeout(function () { setBtnLabel(btnOriginal); }, 3200);
        });
    });
  }

  var reviewForm = document.getElementById("reviewForm");
  if (reviewForm) {
    var reviewStatus = document.getElementById("reviewStatus");
    var reviewBtn = reviewForm.querySelector(".btn");
    var reviewBtnLabel = reviewBtn.querySelector("span:not([hidden])");
    var reviewBtnOriginal = reviewBtnLabel ? reviewBtnLabel.textContent : reviewBtn.textContent;

    var REVIEW_MESSAGES = {
      sending: { ru: "Отправка…", en: "Sending…" },
      success: { ru: "Спасибо! Отзыв отправлен и появится на сайте после проверки.", en: "Thank you! Your review was sent and will appear on the site after a check." },
      invalid: { ru: "Заполните имя и отзыв (от 10 символов).", en: "Please fill in your name and a review (at least 10 characters)." },
      error: { ru: "Не удалось отправить. Попробуйте ещё раз или напишите нам на elivantralaw@gmail.com.", en: "Couldn't send. Please try again or email us at elivantralaw@gmail.com." },
    };

    function reviewLang() {
      return document.documentElement.getAttribute("data-lang") === "en" ? "en" : "ru";
    }
    function setReviewLabel(text) {
      if (reviewBtnLabel) reviewBtnLabel.textContent = text;
      else reviewBtn.textContent = text;
    }
    function showReviewStatus(kind, cls) {
      reviewStatus.textContent = REVIEW_MESSAGES[kind][reviewLang()];
      reviewStatus.className = "form-status" + (cls ? " " + cls : "");
    }

    reviewForm.addEventListener("submit", function (e) {
      e.preventDefault();
      var payload = {
        name: reviewForm.elements["name"].value.trim(),
        country: reviewForm.elements["country"].value.trim(),
        text: reviewForm.elements["text"].value.trim(),
        website: reviewForm.elements["website"].value,
      };
      if (payload.name.length < 2 || payload.text.length < 10) {
        showReviewStatus("invalid", "is-error");
        return;
      }

      reviewBtn.disabled = true;
      setReviewLabel(REVIEW_MESSAGES.sending[reviewLang()]);
      reviewStatus.className = "form-status";
      reviewStatus.textContent = "";

      fetch("/reviews", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      })
        .then(function (res) { return res.json().then(function (data) { return { ok: res.ok, data: data }; }); })
        .then(function (result) {
          if (result.ok && result.data.ok) {
            showReviewStatus("success", "is-success");
            reviewForm.reset();
          } else {
            showReviewStatus(result.data.error === "invalid_input" ? "invalid" : "error", "is-error");
          }
        })
        .catch(function () {
          showReviewStatus("error", "is-error");
        })
        .finally(function () {
          reviewBtn.disabled = false;
          setReviewLabel(reviewBtnOriginal);
        });
    });
  }

  /* ---------- language switch ---------- */
  function applyLang(lang) {
    document.documentElement.setAttribute("data-lang", lang === "en" ? "en" : "ru");
    document.querySelectorAll(".t-ru").forEach(function (el) { el.hidden = lang === "en"; });
    document.querySelectorAll(".t-en").forEach(function (el) { el.hidden = lang !== "en"; });
    document.querySelectorAll("[data-lang-btn]").forEach(function (btn) {
      btn.classList.toggle("is-active", btn.dataset.langBtn === lang);
    });
    try { localStorage.setItem("elivantra-lang", lang); } catch (e) {}
  }

  var initialLang = document.documentElement.getAttribute("data-lang") === "en" ? "en" : "ru";
  applyLang(initialLang);

  document.querySelectorAll("[data-lang-btn]").forEach(function (btn) {
    btn.addEventListener("click", function () { applyLang(btn.dataset.langBtn); });
  });

  /* ---------- theme switch ---------- */
  var themeToggle = document.getElementById("themeToggle");
  if (themeToggle) {
    themeToggle.addEventListener("click", function () {
      var isDark = document.documentElement.getAttribute("data-theme") === "dark";
      var next = isDark ? "light" : "dark";
      if (next === "dark") document.documentElement.setAttribute("data-theme", "dark");
      else document.documentElement.removeAttribute("data-theme");
      try { localStorage.setItem("elivantra-theme", next); } catch (e) {}
    });
  }

  /* ---------- floating eyebrow that follows scroll ---------- */
  var scrollEyebrow = document.getElementById("scrollEyebrow");
  var topHero = document.querySelector(".hero, .page-hero");
  var eyebrowSections = Array.prototype.slice.call(document.querySelectorAll("[data-eyebrow-ru]"));

  if (scrollEyebrow && eyebrowSections.length) {
    var seRu = scrollEyebrow.querySelector(".t-ru");
    var seEn = scrollEyebrow.querySelector(".t-en");
    var currentLabel = null;
    var ticking = false;

    var updateEyebrow = function () {
      ticking = false;
      var y = window.scrollY + 150;

      var active = null;
      for (var i = 0; i < eyebrowSections.length; i++) {
        if (eyebrowSections[i].offsetTop <= y) active = eyebrowSections[i];
      }

      var heroBottom = topHero ? topHero.offsetTop + topHero.offsetHeight : 0;
      var shouldShow = window.scrollY > heroBottom - 220 && !!active;
      scrollEyebrow.classList.toggle("is-visible", shouldShow);

      if (active && active !== currentLabel) {
        currentLabel = active;
        seRu.textContent = active.dataset.eyebrowRu;
        seEn.textContent = active.dataset.eyebrowEn;
      }
    };

    window.addEventListener("scroll", function () {
      if (!ticking) {
        ticking = true;
        requestAnimationFrame(updateEyebrow);
      }
    }, { passive: true });
    window.addEventListener("resize", updateEyebrow);
    updateEyebrow();
  }
});
