---
name: disaster-cop
description: Disaster Common Operating Picture (COP) dashboard auto-generation skill. Use when the user asks to "create a COP", "generate a situation map / disaster dashboard", or "visualize disaster impact" for an earthquake, landslide, debris flow, flood, typhoon, avalanche or search-and-rescue event. Searches public reporting, assembles incident.json per the data contract, and renders an interactive single-file dashboard (map, KPIs, casualty trend, timeline, response forces). Bilingual output: English by default, one-click switch to Simplified Chinese. 触发词：COP、态势图、灾情看板、灾害 dashboard、搜救态势、灾情可视化、common operating picture。
---

# Disaster COP — Disaster Common Operating Picture Generation Skill

Turn the public information about a natural disaster into an interactive COP (Common Operating Picture). This skill is the AI execution entry point of the [Open SAR-COP](https://github.com/open-sar-cop) project. Each generated incident is archived in its own repo named after the event (e.g. [np-rasuwa-landslide-2026](https://github.com/open-sar-cop/np-rasuwa-landslide-2026)); the global index lives in [incidents](https://github.com/open-sar-cop/incidents).

> **Language policy**: all content (READMEs, docs, dashboards, data) is bilingual — **English is the default**, Simplified Chinese is the secondary language. In incident.json, primary fields are English; Chinese goes into `*_zh` fields (e.g. `title_zh`, `summary_zh`, kpi `label_zh`). The dashboard renders English by default and toggles to Chinese.

## Assets (in this skill directory)

| File | Purpose |
|---|---|
| `assets/incident.schema.json` | Incident data contract (the single source of truth for assembling data) |
| `assets/template.html` | COP dashboard template (bilingual EN/中文, `__TITLE__` / `__COP_DATA__` placeholders) |
| `assets/build_cop.py` | Builder: validate + render → single-file HTML |
| `examples/np-rasuwa-landslide-2026.json` | Full bilingual example: Nepal Rasuwa landslide 2026 |

## Workflow

### Step 1: Confirm the event and its sources

- If the user provided a data file → read it and map it onto the schema
- If not → use WebSearch to gather authoritative information (priority: official bulletins > national news agencies / wire services > local media). Focus on:
  - Event metadata: type, onset time (with timezone), region, current status
  - Casualty figures: **every number needs a timestamp and attribution** (e.g. "as of Aug 27 evening, per Nepal Police")
  - Infrastructure damage: roads, bridges, power, telecom, border crossings
  - Response forces: military / police / fire / medical / international coordination, and their tasks
  - Place names of key sites: for approximate geocoding
- If information is thin, **search first, then ask** — never pass off vague assumptions as facts

### Step 2: Assemble incident.json (bilingual)

- Strictly follow `assets/incident.schema.json`; all required fields must be present (the builder enforces this)
- Slug naming: `<country-code>-<region>-<hazard-type>-<year>`, e.g. `np-rasuwa-landslide-2026`
- **English first**: primary fields (`title`, `summary`, kpi `label`/`note`, site `name`/`description`, resource `tasks`, update `text`, source `name`) are written in English; add `*_zh` variants for Simplified Chinese (see the example file)
- Design 4–8 KPI cards: casualties / missing / infrastructure damage / affected extent
- Six site categories: `incident` (hazard site) / `damage` (damaged infrastructure) / `community` (affected settlement) / `command` (command & coordination) / `resource` (response asset) / `risk` (risk zone)
- Coordinates may be approximated from place names, but **every site description must state "approximate location"**（坐标为近似定位）
- Express rivers / roads as `corridor.coords` polylines and note "schematic trace, not exact"
- Casualty evolution goes into `casualty_series`; event progress goes into `updates` (newest first)
- `sources` is required and must not be empty; record name, URL, date for each

### Step 3: Generate the COP

```bash
python3 <skill-dir>/assets/build_cop.py <incident.json path> \
  -t <skill-dir>/assets/template.html \
  -o <output-dir>/<slug>/index.html
```

(Any python3 works; the script has zero third-party dependencies.)

### Step 4: Deliver

- Present the generated HTML with present_files
- State in your reply: data as-of time, attribution, known uncertainties
- Remind the user: figures change as the disaster evolves; with new bulletins, update `casualty_series` / `updates` and regenerate

## Hard rules (violations = rework)

1. **Sources mandatory**: no data without sources may enter incident.json
2. **Timeliness mandatory**: every casualty / damage figure must carry "as-of time + attribution"
3. **Approximation labeling**: estimated coordinates and schematic corridors must be explicitly labeled, never presented as precise
4. **Zero PII**: do not collect or store any personally identifiable information (victim or missing-person lists, etc.)
5. **Map compliance**: use OpenStreetMap basemaps for events outside China; **for events inside China**, use compliant basemaps (Tianditu etc.) and map content from the Ministry of Natural Resources standard map service — **never draw national or administrative boundaries yourself**
6. **Disclaimer**: the template's footer disclaimer must not be removed; also state in your reply that the COP is "for situational awareness only, not the sole basis for rescue decisions"
7. **Bilingual mandatory**: primary fields in English, `*_zh` fields for Chinese; do not deliver monolingual Chinese data

## Data update mode (while the event is active)

When the user provides new bulletins:
1. Update the affected KPI's value / note (+ `*_zh` counterparts)
2. Append the new time point to `casualty_series`
3. Insert the new entry at the head of `updates`
4. Update `last_updated`, re-run the builder

## 中文说明（快速参考）

本技能把一次自然灾害的公开信息变成可交互的 COP 态势图，是 [Open SAR-COP](https://github.com/open-sar-cop) 的 AI 执行入口。

- **双语规则**：所有内容英文默认、中文对照。incident.json 主字段写英文，中文写入 `*_zh` 字段（如 `title_zh`、`label_zh`）；仪表盘默认英文，右上角一键切换中文。
- **流程**：确认事件与信息源（官方通报 > 央媒/通讯社 > 地方媒体）→ 按 schema 组装双语 incident.json → 运行 `assets/build_cop.py` 生成单文件 HTML → 展示并说明数据截至时间与口径。
- **硬性规则**：无来源数据不录入；伤亡数字必须带"截至时间 + 口径"；近似坐标必须标注；零 PII；涉中国境内事件必须用合规底图且不得自绘国界；不得移除免责声明。
- **更新模式**：新通报到达时更新 KPI / `casualty_series` / `updates` 与 `last_updated`（中英同步），重新生成。
