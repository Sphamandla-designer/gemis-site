/* Cookie consent and analytics for GEMIS Studio.

   Analytics never load before the visitor says yes. Until then the studio sets
   no cookies at all; the only thing kept in the browser is the choice itself
   (localStorage, key "gemis-consent"), so the banner is not asked twice.

   TO SWITCH ANALYTICS ON: put the Google Analytics 4 measurement ID below, and
   the same ID in assets/js/consent.js (the corporate site shares this origin,
   the storage key and so the visitor's one choice)
   (Google Analytics → Admin → Data streams → the web stream → "G-…"), then
   rebuild the standalone bundle. While it is empty there is nothing to consent
   to, so no banner shows and "Cookie settings" just opens the privacy notice. */
(function () {
  'use strict';
  var GA_ID = '';

  var KEY = 'gemis-consent'; // shared with assets/js/consent.js: one choice for the whole origin
  var VERSION = '1'; // bump to ask everyone again after the notice changes
  var banner = null;

  if (!/^G-[A-Z0-9]{4,}$/.test(GA_ID)) return;

  function read() {
    try { var v = JSON.parse(localStorage.getItem(KEY) || 'null'); return v && v.v === VERSION ? v.choice : null; }
    catch (e) { return null; }
  }
  function write(choice) {
    try { localStorage.setItem(KEY, JSON.stringify({ v: VERSION, choice: choice, at: new Date().toISOString() })); } catch (e) {}
  }

  function load() {
    if (window.__studioGa) return;
    window.__studioGa = true;
    window['ga-disable-' + GA_ID] = false;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('consent', 'default', { ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied', analytics_storage: 'granted' });
    window.gtag('js', new Date());
    window.gtag('config', GA_ID, { allow_google_signals: false, allow_ad_personalization_signals: false });
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(GA_ID);
    document.head.appendChild(s);
  }

  function unload() {
    window['ga-disable-' + GA_ID] = true;
    if (window.gtag) window.gtag('consent', 'update', { analytics_storage: 'denied' });
    // remove the cookies Google Analytics set on this host
    document.cookie.split(';').forEach(function (c) {
      var name = c.split('=')[0].trim();
      if (/^_ga(_|$)|^_gid$|^_gat/.test(name)) {
        [location.hostname, '.' + location.hostname, ''].forEach(function (d) {
          document.cookie = name + '=; Max-Age=0; path=/' + (d ? '; domain=' + d : '');
        });
      }
    });
  }

  function decide(choice) {
    write(choice);
    if (choice === 'granted') load(); else unload();
    hide();
  }

  function css() {
    var st = document.createElement('style');
    st.textContent =
      '.ck{position:fixed;left:16px;right:16px;bottom:16px;z-index:60;max-width:520px;background:#16161a;color:#f5f6f8;' +
      'padding:24px;font-family:Manrope,Helvetica,Arial,sans-serif;font-size:15px;line-height:1.45;box-shadow:0 24px 60px -24px rgba(0,0,0,.5);' +
      'display:grid;gap:16px;animation:ckIn .4s cubic-bezier(.2,.7,.2,1) both}' +
      '.ck h2{margin:0;font-family:"JetBrains Mono",monospace;font-size:12px;font-weight:400;letter-spacing:.06em;text-transform:uppercase;color:#ff7a12}' +
      '.ck p{margin:0;color:#c9cad1}.ck a{color:#f5f6f8;border-bottom:1px solid #ff7a12}' +
      '.ck__row{display:flex;gap:12px;flex-wrap:wrap}' +
      '.ck button{font-family:"JetBrains Mono",monospace;font-size:13px;letter-spacing:.02em;text-transform:uppercase;cursor:pointer;' +
      'border-radius:999px;padding:12px 20px;border:1px solid #f5f6f8;min-height:44px}' +
      '.ck__yes{background:#f5f6f8;color:#16161a}.ck__no{background:transparent;color:#f5f6f8}' +
      '.ck button:focus-visible{outline:2px solid #ff7a12;outline-offset:3px}' +
      '@keyframes ckIn{from{opacity:0;transform:translateY(12px)}}' +
      '@media (min-width:640px){.ck{left:24px;right:auto;bottom:24px}}' +
      '@media (prefers-reduced-motion:reduce){.ck{animation:none}}';
    document.head.appendChild(st);
  }

  function show(focus) {
    if (banner) { if (focus) banner.querySelector('button').focus(); return; }
    banner = document.createElement('section');
    banner.className = 'ck';
    banner.setAttribute('aria-label', 'Cookie choice');
    banner.innerHTML =
      '<h2>Cookies</h2>' +
      '<p>May we use Google Analytics to count visits and see which pages help? It sets cookies only if you say yes, ' +
      'and no advertising cookies at all. <a href="privacy.html#cookies">How we use it</a>.</p>' +
      '<div class="ck__row"><button type="button" class="ck__yes">Accept analytics</button>' +
      '<button type="button" class="ck__no">Decline</button></div>';
    banner.querySelector('.ck__yes').addEventListener('click', function () { decide('granted'); });
    banner.querySelector('.ck__no').addEventListener('click', function () { decide('denied'); });
    document.body.appendChild(banner);
    if (focus) banner.querySelector('button').focus();
  }

  function hide() {
    if (banner) { banner.remove(); banner = null; }
  }

  // "Cookie settings" in the footer reopens the choice. Delegated, because the
  // homepage footer is rendered by the runtime after this script runs.
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('[data-cookie-settings]');
    if (!a) return;
    e.preventDefault();
    show(true);
  });

  function start() {
    css();
    var choice = read();
    if (choice === 'granted') load();
    else if (!choice) show(false);
  }
  // the single-file bundle inlines this script in <head>, where there is no body yet
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
  window.StudioConsent = { open: function () { show(true); }, choice: read };
})();
