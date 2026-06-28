# Codex Candy Commentary Study

这个仓库保存一次 Codex 糖果题实验的复现程序和脱敏数据。README 只说明如何复现；实验结果请看 `reports/可复现实验报告.md`。

## 前置条件

只复算公开数据需要：

- Python 3.11+

完整重跑实验还需要：

- Codex CLI 可用
- 已登录可用的 Codex/ChatGPT auth
- 可访问 `gpt-5.5`
- 当前环境支持 `model_reasoning_effort="xhigh"`

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

## 完整重跑实验

完整重跑会重新调用 Codex，消耗 quota。模型服务有随机性和时间漂移，重跑结果应视为新的实验批次。

```bash
python -m py_compile scripts/run_experiment.py scripts/analyze_results.py
python scripts/run_experiment.py --total 200 --concurrency 8 --seed 20260628
python scripts/analyze_results.py
```

`run_experiment.py` 默认设置：

```text
model = gpt-5.5
model_reasoning_effort = xhigh
trials = 200
control = 100
treatment = 100
concurrency = 8
```

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

## 隐私边界

这个仓库不包含本次实验的 raw stdout/stderr/events。

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
