# Data Dictionary

第一轮公开数据集位于 `data/runs_sanitized.jsonl` 和 `data/runs.csv`。三轮公开批次位于 `batches/<batch>/data/`。这些文件不包含 raw stderr/stdout/events，也不包含完整 final assistant message。

| 字段 | 含义 |
| --- | --- |
| `run_id` | 稳定 trial ID。 |
| `scheduled_order` | 随机化 schedule 中的顺序。 |
| `arm` | `control` 或 `treatment`。 |
| `status` | trial 状态；本批次全部是 `completed`。 |
| `parser_correct` | deterministic parser 的初始正确性判定。 |
| `adjudicated_correct` | `gpt-5.5-xhigh` 批次最终用于分析的正确性判定。 |
| `strict_correct` | `gpt-5.4-xhigh` 和 `gpt-5.3-codex-spark-xhigh` 批次使用的严格 deterministic 正确性判定：`parser_status == resolved` 且最终数字候选为 `21`。 |
| `parser_status` | parser 状态；`ambiguous` 样本经过 blind adjudication。 |
| `reasoning_output_tokens` | Codex `turn.completed.usage.reasoning_output_tokens`。 |
| `reasoning_tokens_is_516` | `reasoning_output_tokens == 516`。 |
| `reasoning_tokens_is_518n_minus_2` | `reasoning_output_tokens` 是否符合 `518 * n - 2`。 |
| `input_tokens` | Codex usage 中的 input token 数。 |
| `cached_input_tokens` | Codex usage 中的 cached input token 数。 |
| `output_tokens` | Codex usage 中的 output token 数。 |
| `wall_ms` | 单次 `codex exec` 进程耗时，毫秒。 |
| `ttft_ms` | 到首个 final assistant message 的时间；无该事件时使用首个 JSON event fallback。 |
| `tokens_per_second` | `output_tokens / wall_seconds`。 |
| `final_text_sha256` | final assistant message 的 SHA256，用于核对同源样本，不公开正文。 |
| `final_integer_candidate` | parser 看到的最后一个独立数字候选。 |
| `integer_candidates` | parser 从 final message 中提取到的独立数字候选列表。 |
| `contains_21` | final message 中是否出现独立 `21`。 |
| `contains_516_text` | final message 中是否出现独立 `516`。 |

## Batch Layout

```text
batches/
  gpt-5.5-xhigh/
  gpt-5.4-xhigh/
  gpt-5.3-codex-spark-xhigh/
```

每个批次包含：

| 路径 | 含义 |
| --- | --- |
| `manifest.json` | 不含本机绝对路径的公开运行元数据。 |
| `summary.md` | 用公开脱敏数据重算出的批次摘要。 |
| `data/runs_sanitized.jsonl` | 脱敏 per-trial JSONL。 |
| `data/runs.csv` | 脱敏 per-trial CSV。 |
| `data/schedule.jsonl` | 随机化 trial schedule。 |

## Reasoning Token Comparison

`analysis/reasoning-token-comparison/` 包含三轮合并后的 reasoning token 点表。

| 字段 | 含义 |
| --- | --- |
| `batch` | 批次 ID，例如 `gpt-5.4-xhigh`。 |
| `model` | 模型名。 |
| `reasoning_effort` | reasoning effort。 |
| `correct_source` | `correct` 字段来自哪个源字段。 |
| `correct` | 该点使用对应批次主口径后的正确性。 |
| `reasoning_tokens_is_1034` | `reasoning_output_tokens == 1034`。 |
| `reasoning_tokens_is_518n_minus_2` | 是否落在 `518 * n - 2` 格点。 |
| `lattice_n` | 如果落在 `518 * n - 2`，这里记录 `n`。 |
| `lattice_residual` | 相对最近 `518 * n - 2` 格点的差值。 |

## Omitted From Public Dataset

以下内容没有放入公开仓库：

- `raw/stdout`
- `raw/stderr`
- `raw/events`
- per-trial raw `meta`
- complete `final_text`
- local paths
- thread IDs
- account/auth related runtime logs
