# Codex Candy Commentary Experiment Protocol

## Objective

Test whether adding an optional-commentary suppression instruction to project `AGENTS.md` changes Codex candy-prompt correctness under `gpt-5.5` with xhigh reasoning.

## Arms

Control `AGENTS.md`:

```text
Use the task prompt as the source of truth for this experiment.
```

Treatment `AGENTS.md`:

```text
Use the task prompt as the source of truth for this experiment.
DO NOT send optional commentary unless explicitly asked to do so.
```

## Prompt

The prompt is stored in `prompts/candy.txt` and is copied from `haowang02/codex-candy-eval`.

## Endpoints

Primary endpoint:

- final answer correctness: correct only when the final assistant message gives an unambiguous answer of `21` candies.

Secondary endpoints:

- `reasoning_tokens == 516`
- reasoning token count
- output token count
- input token count
- total wall time
- TTFT
- tokens per second
- timeout/API/CLI/error rate
- tool-call/event counts

Exploratory H516:

- Strict hypothesis: `reasoning_tokens == 516` implies the final answer is not correct.
- Falsification rule: any completed trial with `reasoning_tokens == 516` and correct final answer falsifies strict H516.

## Trial Unit

One fresh `codex exec --ephemeral` invocation is one trial. A trial must:

- use exactly one prompt
- run in either `arms/control` or `arms/treatment`
- not use `resume`
- not include follow-up user messages
- save raw artifacts before parsing

## Model And Invocation

Main run:

- model: `gpt-5.5`
- reasoning effort: `xhigh`
- scheduled trials: 200 total, 100 per arm
- concurrency: 8
- randomized blocked order

The command must fix model and reasoning effort explicitly. The runner must record exact argv, `codex --version`, environment summary, arm, prompt hash, and `AGENTS.md` hash.

## Provider Boundary

Primary experiment uses the smallest practical Codex invocation with current ChatGPT auth. It must not use `https://ai.tomandjerry2026.xyz/v1` because the documented CPA reasoning guard retries responses with abnormal reasoning token counts such as `516`, which would confound the H516 and treatment-effect measurements.

The runner may support an AI public client key file for later guarded-path replication, but such runs must be marked `provider_mode=ai_public_guarded` and excluded from this primary report.

## Data Retention

No scheduled trial may disappear.

Every attempted trial must produce or reference:

- run id
- arm
- scheduled order
- start/end timestamp
- command argv
- cwd
- prompt hash and prompt snapshot path
- `AGENTS.md` hash and snapshot path
- exit code, if any
- timeout/error classification, if any
- paths to raw stdout/stderr/jsonl artifacts
- parser/adjudicator status
- timing fields when available

Raw artifacts are append-only and must not be overwritten.

## Failure And Retry Policy

All scheduled trials are recorded. Status values include:

- `completed`
- `timeout`
- `api_error`
- `cli_error`
- `parse_error`
- `adjudication_needed`
- `adjudication_failed`

Primary ITT-style analysis uses all scheduled trials and treats unresolved/non-completed trials as incorrect for correctness. Completed-only sensitivity analysis includes only completed trials with resolved correctness.

Do not retry in place. If extra evidence is needed, create a new trial id with `retry_of=<failed_run_id>` and report retries separately.

## Timing Metrics

Record:

- scheduled_at
- dispatch_at
- process_start_at
- first_stdout_at
- first_stderr_at
- first_json_event_at
- first_assistant_delta_at, if available
- first_final_message_at, if available
- process_end_at
- wall_ms
- queue_ms
- ttft_ms
- `ttft_kind`
- tokens per second, if token usage and timing are available

TTFT is the time from `process_start_at` to first observed assistant output event. If no assistant delta event exists, use first JSON event and mark `ttft_kind`.

## Analysis

Primary:

- Fisher exact test for correctness between arms.
- Report proportions, absolute difference, odds ratio, and confidence intervals where available.

Secondary:

- Fisher exact test for `reasoning_tokens == 516`.
- H516 contingency table and falsification result.
- Token and timing distributions by arm.
- Error/timeout rate by arm.

Do not pool future Spark results into this report.
