from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = BASE_DIR / "outputs"
DEMOGRAPHICS_FILE = Path(
    r"C:\Users\noras\Downloads\gout_nlp_demographics\20260907_070854_00079_7gqsu_04516c8d-85f9-4446-921c-29d2d8aa8b15"
)

METHOD_FILES = {
    "Pattern matching": OUTPUT_DIR / "pattern_matching_patient_level.parquet",
    "Mistral": OUTPUT_DIR / "mistral_patient_level.parquet",
    "Llama": OUTPUT_DIR / "llama_patient_level.parquet",
    "Qwen": OUTPUT_DIR / "qwen_patient_level.parquet",
}

CONCEPT_COLUMNS = {
    "Gout": "gout_mentioned",
    "Urate / uric acid": "urate_mentioned",
    "Allopurinol": "allopurinol_mentioned",
}

TABLE1_FIELDS = ["age_at_index", "sex", "race", "ethnicity"]


def fmt_n_pct(n: int, denom: int) -> str:
    pct = 100 * n / denom if denom else 0
    return f"{n} ({pct:.1f}%)"


def age_mean_sd(series: pd.Series) -> str:
    values = pd.to_numeric(series, errors="coerce").dropna()
    if values.empty:
        return "NA"
    return f"{values.mean():.1f} ({values.std(ddof=1):.1f})"


def age_median(series: pd.Series) -> str:
    values = pd.to_numeric(series, errors="coerce").dropna()
    if values.empty:
        return "NA"
    return f"{values.median():.1f}"


def summarize_category(df: pd.DataFrame, column: str, label: str, denom: int) -> list[dict[str, str]]:
    values = df[column].fillna("Missing").astype(str)
    rows = []
    for level, n in values.value_counts(dropna=False).sort_index().items():
        rows.append({"Characteristic": f"{label}: {level}", "value": fmt_n_pct(int(n), denom)})
    return rows


def table1_for_method(joined: pd.DataFrame, method_name: str) -> pd.DataFrame:
    sample = joined.copy()
    treated = joined[joined["allopurinol_mentioned"].eq(1)].copy()

    groups = {
        "Qualified/sample cohort": sample,
        "Note-derived allopurinol-treated group": treated,
    }

    characteristics: list[str] = []
    by_group: dict[str, dict[str, str]] = {}

    for group_name, group_df in groups.items():
        denom = len(group_df)
        rows = [
            {"Characteristic": "N", "value": str(denom)},
            {"Characteristic": "Age, mean (SD)", "value": age_mean_sd(group_df["age_at_index"])},
            {"Characteristic": "Age, median", "value": age_median(group_df["age_at_index"])},
        ]
        rows.extend(summarize_category(group_df, "sex", "Sex", denom))
        rows.extend(summarize_category(group_df, "race", "Race", denom))
        rows.extend(summarize_category(group_df, "ethnicity", "Ethnicity", denom))
        by_group[group_name] = {row["Characteristic"]: row["value"] for row in rows}
        characteristics.extend(row["Characteristic"] for row in rows)

    ordered_characteristics = list(dict.fromkeys(characteristics))
    table = pd.DataFrame({"Characteristic": ordered_characteristics})
    table.insert(0, "Method", method_name)
    for group_name in groups:
        table[group_name] = table["Characteristic"].map(by_group[group_name]).fillna("0 (0.0%)")
    return table


def main() -> None:
    demographics = pd.read_parquet(DEMOGRAPHICS_FILE, engine="pyarrow")
    required_demo = ["person_id", *TABLE1_FIELDS]
    missing_demo = [column for column in required_demo if column not in demographics.columns]
    if missing_demo:
        raise ValueError(f"Demographics file missing required columns: {missing_demo}")
    if demographics["person_id"].duplicated().any():
        raise ValueError("Demographics file has duplicate person_id values")

    all_tables = []
    concept_summary = pd.DataFrame(index=list(CONCEPT_COLUMNS.keys()))
    concept_summary.index.name = "Concept"
    join_summary = []

    for method_name, patient_path in METHOD_FILES.items():
        patient = pd.read_parquet(patient_path, engine="pyarrow")
        required_patient = ["person_id", *CONCEPT_COLUMNS.values()]
        missing_patient = [column for column in required_patient if column not in patient.columns]
        if missing_patient:
            raise ValueError(f"{patient_path.name} missing columns: {missing_patient}")
        if patient["person_id"].duplicated().any():
            raise ValueError(f"{patient_path.name} has duplicate person_id values")

        joined = patient.merge(demographics[required_demo], on="person_id", how="left", validate="one_to_one")
        missing_demographics = int(joined["age_at_index"].isna().sum())
        if missing_demographics:
            raise ValueError(f"{method_name} has {missing_demographics} patients without demographics")

        for concept, column in CONCEPT_COLUMNS.items():
            concept_summary.loc[concept, f"{method_name} patient count"] = int(joined[column].sum())

        table = table1_for_method(joined, method_name)
        table_path = OUTPUT_DIR / f"{method_name.lower().replace(' ', '_')}_table1_allopurinol_treated.csv"
        table.to_csv(table_path, index=False)
        all_tables.append(table)

        joined_path = OUTPUT_DIR / f"{method_name.lower().replace(' ', '_')}_patient_level_with_demographics.parquet"
        joined.to_parquet(joined_path, index=False)

        join_summary.append(
            {
                "method": method_name,
                "patients": int(joined["person_id"].nunique()),
                "allopurinol_treated_patients": int(joined["allopurinol_mentioned"].sum()),
                "table1_path": str(table_path),
                "joined_path": str(joined_path),
            }
        )

    combined_table = pd.concat(all_tables, ignore_index=True)
    combined_table_path = OUTPUT_DIR / "table1_all_methods_allopurinol_treated.csv"
    combined_table.to_csv(combined_table_path, index=False)

    concept_summary = concept_summary.astype(int)
    concept_summary_path = OUTPUT_DIR / "patient_level_positive_counts_all_methods.csv"
    concept_summary.to_csv(concept_summary_path)

    join_summary_df = pd.DataFrame(join_summary)
    join_summary_path = OUTPUT_DIR / "demographics_join_summary.csv"
    join_summary_df.to_csv(join_summary_path, index=False)

    print("PATIENT_LEVEL_POSITIVE_COUNTS")
    print(concept_summary.to_string())

    print("\nJOIN_SUMMARY")
    print(join_summary_df.to_string(index=False))

    print("\nCOMBINED_TABLE1")
    print(combined_table.to_string(index=False))

    print("\nSAVED_PATHS")
    print(f"Combined Table 1: {combined_table_path}")
    print(f"Positive counts summary: {concept_summary_path}")
    print(f"Join summary: {join_summary_path}")
    for row in join_summary:
        print(f"{row['method']} Table 1: {row['table1_path']}")
        print(f"{row['method']} joined demographics: {row['joined_path']}")
    print(f"Script: {Path(__file__).resolve()}")


if __name__ == "__main__":
    main()
