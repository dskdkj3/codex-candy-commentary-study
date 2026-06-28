# Codex Candy Commentary Study

这个仓库保存一次关于 Codex 糖果题现象的可复现实验程序和脱敏结果。

实验问题很窄：在项目级 `AGENTS.md` 中加入

```text
DO NOT send optional commentary unless explicitly asked to do so.
```

是否会影响 `gpt-5.5` + `xhigh` 在糖果题上的最终正确率，以及是否会降低 `reasoning_output_tokens == 516` 的出现率。

## TL;DR

本批次没有观察到 commentary suppression 的显著收益：

| 分组 | 答对 | 样本数 | 正确率 | `516` 样本 | `516` 率 |
| --- | ---: | ---: | ---: | ---: | ---: |
| `control` | 34 | 100 | 34.0% | 65 | 65.0% |
| `treatment` | 31 | 100 | 31.0% | 64 | 64.0% |

- 正确率 Fisher exact p-value: `0.762839`
- `516` 率 Fisher exact p-value: `1`
- `reasoning_output_tokens == 516`: `0/129` 答对
- `reasoning_output_tokens != 516`: `65/71` 答对

本批次更强的发现是：`516` 和错误答案高度绑定。本轮没有观察到任何 `516` 且答对的反例。

## Repository Name

推荐仓库名：

```text
codex-candy-commentary-study
```

理由：这是一次针对 commentary suppression 与 `516` 现象的实验研究，不是通用 benchmark；`study` 比 `eval` 更准确。

## What Was Tested

两组都包含一个项目级 `AGENTS.md`，避免“是否存在项目指令文件”成为混杂变量。

`control`:

```text
Use the task prompt as the source of truth for this experiment.
```

`treatment`:

```text
Use the task prompt as the source of truth for this experiment.
DO NOT send optional commentary unless explicitly asked to do so.
```

主实验设置：

- model: `gpt-5.5`
- reasoning effort: `xhigh`
- `control`: 100 trials
- `treatment`: 100 trials
- concurrency: 8
- trial unit: one fresh `codex exec --ephemeral`
- prompt: `prompts/candy.txt`

## Results

中文完整报告：

- `reports/可复现实验报告.md`

公开数据：

- `data/runs_sanitized.jsonl`
- `data/runs.csv`
- `data/non516_wrong.csv`
- `data/schedule.jsonl`
- `data/adjudication_output.jsonl`

数据字段说明：

- `docs/data-dictionary.md`

## Non-516 Wrong Pattern

非 `516` 的错误样本并不是随机分散。本批次里：

```text
非 516 样本: 71
非 516 且答错: 6
这些错误全部是 reasoning_output_tokens == 1034
这些错误全部最终答 29
```

详见：

- `data/non516_wrong.csv`

## Reproduce The Analysis

只复算公开数据，不重新调用模型：

```bash
python scripts/analyze_results.py
```

输出：

```text
reports/generated-summary.md
```

## Rerun The Experiment

重新跑完整实验会消耗 Codex quota，并且模型服务有随机性和时间漂移，结果应视为新的实验批次。

```bash
python -m py_compile scripts/run_experiment.py scripts/analyze_results.py
python scripts/run_experiment.py --total 200 --concurrency 8 --seed 20260628
python scripts/analyze_results.py
```

要求：

- Codex CLI 可用
- 已登录可用的 Codex/ChatGPT auth
- 可访问 `gpt-5.5`
- 当前环境支持 `model_reasoning_effort="xhigh"`

## Privacy Boundary

这个仓库不包含本次实验的 raw stdout/stderr/events。

没有公开的内容包括：

- raw stderr/stdout/events
- per-trial raw meta
- full final assistant messages
- local paths
- thread IDs
- account/auth 相关运行时日志

公开数据只保留 token、耗时、正确性、数字候选和 final text SHA256。

## Why Not Use `ai.tomandjerry2026.xyz` For This Run

本次主实验没有使用 `https://ai.tomandjerry2026.xyz/v1`，因为该 public CPA path 有 reasoning guard，可能对 `reasoning_output_tokens == 516` 的响应做重试。那会改变自然 `516` 频率，适合做另一个 guarded-path replication，不适合作为这次主实验。

## Caveats

- 单日期、单 Codex CLI 版本、单账号/auth path、单模型设置、单 prompt。
- 后端模型行为可能随时间变化。
- 8 个 parser-ambiguous 样本使用 blind LLM adjudication。
- 这个结果不证明 `516` 是逻辑充分条件，只说明本批次没有观察到 `516` 且答对的反例。

## License

License is not selected yet.
