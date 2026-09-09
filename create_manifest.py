from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
INPUT_FILE = BASE_DIR / "20260903_120407_00043_dm28i_832f8da8-7e2f-451c-9bd7-573a99eb7e55"
OUTPUT_DIR = BASE_DIR / "outputs"
MASTER_MANIFEST = OUTPUT_DIR / "inference_manifest_master.parquet"
REQUEST_MANIFEST = OUTPUT_DIR / "inference_manifest_llm_requests.parquet"

EXPECTED_COLUMNS = [
    "person_id",
    "cohort_start_date",
    "cohort_end_date",
    "person_source_value",
    "patientepicid",
    "deid_note_key",
    "deid_service_date",
    "note_type",
    "note_text",
]


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    df = pd.read_parquet(INPUT_FILE, engine="pyarrow")
    missing = [column for column in EXPECTED_COLUMNS if column not in df.columns]
    if missing:
        raise ValueError(f"Missing expected columns: {missing}")

    df = df[EXPECTED_COLUMNS].copy()
    blank_note = df["note_text"].isna() | df["note_text"].astype("string").str.strip().eq("")
    df["manifest_status"] = "ready_for_llm"
    df.loc[blank_note, "manifest_status"] = "blank_note"

    request_df = df.loc[~blank_note].copy()

    df.to_parquet(MASTER_MANIFEST, index=False)
    request_df.to_parquet(REQUEST_MANIFEST, index=False)

    print(f"master_manifest={MASTER_MANIFEST}")
    print(f"request_manifest={REQUEST_MANIFEST}")
    print(f"total_source_rows={len(df)}")
    print(f"blank_notes={int(blank_note.sum())}")
    print(f"llm_request_rows={len(request_df)}")
    print("note_type_counts=")
    print(df["note_type"].value_counts(dropna=False).to_string())


if __name__ == "__main__":
    main()
