#!/usr/bin/env python3
"""Open SAR-COP 构建器：incident.json + 模板 -> 单文件 COP 仪表盘。

用法:
    python3 build_cop.py <incident.json> [-o output.html] [-t template.html]

模板查找顺序:
    1. -t/--template 显式指定
    2. 脚本同目录下的 template.html      (skill assets 打包形态)
    3. 脚本上级目录 template/index.html   (cop-kit 仓库形态)
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
        sys.exit(f"[错误] 指定的模板不存在: {p}")
    here = Path(__file__).resolve().parent
    for cand in (here / "template.html", here.parent / "template" / "index.html"):
        if cand.is_file():
            return cand
    sys.exit("[错误] 找不到模板，请用 -t 指定 template.html 路径")


def main() -> None:
    ap = argparse.ArgumentParser(description="生成灾害 COP 仪表盘（单文件 HTML）")
    ap.add_argument("incident", help="incident.json 路径（符合 schema/incident.schema.json）")
    ap.add_argument("-o", "--output", help="输出 HTML 路径，默认 dist/<slug>/index.html")
    ap.add_argument("-t", "--template", help="模板路径")
    args = ap.parse_args()

    incident_path = Path(args.incident)
    if not incident_path.is_file():
        sys.exit(f"[错误] 事件数据不存在: {incident_path}")
    data = json.loads(incident_path.read_text(encoding="utf-8"))

    missing = [f for f in REQUIRED_FIELDS if f not in data or data[f] in (None, "")]
    if missing:
        sys.exit(f"[错误] incident.json 缺少必填字段: {', '.join(missing)}")
    if not data.get("sources"):
        sys.exit("[错误] sources 不能为空：灾害 COP 必须注明数据来源")
    bad_sites = [s.get("name", "?") for s in data["sites"] if not all(k in s for k in ("lat", "lon", "category"))]
    if bad_sites:
        sys.exit(f"[错误] 以下点位缺少 lat/lon/category: {', '.join(bad_sites)}")

    template = find_template(args.template)
    tpl = template.read_text(encoding="utf-8")

    payload = json.dumps(data, ensure_ascii=False, indent=None).replace("<", "\\u003c")
    html_out = tpl.replace("__TITLE__", f"{data['title']} · COP 态势图").replace("__COP_DATA__", payload)

    out = Path(args.output) if args.output else Path("dist") / data["slug"] / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html_out, encoding="utf-8")
    print(f"[OK] COP 已生成: {out}")
    print(f"     事件: {data['slug']} | 点位: {len(data['sites'])} | KPI: {len(data['kpis'])} | 来源: {len(data['sources'])}")


if __name__ == "__main__":
    main()
