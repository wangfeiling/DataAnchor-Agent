# Step 2 方法

## 数据项分类

| 类型 | 重点核验 |
|---|---|
| 维度 | 规范名称、业务键、属性、层次、历史变化、未知值 |
| 指标 | 定义、主体、粒度、窗口、过滤、去重、可加性、维度限制 |
| 标识 | 唯一范围、稳定性、空值、跨系统映射 |
| 时间 | 业务含义、时区、精度、分区关系 |
| 状态 | 枚举、有效期、终态/中间态、未知值 |
| 属性 | 含义、类型、单位、空值、敏感级别 |
| 规则 | 输入、逻辑、版本、适用域和例外 |

## 指标复用类型

- `DIRECT_REUSE`：定义、粒度、时间窗口、过滤和可用维度完全满足。
- `FILTERED_REUSE`：规范指标可复用，但需在允许维度上增加过滤；不得改变指标定义。
- `DERIVED_REUSE`：由一个或多个规范指标做有依据的二次计算；列出公式、单位与边界。
- `NO_REUSABLE_METRIC`：没有可复用定义；标记新增口径需求，不在本阶段自行批准新指标。

同名不代表可复用。任何复用都记录指标 ID、版本、owner、适用域和 evidence。

## 字段来源记录

每项包含：`mapping_id`、`requirement_id`、`item_type`、`business_term`、`source_table`、`source_field_or_expression`、`definition`、`data_type`、`unit`、`time_semantics`、`null_semantics`、`enum_or_domain`、`filter_or_transform`、`mapping_status`、`claim_ids`。

`mapping_status` 使用 `VERIFIED`、`PARTIAL`、`MISSING` 或 `CONFLICTED`。派生表达式必须列出全部原子来源。

## 来源表关系

记录每张表承载的数据项、业务粒度、业务时间、连接键候选和已知限制。若需主表，选择最能承载业务粒度和主体事件的 driving source；辅表必须说明用途。Join 基数若未验证，留给 Step 4 的实现检查，但在本阶段标记风险。
