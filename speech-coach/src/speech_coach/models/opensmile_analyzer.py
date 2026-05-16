"""Module A++ — OpenSMILE eGeMAPS (스켈레톤)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class OpenSmileAnalyzer:
    """정상 분포 reference 경로를 로드하고, 추후 음소 구간별 z-score 산출."""

    def __init__(self, normal_dist_path: str | Path | None = None) -> None:
        self.normal_dist_path = Path(normal_dist_path) if normal_dist_path else None
        self._ref: dict[str, Any] = {}
        if self.normal_dist_path and self.normal_dist_path.is_file():
            self._ref = json.loads(self.normal_dist_path.read_text(encoding="utf-8"))

    def analyze(self, audio_waveform, phoneme_boundaries: list) -> dict[str, float | None]:
        _ = audio_waveform, phoneme_boundaries
        return {}
