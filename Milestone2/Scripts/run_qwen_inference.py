from pathlib import Path

import run_mistral_inference as runner


BASE_DIR = Path(__file__).resolve().parents[1]

runner.CHECKPOINT_DIR = BASE_DIR / "checkpoints" / "qwen"
runner.RESULTS_PATH = BASE_DIR / "outputs" / "qwen_note_level.parquet"
runner.CHECKPOINT_PATH = runner.CHECKPOINT_DIR / "qwen_note_level_checkpoint.parquet"
runner.RUN_SUMMARY_PATH = BASE_DIR / "outputs" / "qwen_run_summary.json"
runner.MODEL_NAME = "Qwen/Qwen3-8B-AWQ"
runner.MAX_MODEL_LEN = 32768
runner.EXTRA_REQUEST_FIELDS = {"chat_template_kwargs": {"enable_thinking": False}}


if __name__ == "__main__":
    runner.main()
