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
