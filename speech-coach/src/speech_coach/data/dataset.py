"""manifest.jsonl 기반 Dataset (스켈레톤)."""

from __future__ import annotations

import json
from pathlib import Path

import torch
from torch.utils.data import Dataset


class ManifestPhonemeDataset(Dataset):
    """각 줄: 설계서 §4.5 스키마 JSON."""

    def __init__(self, manifest_path: str | Path) -> None:
        self.rows: list[dict] = []
        p = Path(manifest_path)
        if not p.is_file():
            return
        for line in p.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                self.rows.append(json.loads(line))

    def __len__(self) -> int:
        return len(self.rows)

    def __getitem__(self, idx: int) -> dict:
        return self.rows[idx]

    @staticmethod
    def collate_fn(batch: list[dict]) -> dict:
        """추후 waveform 로드 + 패딩."""
        return {"batch": batch, "waveforms": torch.zeros(len(batch), 1600)}
