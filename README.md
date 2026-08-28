# skill-disaster-cop — 灾害 COP 自动生成 AI 技能

> 让 AI 助手在新灾害发生时，自动检索公开信息 → 组装标准数据 → 生成可交互的 COP 态势图。
> [Open SAR-COP](https://github.com/open-sar-cop) 项目的 AI 执行入口 · [事件索引](https://github.com/open-sar-cop/incidents) · [项目主页](https://open-sar-cop.github.io)

## 这是什么

一个自包含的 Agent Skill 包。任何支持加载 Skill 的 AI 助手（WorkBuddy、Claude Code 等）加载本目录后，即可响应这类请求：

- "为这次尼泊尔泥石流做一个灾情态势图"
- "帮我把这次地震的公开信息做成 COP dashboard"
- "生成台风灾情看板"

## 组成

```
skill-disaster-cop/
├── SKILL.md                      # 技能指令（工作流 + 硬性规则）
├── assets/
│   ├── incident.schema.json      # 灾害事件数据契约
│   ├── template.html             # COP 仪表盘模板
│   └── build_cop.py              # 零依赖构建器（校验 + 渲染）
└── examples/
    └── np-rasuwa-landslide-2026.json   # 完整样例数据
```

## 手动使用（不经 AI）

```bash
python3 assets/build_cop.py examples/np-rasuwa-landslide-2026.json \
  -t assets/template.html -o out/index.html
```

## 硬性数据规则

见 SKILL.md "硬性规则"：来源强制、时效强制、近似坐标标注、零 PII、中国境内事件地图合规。这些规则不可移除。

## License

MIT © Open SAR-COP Contributors
