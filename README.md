# Codex Candy Commentary Study

这个仓库保存 Codex 糖果题实验的复现程序和脱敏数据。README 只说明如何复现和读取数据；实验结果请看各批次 `summary.md` 或 `reports/可复现实验报告.md`。

## 完整重跑实验

完整重跑会重新调用 Codex，消耗 quota。模型服务有随机性和时间漂移，重跑结果应视为新的实验批次。

前置条件：

- Python 3.11+
- Codex CLI 可用
- 已登录可用的 Codex/ChatGPT auth，或准备好兼容 endpoint 的 key 文件
- 可访问目标模型；公开 runner 默认跑 `gpt-5.5`
- 当前环境支持 `model_reasoning_effort="xhigh"`

默认复现本仓第一轮 `gpt-5.5 xhigh` 设置：

```bash
git clone git@github.com:dskdkj3/codex-candy-commentary-study.git
cd codex-candy-commentary-study
python -m py_compile scripts/run_experiment.py scripts/analyze_results.py
python scripts/run_experiment.py --total 200 --concurrency 8 --seed 20260628
```

如果使用脚本内置的 OpenAI-compatible guarded endpoint：

```bash
python scripts/run_experiment.py \
  --total 200 \
  --concurrency 8 \
  --seed 20260628 \
  --provider-mode ai_public_guarded \
  --ai-public-key-file /path/to/key.txt
```

常用参数：

- `--total`：总样本数，必须是偶数；默认 `200`
- `--concurrency`：并发数；默认 `8`
- `--seed`：交替随机化 schedule 的 seed；本次公开主实验使用 `20260628`
- `--limit`：只跑前 N 个 pending trials，适合冒烟测试
- `--timeout-seconds`：单个 trial 超时秒数；默认 `300`

脚本默认设置：

```text
model = gpt-5.5
model_reasoning_effort = xhigh
trials = 200
control = 100
treatment = 100
concurrency = 8
```

重跑产物：

```text
manifest.json
parsed/schedule.jsonl
parsed/runs.jsonl
raw/
```

`raw/` 和未脱敏的 `parsed/runs.jsonl` 可能包含完整回答、thread ID、本机路径和 provider 运行信息，不要直接公开。每次完整重跑建议使用全新 clone，或先移走旧的 `raw/`、`parsed/` 和 `manifest.json`；脚本会根据已有 `parsed/schedule.jsonl` 和 `parsed/runs.jsonl` 续跑 pending trials。

如需重跑其它模型，复制脚本或修改 `scripts/run_experiment.py` 里的 `build_argv()`/`write_manifest()` 模型字段，然后把新结果作为新的独立批次保存。

## 快速复算公开数据

这一步不会调用模型，不消耗 quota。

```bash
git clone git@github.com:dskdkj3/codex-candy-commentary-study.git
cd codex-candy-commentary-study
python -m py_compile scripts/analyze_results.py
python scripts/analyze_results.py
```

输出文件：

```text
reports/generated-summary.md
```

输入数据：

```text
data/runs_sanitized.jsonl
data/runs.csv
data/non516_wrong.csv
data/schedule.jsonl
data/adjudication_output.jsonl
```

`data/` 保留第一轮 `gpt-5.5 xhigh` 批次，兼容最初的复现脚本。

## 实验输入

Prompt：

```text
prompts/candy.txt
```

Control arm：

```text
arms/control/AGENTS.md
```

Treatment arm：

```text
arms/treatment/AGENTS.md
```

## 数据说明

字段说明见：

```text
docs/data-dictionary.md
```

实验协议和决策记录：

```text
docs/protocol.md
docs/decisions.md
docs/glossary.md
```

公开报告：

```text
reports/可复现实验报告.md
```

## 四轮公开批次数据

四轮非敏感数据位于：

```text
batches/gpt-5.5-xhigh/
batches/gpt-5.5-xhigh-20260629-retest-1414/
batches/gpt-5.4-xhigh/
batches/gpt-5.3-codex-spark-xhigh/
```

每个批次包含：

```text
manifest.json
summary.md
data/runs_sanitized.jsonl
data/runs.csv
data/schedule.jsonl
```

reasoning token 对比点表位于：

```text
analysis/reasoning-token-comparison/
```

## 隐私边界

这个仓库不包含这些实验批次的 raw stdout/stderr/events。

没有公开的内容包括：

- raw stderr/stdout/events
- per-trial raw meta
- full final assistant messages
- local paths
- thread IDs
- account/auth 相关运行时日志

公开数据只保留 token、耗时、正确性、数字候选和 final text SHA256。

## 致谢与参考

- 糖果题 prompt 和初始 CLI eval 思路参考了 [`haowang02/codex-candy-eval`](https://github.com/haowang02/codex-candy-eval)。
- 感谢 Linux.do 社区相关讨论提供实验动机。

## License

MIT
