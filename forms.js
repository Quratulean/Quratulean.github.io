/* Islamic Parenting 101 — forms. Fill in the two endpoints below, then every sign-up box and the contact form switch on automatically.
   signup: the MailerLite embedded-form "subscribe" URL (https://assets.mailerlite.com/jsonp/<ACCOUNT_ID>/forms/<FORM_ID>/subscribe)
   contact: the Formspree form URL (https://formspree.io/f/<FORM_ID>) */
window.SITE_FORMS = { signup: "mailerlite", mlAccount: "2818911", contact: "https://formspree.io/f/mljbopga" };
(function () {
  var C = window.SITE_FORMS;
  if (C.signup) { /* MailerLite universal script (renders the .ml-embedded forms) */
    (function(w,d,e,u,f,l,n){w[f]=w[f]||function(){(w[f].q=w[f].q||[]).push(arguments);},l=d.createElement(e),l.async=1,l.src=u,n=d.getElementsByTagName(e)[0],n.parentNode.insertBefore(l,n);})(window,document,'script','https://assets.mailerlite.com/js/universal.js','ml');
    ml('account', C.mlAccount);
  }
  function $all(s) { return Array.prototype.slice.call(document.querySelectorAll(s)); }
  if (C.signup) $all(".signup,.needs-signup").forEach(function (e) { e.hidden = false; });
  if (C.contact) $all(".needs-contact").forEach(function (e) { e.hidden = false; });
  if (!C.contact) $all(".contact-fallback").forEach(function (e) { e.hidden = false; });
  function note(f, msg, ok) { var n = f.querySelector(".fnote"); if (n) { n.textContent = msg; n.className = "fnote " + (ok ? "ok" : "err"); } }
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
