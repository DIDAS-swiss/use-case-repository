#!/usr/bin/env python3
"""The use-case form, in one place for every script that reads or writes an issue.

A use-case issue is the body GitHub writes for a filled-in form
(.github/ISSUE_TEMPLATE/use-case-candidate.yml): a `### <label>` heading per
field, in the form's order, `_No response_` where a field was left empty. The
intake writes the same body for a batch entry, and ends it with a hash of its
own text so that it can tell an untouched body from one edited by hand.

Field ids are stable; labels may change. A label that was used before is kept
in LEGACY_LABELS, so a body written with an earlier version of the form still
parses: `parse()` reads both. The same holds for a dropdown option that was
retired (LEGACY_OPTIONS).

Needs PyYAML.
"""

import hashlib
import pathlib
import re

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
FORM_PATH = ROOT / ".github" / "ISSUE_TEMPLATE" / "use-case-candidate.yml"
FORM = yaml.safe_load(FORM_PATH.read_text(encoding="utf-8"))
FIELDS = [f for f in FORM["body"] if f.get("id")]
BY_ID = {f["id"]: f for f in FIELDS}
NO_RESPONSE = "_No response_"
BODY_MARKER = "<!-- intake-body sha="

# Labels of earlier versions of the form, by field id. Bodies written before
# 2026-11-10 use these; parse() maps them to the same field.
LEGACY_LABELS = {
    "outcome": ["Outcome: what must be proven (optional)"],
    "credentials": ["Credentials needed"],
    "demand": ["Demand and value (optional)"],
    "open_questions": ["Coordination needs and open questions (optional)"],
    "sources": ["Sources (optional)"],
}

# Retired dropdown options: still understood when reading an earlier body.
LEGACY_OPTIONS = {
    "lighthouse": {"Selected as lighthouse (DIDAS decision)": "selected"},
}

# The six concepts a signal needs, in the order the form asks for them.
CORE = ("title", "summary", "actors", "outcome", "demand", "evidence_status", "sources")

EVIDENCE_STATUS = ("hypothesis", "documented need", "design", "prototype", "pilot", "production")


def label(field_id):
    return BY_ID[field_id]["attributes"]["label"]


def labels():
    """Every label, current and earlier, -> field id."""
    out = {f["attributes"]["label"]: f["id"] for f in FIELDS}
    for fid, old in LEGACY_LABELS.items():
        for lab in old:
            out.setdefault(lab, fid)
    return out


def parse(body):
    """The form's fields in an issue body, as {field id: text}; '' for _No response_.
    Reads bodies of the current and of earlier versions of the form."""
    by_label = labels()
    out, current, buf = {}, None, []
    for line in (body or "").split("\n"):
        m = re.match(r"^### (.+?)\s*$", line)
        if m and m.group(1) in by_label:
            if current:
                out[current] = "\n".join(buf).strip()
            current, buf = by_label[m.group(1)], []
        elif current:
            buf.append(line)
    if current:
        out[current] = "\n".join(buf).strip()
    return {k: ("" if v == NO_RESPONSE else re.sub(r"\n*<!--.*?-->\s*$", "", v, flags=re.S)) for k, v in out.items()}


def options(field_id):
    return BY_ID[field_id]["attributes"].get("options") or []


def chosen(field_id, text):
    """The leading ids of the dropdown options a field's text holds."""
    return [o.lstrip("— ").split(" · ")[0] for o in options(field_id) if o in (text or "")]


def option(field_id, prefix):
    """The form's option text for a choice, found by its leading id (before ' · ' or ':')."""
    for o in options(field_id):
        bare = o.lstrip("— ")
        if bare == prefix or bare.startswith(f"{prefix} · ") or bare.lower().startswith(f"{prefix.lower()}:"):
            return o
    return None


def evidence_status(text):
    """The evidence status a field's text names, as one of EVIDENCE_STATUS, or ''."""
    t = (text or "").strip().lower()
    return next((s for s in EVIDENCE_STATUS if t.startswith(s)), "")


def lighthouse(fields, labels_=()):
    """(proposal, decision) for an issue: proposal from the form ('candidate' or ''),
    decision from the curator's labels ('selected', 'candidate' or ''). A body written
    with the retired option 'Selected as lighthouse (DIDAS decision)' counts as a proposal
    whose decision is recorded by the label."""
    text = fields.get("lighthouse") or ""
    proposal = "candidate" if ("Propose as lighthouse candidate" in text
                               or any(o in text for o in LEGACY_OPTIONS["lighthouse"])) else ""
    decision = "selected" if "lighthouse" in labels_ else "candidate" if "lighthouse-candidate" in labels_ else ""
    return proposal, decision


def body_sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def render(values):
    """The issue body exactly as GitHub writes a filled-in form: every field, in order,
    then the intake's hash of that text."""
    parts = []
    for f in FIELDS:
        v = values.get(f["id"])
        if f["type"] == "checkboxes":
            picked = set(v or [])
            v = "\n".join(f"- [{'X' if o['label'] in picked else ' '}] {o['label']}" for o in f["attributes"]["options"])
        elif isinstance(v, list):
            v = ", ".join(v)
        parts.append(f"### {f['attributes']['label']}\n\n{(v or '').strip() or NO_RESPONSE}")
    text = "\n\n".join(parts)
    return f"{text}\n\n{BODY_MARKER}{body_sha(text)} -->"


def owned_body(body):
    """True when the body is the intake's own and nobody has edited it since."""
    body = body or ""
    if body.startswith("_Filed with the intake batch"):   # the first intake format
        return True
    m = re.search(r"\n\n" + re.escape(BODY_MARKER) + r"([0-9a-f]+) -->\s*$", body)
    return bool(m) and body_sha(body[:m.start()]) == m.group(1)


def short_id(body):
    """The short id of a use-case issue: its form field, or the first line of the first intake format."""
    sid = (parse(body).get("entry_id") or "").strip()
    if re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", sid):
        return sid
    m = re.search(r"backlog (?:`[^`]*` · )?`([a-z0-9-]+)`", (body or "").split("\n", 1)[0])
    return m.group(1) if m else None


def reader_sections(fields, keep=CORE):
    """(label, text) for presenting an issue to a reader: the fields that hold
    something, in form order. A field in `keep` that is empty is listed with
    'Not yet known.', so a missing core fact stays visible; other empty fields are
    left out. The canonical body is not changed by this."""
    out = []
    for f in FIELDS:
        if f["type"] in ("markdown",) or f["id"] in ("title",):
            continue
        text = (fields.get(f["id"]) or "").strip()
        if f["type"] == "checkboxes":
            text = ", ".join(re.findall(r"- \[X\] (.+)", text))
        if text:
            out.append((f["attributes"]["label"], text))
        elif f["id"] in keep:
            out.append((f["attributes"]["label"], "Not yet known."))
    return out
