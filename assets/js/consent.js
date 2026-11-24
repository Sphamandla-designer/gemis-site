/* Cookie consent and analytics for the GEMIS corporate site.

   Analytics never load before the visitor says yes. Until then the site sets
   no cookies at all; the only thing kept in the browser is the choice itself
   (localStorage, key "gemis-consent"), so the banner is not asked twice.

   TO SWITCH ANALYTICS ON: put the Google Analytics 4 measurement ID below, and
   the same ID in studio/assets/consent.js (the studio shares this origin,
   the storage key and so the visitor's one choice)
   (Google Analytics → Admin → Data streams → the web stream → "G-…"), then
   rebuild the standalone bundle. While it is empty there is nothing to consent
   to, so no banner shows and "Cookie settings" just opens the privacy notice. */
(function () {
  'use strict';
  var GA_ID = '';

  var KEY = 'gemis-consent'; // shared with studio/assets/consent.js: one choice for the whole origin
  var VERSION = '1'; // bump to ask everyone again after the notice changes
  var banner = null;
  var ROOT = (function () { try { return new URL('../../', document.currentScript.src).href; } catch (e) { return ''; } })();

  if (!/^G-[A-Z0-9]{4,}$/.test(GA_ID)) return;

  function read() {
    try { var v = JSON.parse(localStorage.getItem(KEY) || 'null'); return v && v.v === VERSION ? v.choice : null; }
    catch (e) { return null; }
  }
  function write(choice) {
    try { localStorage.setItem(KEY, JSON.stringify({ v: VERSION, choice: choice, at: new Date().toISOString() })); } catch (e) {}
  }

  function load() {
    if (window.__gemisGa) return;
    window.__gemisGa = true;
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
      '.ck{position:fixed;left:16px;right:16px;bottom:16px;z-index:200;max-width:520px;background:#0a1230;color:#fff;' +
      'padding:24px;font-family:Montserrat,system-ui,sans-serif;font-size:15px;line-height:1.5;box-shadow:0 24px 60px -24px rgba(0,0,0,.55);' +
      'clip-path:polygon(0 0,calc(100% - 18px) 0,100% 18px,100% 100%,0 100%);display:grid;gap:14px}' +
      '.ck .ck__t{margin:0;font-size:12px;font-weight:500;letter-spacing:.18em;text-transform:uppercase;color:#fff}' +
      '.ck p{margin:0;color:rgba(255,255,255,.86)}.ck .ck__t{color:#fff}.ck a{color:#fff;text-decoration:underline;text-underline-offset:3px}' +
      '.ck__row{display:flex;gap:12px;flex-wrap:wrap}' +
      '.ck button{font:inherit;font-size:12px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;cursor:pointer;' +
      'border-radius:0;padding:12px 20px;border:1px solid #fff;min-height:44px}' +
      '.ck__yes{background:#fff;color:#0a1230}.ck__no{background:transparent;color:#fff}' +
      '.ck button:active{transform:scale(.95)}.ck button:focus-visible{outline:2px solid #fff;outline-offset:3px}' +
      '@media (min-width:640px){.ck{left:24px;right:auto;bottom:24px}}';
    document.head.appendChild(st);
  }

  function show(focus) {
    if (banner) { if (focus) banner.querySelector('button').focus(); return; }
    banner = document.createElement('section');
    banner.className = 'ck';
    banner.setAttribute('aria-label', 'Cookie choice');
    banner.innerHTML =
      '<p class="ck__t">Cookies</p>' +
      '<p>May we use Google Analytics to count visits and see which pages help? It sets cookies only if you say yes, ' +
      'and no advertising cookies at all. <a href="' + ROOT + 'privacy.html#cookies">How we use it</a>.</p>' +
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
  window.GemisConsent = { open: function () { show(true); }, choice: read };
})();
