# Glossary

- Trial: one fresh `codex exec --ephemeral` invocation with exactly one prompt and no resume/follow-up.
- Arm: one of `control` or `treatment`.
- Control arm: the experiment directory whose `AGENTS.md` contains only the neutral source-of-truth instruction.
- Treatment arm: the experiment directory whose `AGENTS.md` adds the optional-commentary suppression instruction.
- Primary endpoint: whether the final assistant answer is correct for the candy prompt.
- Correct answer: an unambiguous final answer of `21` candies.
- Secondary endpoint: a non-primary metric used for mechanism or sensitivity analysis.
- H516: exploratory strict falsifiable hypothesis that `reasoning_tokens == 516` implies the final answer is not correct.
- Raw artifact: unmodified stdout, stderr, JSON event stream, prompt snapshot, AGENTS snapshot, or per-trial metadata saved before parsing.
- ITT-style analysis: analysis over all scheduled trials, treating unresolved/non-completed trials as incorrect for correctness.
- Completed-only analysis: sensitivity analysis over completed trials with resolved correctness.
- Guarded path: a CPA/public proxy path that may retry and hide `reasoning_tokens == 516` responses before the client sees them.
