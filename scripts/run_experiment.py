#!/usr/bin/env python3
"""Run the Codex candy commentary experiment with raw artifact retention."""

from __future__ import annotations

import argparse
import asyncio
import datetime as dt
import hashlib
import json
import os
import random
import re
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


EXP_DIR = Path(__file__).resolve().parents[1]
PROMPT_PATH = EXP_DIR / "prompts" / "candy.txt"
ARMS_DIR = EXP_DIR / "arms"
RAW_DIR = EXP_DIR / "raw"
PARSED_DIR = EXP_DIR / "parsed"
REPORTS_DIR = EXP_DIR / "reports"
SCHEDULE_PATH = PARSED_DIR / "schedule.jsonl"
RUNS_PATH = PARSED_DIR / "runs.jsonl"
MANIFEST_PATH = EXP_DIR / "manifest.json"

ANSWER_PATTERN = re.compile(r"(?<!\d)21(?!\d)")
INT_PATTERN = re.compile(r"(?<!\d)(\d+)(?!\d)")


def utc_now() -> str:
    return dt.datetime.now(dt.UTC).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_json(path: Path, data: dict[str, Any]) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    tmp.replace(path)


def append_jsonl(path: Path, data: dict[str, Any]) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False, sort_keys=True) + "\n")


def codex_version() -> str:
    try:
        proc = subprocess.run(["codex", "--version"], check=False, capture_output=True, text=True, timeout=10)
    except Exception as exc:  # noqa: BLE001
        return f"ERROR: {exc}"
    return (proc.stdout or proc.stderr).strip()


def build_argv(arm_dir: Path, provider_mode: str) -> list[str]:
    argv = [
        "codex",
        "--ask-for-approval",
        "never",
        "exec",
        "--json",
        "--ephemeral",
        "--skip-git-repo-check",
        "--sandbox",
        "read-only",
        "--disable",
        "memories",
        "--ignore-user-config",
        "-m",
        "gpt-5.5",
        "-c",
        'model_reasoning_effort="xhigh"',
        "--cd",
        str(arm_dir),
    ]
    if provider_mode == "ai_public_guarded":
        argv.extend(
            [
                "-c",
                'model_providers.ai_public_guarded.name="AI Public Guarded"',
                "-c",
                'model_providers.ai_public_guarded.base_url="https://ai.tomandjerry2026.xyz/v1"',
                "-c",
                'model_providers.ai_public_guarded.wire_api="responses"',
                "-c",
                'model_providers.ai_public_guarded.env_key="CODEX_CANDY_AI_PUBLIC_KEY"',
                "-c",
                'model_provider="ai_public_guarded"',
            ]
        )
    return argv


def load_or_create_schedule(total: int, seed: int) -> list[dict[str, Any]]:
    if SCHEDULE_PATH.exists():
        rows = []
        for line in SCHEDULE_PATH.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rows.append(json.loads(line))
        return rows

    if total % 2 != 0:
        raise ValueError("total must be even so arms are balanced")
    rng = random.Random(seed)
    blocks: list[str] = []
    for _ in range(total // 2):
        pair = ["control", "treatment"]
        rng.shuffle(pair)
        blocks.extend(pair)

    rows = []
    for idx, arm in enumerate(blocks, start=1):
        run_id = f"run-{idx:04d}-{arm}"
        row = {
            "run_id": run_id,
            "scheduled_order": idx,
            "arm": arm,
            "scheduled_at": utc_now(),
            "seed": seed,
            "retry_of": None,
        }
        rows.append(row)

    for row in rows:
        append_jsonl(SCHEDULE_PATH, row)
    return rows


def completed_run_ids() -> set[str]:
    if not RUNS_PATH.exists():
        return set()
    done = set()
    for line in RUNS_PATH.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        run_id = row.get("run_id")
        if run_id:
            done.add(run_id)
    return done


def classify_error(exit_code: int | None, timed_out: bool, stderr_tail: str, stdout_tail: str) -> str:
    if timed_out:
        return "timeout"
    text = f"{stderr_tail}\n{stdout_tail}".lower()
    if exit_code == 0:
        return "completed"
    if "401 unauthorized" in text or "429" in text or "api" in text or "unexpected status" in text:
        return "api_error"
    return "cli_error"


def parse_events(events: list[dict[str, Any]]) -> dict[str, Any]:
    final_text = ""
    usage: dict[str, Any] = {}
    item_counts: dict[str, int] = {}
    event_counts: dict[str, int] = {}
    thread_id = None
    error_message = None

    for event in events:
        event_type = event.get("type")
        if event_type:
            event_counts[event_type] = event_counts.get(event_type, 0) + 1
        if event_type == "thread.started":
            thread_id = event.get("thread_id") or thread_id
        if event_type == "item.completed":
            item = event.get("item") or {}
            item_type = item.get("type")
            if item_type:
                item_counts[item_type] = item_counts.get(item_type, 0) + 1
            if item_type == "agent_message":
                final_text = str(item.get("text") or "")
        elif event_type == "turn.completed":
            usage = event.get("usage") or {}
        elif event_type in {"error", "turn.failed"}:
            error = event.get("error") or {}
            error_message = event.get("message") or error.get("message") or error_message

    ints = INT_PATTERN.findall(final_text)
    distinct_ints = sorted(set(ints), key=ints.index)
    contains_21 = bool(ANSWER_PATTERN.search(final_text))
    contains_516 = bool(re.search(r"(?<!\d)516(?!\d)", final_text))
    final_integer = ints[-1] if ints else None
    parser_correct = contains_21
    parser_status = "resolved" if final_text else "no_final_message"
    if final_text and contains_21 and len(distinct_ints) > 1 and final_integer != "21":
        parser_status = "ambiguous"

    output_tokens = usage.get("output_tokens")
    reasoning_tokens = usage.get("reasoning_output_tokens")

    return {
        "thread_id": thread_id,
        "final_text": final_text,
        "final_text_sha256": sha256_text(final_text),
        "final_text_length": len(final_text),
        "integer_candidates": ints,
        "distinct_integer_candidates": distinct_ints,
        "final_integer_candidate": final_integer,
        "contains_21": contains_21,
        "contains_516_text": contains_516,
        "parser_correct": parser_correct,
        "parser_status": parser_status,
        "usage": usage,
        "input_tokens": usage.get("input_tokens"),
        "cached_input_tokens": usage.get("cached_input_tokens"),
        "output_tokens": output_tokens,
        "reasoning_output_tokens": reasoning_tokens,
        "reasoning_tokens_is_516": reasoning_tokens == 516,
        "event_counts": event_counts,
        "item_counts": item_counts,
        "error_message": error_message,
    }


async def read_stream(
    stream: asyncio.StreamReader,
    raw_path: Path,
    is_stdout: bool,
    timing: dict[str, Any],
    events: list[dict[str, Any]],
) -> None:
    with raw_path.open("wb") as raw:
        while True:
            line = await stream.readline()
            if not line:
                break
            now = time.monotonic_ns()
            raw.write(line)
            raw.flush()
            if is_stdout and timing.get("first_stdout_ns") is None:
                timing["first_stdout_ns"] = now
            if (not is_stdout) and timing.get("first_stderr_ns") is None:
                timing["first_stderr_ns"] = now
            if is_stdout:
                text = line.decode("utf-8", errors="replace").strip()
                if text.startswith("{"):
                    try:
                        event = json.loads(text)
                    except json.JSONDecodeError:
                        continue
                    events.append(event)
                    if timing.get("first_json_event_ns") is None:
                        timing["first_json_event_ns"] = now
                    if event.get("type") == "item.completed":
                        item = event.get("item") or {}
                        if item.get("type") == "agent_message" and timing.get("first_final_message_ns") is None:
                            timing["first_final_message_ns"] = now


def ns_delta_ms(start_ns: int | None, end_ns: int | None) -> int | None:
    if start_ns is None or end_ns is None:
        return None
    return round((end_ns - start_ns) / 1_000_000)


async def run_trial(
    row: dict[str, Any],
    args: argparse.Namespace,
    prompt_text: str,
    write_lock: asyncio.Lock,
) -> dict[str, Any]:
    run_id = row["run_id"]
    arm = row["arm"]
    arm_dir = ARMS_DIR / arm
    agents_path = arm_dir / "AGENTS.md"

    paths = {
        "events": RAW_DIR / "events" / f"{run_id}.jsonl",
        "stdout": RAW_DIR / "stdout" / f"{run_id}.txt",
        "stderr": RAW_DIR / "stderr" / f"{run_id}.txt",
        "meta": RAW_DIR / "meta" / f"{run_id}.json",
        "agents": RAW_DIR / "agents" / f"{run_id}.AGENTS.md",
        "prompt": RAW_DIR / "prompts" / f"{run_id}.prompt.txt",
    }

    for path in paths.values():
        path.parent.mkdir(parents=True, exist_ok=True)
    if any(path.exists() for path in paths.values()):
        raise RuntimeError(f"raw artifact already exists for {run_id}")

    agents_text = read_text(agents_path)
    paths["agents"].write_text(agents_text, encoding="utf-8")
    paths["prompt"].write_text(prompt_text, encoding="utf-8")

    argv = build_argv(arm_dir, args.provider_mode)
    env = os.environ.copy()
    env.setdefault("RUST_LOG", args.rust_log)
    provider_key_sha256 = None
    provider_key_file = None
    if args.provider_mode == "ai_public_guarded":
        if not args.ai_public_key_file:
            raise RuntimeError("--ai-public-key-file is required for ai_public_guarded")
        key_path = Path(args.ai_public_key_file)
        key = key_path.read_text(encoding="utf-8").strip()
        if not key:
            raise RuntimeError(f"empty AI public key file: {key_path}")
        env["CODEX_CANDY_AI_PUBLIC_KEY"] = key
        provider_key_sha256 = sha256_text(key)
        provider_key_file = str(key_path)

    scheduled_at = row.get("scheduled_at")
    dispatch_at = utc_now()
    dispatch_ns = time.monotonic_ns()
    timing: dict[str, Any] = {
        "first_stdout_ns": None,
        "first_stderr_ns": None,
        "first_json_event_ns": None,
        "first_final_message_ns": None,
    }
    events: list[dict[str, Any]] = []
    meta: dict[str, Any] = {
        "run_id": run_id,
        "arm": arm,
        "scheduled_order": row.get("scheduled_order"),
        "scheduled_at": scheduled_at,
        "dispatch_at": dispatch_at,
        "argv": argv,
        "cwd": str(arm_dir),
        "prompt_sha256": sha256_text(prompt_text),
        "agents_sha256": sha256_text(agents_text),
        "paths": {key: str(value) for key, value in paths.items()},
        "provider_mode": args.provider_mode,
        "provider_key_file": provider_key_file,
        "provider_key_sha256_prefix": provider_key_sha256[:16] if provider_key_sha256 else None,
        "retry_of": row.get("retry_of"),
        "status": "started",
    }
    write_json(paths["meta"], meta)

    process_start_at = utc_now()
    process_start_ns = time.monotonic_ns()
    proc = await asyncio.create_subprocess_exec(
        *argv,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        env=env,
    )
    assert proc.stdin is not None
    assert proc.stdout is not None
    assert proc.stderr is not None
    proc.stdin.write(prompt_text.encode("utf-8"))
    await proc.stdin.drain()
    proc.stdin.close()

    stdout_task = asyncio.create_task(read_stream(proc.stdout, paths["stdout"], True, timing, events))
    stderr_task = asyncio.create_task(read_stream(proc.stderr, paths["stderr"], False, timing, events))
    timed_out = False
    try:
        await asyncio.wait_for(proc.wait(), timeout=args.timeout_seconds)
    except asyncio.TimeoutError:
        timed_out = True
        proc.send_signal(signal.SIGTERM)
        try:
            await asyncio.wait_for(proc.wait(), timeout=10)
        except asyncio.TimeoutError:
            proc.kill()
            await proc.wait()
    await stdout_task
    await stderr_task
    process_end_ns = time.monotonic_ns()
    process_end_at = utc_now()

    with paths["events"].open("w", encoding="utf-8") as f:
        for event in events:
            f.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")

    stdout_tail = paths["stdout"].read_text(encoding="utf-8", errors="replace")[-2000:]
    stderr_tail = paths["stderr"].read_text(encoding="utf-8", errors="replace")[-4000:]
    parsed = parse_events(events)
    status = classify_error(proc.returncode, timed_out, stderr_tail, stdout_tail)
    if status == "completed" and not parsed["final_text"]:
        status = "parse_error"

    wall_ms = ns_delta_ms(process_start_ns, process_end_ns)
    output_tokens = parsed.get("output_tokens")
    tokens_per_second = None
    if isinstance(output_tokens, int) and wall_ms and wall_ms > 0:
        tokens_per_second = output_tokens / (wall_ms / 1000)

    result = {
        **row,
        "provider_mode": args.provider_mode,
        "model": "gpt-5.5",
        "model_reasoning_effort": "xhigh",
        "status": status,
        "exit_code": proc.returncode,
        "timed_out": timed_out,
        "dispatch_at": dispatch_at,
        "process_start_at": process_start_at,
        "process_end_at": process_end_at,
        "wall_ms": wall_ms,
        "queue_ms": ns_delta_ms(dispatch_ns, process_start_ns),
        "first_stdout_ms": ns_delta_ms(process_start_ns, timing.get("first_stdout_ns")),
        "first_stderr_ms": ns_delta_ms(process_start_ns, timing.get("first_stderr_ns")),
        "first_json_event_ms": ns_delta_ms(process_start_ns, timing.get("first_json_event_ns")),
        "first_final_message_ms": ns_delta_ms(process_start_ns, timing.get("first_final_message_ns")),
        "ttft_ms": ns_delta_ms(process_start_ns, timing.get("first_final_message_ns") or timing.get("first_json_event_ns")),
        "ttft_kind": "final_message" if timing.get("first_final_message_ns") else "first_json_event",
        "tokens_per_second": tokens_per_second,
        "prompt_sha256": sha256_text(prompt_text),
        "agents_sha256": sha256_text(agents_text),
        "paths": {key: str(value) for key, value in paths.items()},
        "provider_key_sha256_prefix": provider_key_sha256[:16] if provider_key_sha256 else None,
        **parsed,
    }

    meta.update(result)
    write_json(paths["meta"], meta)

    async with write_lock:
        append_jsonl(RUNS_PATH, result)

    return result


def write_manifest(args: argparse.Namespace, seed: int) -> None:
    control_agents = ARMS_DIR / "control" / "AGENTS.md"
    treatment_agents = ARMS_DIR / "treatment" / "AGENTS.md"
    manifest = {
        "created_at": utc_now(),
        "experiment_dir": str(EXP_DIR),
        "codex_version": codex_version(),
        "model": "gpt-5.5",
        "model_reasoning_effort": "xhigh",
        "total_scheduled": args.total,
        "per_arm": args.total // 2,
        "concurrency": args.concurrency,
        "seed": seed,
        "provider_mode": args.provider_mode,
        "ai_public_guarded_note": (
            "Excluded from primary natural-behavior report because CPA reasoning guard can retry 516 responses."
            if args.provider_mode == "ai_public_guarded"
            else None
        ),
        "prompt_path": str(PROMPT_PATH),
        "prompt_sha256": sha256_file(PROMPT_PATH),
        "control_agents_path": str(control_agents),
        "control_agents_sha256": sha256_file(control_agents),
        "treatment_agents_path": str(treatment_agents),
        "treatment_agents_sha256": sha256_file(treatment_agents),
        "command_template": build_argv(Path("$ARM_DIR"), args.provider_mode),
    }
    write_json(MANIFEST_PATH, manifest)


async def main_async(args: argparse.Namespace) -> int:
    if args.total % 2 != 0:
        raise SystemExit("--total must be even")
    seed = args.seed if args.seed is not None else int(time.time_ns() % (2**32))
    write_manifest(args, seed)
    prompt_text = read_text(PROMPT_PATH)
    schedule = load_or_create_schedule(args.total, seed)
    done = completed_run_ids()
    pending = [row for row in schedule if row["run_id"] not in done]
    if args.limit:
        pending = pending[: args.limit]
    print(f"scheduled={len(schedule)} done={len(done)} pending_now={len(pending)} concurrency={args.concurrency}")

    sem = asyncio.Semaphore(args.concurrency)
    lock = asyncio.Lock()
    results: list[dict[str, Any]] = []

    async def bounded(row: dict[str, Any]) -> None:
        async with sem:
            result = await run_trial(row, args, prompt_text, lock)
            results.append(result)
            print(
                json.dumps(
                    {
                        "run_id": result["run_id"],
                        "arm": result["arm"],
                        "status": result["status"],
                        "correct": result.get("parser_correct"),
                        "reasoning": result.get("reasoning_output_tokens"),
                        "wall_ms": result.get("wall_ms"),
                    },
                    ensure_ascii=False,
                    sort_keys=True,
                ),
                flush=True,
            )

    await asyncio.gather(*(bounded(row) for row in pending))
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--total", type=int, default=200)
    parser.add_argument("--concurrency", type=int, default=8)
    parser.add_argument("--seed", type=int)
    parser.add_argument("--limit", type=int, help="Run only the first N pending scheduled trials.")
    parser.add_argument("--timeout-seconds", type=int, default=300)
    parser.add_argument("--rust-log", default="info")
    parser.add_argument(
        "--provider-mode",
        choices=["chatgpt_auth", "ai_public_guarded"],
        default="chatgpt_auth",
    )
    parser.add_argument("--ai-public-key-file")
    return parser.parse_args()


def main() -> int:
    for path in [RAW_DIR / "events", RAW_DIR / "stdout", RAW_DIR / "stderr", RAW_DIR / "meta", RAW_DIR / "agents", RAW_DIR / "prompts", PARSED_DIR, REPORTS_DIR]:
        path.mkdir(parents=True, exist_ok=True)
    args = parse_args()
    return asyncio.run(main_async(args))


if __name__ == "__main__":
    raise SystemExit(main())
