/* Backlog page: reads the use-case issues and open pull requests from the
 * public GitHub API and places every use case at its step: candidate, taken by
 * a working group, drafting, published or not pursued. Published entries come
 * from the site itself. Nothing is stored; the page reads GitHub each time.
 */
(function () {
 // The layout embeds the sector list after the page content, so start once the document is parsed.
 function start() {
  var REPO = 'DIDAS-swiss/use-case-repository';
  var API = 'https://api.github.com/repos/' + REPO;
  var box = document.getElementById('backlog-app');
  if (!box) return;

  var read = function (id) {
    var el = document.getElementById(id);
    return el ? JSON.parse(el.textContent) : [];
  };
  var entries = read('backlog-entries');
  var groups = {};
  read('backlog-groups').forEach(function (g) { groups[g.id] = g.name; });
  var sectors = {};
  read('sector-data').forEach(function (s) { sectors[s.id] = s; });
  var sectionOf = function (id) {
    var s = sectors[id];
    while (s && s.broader) s = sectors[s.broader];
    return s ? s : null;
  };

  var STEPS = [
    ['candidate', 'Candidate'], ['taken', 'Taken'], ['drafting', 'Drafting'],
    ['published', 'Published entry'], ['not-pursued', 'Not pursued']
  ];

  function getAll(path) {
    var out = [];
    function page(n) {
      return fetch(API + path + (path.indexOf('?') < 0 ? '?' : '&') + 'per_page=100&page=' + n,
                   { headers: { Accept: 'application/vnd.github+json' } })
        .then(function (r) {
          if (!r.ok) throw new Error('GitHub answered ' + r.status);
          return r.json();
        })
        .then(function (items) {
          out = out.concat(items);
          return items.length === 100 ? page(n + 1) : out;
        });
    }
    return page(1);
  }

  // A form field of an issue body. Labels of earlier versions of the form are
  // listed too (scripts/use_case_form.py, LEGACY_LABELS), so older bodies still read.
  var LABELS = {
    entry_id: ['Short id (optional)'],
    sectors: ['Sector(s)'],
    summary: ['Summary'],
    actors: ['Actors and roles'],
    outcome: ['Facts to prove', 'Outcome: what must be proven (optional)'],
    demand: ['Demand and value', 'Demand and value (optional)'],
    evidence: ['Evidence status']
  };
  function field(body, id) {
    var labels = LABELS[id] || [id];
    for (var k = 0; k < labels.length; k++) {
      var parts = ('\n' + (body || '')).split('\n### ' + labels[k] + '\n');
      if (parts.length < 2) continue;
      var v = parts[1].split('\n### ')[0].replace(/<!--[\s\S]*?-->/g, '').trim();
      return v === '_No response_' ? '' : v;
    }
    return '';
  }
  // The English part of a field (the German follows a **DE:** line).
  function english(v) { return v.split(/\n\*\*DE:\*\*/)[0].trim(); }

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; });
  }

  Promise.all([getAll('/issues?labels=use-case&state=all'), getAll('/pulls?state=open')])
    .then(function (res) {
      var issues = res[0].filter(function (i) { return !i.pull_request; });
      var drafts = {};
      res[1].forEach(function (p) {
        var m = /^draft\/(.+)$/.exec(p.head && p.head.ref || '');
        if (m) drafts[m[1]] = p;
      });
      var byEntry = {};
      entries.forEach(function (e) { byEntry[e.id] = e; });
      var seen = {};

      var items = issues.map(function (i) {
        var labels = i.labels.map(function (l) { return l.name; });
        var id = field(i.body, 'entry_id');
        var secIds = (field(i.body, 'sectors').match(/ISIC-[A-Z0-9]+/g) || []);
        var evidence = (field(i.body, 'evidence').split(':')[0] || '').trim();
        // the reader sees the fields that hold something; empty ones are left out
        var details = [['Summary', 'summary'], ['Actors and roles', 'actors'], ['Facts to prove', 'outcome'],
                       ['Demand and value', 'demand']]
          .map(function (d) { return [d[0], english(field(i.body, d[1]))]; })
          .filter(function (d) { return d[1]; });
        var secs = [];
        secIds.forEach(function (x) {
          var s = sectionOf(x), letter = s && s.id.replace('ISIC-', '');
          if (letter && secs.indexOf(letter) < 0) secs.push(letter);
        });
        if (!secs.length) labels.forEach(function (l) { var m = /^ISIC ([A-Z])$/.exec(l); if (m) secs.push(m[1]); });
        var wg = labels.filter(function (l) { return l.indexOf('wg: ') === 0; }).map(function (l) { return l.slice(4); })[0] || '';
        var lighthouse = labels.indexOf('lighthouse') >= 0 ? 'Lighthouse' : labels.indexOf('lighthouse-candidate') >= 0 ? 'Candidate' : '';
        var entry = byEntry[id];
        var step;
        if (i.state === 'closed' && (i.state_reason === 'not_planned' || labels.indexOf('duplicate') >= 0 || labels.indexOf('out-of-scope') >= 0)) step = 'not-pursued';
        else if (entry) step = 'published';
        else if (drafts[id] || labels.indexOf('drafting') >= 0) step = 'drafting';
        else if (wg) step = 'taken';
        else step = 'candidate';
        if (entry) seen[entry.id] = true;
        return { number: i.number, url: i.html_url, title: i.title, id: id, sectors: secs, wg: wg,
                 lighthouse: lighthouse, step: step, entry: entry, draft: drafts[id],
                 evidence: evidence, details: details };
      });
      entries.forEach(function (e) {   // published entries without an issue
        if (!seen[e.id]) items.push({ title: e.title, id: e.id, sectors: [], wg: '', step: 'published', entry: e,
                                      evidence: e.evidence || '', details: [],
                                      lighthouse: e.lighthouse === 'selected' ? 'Lighthouse' : e.lighthouse === 'candidate' ? 'Candidate' : '' });
      });
      render(items);
    })
    .catch(function (e) {
      box.innerHTML = '<p class="note">The use cases could not be read from GitHub (' + esc(e.message) +
        '). GitHub limits unauthenticated reads to 60 an hour per visitor; try again later, or see the ' +
        '<a href="https://github.com/' + REPO + '/issues?q=is%3Aissue+label%3Ause-case">issues on GitHub</a>.</p>';
    });

  function render(items) {
    var state = { step: '', sector: '', wg: '', lighthouse: '', q: '' };
    var sectionsUsed = {};
    items.forEach(function (it) { it.sectors.forEach(function (s) { sectionsUsed[s] = true; }); });
    var sectionRows = Object.keys(sectors).map(function (k) { return sectors[k]; })
      .filter(function (s) { return s.level === 'section' && sectionsUsed[s.id.replace('ISIC-', '')]; });

    var opts = function (list) { return list.map(function (o) { return '<option value="' + esc(o[0]) + '">' + esc(o[1]) + '</option>'; }).join(''); };
    box.innerHTML =
      '<div class="lifecycle" role="group" aria-label="Lifecycle steps">' +
      STEPS.map(function (s) { return '<button type="button" class="step" data-step="' + s[0] + '"><span class="count"></span><span class="label">' + s[1] + '</span></button>'; }).join('<span class="arrow" aria-hidden="true">→</span>') +
      '</div>' +
      '<div class="filters">' +
      '<label>Sector <select data-f="sector"><option value="">All</option>' + opts(sectionRows.map(function (s) { return [s.id.replace('ISIC-', ''), s.id.replace('ISIC-', '') + ' — ' + s.label]; })) + '</select></label>' +
      '<label>Working group <select data-f="wg"><option value="">All</option><option value="-">None yet</option>' + opts(Object.keys(groups).map(function (g) { return [g, groups[g]]; })) + '</select></label>' +
      '<label>Lighthouse <select data-f="lighthouse"><option value="">All</option>' + opts([['Lighthouse', 'Lighthouse'], ['Candidate', 'Candidate'], ['-', 'Neither']]) + '</select></label>' +
      '<label>Search <input type="search" data-f="q" placeholder="title or id"></label>' +
      '<span class="shown" aria-live="polite"></span>' +
      '</div>' +
      '<table class="backlog-table"><thead><tr><th>#</th><th>Use case</th><th>Sector</th><th>Working group</th><th>Lighthouse</th><th>Evidence</th><th>Step</th></tr></thead><tbody></tbody></table>';

    var tbody = box.querySelector('tbody');
    function update() {
      var match = function (it, ignoreStep) {
        if (!ignoreStep && state.step && it.step !== state.step) return false;
        if (state.sector && it.sectors.indexOf(state.sector) < 0) return false;
        if (state.wg && (state.wg === '-' ? it.wg : it.wg !== state.wg)) return false;
        if (state.lighthouse && (state.lighthouse === '-' ? it.lighthouse : it.lighthouse !== state.lighthouse)) return false;
        if (state.q && (it.title + ' ' + it.id).toLowerCase().indexOf(state.q.toLowerCase()) < 0) return false;
        return true;
      };
      STEPS.forEach(function (s) {
        var b = box.querySelector('[data-step="' + s[0] + '"]');
        b.querySelector('.count').textContent = items.filter(function (it) { return it.step === s[0] && match(it, true); }).length;
        b.setAttribute('aria-pressed', String(state.step === s[0]));
      });
      var shown = items.filter(function (it) { return match(it, false); })
        .sort(function (a, b) { return (a.number || 1e9) - (b.number || 1e9); });
      box.querySelector('.shown').textContent = shown.length + ' of ' + items.length;
      tbody.innerHTML = shown.map(function (it) {
        var label = STEPS.filter(function (s) { return s[0] === it.step; })[0][1];
        var extra = it.entry ? ' <a href="' + esc(it.entry.url) + '">entry</a> · ' + esc(it.entry.stage) :
          it.draft ? ' <a href="' + esc(it.draft.html_url) + '">draft #' + it.draft.number + '</a>' : '';
        return '<tr>' +
          '<td>' + (it.number ? '<a href="' + esc(it.url) + '">#' + it.number + '</a>' : '') + '</td>' +
          '<td>' + (it.url ? '<a href="' + esc(it.url) + '">' + esc(it.title) + '</a>' : esc(it.title)) + (it.id ? '<br><code>' + esc(it.id) + '</code>' : '') +
          (it.details.length ? '<details class="uc-details"><summary>Details</summary>' + it.details.map(function (d) {
            return '<p><strong>' + esc(d[0]) + '</strong><br>' + esc(d[1]).replace(/\n/g, '<br>') + '</p>';
          }).join('') + '</details>' : '') + '</td>' +
          '<td>' + esc(it.sectors.join(', ')) + '</td>' +
          '<td>' + esc(groups[it.wg] || it.wg || '') + '</td>' +
          '<td>' + (it.lighthouse ? '<span class="pill ' + (it.lighthouse === 'Lighthouse' ? 'supply-available' : 'supply-emerging') + '">' + it.lighthouse + '</span>' : '') + '</td>' +
          '<td>' + esc(it.evidence || '') + '</td>' +
          '<td><span class="pill step-' + it.step + '">' + label + '</span>' + extra + '</td>' +
          '</tr>';
      }).join('');
    }
    box.addEventListener('click', function (e) {
      var b = e.target.closest('[data-step]');
      if (!b) return;
      state.step = state.step === b.getAttribute('data-step') ? '' : b.getAttribute('data-step');
      update();
    });
    box.addEventListener('input', function (e) {
      var f = e.target.getAttribute('data-f');
      if (f) { state[f] = e.target.value; update(); }
    });
    update();
  }
 }
 if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start);
 else start();
})();
