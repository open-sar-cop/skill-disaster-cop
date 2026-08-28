#!/usr/bin/env python3
"""Open SAR-COP builder: incident.json + template -> single-file COP dashboard.

Bilingual by design: primary data fields are English (default display),
optional *_zh fields provide Simplified Chinese; the dashboard has an
EN/中文 toggle.

Usage:
    python3 build_cop.py <incident.json> [-o output.html] [-t template.html]

Template lookup order:
    1. -t/--template explicit path
    2. template.html next to this script     (skill assets layout)
    3. ../template/index.html                (cop-kit repo layout)
"""
import argparse
import json
import sys
from pathlib import Path

REQUIRED_FIELDS = [
    "slug", "title", "event_type", "country", "onset",
    "status", "severity", "last_updated", "summary",
    "kpis", "sites", "updates", "sources",
]


def find_template(explicit: str | None) -> Path:
    if explicit:
        p = Path(explicit)
        if p.is_file():
            return p
        sys.exit(f"[error] template not found: {p}")
    here = Path(__file__).resolve().parent
    for cand in (here / "template.html", here.parent / "template" / "index.html"):
        if cand.is_file():
            return cand
    sys.exit("[error] template not found; pass -t template.html")


def main() -> None:
    ap = argparse.ArgumentParser(description="Build a disaster COP dashboard (single-file HTML, EN default + 中文)")
    ap.add_argument("incident", help="path to incident.json (per incident.schema.json)")
    ap.add_argument("-o", "--output", help="output HTML path; default dist/<slug>/index.html")
    ap.add_argument("-t", "--template", help="template path")
    args = ap.parse_args()

    incident_path = Path(args.incident)
    if not incident_path.is_file():
        sys.exit(f"[error] incident data not found: {incident_path}")
    data = json.loads(incident_path.read_text(encoding="utf-8"))

    missing = [f for f in REQUIRED_FIELDS if f not in data or data[f] in (None, "")]
    if missing:
        sys.exit(f"[error] incident.json is missing required fields: {', '.join(missing)}")
    if not data.get("sources"):
        sys.exit("[error] sources must not be empty: a disaster COP must cite its data sources")
    bad_sites = [s.get("name", "?") for s in data["sites"] if not all(k in s for k in ("lat", "lon", "category"))]
    if bad_sites:
        sys.exit(f"[error] these sites lack lat/lon/category: {', '.join(bad_sites)}")

    template = find_template(args.template)
    tpl = template.read_text(encoding="utf-8")

    payload = json.dumps(data, ensure_ascii=False, indent=None).replace("<", "\\u003c")
    html_out = tpl.replace("__TITLE__", f"{data['title']} · COP").replace("__COP_DATA__", payload)

    out = Path(args.output) if args.output else Path("dist") / data["slug"] / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html_out, encoding="utf-8")
    print(f"[OK] COP generated: {out}")
    print(f"     incident: {data['slug']} | sites: {len(data['sites'])} | KPIs: {len(data['kpis'])} | sources: {len(data['sources'])}")
    print(f"     bilingual: {'yes (has *_zh fields)' if '_zh' in payload else 'EN only'}")


if __name__ == "__main__":
    main()
