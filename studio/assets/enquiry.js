/* The studio enquiry rules, shared by the homepage form (the Design Canvas
   component) and the Contact page form (plain HTML), so the two cannot drift.

   StudioEnquiry.validate(values)  -> { field: message } for every field that fails
   StudioEnquiry.normaliseUrl(v)   -> "acme.co.za" becomes "https://acme.co.za"
   StudioEnquiry.looksLikeBot(f)   -> true when the honeypot is filled or the form
                                      was sent faster than a person could type it

   Spam: the site is static and the form hands off to the visitor's own email app,
   so nothing is posted anywhere a bot could flood. The two traps still stop a
   script from triggering the hand-off, and they are ready for the day the form
   posts to a real endpoint. */
(function () {
  'use strict';
  var EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
  var MIN_MS = 3000; // faster than this from first sight of the form is not a person
  var shownAt = Date.now();

  function normaliseUrl(v) {
    v = (v || '').trim();
    if (v && !/^https?:\/\//i.test(v)) v = 'https://' + v;
    return v;
  }

  function validUrl(v) {
    if (!v) return true;
    try { var u = new URL(normaliseUrl(v)); return /\./.test(u.hostname); } catch (e) { return false; }
  }

  function validate(v) {
    var e = {};
    var name = (v.name || '').trim();
    var email = (v.email || '').trim();
    var message = (v.message || '').trim();
    if (!name) e.name = 'Enter your name.';
    else if (name.length < 2) e.name = 'Enter your full name.';
    if (!email) e.email = 'Enter your work email, so we can reply.';
    else if (!EMAIL.test(email)) e.email = 'Enter an email address like name@company.co.za.';
    if (!validUrl(v.url)) e.url = 'Enter a web address like acme.co.za, or leave it empty.';
    if (!message) e.message = "Tell us what isn't working — a sentence or two is enough.";
    else if (message.length < 15) e.message = 'Add a little more detail, so the reply can be specific.';
    if (!v.consent) e.consent = 'Tick the box to agree to the privacy notice before sending.';
    return e;
  }

  function looksLikeBot(form) {
    var trap = form && form.querySelector('[name="website"]');
    if (trap && trap.value) return true;
    return Date.now() - shownAt < MIN_MS;
  }

  window.StudioEnquiry = { validate: validate, normaliseUrl: normaliseUrl, looksLikeBot: looksLikeBot, FIELDS: ['name', 'email', 'url', 'message', 'consent'] };
})();
