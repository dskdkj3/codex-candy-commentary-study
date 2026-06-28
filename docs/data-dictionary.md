# Data Dictionary

公开数据集位于 `data/runs_sanitized.jsonl` 和 `data/runs.csv`。这两个文件不包含 raw stderr/stdout/events，也不包含完整 final assistant message。

| 字段 | 含义 |
| --- | --- |
| `run_id` | 稳定 trial ID。 |
| `scheduled_order` | 随机化 schedule 中的顺序。 |
| `arm` | `control` 或 `treatment`。 |
| `status` | trial 状态；本批次全部是 `completed`。 |
| `parser_correct` | deterministic parser 的初始正确性判定。 |
| `adjudicated_correct` | 最终用于分析的正确性判定。 |
| `parser_status` | parser 状态；`ambiguous` 样本经过 blind adjudication。 |
| `reasoning_output_tokens` | Codex `turn.completed.usage.reasoning_output_tokens`。 |
| `reasoning_tokens_is_516` | `reasoning_output_tokens == 516`。 |
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
