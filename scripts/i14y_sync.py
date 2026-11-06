#!/usr/bin/env python3
"""Federate credential schemas from I14Y.

For every credential in credentials/ whose front matter names an I14Y dataset
(`i14y_id`), this fetches the dataset record and its structure from the public
I14Y API and writes, under federation/i14y/<credential-id>/:

  dataset.json     the dataset record, as published
  structure.jsonld the structure (SHACL shapes), as published, key-sorted
  structure.ttl    the same structure in Turtle, as published
  schema.json      a compact attribute list derived from the structure
  README.md        the attribute list as a table, readable on GitHub

and copies README.md's table to _includes/i14y/<credential-id>.md, where the
site layout picks it up. It also lists every credential dataset on I14Y (any
dataset identified by a `urn:vct:` credential type), published or still a
candidate, in _data/i14y-credentials.csv, which the issue form offers as a
choice. Nothing here is edited by hand: I14Y stays the
authoritative source, and a change upstream reaches this repository as a pull
request from the federation-sync workflow, never silently.

Run from the repository root:  python3 scripts/i14y_sync.py
Standard library only, so it runs on a stock GitHub Actions runner.
"""

import csv
import io
import json
import pathlib
import re
import sys
import urllib.request

API = "https://api.i14y.admin.ch/api/public/v1"
CATALOG = "https://www.i14y.admin.ch/de/catalog"
ROOT = pathlib.Path(__file__).resolve().parent.parent
LANGS = ("en", "de", "fr", "it")

SH = "http://www.w3.org/ns/shacl#"
DCT = "http://purl.org/dc/terms/"
XSD = "http://www.w3.org/2001/XMLSchema#"
CUBE_DSD = "http://purl.org/linked-data/cube#DataStructureDefinition"


def get(url, raw=False):
    req = urllib.request.Request(url, headers={"User-Agent": "didas-use-case-repository i14y-sync"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        body = resp.read().decode("utf-8")
    return body if raw else json.loads(body)


def front_matter(path):
    """The handful of flat front-matter fields this script needs."""
    text = path.read_text(encoding="utf-8")
    block = text.split("---", 2)[1] if text.startswith("---") else ""
    fields = {}
    for line in block.splitlines():
        m = re.match(r"^([a-z0-9_]+):\s*(.*?)\s*$", line)
        if m:
            fields[m.group(1)] = m.group(2)
    return fields


def literals(node, key):
    """Language-tagged values of a JSON-LD property, as {lang: text}."""
    out = {}
    for v in node.get(key, []):
        if "@value" in v:
            out.setdefault(v.get("@language", ""), v["@value"])
    return out


def first(node, key):
    vals = node.get(key, [])
    if not vals:
        return None
    v = vals[0]
    return v.get("@id", v.get("@value"))


def pick(texts):
    for lang in LANGS + ("",):
        t = (texts.get(lang) or "").strip()
        # I14Y sometimes stores an empty multilingual object as its string form
        if t and not t.startswith("{'"):
            return t
    return ""


def concept_index():
    """identifier@version -> catalog URL, for the concepts attributes conform to."""
    index = {}
    for c in get(f"{API}/concepts").get("data", []):
        for ident in c.get("identifiers") or []:
            index[f"{ident}@{c.get('version')}"] = f"{CATALOG}/concepts/{c['id']}/description"
    return index


def compact(graph, concepts):
    nodes = {n["@id"]: n for n in graph}
    root = next(n for n in graph if CUBE_DSD in n.get("@type", []))
    local = lambda iri: iri.rsplit("/", 1)[-1]

    groups = []

    def walk(shape_iri, parent_key):
        shape = nodes[shape_iri]
        attrs = []
        for ref in shape.get(SH + "property", []):
            p = nodes.get(ref["@id"])
            if not p:
                continue
            attr = {
                "key": local(p["@id"]),
                "label": {k: v for k, v in literals(p, SH + "name").items() if k},
                "description": pick(literals(p, SH + "description")),
                "datatype": (first(p, SH + "datatype") or "").replace(XSD, "") or None,
                "min": first(p, SH + "minCount"),
                "max": first(p, SH + "maxCount"),
                "order": int(first(p, SH + "order") or 9999),
            }
            conforms = first(p, DCT + "conformsTo")
            if conforms:
                m = re.search(r"/concept/([^/]+)/version/([^/]+)$", conforms)
                if m:
                    attr["concept"] = {
                        "identifier": m.group(1),
                        "version": m.group(2),
                        "url": concepts.get(f"{m.group(1)}@{m.group(2)}"),
                    }
            values = p.get(SH + "in")
            if values:
                attr["values"] = [v.get("@value") for v in values[0].get("@list", [])]
            child = first(p, SH + "node")
            if child:
                attr["group"] = local(child)
            attrs.append(attr)
        attrs.sort(key=lambda a: (a["order"], a["key"]))
        for a in attrs:
            del a["order"]
        groups.append({
            "key": local(shape_iri),
            "parent": parent_key,
            "label": {k: v for k, v in literals(shape, DCT + "title").items() if k},
            "attributes": attrs,
        })
        for a in attrs:
            if "group" in a:
                walk(shape_iri.rsplit("/", 1)[0] + "/" + a["group"], local(shape_iri))

    walk(root["@id"], None)
    return {
        "title": {k: v for k, v in literals(root, DCT + "title").items() if k},
        "version": first(root, "https://schema.org/version"),
        "valid_from": first(root, "https://schema.org/validFrom"),
        "groups": groups,
    }


def cardinality(a):
    lo = a.get("min") or "0"
    hi = a.get("max") or "n"
    return f"{lo}..{hi}"


def render(credential_id, record, schema, dataset_url):
    name = lambda d: d.get("en") or d.get("de") or ""
    pub = record.get("publisher") or {}
    lines = [
        f"| I14Y dataset | [`{record['identifiers'][0]}`]({dataset_url}) |",
        f"|---|---|",
        f"| Title | {name(record.get('title') or {})} |",
        f"| Publisher | {name(pub.get('name') or {})} (`{pub.get('identifier', '')}`) |",
        f"| Registration status | {record.get('registrationStatus', '')} |",
        f"| Access rights | {name((record.get('accessRights') or {}).get('name') or {})} |",
        f"| Personal data | {name((record.get('confidentialityPerson') or {}).get('name') or {})} |",
        f"| Structure version | {schema.get('version') or ''}, valid from {schema.get('valid_from') or ''} |",
        f"| Last modified on I14Y | {((record.get('system') or {}).get('modifiedAt') or '')[:10]} |",
        "",
    ]
    for g in schema["groups"]:
        if g["parent"]:
            lines.append(f"**{g['key']}** (in `{g['parent']}`)")
            lines.append("")
        lines += [
            "| Attribute | Label (EN · DE · FR · IT) | Type | Card. | I14Y concept |",
            "|---|---|---|---|---|",
        ]
        for a in g["attributes"]:
            label = " · ".join(a["label"].get(l, "") for l in LANGS if a["label"].get(l))
            typ = f"→ `{a['group']}`" if "group" in a else (a.get("datatype") or "")
            if a.get("values"):
                typ += " (" + ", ".join(f"`{v}`" for v in a["values"]) + ")"
            c = a.get("concept")
            concept = ""
            if c:
                concept = f"[{c['identifier']} {c['version']}]({c['url']})" if c.get("url") else f"{c['identifier']} {c['version']}"
            lines.append(f"| `{a['key']}` | {label} | {typ} | {cardinality(a)} | {concept} |")
        lines.append("")
    return "\n".join(lines)


def sync(path, concepts):
    fm = front_matter(path)
    credential_id, dataset_uuid, urn = fm.get("id"), fm.get("i14y_id"), fm.get("i14y_dataset")
    if not dataset_uuid:
        return None
    out = ROOT / "federation" / "i14y" / credential_id
    out.mkdir(parents=True, exist_ok=True)

    record = get(f"{API}/datasets/{dataset_uuid}")["data"]
    if urn and urn not in (record.get("identifiers") or []):
        sys.exit(f"{path}: i14y_id {dataset_uuid} is {record.get('identifiers')}, not {urn}")
    graph = get(f"{API}/datasets/{dataset_uuid}/structures/exports/JsonLd")
    graph = sorted(graph, key=lambda n: n["@id"])
    ttl = get(f"{API}/datasets/{dataset_uuid}/structures/exports/Ttl", raw=True)

    dataset_url = f"{CATALOG}/datasets/{record['identifiers'][0]}/description"
    schema = compact(graph, concepts)
    schema = {"credential": credential_id, "dataset": record["identifiers"][0],
              "dataset_url": dataset_url, **schema}
    table = render(credential_id, record, schema, dataset_url)
    title = (record.get("title") or {}).get("en") or (record.get("title") or {}).get("de") or credential_id

    dump = lambda o: json.dumps(o, ensure_ascii=False, indent=1, sort_keys=True) + "\n"
    files = {
        out / "dataset.json": dump(record),
        out / "structure.jsonld": dump(graph),
        out / "schema.json": dump(schema),
        out / "README.md": (
            f"# {title}: schema federated from I14Y\n\n"
            f"Generated by `scripts/i14y_sync.py` from the public I14Y API. Do not edit:\n"
            f"I14Y is the authoritative source. Credential entry: "
            f"[`credentials/{credential_id}.md`](../../../credentials/{credential_id}.md).\n\n"
            f"Exports: [`structure.ttl`](structure.ttl) (SHACL, Turtle) · "
            f"[`structure.jsonld`](structure.jsonld) · [`schema.json`](schema.json) (compact) · "
            f"[`dataset.json`](dataset.json) (dataset record)\n\n" + table
        ),
        ROOT / "_includes" / "i14y" / f"{credential_id}.md": table,
    }
    # The Turtle export is only rewritten when the structure itself changed,
    # so a reordered serialisation never shows up as a change.
    old_graph = (out / "structure.jsonld").read_text(encoding="utf-8") if (out / "structure.jsonld").exists() else None
    if old_graph != files[out / "structure.jsonld"] or not (out / "structure.ttl").exists():
        files[out / "structure.ttl"] = ttl

    changed = []
    for f, content in files.items():
        f.parent.mkdir(parents=True, exist_ok=True)
        if not f.exists() or f.read_text(encoding="utf-8") != content:
            f.write_text(content, encoding="utf-8")
            changed.append(str(f.relative_to(ROOT)))
    return credential_id, changed


def catalogue():
    """Every credential dataset on I14Y, whatever its registration status."""
    rows = []
    for d in get(f"{API}/datasets").get("data", []):
        urn = next((i for i in d.get("identifiers") or [] if i.startswith("urn:vct:")), None)
        if not urn:
            continue
        title = d.get("title") or {}
        pub = d.get("publisher") or {}
        rows.append({
            "identifier": urn,
            "title": title.get("en") or title.get("de") or urn,
            "title_de": title.get("de") or "",
            "publisher": pub.get("identifier") or "",
            "publisher_name": (pub.get("name") or {}).get("en") or (pub.get("name") or {}).get("de") or "",
            "registration_status": d.get("registrationStatus") or "",
            "id": d["id"],
            "url": f"{CATALOG}/datasets/{urn}/description",
        })
    rows.sort(key=lambda r: r["identifier"])
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=list(rows[0]) if rows else ["identifier"], lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
    out = ROOT / "_data" / "i14y-credentials.csv"
    if not out.exists() or out.read_text(encoding="utf-8") != buf.getvalue():
        out.write_text(buf.getvalue(), encoding="utf-8")
        print(f"i14y catalogue: updated, {len(rows)} credential datasets")
    else:
        print(f"i14y catalogue: unchanged, {len(rows)} credential datasets")


def main():
    catalogue()
    concepts = concept_index()
    for path in sorted((ROOT / "credentials").glob("*.md")):
        if path.name.startswith(("_", "README")):
            continue
        result = sync(path, concepts)
        if result:
            cid, changed = result
            print(f"{cid}: {'updated ' + ', '.join(changed) if changed else 'unchanged'}")


if __name__ == "__main__":
    main()
