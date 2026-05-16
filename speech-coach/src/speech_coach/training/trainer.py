"""학습 엔트리 호환 래퍼."""

from __future__ import annotations

from speech_coach.training.train_ctc import run_ctc_training


def run_training_placeholder(stage: str) -> None:
    """구 코드 호환. 실제 학습은 `run_ctc_training` / scripts/train_stage1.py 사용."""
    print(f"[trainer] placeholder stage={stage!r} — use: python scripts/train_stage1.py ...")


__all__ = ["run_ctc_training", "run_training_placeholder"]
