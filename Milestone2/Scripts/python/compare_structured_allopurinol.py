from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = BASE_DIR / "outputs"
STRUCTURED_FILE = Path(
    r"C:\Users\noras\Downloads\gout_nlp_structured_allopurinol\20260907_193603_00178_z3xih_f06b55ef-a309-4652-8336-c7fb5945f91f"
)

METHOD_FILES = {
    "Pattern matching": OUTPUT_DIR / "pattern_matching_patient_level.parquet",
    "Mistral": OUTPUT_DIR / "mistral_patient_level.parquet",
    "Llama": OUTPUT_DIR / "llama_patient_level.parquet",
    "Qwen": OUTPUT_DIR / "qwen_patient_level.parquet",
}

SUMMARY_CSV = OUTPUT_DIR / "structured_vs_note_allopurinol_summary.csv"
SUMMARY_MD = OUTPUT_DIR / "structured_vs_note_allopurinol_summary.md"


def pct(numerator: int, denominator: int) -> float | None:
    if denominator == 0:
        return None
    return numerator / denominator


def fmt_metric(value: float | None) -> str:
    if value is None:
        return "NA"
    return f"{value:.3f}"


def confusion_label(row: pd.Series) -> str:
    if pd.isna(row["allopurinol_mentioned"]):
        return "not_evaluable"
    structured = int(row["structured_allopurinol"])
    note = int(row["allopurinol_mentioned"])
    if structured == 1 and note == 1:
        return "TP"
    if structured == 1 and note == 0:
        return "FN"
    if structured == 0 and note == 1:
        return "FP"
    return "TN"


def compute_metrics(detail: pd.DataFrame) -> dict[str, int | float | None | str]:
    evaluable = detail[detail["confusion_category"].ne("not_evaluable")]
    tp = int((evaluable["confusion_category"] == "TP").sum())
    fn = int((evaluable["confusion_category"] == "FN").sum())
    fp = int((evaluable["confusion_category"] == "FP").sum())
    tn = int((evaluable["confusion_category"] == "TN").sum())
    return {
        "patients_joined": int(len(detail)),
        "evaluable_patients": int(len(evaluable)),
        "non_evaluable_patients": int((detail["confusion_category"] == "not_evaluable").sum()),
        "structured_positive": int((detail["structured_allopurinol"] == 1).sum()),
        "structured_negative": int((detail["structured_allopurinol"] == 0).sum()),
        "note_positive": int((evaluable["allopurinol_mentioned"] == 1).sum()),
        "note_negative": int((evaluable["allopurinol_mentioned"] == 0).sum()),
        "TP": tp,
        "FN": fn,
        "FP": fp,
        "TN": tn,
        "sensitivity": pct(tp, tp + fn),
        "specificity": pct(tn, tn + fp),
        "PPV": pct(tp, tp + fp),
        "NPV": pct(tn, tn + fn),
        "overall_agreement": pct(tp + tn, tp + fn + fp + tn),
    }


def validate_structured(structured: pd.DataFrame) -> None:
    expected = ["person_id", "cohort_start_date", "structured_allopurinol"]
    missing = [column for column in expected if column not in structured.columns]
    if missing:
        raise ValueError(f"Structured export missing expected columns: {missing}")
    if structured["person_id"].duplicated().any():
        raise ValueError("Structured export has duplicate person_id values")
    values = set(structured["structured_allopurinol"].dropna().astype(int).unique().tolist())
    if values != {0, 1}:
        raise ValueError(f"structured_allopurinol values are not exactly 0/1: {values}")


def markdown_table(summary: pd.DataFrame) -> str:
    display = summary.copy()
    for column in ["sensitivity", "specificity", "PPV", "NPV", "overall_agreement"]:
        display[column] = display[column].map(fmt_metric)
    columns = [
        "method",
        "evaluable_patients",
        "TP",
        "FN",
        "FP",
        "TN",
        "sensitivity",
        "specificity",
        "PPV",
        "NPV",
        "overall_agreement",
    ]
    display = display[columns]
    header = "| " + " | ".join(columns) + " |"
    separator = "|" + "|".join(["---"] * len(columns)) + "|"
    rows = [header, separator]
    for _, row in display.iterrows():
        rows.append("| " + " | ".join(str(row[column]) for column in columns) + " |")
    return "\n".join(rows) + "\n"


def main() -> None:
    structured = pd.read_parquet(STRUCTURED_FILE, engine="pyarrow")
    validate_structured(structured)

    structured_counts = structured["structured_allopurinol"].value_counts().sort_index().to_dict()
    if structured["person_id"].nunique() != 4985 or structured_counts.get(1, 0) != 1849 or structured_counts.get(0, 0) != 3136:
        raise ValueError(
            "Structured export count validation failed: "
            f"unique={structured['person_id'].nunique()}, counts={structured_counts}"
        )

    summary_rows = []
    detail_paths = []
    for method, path in METHOD_FILES.items():
        patient = pd.read_parquet(path, engine="pyarrow")
        required = ["person_id", "allopurinol_mentioned"]
        missing = [column for column in required if column not in patient.columns]
        if missing:
            raise ValueError(f"{path.name} missing required columns: {missing}")
        if patient["person_id"].duplicated().any():
            raise ValueError(f"{path.name} has duplicate person_id values")

        detail = structured.merge(
            patient[["person_id", "allopurinol_mentioned"]],
            on="person_id",
            how="left",
            validate="one_to_one",
        )
        detail["method"] = method
        detail["confusion_category"] = detail.apply(confusion_label, axis=1)
        detail = detail[
            [
                "method",
                "person_id",
                "cohort_start_date",
                "structured_allopurinol",
                "allopurinol_mentioned",
                "confusion_category",
            ]
        ]

        safe_method = method.lower().replace(" ", "_")
        detail_path = OUTPUT_DIR / f"structured_vs_note_allopurinol_{safe_method}_detail.csv"
        detail.to_csv(detail_path, index=False)
        detail_paths.append((method, detail_path))

        metrics = compute_metrics(detail)
        metrics["method"] = method
        metrics["detail_path"] = str(detail_path)
        summary_rows.append(metrics)

    summary = pd.DataFrame(summary_rows)
    ordered_columns = [
        "method",
        "patients_joined",
        "evaluable_patients",
        "non_evaluable_patients",
        "structured_positive",
        "structured_negative",
        "note_positive",
        "note_negative",
        "TP",
        "FN",
        "FP",
        "TN",
        "sensitivity",
        "specificity",
        "PPV",
        "NPV",
        "overall_agreement",
        "detail_path",
    ]
    summary = summary[ordered_columns]
    summary.to_csv(SUMMARY_CSV, index=False)

    md = "# Structured vs Note-Derived Allopurinol\n\n"
    md += markdown_table(summary)
    md += "\n## Files\n\n"
    md += f"- Summary CSV: `{SUMMARY_CSV}`\n"
    for method, detail_path in detail_paths:
        md += f"- {method} detail CSV: `{detail_path}`\n"
    SUMMARY_MD.write_text(md, encoding="utf-8")

    display = summary.copy()
    for column in ["sensitivity", "specificity", "PPV", "NPV", "overall_agreement"]:
        display[column] = display[column].map(fmt_metric)
    print("STRUCTURED_EXPORT_VALIDATION")
    print(f"unique patients: {structured['person_id'].nunique()}")
    print(f"structured_allopurinol=1: {int(structured_counts.get(1, 0))}")
    print(f"structured_allopurinol=0: {int(structured_counts.get(0, 0))}")

    print("\nCOMPARISON_SUMMARY")
    print(display.drop(columns=["detail_path"]).to_string(index=False))

    print("\nSAVED_PATHS")
    print(f"Combined summary CSV: {SUMMARY_CSV}")
    print(f"Markdown summary: {SUMMARY_MD}")
    for method, detail_path in detail_paths:
        print(f"{method} detail CSV: {detail_path}")
    print(f"Script: {Path(__file__).resolve()}")


if __name__ == "__main__":
    main()
