"""Module A — Wav2Vec2 CTC 음소 인식 (스켈레톤 + 스텁)."""

from __future__ import annotations

from typing import TYPE_CHECKING

import torch

if TYPE_CHECKING:
    pass


class PhonemeRecognizer:
    """실제 학습 후 transformers 모델을 로드해 구현."""

    def __init__(self, ckpt_dir: str | None = None) -> None:
        self.ckpt_dir = ckpt_dir

    @classmethod
    def from_pretrained(cls, ckpt_dir: str | None, stub: bool = True) -> PhonemeRecognizer:
        if stub:
            return PhonemeRecognizerStub(ckpt_dir)
        return cls(ckpt_dir)

    def predict(
        self,
        waveform: torch.Tensor,
        target_phonemes: list[str] | None = None,
    ) -> tuple[list[str], torch.Tensor, float]:
        raise NotImplementedError("학습 체크포인트 연동 후 구현")


class PhonemeRecognizerStub(PhonemeRecognizer):
    """개발용: target_phonemes가 있으면 그대로 에코."""

    def predict(
        self,
        waveform: torch.Tensor,
        target_phonemes: list[str] | None = None,
    ) -> tuple[list[str], torch.Tensor, float]:
        if target_phonemes:
            seq = list(target_phonemes)
        else:
            seq = ["sil"]
        t_frames = max(waveform.shape[-1] // 320, 1)
        vocab = 40
        logits = torch.zeros(1, t_frames, vocab, dtype=torch.float32)
        return seq, logits, 1.0
