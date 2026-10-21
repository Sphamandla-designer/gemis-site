/* ──────────────────────────────────────────────────────────────────────
   Our Work filters.

   The filter bar is hidden in the markup and revealed here, so with JavaScript
   off nobody sees controls that cannot work — and every project is listed
   anyway, because filtering only ever hides cards that are already on the page.

   Buttons carry aria-pressed, so a screen reader hears which filter is on.
   ────────────────────────────────────────────────────────────────────── */
(function () {
  'use strict';

  var bar = document.querySelector('[data-filters]');
  var grid = document.querySelector('[data-grid]');
  if (!bar || !grid) return;

  var cards = [].slice.call(grid.querySelectorAll('.wk__card'));
  var state = { industry: 'all', capability: 'all' };

  bar.hidden = false;

  function matches(card) {
    var ind = card.getAttribute('data-industry') || '';
    var cap = card.getAttribute('data-capability') || '';
    return (state.industry === 'all' || ind === state.industry) &&
           (state.capability === 'all' || cap.split(/\s+/).indexOf(state.capability) !== -1);
  }

  function apply() {
    var shown = 0;
    cards.forEach(function (c) {
      var ok = matches(c);
      c.hidden = !ok;
      if (ok) shown++;
    });
    // tell anyone using a screen reader what just happened
    var live = document.getElementById('wkCount');
    if (live) live.textContent = shown + (shown === 1 ? ' project shown' : ' projects shown');
  }

  bar.addEventListener('click', function (e) {
    var btn = e.target.closest('button[data-filter]');
    if (!btn) return;
    var group = btn.getAttribute('data-filter');
    state[group] = btn.getAttribute('data-value');
    [].forEach.call(bar.querySelectorAll('button[data-filter="' + group + '"]'), function (b) {
      b.setAttribute('aria-pressed', String(b === btn));
    });
    apply();
  });

  apply();
})();
