# Step 2: 字段来源与指标口径方案

## 1. 文档信息

| 项目 | 内容 |
|---|---|
| Request / Artifact ID |  |
| Step 1 输入版本 |  |
| 知识库版本/观测时间 |  |
| Hive 环境 |  |
| 状态 | `PASS / CONDITIONAL / BLOCKED` |

## 2. 需求项与检索计划

| Item ID | Requirement ID | 类型 | 业务术语 | 主体/粒度/时间 | 检索词 | 检索能力 |
|---|---|---|---|---|---|---|
| ITEM-001 | REQ-001 | 维度/指标/标识/时间/状态/属性/规则 |  |  |  |  |

## 3. 知识库检索记录

| Search ID | Item ID | 来源 | 查询/版本 | 命中 | Evidence ID | 限制 |
|---|---|---|---|---|---|---|
| SEARCH-001 | ITEM-001 |  |  |  |  |  |

## 4. 指标复用方案

| Metric Mapping ID | Requirement ID | 规范指标 ID/版本 | 复用类型 | 定义/公式 | 粒度与窗口 | 过滤/去重 | 可用维度 | Owner | Evidence | 状态 |
|---|---|---|---|---|---|---|---|---|---|---|
| METRIC-001 | REQ-001 |  | `DIRECT/FILTERED/DERIVED/NO_REUSE` |  |  |  |  |  |  |  |

## 5. 字段来源与口径

| Mapping ID | Requirement/Item ID | 业务项 | Hive 来源字段/表达式 | 类型 | 口径说明 | 单位/时间 | 空值/枚举 | 过滤/转换 | Evidence | 状态 |
|---|---|---|---|---|---|---|---|---|---|---|
| MAP-001 | REQ-001 / ITEM-001 |  | `database.table.column` |  |  |  |  |  |  |  |

## 6. Hive 来源表

| Source ID | Hive 表 | 承载需求项 | 业务粒度 | 业务时间 | 用途 | Join 键候选 | 限制 | Evidence |
|---|---|---|---|---|---|---|---|---|
| TABLE-001 | `database.table` |  |  |  | driving/auxiliary |  |  |  |

> 本阶段不判断目标 ODS/DWD/DIM/DWS/ADS 落层，不决定改表或新建表。

## 7. 冲突与缺失映射

| Item ID | 类型 | 当前结果 | 影响 | 验证动作 | Owner | Severity |
|---|---|---|---|---|---|---|
| O-201 |  |  |  |  |  |  |

## 8. Step 2 结论

`<字段/指标覆盖率、核心冲突、能否进入 Step 3>`
