---
name: disaster-cop
description: 灾害通用态势图（COP/Dashboard）自动生成技能。当用户提到为地震、泥石流、山洪、台风、洪涝、滑坡、雪崩等自然灾害或搜救事件"创建 COP"、"生成态势图/灾情看板/dashboard"、"灾情可视化"时使用。基于公开报道检索信息，按数据契约组装 incident.json，一键渲染可交互的单文件态势仪表盘（地图、KPI、伤亡趋势、时间线、响应力量）。触发词：COP、态势图、灾情看板、灾害 dashboard、搜救态势、common operating picture。
---

# Disaster COP — 灾害通用态势图生成技能

把一次自然灾害的公开信息，变成一张可交互的 COP（Common Operating Picture）态势图。本技能是 [Open SAR-COP](https://github.com/open-sar-cop) 项目的 AI 执行入口，生成的每个事件数据归档于以事件命名的独立仓库（如 [np-rasuwa-landslide-2026](https://github.com/open-sar-cop/np-rasuwa-landslide-2026)），全局索引见 [incidents](https://github.com/open-sar-cop/incidents)。

## 资产清单（本技能目录内）

| 文件 | 用途 |
|---|---|
| `assets/incident.schema.json` | 灾害事件数据契约（组装数据的唯一依据） |
| `assets/template.html` | COP 仪表盘模板（含 `__TITLE__` / `__COP_DATA__` 占位符） |
| `assets/build_cop.py` | 构建器：校验 + 渲染，输出单文件 HTML |
| `examples/np-rasuwa-landslide-2026.json` | 完整样例：2026 尼泊尔热索瓦特大泥石流 |

## 执行流程

### 第 1 步：确认事件与信息源

- 若用户已提供数据文件 → 读取并映射到 schema
- 若未提供 → 用 WebSearch 检索权威信息（优先级：官方通报 > 央媒/通讯社 > 地方媒体），重点收集：
  - 事件元数据：类型、发生时间（含时区）、区域、当前状态
  - 伤亡数字：**每个数字都要有时间戳和口径**（如"截至 8/27 晚，警方口径"）
  - 基础设施损毁：道路、桥梁、电力、通信、口岸等
  - 响应力量：军队/警察/消防/医疗/国际协调，各自任务
  - 关键点位地名：用于近似定位坐标
- 信息不足时**先检索再询问**，不要拿模糊假设充当事实

### 第 2 步：组装 incident.json

- 严格遵循 `assets/incident.schema.json`，必填字段缺一不可（构建器会强制校验）
- slug 命名：`<国家二字码>-<地区>-<灾害类型>-<年份>`，如 `np-rasuwa-landslide-2026`
- KPI 设计 4-8 张卡片：伤亡/失联/设施损毁/受灾范围等
- 点位 6 类别：`incident`（灾害点）/`damage`（设施损毁）/`community`（受灾村镇）/`command`（指挥协调）/`resource`（救援力量）/`risk`（风险区）
- 坐标可用地名近似估测，但**每个点位描述必须注明"坐标为近似定位"**
- 河流/道路等线状风险用 `corridor.coords` 折线表达并注明"示意走向，非精确"
- 伤亡数字演进写入 `casualty_series`，事件进展写入 `updates`（新的在前）
- `sources` 必填且不可为空，逐条注明名称、URL、日期

### 第 3 步：生成 COP

```bash
/Users/echo/.workbuddy/binaries/python/versions/3.13.12/bin/python3 \
  <本技能目录>/assets/build_cop.py <incident.json 路径> \
  -t <本技能目录>/assets/template.html \
  -o <输出目录>/<slug>/index.html
```

（其他环境的 python3 同样可用，脚本零第三方依赖。）

### 第 4 步：交付

- 用 present_files 展示生成的 HTML
- 在回复中说明：数据截至时间、口径、已知不确定性
- 提醒用户：灾害发展中数字会变化，提供新通报后可更新 `casualty_series`/`updates` 重新生成

## 硬性规则（违反即返工）

1. **来源强制**：没有 sources 的数据不许进 incident.json
2. **时效强制**：所有伤亡/损毁数字必须带"截至时间 + 口径"
3. **近似标注**：估测坐标、示意廊道必须显式标注，不得伪装成精确定位
4. **零 PII**：不采集、不存储任何个人身份信息（遇难者/失联者名单等）
5. **地图合规**：境外事件用 OpenStreetMap 底图；**涉及中国境内的事件**必须使用合规底图（天地图等）与自然资源部标准地图服务提供的地图内容，**不得自行绘制国界、行政区域界线**
6. **免责声明**：模板页脚自带免责声明，不得移除；回复中也要说明"仅供态势参考，不作为救援决策唯一依据"

## 数据更新模式（事件进行中）

用户给出新通报时：
1. 更新对应 KPI 的 value/note
2. 在 `casualty_series` 追加新时间点
3. 在 `updates` 头部插入新条目
4. 更新 `last_updated`，重新运行构建器
