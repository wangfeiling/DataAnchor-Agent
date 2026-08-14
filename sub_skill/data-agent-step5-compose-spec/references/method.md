# Step 5 方法

## 版本锁定

在组装报告中列出每个输入 artifact ID、状态、生成时间和 supersedes 关系。只使用明确选定的版本，不自动读取目录中的“最新文件”。

## 追踪矩阵

每个 requirement 至少关联：Step 2 mapping/metric ID、Step 3 placement/table-change/extension ID、Step 4 target field/transform/test ID。未覆盖项不能标为完成；无需求支撑的目标字段必须说明治理用途或删除。

## 一致性检查

比较：

- Step 1 业务粒度与 Step 2 来源粒度、Step 3 目标粒度；
- 时间、时区、窗口、快照和迟到规则；
- 指标版本、过滤、聚合和维度限制；
- Hive 表字段全限定名与环境；
- ODS–ADS 层级、改表/建表和上游逐跳扩展；
- schema、类型、空值、单位、枚举、分区和 TTL；
- 调度、回填、质量、测试、发布、回滚与 owner。

发现不一致时指向产生差异的最早 artifact，不在 Step 5 裁决。

## 最终状态

最终状态不得优于仍有效的最弱上游核心状态。`PASS` 仅表示设计与证据链通过，不代表开发、SQL 执行、回填或业务验收已完成。
