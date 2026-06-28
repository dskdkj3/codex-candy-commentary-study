# gpt-5.3-codex-spark-xhigh public batch summary

- model: `gpt-5.3-codex-spark`
- reasoning effort: `xhigh`
- trials: `200` (`100 control` + `100 treatment`)
- concurrency: `8`
- seed: `20260628`
- correctness field: `strict_correct`
- raw stdout/stderr/events and full final text are not included.

## Completion

- status: `{'completed': 200}`
- parser_status: `{'resolved': 199, 'ambiguous': 1}`

## Correctness

| arm | correct | incorrect | n | rate | 95% Wilson CI |
| --- | ---: | ---: | ---: | ---: | --- |
| control | 0 | 100 | 100 | 0.0% | 0.0% - 3.7% |
| treatment | 0 | 100 | 100 | 0.0% | 0.0% - 3.7% |

- Fisher exact p-value: `1`

## Reasoning Token Markers

| metric | control | treatment | total | Fisher p |
| --- | ---: | ---: | ---: | ---: |
| `reasoning_output_tokens == 516` | 0/100 | 0/100 | 0/200 | 1 |
| `reasoning_output_tokens = 518n - 2` | 0/100 | 0/100 | 0/200 | 1 |

## Marker Correctness

| group | correct | incorrect | n | rate |
| --- | ---: | ---: | ---: | ---: |
| `516` | 0 | 0 | 0 | NA |
| `non-516` | 0 | 200 | 200 | 0.0% |
| `518n-2` | 0 | 0 | 0 | NA |
| `non-lattice` | 0 | 200 | 200 | 0.0% |

## Timing And Tokens

| arm | wall ms median | wall ms p90 | TTFT ms median | output tokens median | reasoning tokens median | tps median |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| control | 9310.50 | 12814.00 | 7694.00 | 3364.00 | 3043.50 | 349.97 |
| treatment | 9326.50 | 12223.90 | 7610.50 | 3434.00 | 3134.00 | 368.27 |

## Final Integer Candidates

| final integer | count |
| --- | ---: |
| `29` | 194 |
| `28` | 3 |
| `32` | 1 |
| `17` | 1 |
| `30` | 1 |

## Reasoning Token Distribution Summary

- unique values: `190`
- min: `1399`
- median: `3109.00`
- max: `6950`

| reasoning_output_tokens | count | correct |
| ---: | ---: | ---: |
| 3148 | 2 | 0 |
| 1958 | 2 | 0 |
| 2987 | 2 | 0 |
| 2790 | 2 | 0 |
| 1742 | 2 | 0 |
| 4611 | 2 | 0 |
| 3404 | 2 | 0 |
| 2333 | 2 | 0 |
| 4613 | 2 | 0 |
| 3694 | 2 | 0 |
| 4407 | 1 | 0 |
| 3754 | 1 | 0 |
| 2413 | 1 | 0 |
| 5759 | 1 | 0 |
| 2509 | 1 | 0 |
| 4466 | 1 | 0 |
| 3679 | 1 | 0 |
| 3527 | 1 | 0 |
| 2950 | 1 | 0 |
| 3434 | 1 | 0 |
| 6950 | 1 | 0 |
| 2787 | 1 | 0 |
| 3237 | 1 | 0 |
| 6551 | 1 | 0 |
| 2530 | 1 | 0 |
| 3122 | 1 | 0 |
| 4282 | 1 | 0 |
| 5121 | 1 | 0 |
| 3421 | 1 | 0 |
| 2183 | 1 | 0 |
| 3243 | 1 | 0 |
| 2958 | 1 | 0 |
| 2644 | 1 | 0 |
| 3720 | 1 | 0 |
| 5224 | 1 | 0 |
| 1992 | 1 | 0 |
| 3088 | 1 | 0 |
| 2105 | 1 | 0 |
| 4222 | 1 | 0 |
| 3139 | 1 | 0 |
