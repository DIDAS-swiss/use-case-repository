/* Theme and text-size controls of the shared DIDAS masthead. They read and
 * write the same localStorage keys as the other DIDAS sites (`theme`,
 * `font_size_preference`), which share this origin, so a preference set on
 * one of them holds on all of them. Storage can be unavailable (private
 * browsing, blocked site data); the controls then work for the page view only.
 */
(function () {
  var root = document.documentElement;
  var systemDark = window.matchMedia('(prefers-color-scheme: dark)');
  var FONT = { key: 'font_size_preference', min: 13, max: 22, base: 16 };

  function read(key) {
    try { return window.localStorage.getItem(key); } catch (e) { return null; }
  }
  function write(key, value) {
    try { window.localStorage.setItem(key, value); } catch (e) { /* ignore */ }
  }

  function storedTheme() {
    var v = read('theme');
    return v === 'light' || v === 'dark' ? v : 'auto';
  }
  function applyTheme() {
    var t = storedTheme();
    if (t === 'auto') t = systemDark.matches ? 'dark' : 'light';
    root.setAttribute('data-theme', t);
    var buttons = document.querySelectorAll('.site-masthead [data-theme-value]');
    for (var i = 0; i < buttons.length; i++) {
      buttons[i].setAttribute('aria-pressed',
        String(buttons[i].getAttribute('data-theme-value') === storedTheme()));
    }
  }

  function fontSize() {
    var v = Number.parseFloat(read(FONT.key));
    return v >= FONT.min && v <= FONT.max ? v : FONT.base;
  }
  function applyFont(px) {
    document.body.style.fontSize = px + 'px';
  }

  var themeButtons = document.querySelectorAll('.site-masthead [data-theme-value]');
  for (var i = 0; i < themeButtons.length; i++) {
    themeButtons[i].addEventListener('click', function (event) {
      write('theme', event.currentTarget.getAttribute('data-theme-value'));
      applyTheme();
    });
  }

  var fontButtons = document.querySelectorAll('.site-masthead [data-font-step]');
  for (var j = 0; j < fontButtons.length; j++) {
    fontButtons[j].addEventListener('click', function (event) {
      var step = Number(event.currentTarget.getAttribute('data-font-step'));
      var px = Math.min(FONT.max, Math.max(FONT.min, fontSize() + step));
      write(FONT.key, String(px));
      applyFont(px);
    });
  }

  systemDark.addEventListener('change', applyTheme);
  applyTheme();
  applyFont(fontSize());
})();

/* Sector selector. Any table with a "Sectors" column gets a select listing the
 * ISIC Rev. 5 sectors of the DIDAS Industry Function Graph (from _data/
 * sectors.csv). Choosing a sector keeps the rows filed under it or under any
 * division or class inside it, so "L" finds both banking and insurance.
 */
(function () {
  var data = document.getElementById('sector-data');
  if (!data) return;
  var sectors = JSON.parse(data.textContent);
  var byId = {};
  sectors.forEach(function (s) { byId[s.id] = s; });

  function within(id, ancestor) {
    for (var s = byId[id]; s; s = byId[s.broader]) {
      if (s.id === ancestor) return true;
    }
    return false;
  }

  var tables = document.querySelectorAll('.content table');
  Array.prototype.forEach.call(tables, function (table, n) {
    var heads = Array.prototype.map.call(table.querySelectorAll('thead th'), function (th) {
      return th.textContent.trim();
    });
    var col = heads.indexOf('Sectors');
    if (col < 0) return;
    var rows = Array.prototype.slice.call(table.querySelectorAll('tbody tr'));

    // Offer only the sectors that the rows use, with the sections and
    // divisions above them, so the list never leads to an empty table.
    var used = {};
    rows.forEach(function (row) {
      (row.cells[col].textContent.match(/ISIC-[A-Z0-9]+/g) || []).forEach(function (id) {
        for (var s = byId[id]; s; s = byId[s.broader]) used[s.id] = true;
      });
    });

    var label = document.createElement('label');
    label.className = 'sector-filter';
    var select = document.createElement('select');
    select.id = 'sector-filter-' + n;
    label.htmlFor = select.id;
    label.appendChild(document.createTextNode('Sector (ISIC Rev. 5) '));
    select.appendChild(new Option('All sectors', ''));
    // Each section, then the divisions and classes under it, indented.
    function add(s, depth) {
      if (!used[s.id]) return;
      var text = '\u00a0\u00a0\u00a0'.repeat(depth) + s.id.replace('ISIC-', '') + ' \u2014 ' + s.label;
      select.appendChild(new Option(text, s.id));
      sectors.forEach(function (c) { if (c.broader === s.id) add(c, depth + 1); });
    }
    sectors.forEach(function (s) { if (!s.broader) add(s, 0); });
    label.appendChild(select);

    var count = document.createElement('span');
    count.className = 'sector-count';
    count.setAttribute('aria-live', 'polite');
    label.appendChild(count);
    table.parentNode.insertBefore(label, table);

    function apply() {
      var chosen = select.value;
      var shown = 0;
      rows.forEach(function (row) {
        var ids = row.cells[col].textContent.match(/ISIC-[A-Z0-9]+/g) || [];
        var keep = !chosen || ids.some(function (id) { return within(id, chosen); });
        row.hidden = !keep;
        if (keep) shown++;
      });
      count.textContent = chosen ? shown + ' of ' + rows.length : '';
    }
    select.addEventListener('change', apply);
  });
})();
