# Public Experiment Batches

这个目录保存四轮 Codex 糖果题实验的公开脱敏 per-trial 数据。

| batch | model | effort | trials | correctness field | notes |
| --- | --- | --- | ---: | --- | --- |
| [`gpt-5.5-xhigh`](./gpt-5.5-xhigh/summary.md) | `gpt-5.5` | `xhigh` | 200 | `adjudicated_correct` | 不包含 raw artifacts 和完整 final text |
| [`gpt-5.5-xhigh-20260629-retest-1414`](./gpt-5.5-xhigh-20260629-retest-1414/summary.md) | `gpt-5.5` | `xhigh` | 200 | `strict_correct` | 2026-06-29 下午重测；首跑失败索引已脱敏保留 |
| [`gpt-5.4-xhigh`](./gpt-5.4-xhigh/summary.md) | `gpt-5.4` | `xhigh` | 200 | `strict_correct` | 不包含 raw artifacts 和完整 final text |
| [`gpt-5.3-codex-spark-xhigh`](./gpt-5.3-codex-spark-xhigh/summary.md) | `gpt-5.3-codex-spark` | `xhigh` | 200 | `strict_correct` | 不包含 raw artifacts 和完整 final text |

每个批次包含：

- `manifest.json`: 不含本机绝对路径的公开运行元数据。
- `summary.md`: 用公开脱敏行重算的摘要。
- `data/runs_sanitized.jsonl`: 脱敏 per-trial JSONL。
- `data/runs.csv`: 脱敏 per-trial CSV。
- `data/schedule.jsonl`: 随机化 schedule。
- `data/first_attempt_failures.jsonl` / `data/first_attempt_failures.csv`: 仅部分重试批次包含；记录首跑失败的 run ID、状态、错误类别和耗时，不含 raw logs。

根目录原有 `data/` 保留为第一轮 `gpt-5.5-xhigh` 批次的兼容入口。
