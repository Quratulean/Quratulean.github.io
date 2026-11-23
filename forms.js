/* Islamic Parenting 101 — forms. Fill in the two endpoints below, then every sign-up box and the contact form switch on automatically.
   signup: the MailerLite embedded-form "subscribe" URL (https://assets.mailerlite.com/jsonp/<ACCOUNT_ID>/forms/<FORM_ID>/subscribe)
   contact: the Formspree form URL (https://formspree.io/f/<FORM_ID>) */
window.SITE_FORMS = { signup: "", contact: "" };
(function () {
  var C = window.SITE_FORMS;
  function $all(s) { return Array.prototype.slice.call(document.querySelectorAll(s)); }
  if (C.signup) $all(".signup,.needs-signup").forEach(function (e) { e.hidden = false; });
  if (C.contact) $all(".needs-contact").forEach(function (e) { e.hidden = false; });
  if (!C.contact) $all(".contact-fallback").forEach(function (e) { e.hidden = false; });
  function note(f, msg, ok) { var n = f.querySelector(".fnote"); if (n) { n.textContent = msg; n.className = "fnote " + (ok ? "ok" : "err"); } }
  $all("form.signup-form").forEach(function (f) {
    f.addEventListener("submit", function (ev) {
      ev.preventDefault();
      if (f.querySelector("[name=website]").value) return; // honeypot
      var email = f.querySelector("[name=email]").value.trim();
      if (!/^\S+@\S+\.\S+$/.test(email)) { note(f, "Please enter a valid email address.", false); return; }
      var fd = new FormData();
      fd.append("fields[email]", email);
      fd.append("fields[name]", (f.querySelector("[name=name]") || {}).value || "");
      fd.append("ml-submit", "1"); fd.append("anticsrf", "true");
      var b = f.querySelector("button"); b.disabled = true; b.textContent = "Sending…";
      fetch(C.signup, { method: "POST", body: fd, mode: "no-cors" })
        .then(function () { location.href = "thank-you.html"; })
        .catch(function () { b.disabled = false; b.textContent = "Send me the free kit"; note(f, "Something went wrong. Please try again.", false); });
    });
  });
  $all("form.contact-form").forEach(function (f) {
    f.addEventListener("submit", function (ev) {
      ev.preventDefault();
      if (f.querySelector("[name=website]").value) return;
      var data = { name: f.name.value, email: f.email.value, message: f.message.value };
      var b = f.querySelector("button"); b.disabled = true; b.textContent = "Sending…";
      fetch(C.contact, { method: "POST", headers: { "Content-Type": "application/json", "Accept": "application/json" }, body: JSON.stringify(data) })
        .then(function (r) { if (!r.ok) throw 0; f.reset(); b.disabled = false; b.textContent = "Send message"; note(f, "Thank you! Your message was sent. I read every one.", true); })
        .catch(function () { b.disabled = false; b.textContent = "Send message"; note(f, "Sorry, that did not send. Please try again.", false); });
    });
  });
})();
