/* ──────────────────────────────────────────────────────────────────────
   Review mode.

   ?review=1 on any URL puts the unconfirmed placeholders back on screen, so
   the outstanding items can be seen in context. Without it — which is every
   live visit — the page shows only confirmed content and its fallbacks, and
   that state is pure CSS, so it is correct with this file absent.
   ────────────────────────────────────────────────────────────────────── */
(function () {
  'use strict';
  try {
    if (new URLSearchParams(location.search).get('review') !== '1') return;
  } catch (e) { return; }

  document.documentElement.classList.add('review');

  document.addEventListener('DOMContentLoaded', function () {
    var n = document.querySelectorAll('[data-tbc]').length;
    var bar = document.createElement('p');
    bar.className = 'review-flag';
    bar.textContent = 'Review mode — ' + n + ' unconfirmed item' + (n === 1 ? '' : 's')
                    + ' shown. This is not what visitors see.';
    document.body.insertBefore(bar, document.body.firstChild);
  });
})();
