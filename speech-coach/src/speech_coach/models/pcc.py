"""Module C — PCC (자음 정확도) 스텁: 음소 OK 비율 기반."""

from __future__ import annotations


def calc_pcc(classifications: list[tuple[str, str | None, str, str | None, float | None]]) -> float:
    """목표 음소 중 status==OK 비율을 0~100으로."""
    if not classifications:
        return 0.0
    ok = sum(1 for row in classifications if row[2] == "OK")
    return round(100.0 * ok / len(classifications), 2)
