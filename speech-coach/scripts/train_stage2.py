#!/usr/bin/env python3
"""Stage 2 학습 엔트리 (현재는 train_ctc와 동일 CLI — 추후 stage2 전용 config 분기)."""

from speech_coach.training.train_ctc import run_ctc_training

if __name__ == "__main__":
    run_ctc_training()
