"""정상 분포 reference 추출 (§6.4 연동 예정)."""

from __future__ import annotations

from pathlib import Path


def build_reference_placeholder(out_path: Path) -> None:
    out_path.write_text("{}", encoding="utf-8")
