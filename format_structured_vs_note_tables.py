from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = BASE_DIR / "outputs"
INPUT_PATH = OUTPUT_DIR / "structured_vs_note_allopurinol_summary.csv"
CONFUSION_PATH = OUTPUT_DIR / "structured_vs_note_confusion_table.csv"
VIDEO_PATH = OUTPUT_DIR / "structured_vs_note_video_table.csv"
MARKDOWN_PATH = OUTPUT_DIR / "structured_vs_note_tables.md"

METHOD_ORDER = ["Pattern matching", "Mistral", "Llama", "Qwen"]


def pct(series: pd.Series) -> pd.Series:
    return (series.astype(float) * 100).map(lambda value: f"{value:.1f}%")


def markdown_table(df: pd.DataFrame) -> str:
    columns = list(df.columns)
    lines = ["| " + " | ".join(columns) + " |", "|" + "|".join(["---"] * len(columns)) + "|"]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[column]) for column in columns) + " |")
    return "\n".join(lines)


def main() -> None:
    summary = pd.read_csv(INPUT_PATH)
    summary["method"] = pd.Categorical(summary["method"], categories=METHOD_ORDER, ordered=True)
    summary = summary.sort_values("method")

    confusion = pd.DataFrame(
        {
            "Method": summary["method"].astype(str),
            "True Positive (TP)": summary["TP"].astype(int),
            "False Negative (FN)": summary["FN"].astype(int),
            "False Positive (FP)": summary["FP"].astype(int),
            "True Negative (TN)": summary["TN"].astype(int),
            "Sensitivity": pct(summary["sensitivity"]),
            "Specificity": pct(summary["specificity"]),
        }
    )

    video = pd.DataFrame(
        {
            "Method": summary["method"].astype(str),
            "TP": summary["TP"].astype(int),
            "FN": summary["FN"].astype(int),
            "Sensitivity": pct(summary["sensitivity"]),
        }
    )

    confusion.to_csv(CONFUSION_PATH, index=False)
    video.to_csv(VIDEO_PATH, index=False)

    markdown = "# Structured vs Note-Derived Allopurinol Tables\n\n"
    markdown += "## Presentation Table\n\n"
    markdown += markdown_table(confusion)
    markdown += "\n\n## Video Table\n\n"
    markdown += markdown_table(video)
    markdown += "\n"
    MARKDOWN_PATH.write_text(markdown, encoding="utf-8")

    print("PRESENTATION_TABLE")
    print(markdown_table(confusion))
    print("\nVIDEO_TABLE")
    print(markdown_table(video))
    print("\nSAVED_PATHS")
    print(CONFUSION_PATH)
    print(VIDEO_PATH)
    print(MARKDOWN_PATH)


if __name__ == "__main__":
    main()
