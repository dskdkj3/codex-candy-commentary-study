# Decisions

## D1 Primary endpoint

Use final answer correctness as the primary endpoint. Treat `reasoning_tokens == 516` as a secondary/mechanistic endpoint.

## D2 Trial unit

One fresh `codex exec --ephemeral` invocation is one trial. Do not use TUI multi-turn sessions, `resume`, or follow-up messages as independent samples.

## D3 H516

Record H516 as an exploratory strict falsifiable hypothesis: any trial with `reasoning_tokens == 516` and a correct final answer falsifies the strict form.

## D4 Configuration isolation

Use the smallest practical Codex invocation that still preserves working ChatGPT authentication. Disable memories, use empty arm directories, and fix model/reasoning flags explicitly.

## D5 Treatment contrast

The only intended arm difference is the optional-commentary suppression instruction in `arms/treatment/AGENTS.md`.

## D6 Prompt

Use the exact prompt text from `haowang02/codex-candy-eval` as the main prompt. Later prompt variants must be separate phases.

## D7 Adjudication

Use deterministic parsing for unambiguous answers. Use blind LLM adjudication only for parser-ambiguous final messages, with adjudicator input limited to the final assistant message.

## D8 Failure retention

No scheduled trial may disappear. Failed, timed-out, parse-error, and CLI-error trials remain in the ledger.

## D9 Retry policy

Do not retry in place. Additional retry evidence must use a new trial id and `retry_of`, and must not replace the original scheduled trial.

## D10 Initial sample size

Run 200 scheduled trials: 100 control and 100 treatment, with concurrency 8.

## D11 Model

Use `gpt-5.5` with `model_reasoning_effort="xhigh"` for this run. `gpt-5.3-codex-spark` is a later separate experiment.

## D12 Public AI key

Do not use `https://ai.tomandjerry2026.xyz/v1` for the primary natural-behavior experiment because the documented CPA reasoning guard retries `reasoning_tokens == 516` responses. A new AI public client key may be used later for a separate guarded-path replication.
