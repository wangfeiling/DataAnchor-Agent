# Step 1 方法

## 保真与增强

增强不是“替业务方补答案”，而是把原始表达变成结构清晰、可讨论、可验收的业务需求。每个增强结论都引用 source requirement ID，并区分原文、用户确认和分析推断。

## Requirement atom

每个 atom 包含：

- `requirement_id`、`business_goal`、`consumer`；
- `subject`、`business_event_or_state`；
- `business_grain`：使用“一行/一次/一个……”的业务语言；
- `scope_in`、`scope_out`；
- `time_semantics`：事件时间、统计窗口、时区、自然日/业务日/账期；
- `business_rules`、`expected_output`；
- `priority`、`dependencies`；
- `source_requirement_ids`、`acceptance_criteria_ids`。

若一句话包含不同主体、事件、粒度、时间窗口或验收结果，拆成多个 atom。若只是同一业务概念的展示属性，保留在业务输出中，不提前猜测物理字段。

## 主动检查的隐含问题

- 统计主体与去重主体是否一致；
- 事件发生、创建、支付、结算、入库等时间的区别；
- 当前状态、历史状态、日快照或区间状态；
- 取消、退款、删除、测试、迟到和重复数据的业务处理；
- 组织、渠道、区域、产品和用户范围；
- 金额单位、币种、汇率、含税/未税；
- 历史起点、时效、SLA、权限与保留期。

只提出问题或列出解释分支，不查询知识库寻找答案。

## 验收条件

用给定—当—则或同等可判断结构，覆盖正常情况、时间边界、排除规则、冲突场景和对账预期。验收只描述业务观察结果，不指定 Hive 字段实现。
