# Hive Debug SQL Runbook

## 运行范围与安全声明

| 项目 | 内容 |
|---|---|
| Request / Artifact ID |  |
| Hive 环境/版本 |  |
| 日期/分区参数 |  |
| 扫描/成本边界 |  |
| 敏感数据限制 |  |
| 执行状态 | `NOT_RUN` |

## 检查清单

| Check ID | Claim/Requirement | 目的 | SQL 段 | 期望/阈值依据 | 失败动作 | Owner |
|---|---|---|---|---|---|---|

## 推荐执行顺序

`<元数据→分区→粒度→字段→Join→SCD→对账→回填规模→EXPLAIN>`

## 执行结果

| Check ID | 状态 | Hive Task ID | 扫描量 | 结果摘要 | Evidence ID |
|---|---|---|---|---|---|
