# 事实与证据政策

## Claim 状态

| 状态 | 含义 | 使用边界 |
|---|---|---|
| `VERIFIED` | 已由适合该事实类型的直接来源支持 | 可作为实现依据 |
| `USER_CONFIRMED` | 用户明确确认的需求或约束 | 可作为本次需求依据 |
| `USER_STATED` | 仅出现在原始需求，尚未外部核验 | 可作为业务需求，不可作为 Hive 物理事实 |
| `INFERRED` | 根据其他信息推断 | 只能作为候选或风险 |
| `UNKNOWN` | 缺少信息 | 不可形成确定结论 |
| `CONFLICTED` | 来源互相冲突 | 裁决前不可使用 |

## Evidence 字段

每条 evidence 至少记录：

- `evidence_id`、`source_type`、`locator`、`observed_at`；
- `supports`：支持的 claim ID；
- `summary`、`freshness`、`directness`；
- 必要时记录环境、知识库版本、Hive database/table、分区、查询任务 ID、代码版本和限制。

不要保存口令、令牌或不必要的敏感明细。

## 权威来源按事实类型选择

- 业务需求：原始需求文档与用户确认。
- 指标业务口径：已审批指标字典/指标知识库 > 用户确认 > 历史 SQL。
- Hive 表字段存在性：当前 Hive catalog/metastore 或只读查询 > 当前 DDL > 文档。
- 层级归属：组织分层登记或表元数据 > 仅由表名前缀推断。
- 血缘：当前运行/解析血缘和可定位 SQL > 手工文档。
- 新鲜度与 TTL：分区和任务运行事实 > 配置文档。
- 热度、召回分数和名称相似：只能用于召回或排序，不能证明语义正确。

## 冲突与新鲜度

同时保留冲突来源，先检查环境、版本、分区日期、同名对象和口径适用域。影响核心决策的冲突必须设为 blocking。Schema、层级、TTL、owner、血缘、调度和热度均需记录观测时间。

## 下游继承

下游不得静默升级上游状态。继承 claim 时填写 `origin_artifact_id`；新增物理事实必须拥有本阶段直接 evidence。Step 5 原则上只继承，不产生新的业务或架构事实。
