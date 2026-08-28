# skill-disaster-cop — 灾害 COP 自动生成 AI 技能

[English](README.md) | **简体中文**

> 让 AI 助手在新灾害发生时，自动检索公开信息 → 组装标准数据 → 生成可交互的 COP（Common Operating Picture）态势图。
> [Open SAR-COP](https://github.com/open-sar-cop) 项目的 AI 执行入口 · [事件索引](https://github.com/open-sar-cop/incidents) · [项目主页](https://open-sar-cop.github.io)

所有产出**双语：默认英文，简体中文对照**。

## 这是什么

一个自包含的 Agent Skill 包。任何支持加载 Skill 的 AI 助手（WorkBuddy、Claude Code 等）加载本目录后，即可响应这类请求：

- "为这次尼泊尔泥石流做一个灾情态势图"
- "帮我把这次地震的公开信息做成 COP dashboard"
- "Create a COP dashboard for this typhoon"

## 组成

```
skill-disaster-cop/
├── SKILL.md                      # 技能指令（工作流 + 硬性规则，英文 + 中文）
├── assets/
│   ├── incident.schema.json      # 数据契约（支持 *_zh 双语字段）
│   ├── template.html             # COP 仪表盘模板（默认英文，可切中文）
│   └── build_cop.py              # 零依赖构建器（校验 + 渲染）
└── examples/
    └── np-rasuwa-landslide-2026.json   # 完整双语样例
```

## 手动使用（不经 AI）

```bash
python3 assets/build_cop.py examples/np-rasuwa-landslide-2026.json \
  -t assets/template.html -o out/index.html
```

## 双语数据约定

`incident.json` 主字段为英文（默认显示语言），简体中文写入可选的 `*_zh` 字段：

```json
{ "title": "Nepal Rasuwa Catastrophic Landslide 2026", "title_zh": "尼泊尔热索瓦（Rasuwa）特大泥石流灾害" }
```

仪表盘默认渲染英文，一键切换中文（localStorage 记忆）。`*_zh` 字段缺失时自动回退到主字段。

## 硬性数据规则

见 SKILL.md "Hard rules"：来源强制、时效与口径强制、近似坐标标注、零 PII、中国境内事件地图合规。这些规则不可移除。

## License

MIT © Open SAR-COP Contributors
