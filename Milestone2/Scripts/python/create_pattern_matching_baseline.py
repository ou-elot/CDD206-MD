from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
INPUT_FILE = BASE_DIR / "20260903_120407_00043_dm28i_832f8da8-7e2f-451c-9bd7-573a99eb7e55"
OUTPUT_DIR = BASE_DIR / "outputs"

PATTERN_NOTE_PATH = OUTPUT_DIR / "pattern_matching_note_level.parquet"
PATTERN_PATIENT_PATH = OUTPUT_DIR / "pattern_matching_patient_level.parquet"
COMPARISON_PATH = OUTPUT_DIR / "patient_level_concept_summary.csv"

CONCEPT_COLUMNS = {
    "Gout": "gout_mentioned",
    "Urate / uric acid": "urate_mentioned",
    "Allopurinol": "allopurinol_mentioned",
}

PATTERNS = {
    "gout_mentioned": r"gout",
    "urate_mentioned": r"uric acid|serum urate|blood urate|urate",
    "allopurinol_mentioned": r"allopurinol",
}

LLM_PATIENT_FILES = {
    "Mistral": OUTPUT_DIR / "mistral_patient_level.parquet",
    "Llama": OUTPUT_DIR / "llama_patient_level.parquet",
    "Qwen": OUTPUT_DIR / "qwen_patient_level.parquet",
}


def load_dataset() -> pd.DataFrame:
    df = pd.read_parquet(INPUT_FILE, engine="pyarrow")
    required = ["person_id", "deid_note_key", "note_text"]
    missing = [column for column in required if column not in df.columns]
    if missing:
        raise ValueError(f"Input dataset missing required columns: {missing}")
    return df


def make_pattern_labels(df: pd.DataFrame) -> pd.DataFrame:
    note_text = df["note_text"].fillna("").astype(str)
    note_level = df[["person_id", "deid_note_key"]].copy()
    if "deid_service_date" in df.columns:
        note_level["deid_service_date"] = df["deid_service_date"]
    if "note_type" in df.columns:
        note_level["note_type"] = df["note_type"]

    for column, pattern in PATTERNS.items():
        note_level[column] = note_text.str.contains(pattern, case=False, regex=True, na=False).astype(int)

    return note_level


def make_patient_level(note_level: pd.DataFrame) -> pd.DataFrame:
    return (
        note_level.groupby("person_id", as_index=False)
        .agg(
            gout_mentioned=("gout_mentioned", "max"),
            urate_mentioned=("urate_mentioned", "max"),
            allopurinol_mentioned=("allopurinol_mentioned", "max"),
            selected_note_count=("deid_note_key", "count"),
        )
    )


def load_llm_patient_counts() -> dict[str, dict[str, int]]:
    counts: dict[str, dict[str, int]] = {}
    for model_name, path in LLM_PATIENT_FILES.items():
        if not path.exists():
            raise FileNotFoundError(f"Missing patient-level LLM output: {path}")
        df = pd.read_parquet(path, engine="pyarrow")
        missing = [column for column in CONCEPT_COLUMNS.values() if column not in df.columns]
        if missing:
            raise ValueError(f"{path.name} missing concept columns: {missing}")
        counts[model_name] = {
            concept: int(df[column].sum()) for concept, column in CONCEPT_COLUMNS.items()
        }
    return counts


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    df = load_dataset()
    note_level = make_pattern_labels(df)
    patient_level = make_patient_level(note_level)

    note_level.to_parquet(PATTERN_NOTE_PATH, index=False)
    patient_level.to_parquet(PATTERN_PATIENT_PATH, index=False)

    pattern_counts = {
        concept: int(patient_level[column].sum()) for concept, column in CONCEPT_COLUMNS.items()
    }
    llm_counts = load_llm_patient_counts()

    comparison = pd.DataFrame(index=list(CONCEPT_COLUMNS.keys()))
    comparison.index.name = "Concept"
    comparison["Pattern matching patient count"] = pd.Series(pattern_counts)
    for model_name in ["Mistral", "Llama", "Qwen"]:
        comparison[f"{model_name} patient count"] = pd.Series(llm_counts[model_name])
    comparison.to_csv(COMPARISON_PATH)

    note_positive_counts = {
        concept: int(note_level[column].sum()) for concept, column in CONCEPT_COLUMNS.items()
    }

    print("PATTERN_NOTE_LEVEL_POSITIVE_COUNTS")
    print(pd.Series(note_positive_counts).to_string())

    print("\nPATTERN_PATIENT_LEVEL_POSITIVE_COUNTS")
    print(pd.Series(pattern_counts).to_string())

    print(f"\nTOTAL_PATIENTS_REPRESENTED\n{patient_level['person_id'].nunique()}")

    print("\nPATIENT_LEVEL_COMPARISON")
    print(comparison.to_string())

    print("\nSAVED_PATHS")
    print(f"Pattern note level: {PATTERN_NOTE_PATH}")
    print(f"Pattern patient level: {PATTERN_PATIENT_PATH}")
    print(f"Comparison CSV: {COMPARISON_PATH}")
    print(f"Script: {Path(__file__).resolve()}")


if __name__ == "__main__":
    main()
