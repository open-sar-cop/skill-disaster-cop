# skill-disaster-cop — AI Skill for Auto-Generating Disaster COP Dashboards

**English** | [简体中文](README.zh-CN.md)

> Lets an AI assistant respond to a new disaster by automatically searching public information → assembling standardized data → generating an interactive COP (Common Operating Picture) dashboard.
> AI execution entry point of the [Open SAR-COP](https://github.com/open-sar-cop) project · [Incident index](https://github.com/open-sar-cop/incidents) · [Homepage](https://open-sar-cop.github.io)

All outputs are **bilingual: English by default, Simplified Chinese alongside**.

## What is this

A self-contained Agent Skill package. Any AI assistant that supports loading skills (WorkBuddy, Claude Code, etc.) can load this directory and respond to requests like:

- "Create a COP dashboard for this Nepal landslide"
- "Turn the public information about this earthquake into a situation map"
- "生成台风灾情看板"

## Layout

```
skill-disaster-cop/
├── SKILL.md                      # Skill instructions (workflow + hard rules, EN + 中文)
├── assets/
│   ├── incident.schema.json      # Incident data contract (bilingual *_zh fields)
│   ├── template.html             # COP dashboard template (EN default, 中文 toggle)
│   └── build_cop.py              # Zero-dependency builder (validate + render)
└── examples/
    └── np-rasuwa-landslide-2026.json   # Full bilingual example
```

## Manual usage (without an AI)

```bash
python3 assets/build_cop.py examples/np-rasuwa-landslide-2026.json \
  -t assets/template.html -o out/index.html
```

## Bilingual data convention

Primary fields in `incident.json` are English (the default display language); Simplified Chinese goes into optional `*_zh` fields:

```json
{ "title": "Nepal Rasuwa Catastrophic Landslide 2026", "title_zh": "尼泊尔热索瓦（Rasuwa）特大泥石流灾害" }
```

The dashboard renders English by default and switches to Chinese with one click (remembered in localStorage). If a `*_zh` field is missing, it falls back to the primary field.

## Hard data rules

See "Hard rules" in SKILL.md: mandatory sourcing, mandatory timeliness/attribution, approximate-location labeling, zero PII, and map compliance for events in China. These rules cannot be removed.

## License

MIT © Open SAR-COP Contributors
