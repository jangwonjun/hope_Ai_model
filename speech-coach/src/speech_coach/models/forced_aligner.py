"""Module A+ — torchaudio forced_align 래퍼 (스켈레톤)."""

from __future__ import annotations

from dataclasses import dataclass

import torch


@dataclass
class PhonemeBoundary:
    phoneme_index: int
    start_frame: int
    end_frame: int


class ForcedAligner:
    """설계서 §5.5 — log-probs + 예측 음소 인덱스로 경계 추정."""

    def __init__(self, blank_idx: int = 0) -> None:
        self.blank_idx = blank_idx

    def __call__(
        self,
        frame_logits: torch.Tensor,
        predicted_phoneme_indices: torch.Tensor,
    ) -> list[PhonemeBoundary]:
        # 스켈레톤: 균등 분할. 실제는 torchaudio.functional.forced_align 사용.
        _ = frame_logits, predicted_phoneme_indices
        return []
