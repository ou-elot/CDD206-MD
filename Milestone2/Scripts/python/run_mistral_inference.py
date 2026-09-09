import argparse
import json
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = BASE_DIR / "outputs"
CHECKPOINT_DIR = BASE_DIR / "checkpoints" / "mistral"
LOG_DIR = BASE_DIR / "logs"
MASTER_MANIFEST = OUTPUT_DIR / "inference_manifest_master.parquet"
RESULTS_PATH = OUTPUT_DIR / "mistral_note_level.parquet"
CHECKPOINT_PATH = CHECKPOINT_DIR / "mistral_note_level_checkpoint.parquet"
RUN_SUMMARY_PATH = OUTPUT_DIR / "mistral_run_summary.json"

MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.3"
BASE_URL = "http://127.0.0.1:18000/v1"
CHAT_COMPLETIONS_URL = f"{BASE_URL}/chat/completions"
MAX_MODEL_LEN = 8192
EXTRA_REQUEST_FIELDS: dict[str, Any] = {}

PROMPT_TEMPLATE = """You are reviewing one clinical note for a retrospective cohort study. Classify only what is supported by the note. Do not infer facts that are not documented. Distinguish patient-specific documentation from negation, rule-out language, family history, hypothetical discussion, and generic education.

Return exactly one JSON object with integer values 0 or 1 and no additional prose:

```json
{{
  "gout_mentioned": 0,
  "urate_mentioned": 0,
  "allopurinol_mentioned": 0
}}
```

Definitions:
- `gout_mentioned = 1` if the note indicates the patient has gout or a documented history of gout. Use 0 for negated gout, rule-out/suspected-only gout, family history only, or hypothetical discussion.
- `urate_mentioned = 1` if the note discusses a patient-specific serum urate, blood urate, or uric acid measurement/result. Use 0 for generic discussion or a future plan to measure without an actual patient result.
- `allopurinol_mentioned = 1` if the note indicates that the patient is taking, prescribed, starting, continuing, stopping, holding, or otherwise being treated with allopurinol. Use 0 for allergy-only, hypothetical, family-member, or generic mentions without evidence of patient treatment.

Clinical note:
`{note_text}`"""

LABEL_COLUMNS = ["gout_mentioned", "urate_mentioned", "allopurinol_mentioned"]
ID_COLUMNS = ["person_id", "deid_note_key", "note_type", "deid_service_date"]
OUTPUT_COLUMNS = ID_COLUMNS + LABEL_COLUMNS + [
    "model_name",
    "inference_status",
    "error_type",
    "error_message",
    "attempt_count",
    "response_text",
    "completed_at_utc",
]


def empty_label_row(row: pd.Series, status: str, error_type: str = "", error_message: str = "") -> dict[str, Any]:
    result = {column: row[column] for column in ID_COLUMNS}
    for column in LABEL_COLUMNS:
        result[column] = pd.NA
    result.update(
        {
            "model_name": MODEL_NAME,
            "inference_status": status,
            "error_type": error_type,
            "error_message": error_message,
            "attempt_count": 0,
            "response_text": "",
            "completed_at_utc": datetime.now(timezone.utc).isoformat(),
        }
    )
    return result


def load_existing_results() -> pd.DataFrame:
    paths = [RESULTS_PATH, CHECKPOINT_PATH]
    for path in paths:
        if path.exists():
            return pd.read_parquet(path, engine="pyarrow")
    return pd.DataFrame(columns=OUTPUT_COLUMNS)


def write_results(results: list[dict[str, Any]]) -> None:
    frame = pd.DataFrame(results, columns=OUTPUT_COLUMNS)
    frame.to_parquet(CHECKPOINT_PATH, index=False)
    frame.to_parquet(RESULTS_PATH, index=False)


def extract_json_object(text: str) -> dict[str, Any]:
    stripped = text.strip()
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        pass

    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", stripped, flags=re.IGNORECASE | re.DOTALL)
    if fenced:
        return json.loads(fenced.group(1))

    start = stripped.find("{")
    end = stripped.rfind("}")
    if start != -1 and end != -1 and end > start:
        return json.loads(stripped[start : end + 1])

    raise ValueError("No JSON object found in model response")


def parse_response(text: str) -> tuple[dict[str, int] | None, str, str]:
    try:
        payload = extract_json_object(text)
    except Exception as exc:
        return None, "parsing_error", str(exc)

    if set(payload.keys()) != set(LABEL_COLUMNS):
        return None, "parsing_error", f"Unexpected JSON keys: {sorted(payload.keys())}"

    labels: dict[str, int] = {}
    for column in LABEL_COLUMNS:
        value = payload[column]
        if isinstance(value, bool) or value not in (0, 1):
            return None, "invalid_label", f"Invalid value for {column}: {value!r}"
        labels[column] = int(value)
    return labels, "", ""


def is_context_error(message: str) -> bool:
    lowered = message.lower()
    patterns = [
        "maximum context length",
        "context length",
        "max_model_len",
        "maximum sequence length",
        "input is too long",
        "prompt is too long",
        "too many tokens",
        "token indices sequence length",
    ]
    return any(pattern in lowered for pattern in patterns)


def call_model(note_text: str, timeout: int, retries: int) -> tuple[str | None, str, str, int]:
    prompt = PROMPT_TEMPLATE.format(note_text=note_text)
    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0,
        "max_tokens": 96,
    }
    payload.update(EXTRA_REQUEST_FIELDS)

    last_error = ""
    for attempt in range(1, retries + 2):
        try:
            request = Request(
                CHAT_COMPLETIONS_URL,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urlopen(request, timeout=timeout) as response:
                data = json.loads(response.read().decode("utf-8"))
                text = data["choices"][0]["message"]["content"]
                return text, "", "", attempt
        except HTTPError as exc:
            last_error = exc.read().decode("utf-8", errors="replace")[:2000]
            if is_context_error(last_error):
                return None, "context_error", last_error, attempt
            if exc.code in {408, 429, 500, 502, 503, 504} and attempt <= retries + 1:
                time.sleep(min(60, 2**attempt))
                continue
            return None, "api_error", last_error, attempt
        except URLError as exc:
            last_error = str(exc)
            if is_context_error(last_error):
                return None, "context_error", last_error, attempt
            if attempt <= retries + 1:
                time.sleep(min(60, 2**attempt))
                continue
            return None, "api_error", last_error, attempt
        except TimeoutError as exc:
            last_error = str(exc)
            if attempt <= retries + 1:
                time.sleep(min(60, 2**attempt))
                continue
            return None, "api_error", last_error, attempt
        except json.JSONDecodeError as exc:
            return None, "api_error", str(exc), attempt
        except Exception as exc:
            return None, "api_error", str(exc), attempt

    return None, "api_error", last_error, retries + 1


def result_key(row: pd.Series) -> str:
    return str(row["deid_note_key"])


def classify_row(row: dict[str, Any], timeout: int, retries: int) -> dict[str, Any]:
    response_text, call_error_type, call_error_message, attempt_count = call_model(
        str(row["note_text"]), timeout=timeout, retries=retries
    )

    base = {column: row[column] for column in ID_COLUMNS}
    base.update(
        {
            "model_name": MODEL_NAME,
            "attempt_count": attempt_count,
            "response_text": response_text or "",
            "completed_at_utc": datetime.now(timezone.utc).isoformat(),
        }
    )

    if call_error_type:
        for column in LABEL_COLUMNS:
            base[column] = pd.NA
        base.update(
            {
                "inference_status": call_error_type,
                "error_type": call_error_type,
                "error_message": call_error_message,
            }
        )
        return base

    labels, parse_error_type, parse_error_message = parse_response(response_text or "")
    if labels is None:
        for column in LABEL_COLUMNS:
            base[column] = pd.NA
        base.update(
            {
                "inference_status": parse_error_type,
                "error_type": parse_error_type,
                "error_message": parse_error_message,
            }
        )
        return base

    base.update(labels)
    base.update({"inference_status": "ok", "error_type": "", "error_message": ""})
    return base


def summarize(results: list[dict[str, Any]], started: float) -> dict[str, Any]:
    frame = pd.DataFrame(results)
    status_counts = frame["inference_status"].value_counts(dropna=False).to_dict() if len(frame) else {}
    error_counts = frame["error_type"].value_counts(dropna=False).to_dict() if len(frame) else {}
    attempted = int(frame[~frame["inference_status"].isin(["blank_note"])].shape[0])
    summary = {
        "model_name": MODEL_NAME,
        "max_model_len": MAX_MODEL_LEN,
        "total_source_rows": int(len(frame)),
        "blank_notes_skipped": int(status_counts.get("blank_note", 0)),
        "total_llm_requests_attempted": attempted,
        "successful_requests": int(status_counts.get("ok", 0)),
        "api_errors": int(error_counts.get("api_error", 0)),
        "parsing_errors": int(error_counts.get("parsing_error", 0)),
        "invalid_labels": int(error_counts.get("invalid_label", 0)),
        "context_errors": int(error_counts.get("context_error", 0)),
        "runtime_seconds": round(time.time() - started, 1),
        "results_path": str(RESULTS_PATH),
        "checkpoint_path": str(CHECKPOINT_PATH),
        "completed_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    RUN_SUMMARY_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def print_progress(summary: dict[str, Any], total_llm_requests: int) -> None:
    attempted = int(summary["total_llm_requests_attempted"])
    failed = int(
        summary["api_errors"]
        + summary["parsing_errors"]
        + summary["invalid_labels"]
        + summary["context_errors"]
    )
    progress = {
        "event": "progress",
        "processed_llm_requests": attempted,
        "total_llm_requests": total_llm_requests,
        "percent_complete": round(100 * attempted / total_llm_requests, 1) if total_llm_requests else 100.0,
        "successful_requests": summary["successful_requests"],
        "failed_requests": failed,
        "runtime_seconds": summary["runtime_seconds"],
        "completed_at_utc": summary["completed_at_utc"],
    }
    print(json.dumps(progress), flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint-every", type=int, default=100)
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--retries", type=int, default=3)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--concurrency", type=int, default=4)
    parser.add_argument("--progress-every", type=int, default=500)
    parser.add_argument("--retry-status", action="append", default=[])
    args = parser.parse_args()

    OUTPUT_DIR.mkdir(exist_ok=True)
    CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(exist_ok=True)

    started = time.time()
    manifest = pd.read_parquet(MASTER_MANIFEST, engine="pyarrow")
    existing = load_existing_results()
    results = existing.to_dict("records")

    retry_statuses = set(args.retry_status)
    completed_ok = set(existing.loc[existing["inference_status"].eq("ok"), "deid_note_key"].astype(str)) if len(existing) else set()
    terminal_statuses = {"blank_note", "context_error"} - retry_statuses
    terminal_nonretry = set(existing.loc[existing["inference_status"].isin(terminal_statuses), "deid_note_key"].astype(str)) if len(existing) else set()
    retry_keys = set(existing.loc[existing["inference_status"].isin(retry_statuses), "deid_note_key"].astype(str)) if len(existing) and retry_statuses else set()
    represented = set(existing["deid_note_key"].astype(str)) if len(existing) else set()

    for _, row in manifest[manifest["manifest_status"].eq("blank_note")].iterrows():
        key = result_key(row)
        if key not in represented:
            results.append(empty_label_row(row, "blank_note", "blank_note", "note_text is null or blank"))
            represented.add(key)

    pending_rows: list[dict[str, Any]] = []
    request_rows = manifest[manifest["manifest_status"].eq("ready_for_llm")]
    total_llm_requests = int(len(request_rows))
    for _, row in request_rows.iterrows():
        key = result_key(row)
        if retry_keys and key not in retry_keys:
            continue
        if key in completed_ok or key in terminal_nonretry:
            continue
        if args.limit and len(pending_rows) >= args.limit:
            break
        pending_rows.append(row.to_dict())

    processed_this_run = 0
    try:
        with ThreadPoolExecutor(max_workers=max(1, args.concurrency)) as executor:
            futures = [executor.submit(classify_row, row, args.timeout, args.retries) for row in pending_rows]
            for future in as_completed(futures):
                base = future.result()
                key = str(base["deid_note_key"])
                prior_indexes = [index for index, item in enumerate(results) if str(item["deid_note_key"]) == key]
                for index in reversed(prior_indexes):
                    results.pop(index)
                results.append(base)
                processed_this_run += 1

                if processed_this_run % args.checkpoint_every == 0:
                    write_results(results)
                    summary = summarize(results, started)
                    if args.progress_every and summary["total_llm_requests_attempted"] % args.progress_every == 0:
                        print_progress(summary, total_llm_requests)
    finally:
        write_results(results)

    print(json.dumps(summarize(results, started), indent=2), flush=True)


if __name__ == "__main__":
    main()
