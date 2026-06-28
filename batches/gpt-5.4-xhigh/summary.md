# gpt-5.4-xhigh public batch summary

- model: `gpt-5.4`
- reasoning effort: `xhigh`
- trials: `200` (`100 control` + `100 treatment`)
- concurrency: `8`
- seed: `20260628`
- correctness field: `strict_correct`
- raw stdout/stderr/events and full final text are not included.

## Completion

- status: `{'completed': 200}`
- parser_status: `{'resolved': 194, 'ambiguous': 6}`

## Correctness

| arm | correct | incorrect | n | rate | 95% Wilson CI |
| --- | ---: | ---: | ---: | ---: | --- |
| control | 71 | 29 | 100 | 71.0% | 61.5% - 79.0% |
| treatment | 71 | 29 | 100 | 71.0% | 61.5% - 79.0% |

- Fisher exact p-value: `1`

## Reasoning Token Markers

| metric | control | treatment | total | Fisher p |
| --- | ---: | ---: | ---: | ---: |
| `reasoning_output_tokens == 516` | 20/100 | 18/100 | 38/200 | 0.857169 |
| `reasoning_output_tokens = 518n - 2` | 37/100 | 36/100 | 73/200 | 1 |

## Marker Correctness

| group | correct | incorrect | n | rate |
| --- | ---: | ---: | ---: | ---: |
| `516` | 1 | 37 | 38 | 2.6% |
| `non-516` | 141 | 21 | 162 | 87.0% |
| `518n-2` | 30 | 43 | 73 | 41.1% |
| `non-lattice` | 112 | 15 | 127 | 88.2% |

## Timing And Tokens

| arm | wall ms median | wall ms p90 | TTFT ms median | output tokens median | reasoning tokens median | tps median |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| control | 115659.50 | 204490.70 | 26532.00 | 6104.00 | 5694.00 | 53.49 |
| treatment | 112361.00 | 216584.20 | 106611.50 | 5935.50 | 5546.50 | 53.39 |

## Final Integer Candidates

| final integer | count |
| --- | ---: |
| `21` | 142 |
| `29` | 39 |
| `28` | 4 |
| `36` | 4 |
| `25` | 2 |
| `23` | 2 |
| `26` | 1 |
| `9` | 1 |
| `3` | 1 |
| `20` | 1 |
| `17` | 1 |
| `11` | 1 |
| `27` | 1 |

## Reasoning Token Distribution Summary

- unique values: `144`
- min: `516`
- median: `5662.50`
- max: `16482`

| reasoning_output_tokens | count | correct |
| ---: | ---: | ---: |
| 516 | 38 | 1 |
| 4660 | 4 | 4 |
| 5696 | 4 | 4 |
| 4142 | 3 | 3 |
| 1034 | 3 | 0 |
| 6732 | 3 | 3 |
| 7768 | 3 | 3 |
| 9322 | 2 | 2 |
| 5178 | 2 | 2 |
| 2070 | 2 | 0 |
| 5376 | 2 | 1 |
| 6214 | 2 | 2 |
| 6565 | 1 | 1 |
| 9087 | 1 | 1 |
| 11912 | 1 | 1 |
| 7382 | 1 | 1 |
| 1552 | 1 | 0 |
| 5405 | 1 | 1 |
| 7717 | 1 | 1 |
| 11971 | 1 | 1 |
| 5663 | 1 | 1 |
| 7232 | 1 | 1 |
| 13416 | 1 | 1 |
| 6649 | 1 | 1 |
| 15980 | 1 | 1 |
| 12371 | 1 | 1 |
| 10029 | 1 | 1 |
| 5959 | 1 | 1 |
| 5362 | 1 | 1 |
| 6202 | 1 | 1 |
| 12331 | 1 | 1 |
| 10358 | 1 | 1 |
| 10065 | 1 | 1 |
| 5220 | 1 | 1 |
| 6571 | 1 | 1 |
| 8869 | 1 | 1 |
| 11771 | 1 | 1 |
| 4615 | 1 | 1 |
| 4630 | 1 | 1 |
| 9840 | 1 | 1 |
