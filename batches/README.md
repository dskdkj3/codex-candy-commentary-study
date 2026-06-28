# Public Experiment Batches

这个目录保存三轮 Codex 糖果题实验的公开脱敏 per-trial 数据。

| batch | model | effort | trials | correctness field | notes |
| --- | --- | --- | ---: | --- | --- |
| [`gpt-5.5-xhigh`](./gpt-5.5-xhigh/summary.md) | `gpt-5.5` | `xhigh` | 200 | `adjudicated_correct` | 不包含 raw artifacts 和完整 final text |
| [`gpt-5.4-xhigh`](./gpt-5.4-xhigh/summary.md) | `gpt-5.4` | `xhigh` | 200 | `strict_correct` | 不包含 raw artifacts 和完整 final text |
| [`gpt-5.3-codex-spark-xhigh`](./gpt-5.3-codex-spark-xhigh/summary.md) | `gpt-5.3-codex-spark` | `xhigh` | 200 | `strict_correct` | 不包含 raw artifacts 和完整 final text |

每个批次包含：

- `manifest.json`: 不含本机绝对路径的公开运行元数据。
- `summary.md`: 用公开脱敏行重算的摘要。
- `data/runs_sanitized.jsonl`: 脱敏 per-trial JSONL。
- `data/runs.csv`: 脱敏 per-trial CSV。
- `data/schedule.jsonl`: 随机化 schedule。

根目录原有 `data/` 保留为第一轮 `gpt-5.5-xhigh` 批次的兼容入口。
