"""Wav2Vec2 배치 패딩 + 음소 id 라벨 (§5.2 IPA 토큰)."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import torch
from transformers import Wav2Vec2Processor

from speech_coach.data.ipa_vocab import PHONEME_TO_ID


@dataclass
class DataCollatorCTCWithPadding:
    processor: Wav2Vec2Processor
    pad_to_multiple_of: int | None = None

    def __call__(self, features: list[dict]) -> dict[str, torch.Tensor]:
        input_values = [f["input_values"] for f in features]
        phoneme_labels = [f["phoneme_labels"] for f in features]
        batch = self.processor(
            [np.asarray(x, dtype=np.float32) for x in input_values],
            sampling_rate=16000,
            return_tensors="pt",
            padding=True,
            pad_to_multiple_of=self.pad_to_multiple_of,
        )
        unk = PHONEME_TO_ID["<unk>"]
        max_lab = max(len(labs) for labs in phoneme_labels)
        label_matrix = torch.full((len(phoneme_labels), max_lab), -100, dtype=torch.long)
        for i, labs in enumerate(phoneme_labels):
            for j, p in enumerate(labs):
                label_matrix[i, j] = PHONEME_TO_ID.get(p, unk)
        batch["labels"] = label_matrix
        return batch
