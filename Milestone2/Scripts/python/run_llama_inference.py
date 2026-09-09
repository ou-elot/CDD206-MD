from pathlib import Path

import run_mistral_inference as runner


BASE_DIR = Path(__file__).resolve().parents[1]

runner.CHECKPOINT_DIR = BASE_DIR / "checkpoints" / "llama"
runner.RESULTS_PATH = BASE_DIR / "outputs" / "llama_note_level.parquet"
runner.CHECKPOINT_PATH = runner.CHECKPOINT_DIR / "llama_note_level_checkpoint.parquet"
runner.RUN_SUMMARY_PATH = BASE_DIR / "outputs" / "llama_run_summary.json"
runner.MODEL_NAME = "meta-llama/Llama-3.1-8B-Instruct"
runner.MAX_MODEL_LEN = 20480


if __name__ == "__main__":
    runner.main()
