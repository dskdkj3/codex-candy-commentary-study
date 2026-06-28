#!/usr/bin/env python3
"""Analyze the public sanitized Codex candy commentary dataset."""

from __future__ import annotations

import json
import math
import statistics
from collections import Counter
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "runs_sanitized.jsonl"
OUT = ROOT / "reports" / "generated-summary.md"


def read_rows() -> list[dict]:
    return [json.loads(line) for line in DATA.read_text(encoding="utf-8").splitlines() if line.strip()]


def fisher_two_sided(a: int, b: int, c: int, d: int) -> float:
    r1 = a + b
    r2 = c + d
    col1 = a + c
    n = r1 + r2

    def prob(x: int) -> float:
        return math.comb(col1, x) * math.comb(n - col1, r1 - x) / math.comb(n, r1)

    lo = max(0, r1 - (n - col1))
    hi = min(r1, col1)
    p_obs = prob(a)
    return sum(prob(x) for x in range(lo, hi + 1) if prob(x) <= p_obs + 1e-12)


def wilson(k: int, n: int, z: float = 1.959963984540054) -> tuple[float, float]:
    phat = k / n
    denom = 1 + z * z / n
    center = (phat + z * z / (2 * n)) / denom
    margin = z * math.sqrt((phat * (1 - phat) + z * z / (4 * n)) / n) / denom
    return (center - margin, center + margin)


def pct(x: float) -> str:
    return f"{x * 100:.1f}%"


def median(values: Iterable[int | float | None]) -> float | None:
    vals = [v for v in values if isinstance(v, (int, float))]
    return statistics.median(vals) if vals else None


def counter_text(counter: Counter) -> str:
    return ", ".join(f"{key}: {value}" for key, value in counter.most_common())


def arm_counts(rows: list[dict], metric: str) -> dict[str, tuple[int, int]]:
    result = {}
    for arm in ["control", "treatment"]:
        subset = [row for row in rows if row["arm"] == arm]
        result[arm] = (sum(1 for row in subset if row[metric]), len(subset))
    return result


def main() -> int:
    rows = read_rows()
    correctness = arm_counts(rows, "adjudicated_correct")
    r516 = arm_counts(rows, "reasoning_tokens_is_516")

    c_ok, c_n = correctness["control"]
    t_ok, t_n = correctness["treatment"]
    correctness_p = fisher_two_sided(c_ok, c_n - c_ok, t_ok, t_n - t_ok)

    c_516, c516_n = r516["control"]
    t_516, t516_n = r516["treatment"]
    r516_p = fisher_two_sided(c_516, c516_n - c_516, t_516, t516_n - t_516)

    h516_rows = [row for row in rows if row["reasoning_tokens_is_516"]]
    non_h516_rows = [row for row in rows if not row["reasoning_tokens_is_516"]]
    h516_ok = sum(1 for row in h516_rows if row["adjudicated_correct"])
    non_h516_ok = sum(1 for row in non_h516_rows if row["adjudicated_correct"])
    h516_p = fisher_two_sided(
        h516_ok,
        len(h516_rows) - h516_ok,
        non_h516_ok,
        len(non_h516_rows) - non_h516_ok,
    )

    reasoning_counts = Counter(row["reasoning_output_tokens"] for row in rows)
    non516_wrong = [
        row for row in rows if not row["reasoning_tokens_is_516"] and not row["adjudicated_correct"]
    ]
    lattice_rows = [row for row in rows if (row["reasoning_output_tokens"] + 2) % 518 == 0]
    off_lattice_rows = [row for row in rows if (row["reasoning_output_tokens"] + 2) % 518 != 0]

    lines = [
        "# Generated Summary",
        "",
        f"Rows: `{len(rows)}`",
        "",
        "## Correctness",
        "",
        "| arm | correct | n | rate | 95% Wilson CI |",
        "| --- | ---: | ---: | ---: | --- |",
    ]
    for arm, (ok, n) in correctness.items():
        lo, hi = wilson(ok, n)
        lines.append(f"| {arm} | {ok} | {n} | {pct(ok / n)} | {pct(lo)} - {pct(hi)} |")
    lines.extend(["", f"Fisher exact p-value: `{correctness_p:.6g}`", "", "## Reasoning Tokens 516", ""])
    lines.extend(["| arm | 516 | n | rate |", "| --- | ---: | ---: | ---: |"])
    for arm, (count, n) in r516.items():
        lines.append(f"| {arm} | {count} | {n} | {pct(count / n)} |")
    lines.extend(
        [
            "",
            f"Fisher exact p-value: `{r516_p:.6g}`",
            "",
            "## H516",
            "",
            f"- `reasoning_tokens == 516`: `{h516_ok}/{len(h516_rows)}` correct",
            f"- `reasoning_tokens != 516`: `{non_h516_ok}/{len(non_h516_rows)}` correct",
            f"- Fisher exact p-value: `{h516_p:.6g}`",
            "",
            "## Non-516 Wrong Samples",
            "",
            f"- Count: `{len(non516_wrong)}`",
            f"- Reasoning token buckets: `{dict(Counter(row['reasoning_output_tokens'] for row in non516_wrong))}`",
            "",
            "## Reasoning Token Distribution",
            "",
            "| reasoning_output_tokens | count |",
            "| ---: | ---: |",
        ]
    )
    for value, count in sorted(reasoning_counts.items()):
        lines.append(f"| {value} | {count} |")
    lines.extend(
        [
            "",
            "## Reasoning Token Lattice",
            "",
            f"- Exact matches for `reasoning_output_tokens = 518 * k - 2`: "
            f"`{len(lattice_rows)}/{len(rows)}`",
            f"- Off-lattice samples: `{len(off_lattice_rows)}`",
            "",
            "| reasoning_output_tokens | count | k if exact | residual vs nearest `518*k - 2` | mod 512 | correct | final integer candidates |",
            "| ---: | ---: | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for value, count in sorted(reasoning_counts.items()):
        exact_k = (value + 2) // 518 if (value + 2) % 518 == 0 else None
        nearest_k = round((value + 2) / 518)
        residual = value - (518 * nearest_k - 2)
        subset = [row for row in rows if row["reasoning_output_tokens"] == value]
        ok = sum(1 for row in subset if row["adjudicated_correct"])
        candidates = Counter(row.get("final_integer_candidate") for row in subset)
        lines.append(
            f"| {value} | {count} | {exact_k if exact_k is not None else ''} | "
            f"{residual} | {value % 512} | {ok} | {counter_text(candidates)} |"
        )
    lines.extend(
        [
            "",
            "| group | n | correct | final candidate 21 | final candidate 29 | median output tokens | median TTFT ms |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    groups = [
        ("516 / k=1", lambda row: row["reasoning_output_tokens"] == 516),
        ("1034 / k=2", lambda row: row["reasoning_output_tokens"] == 1034),
        (
            "non-516 exact lattice",
            lambda row: row["reasoning_output_tokens"] != 516
            and (row["reasoning_output_tokens"] + 2) % 518 == 0,
        ),
        ("off lattice", lambda row: (row["reasoning_output_tokens"] + 2) % 518 != 0),
    ]
    for label, predicate in groups:
        subset = [row for row in rows if predicate(row)]
        lines.append(
            f"| {label} | {len(subset)} | {sum(1 for row in subset if row['adjudicated_correct'])} | "
            f"{sum(1 for row in subset if row.get('final_integer_candidate') == '21')} | "
            f"{sum(1 for row in subset if row.get('final_integer_candidate') == '29')} | "
            f"{median(row['output_tokens'] for row in subset):.2f} | "
            f"{median(row['ttft_ms'] for row in subset):.2f} |"
        )
    lines.extend(
        [
            "",
            "## Timing",
            "",
            "| arm | median wall ms | median TTFT ms | median output tokens | median reasoning tokens |",
            "| --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for arm in ["control", "treatment"]:
        subset = [row for row in rows if row["arm"] == arm]
        lines.append(
            f"| {arm} | {median(row['wall_ms'] for row in subset):.2f} | "
            f"{median(row['ttft_ms'] for row in subset):.2f} | "
            f"{median(row['output_tokens'] for row in subset):.2f} | "
            f"{median(row['reasoning_output_tokens'] for row in subset):.2f} |"
        )

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
