# gpt-5.5-xhigh public batch summary

- model: `gpt-5.5`
- reasoning effort: `xhigh`
- trials: `200` (`100 control` + `100 treatment`)
- concurrency: `8`
- seed: `20260628`
- correctness field: `adjudicated_correct`
- raw stdout/stderr/events and full final text are not included.

## Completion

- status: `{'completed': 200}`
- parser_status: `{'resolved': 192, 'ambiguous': 8}`

## Correctness

| arm | correct | incorrect | n | rate | 95% Wilson CI |
| --- | ---: | ---: | ---: | ---: | --- |
| control | 34 | 66 | 100 | 34.0% | 25.5% - 43.7% |
| treatment | 31 | 69 | 100 | 31.0% | 22.8% - 40.6% |

- Fisher exact p-value: `0.762839`

## Reasoning Token Markers

| metric | control | treatment | total | Fisher p |
| --- | ---: | ---: | ---: | ---: |
| `reasoning_output_tokens == 516` | 65/100 | 64/100 | 129/200 | 1 |
| `reasoning_output_tokens = 518n - 2` | 98/100 | 96/100 | 194/200 | 0.682717 |

## Marker Correctness

| group | correct | incorrect | n | rate |
| --- | ---: | ---: | ---: | ---: |
| `516` | 0 | 129 | 129 | 0.0% |
| `non-516` | 65 | 6 | 71 | 91.5% |
| `518n-2` | 59 | 135 | 194 | 30.4% |
| `non-lattice` | 6 | 0 | 6 | 100.0% |

## Timing And Tokens

| arm | wall ms median | wall ms p90 | TTFT ms median | output tokens median | reasoning tokens median | tps median |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| control | 23210.50 | 112614.90 | 20427.50 | 899.50 | 516.00 | 40.98 |
| treatment | 21493.50 | 101913.20 | 19994.00 | 819.00 | 516.00 | 40.85 |

## Final Integer Candidates

| final integer | count |
| --- | ---: |
| `29` | 97 |
| `21` | 57 |
| `27` | 8 |
| `30` | 7 |
| `28` | 6 |
| `36` | 4 |
| `35` | 4 |
| `31` | 3 |
| `25` | 3 |
| `12` | 2 |
| `20` | 2 |
| `33` | 2 |
| `18` | 2 |
| `38` | 1 |
| `11` | 1 |
| `26` | 1 |

## Reasoning Token Distribution Summary

- unique values: `24`
- min: `516`
- median: `516.00`
- max: `10876`

| reasoning_output_tokens | count | correct |
| ---: | ---: | ---: |
| 516 | 129 | 0 |
| 4142 | 8 | 8 |
| 3624 | 8 | 8 |
| 3106 | 7 | 7 |
| 1034 | 6 | 0 |
| 4660 | 6 | 6 |
| 2588 | 5 | 5 |
| 5178 | 5 | 5 |
| 6214 | 5 | 5 |
| 5696 | 3 | 3 |
| 7250 | 2 | 2 |
| 7768 | 2 | 2 |
| 9840 | 2 | 2 |
| 6732 | 2 | 2 |
| 6160 | 1 | 1 |
| 8797 | 1 | 1 |
| 2070 | 1 | 1 |
| 10876 | 1 | 1 |
| 3407 | 1 | 1 |
| 5552 | 1 | 1 |
| 8804 | 1 | 1 |
| 7525 | 1 | 1 |
| 3060 | 1 | 1 |
| 8286 | 1 | 1 |
