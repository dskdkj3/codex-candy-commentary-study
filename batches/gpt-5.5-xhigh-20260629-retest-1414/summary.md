# gpt-5.5-xhigh-20260629-retest-1414 public batch summary

- model: `gpt-5.5`
- reasoning effort: `xhigh`
- trials: `200` (`100 control` + `100 treatment`)
- concurrency: `8`
- seed: `20260628`
- correctness field: `strict_correct`
- raw stdout/stderr/events and full final text are not included.
- first attempt: `189 completed`, `7 api_error`, `4 timeout`; failures were retried to produce `200 completed` rows.

## Completion

- status: `{'completed': 200}`
- parser_status: `{'resolved': 193, 'ambiguous': 7}`

## Correctness

| arm | correct | incorrect | n | rate | 95% Wilson CI |
| --- | ---: | ---: | ---: | ---: | --- |
| control | 19 | 81 | 100 | 19.0% | 12.5% - 27.8% |
| treatment | 32 | 68 | 100 | 32.0% | 23.7% - 41.7% |

- Fisher exact p-value: `0.0509454`

## Reasoning Token Markers

| metric | control | treatment | total | Fisher p |
| --- | ---: | ---: | ---: | ---: |
| `reasoning_output_tokens == 516` | 77/100 | 59/100 | 136/200 | 0.00968759 |
| `reasoning_output_tokens == 1034` | 1/100 | 6/100 | 7/200 | 0.118405 |
| `reasoning_output_tokens = 518n - 2` | 96/100 | 98/100 | 194/200 | 0.682717 |

## Marker Correctness

| group | correct | incorrect | n | rate |
| --- | ---: | ---: | ---: | ---: |
| `516` | 0 | 136 | 136 | 0.0% |
| `non-516` | 51 | 13 | 64 | 79.7% |
| `1034` | 0 | 7 | 7 | 0.0% |
| `518n-2` | 46 | 148 | 194 | 23.7% |
| `non-lattice` | 5 | 1 | 6 | 83.3% |

## Timing And Tokens

| arm | wall ms median | wall ms p90 | TTFT ms median | output tokens median | reasoning tokens median | tps median |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| control | 23640.00 | 123832.00 | 20242.50 | 841.50 | 516.00 | 38.75 |
| treatment | 29416.50 | 133293.00 | 25306.00 | 889.00 | 516.00 | 38.99 |

## Final Integer Candidates

| final integer | count |
| --- | ---: |
| `29` | 102 |
| `21` | 51 |
| `36` | 9 |
| `27` | 7 |
| `35` | 6 |
| `28` | 4 |
| `30` | 4 |
| `23` | 3 |
| `20` | 2 |
| `34` | 2 |
| `25` | 2 |
| `22` | 1 |
| `4` | 1 |
| `24` | 1 |
| `33` | 1 |
| `31` | 1 |
| `32` | 1 |
| `11` | 1 |
| `26` | 1 |

## Reasoning Token Distribution Summary

- unique values: `22`
- min: `471`
- median: `516.00`
- max: `10358`

| reasoning_output_tokens | count | correct |
| ---: | ---: | ---: |
| 471 | 1 | 0 |
| 516 | 136 | 0 |
| 1034 | 7 | 0 |
| 2070 | 1 | 1 |
| 2588 | 6 | 6 |
| 3106 | 6 | 5 |
| 3623 | 1 | 1 |
| 3624 | 7 | 6 |
| 3985 | 1 | 1 |
| 4035 | 1 | 1 |
| 4142 | 5 | 4 |
| 4660 | 6 | 6 |
| 5178 | 3 | 3 |
| 5696 | 4 | 4 |
| 6214 | 2 | 1 |
| 6598 | 1 | 1 |
| 6732 | 2 | 2 |
| 7250 | 6 | 5 |
| 7768 | 1 | 1 |
| 8286 | 1 | 1 |
| 8792 | 1 | 1 |
| 10358 | 1 | 1 |
