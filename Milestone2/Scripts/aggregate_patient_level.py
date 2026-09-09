from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = BASE_DIR / "outputs"

MODEL_FILES = {
    "Mistral": "mistral_note_level.parquet",
    "Llama": "llama_note_level.parquet",
    "Qwen": "qwen_note_level.parquet",
}

CONCEPT_COLUMNS = {
    "Gout": "gout_mentioned",
    "Urate / uric acid": "urate_mentioned",
    "Allopurinol": "allopurinol_mentioned",
}

REQUIRED_COLUMNS = ["person_id", "inference_status", *CONCEPT_COLUMNS.values()]


def validate_binary_labels(df: pd.DataFrame, model_name: str) -> None:
    ok = df[df["inference_status"].eq("ok")]
    for column in CONCEPT_COLUMNS.values():
        values = set(ok[column].dropna().astype(int).unique().tolist())
        if not values.issubset({0, 1}):
            raise ValueError(f"{model_name}: {column} has non-binary values in successful rows: {values}")


def main() -> None:
    patient_counts: dict[str, dict[str, int]] = {concept: {} for concept in CONCEPT_COLUMNS}
    note_counts: dict[str, dict[str, int]] = {}
    model_summaries: dict[str, dict[str, int | str]] = {}

    for model_name, file_name in MODEL_FILES.items():
        note_path = OUTPUT_DIR / file_name
        df = pd.read_parquet(note_path, engine="pyarrow")
        missing = [column for column in REQUIRED_COLUMNS if column not in df.columns]
        if missing:
            raise ValueError(f"{file_name} missing required columns: {missing}. Columns found: {list(df.columns)}")

        validate_binary_labels(df, model_name)

        ok = df[df["inference_status"].eq("ok")].copy()
        ok[list(CONCEPT_COLUMNS.values())] = ok[list(CONCEPT_COLUMNS.values())].astype(int)

        patient_level = (
            ok.groupby("person_id", as_index=False)
            .agg(
                gout_mentioned=("gout_mentioned", "max"),
                urate_mentioned=("urate_mentioned", "max"),
                allopurinol_mentioned=("allopurinol_mentioned", "max"),
                successful_note_count=("deid_note_key", "count"),
            )
        )

        out_path = OUTPUT_DIR / file_name.replace("note_level", "patient_level")
        patient_level.to_parquet(out_path, index=False)

        note_counts[model_name] = {
            concept: int(ok[column].sum()) for concept, column in CONCEPT_COLUMNS.items()
        }
        for concept, column in CONCEPT_COLUMNS.items():
            patient_counts[concept][f"{model_name} patient count"] = int(patient_level[column].sum())

        model_summaries[model_name] = {
            "note_file": str(note_path),
            "patient_file": str(out_path),
            "note_rows": int(len(df)),
            "successful_note_rows": int(len(ok)),
            "failed_or_skipped_note_rows": int(len(df) - len(ok)),
            "patients_represented": int(patient_level["person_id"].nunique()),
            "note_gout_positive": note_counts[model_name]["Gout"],
            "note_urate_positive": note_counts[model_name]["Urate / uric acid"],
            "note_allopurinol_positive": note_counts[model_name]["Allopurinol"],
            "patient_gout_positive": int(patient_level["gout_mentioned"].sum()),
            "patient_urate_positive": int(patient_level["urate_mentioned"].sum()),
            "patient_allopurinol_positive": int(patient_level["allopurinol_mentioned"].sum()),
        }

    summary = pd.DataFrame.from_dict(patient_counts, orient="index")
    summary.index.name = "Concept"
    summary_path = OUTPUT_DIR / "patient_level_concept_summary.csv"
    summary.to_csv(summary_path)

    print("SCHEMAS")
    for model_name, file_name in MODEL_FILES.items():
        df = pd.read_parquet(OUTPUT_DIR / file_name, engine="pyarrow")
        print(f"{model_name}: {list(df.columns)}")

    print("\nNOTE_LEVEL_POSITIVE_COUNTS")
    print(pd.DataFrame(note_counts).to_string())

    print("\nMODEL_SUMMARIES")
    print(pd.DataFrame.from_dict(model_summaries, orient="index").to_string())

    print("\nPATIENT_LEVEL_SUMMARY")
    print(summary.to_string())

    print("\nSAVED_PATHS")
    for model_name, details in model_summaries.items():
        print(f"{model_name}: {details['patient_file']}")
    print(f"CSV summary: {summary_path}")


if __name__ == "__main__":
    main()
