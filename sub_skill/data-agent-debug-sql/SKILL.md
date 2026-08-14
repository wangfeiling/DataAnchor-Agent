---
name: data-agent-debug-sql
description: 为 Hive Data Agent 的 QA 或 Spec 生成安全、只读、具备分区边界的 Hive SQL 验证脚本，检查字段存在性、业务粒度唯一性、空值、枚举、分区新鲜度、TTL、Join fanout、SCD 重叠、指标对账和回填规模。用于可选联调和排障；默认只生成不执行，禁止 DDL/DML，并明确 Hive 方言、参数、成本边界和关联 claim。
---

# Optional: Hive SQL 调试验证

## 启动前

1. 完整读取 [../../references/evidence-policy.md](../../references/evidence-policy.md)。
2. 读取 [references/method.md](references/method.md)，并使用 [../../template/debug-sql-runbook-template.md](../../template/debug-sql-runbook-template.md)。

## 流程

1. 将每个待验证事项转换为 check ID，并关联 claim、requirement 或 test。
2. 定义通过条件、失败含义和下一步动作；阈值必须有依据。
3. 生成只读 Hive SQL，明确数据库、表、字段、分区窗口和参数类型。
4. 优先元数据与低成本聚合，再生成 fanout、对账或 `EXPLAIN`。
5. 输出 `debug-checks.sql`、`debug-runbook.md` 和 `debug-sql-handoff.json`。
6. 默认 `execution_status = NOT_RUN`；只有用户明确要求并具备安全查询能力时才执行。

## 安全边界

- 允许 `SELECT`、`WITH`、`EXPLAIN`、`SHOW`、`DESCRIBE` 等只读语句。
- 禁止 `INSERT`、`UPDATE`、`DELETE`、`MERGE`、`CREATE`、`ALTER`、`DROP`、`TRUNCATE`、授权和过程调用。
- 禁止无分区限制扫描大型 Hive 表、`SELECT *` 和不必要的敏感明细输出。
- 未执行的脚本不得产生“已验证”“数据正确”等结论。
