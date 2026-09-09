from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = BASE_DIR / "outputs"
OUT_CSV = OUTPUT_DIR / "allopurinol_rates_by_note_type.csv"

NOTE_TYPES = ["Progress Notes", "Assessment & Plan Note"]
METHOD_FILES = {
    "Pattern matching": OUTPUT_DIR / "pattern_matching_note_level.parquet",
    "Mistral": OUTPUT_DIR / "mistral_note_level.parquet",
    "Llama": OUTPUT_DIR / "llama_note_level.parquet",
    "Qwen": OUTPUT_DIR / "qwen_note_level.parquet",
}


def to_markdown(df: pd.DataFrame) -> str:
    columns = list(df.columns)
    lines = ["| " + " | ".join(columns) + " |", "|" + "|".join(["---"] * len(columns)) + "|"]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[column]) for column in columns) + " |")
    return "\n".join(lines)


def is_evaluable(df: pd.DataFrame) -> pd.Series:
    if "inference_status" in df.columns:
        return df["inference_status"].eq("ok") & df["allopurinol_mentioned"].notna()
    return df["allopurinol_mentioned"].notna()


def main() -> None:
    rows = []
    for method, path in METHOD_FILES.items():
        df = pd.read_parquet(path, engine="pyarrow")
        required = ["note_type", "allopurinol_mentioned"]
        missing = [column for column in required if column not in df.columns]
        if missing:
            raise ValueError(f"{path.name} missing required columns: {missing}")

        eval_mask = is_evaluable(df)
        for note_type in NOTE_TYPES:
            note_type_mask = df["note_type"].eq(note_type)
            evaluable = df[note_type_mask & eval_mask].copy()
            excluded = int((note_type_mask & ~eval_mask).sum())
            total = int(len(evaluable))
            positive = int(evaluable["allopurinol_mentioned"].astype(int).sum()) if total else 0
            pct = 100 * positive / total if total else 0
            rows.append(
                {
                    "method": method,
                    "note_type": note_type,
                    "total_evaluable_notes": total,
                    "allopurinol_positive_notes": positive,
                    "allopurinol_positive_percent": round(pct, 1),
                    "excluded_missing_or_failed_notes": excluded,
                }
            )

    result = pd.DataFrame(rows)
    result.to_csv(OUT_CSV, index=False)

    print("MARKDOWN_TABLE")
    print(to_markdown(result))
    print("\nSAVED_PATH")
    print(OUT_CSV)


if __name__ == "__main__":
    main()
