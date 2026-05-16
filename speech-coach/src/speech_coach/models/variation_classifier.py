"""Module B-2 — 변동 분류 (룰 기반 스텁)."""

from __future__ import annotations


def classify_alignment_row(
    tgt: str | None,
    act: str | None,
    acoustic_z: float | None = None,
    z_dis_threshold: float = 2.5,
) -> tuple[str, str | None, float | None]:
    """(status, variation, z) 반환."""
    if tgt is None:
        return "OK", None, acoustic_z  # 예측 쪽 첨가 등은 PCC 정의에 따라 무시 가능
    if act is None:
        return "DEL", None, acoustic_z
    if tgt != act:
        return "SUB", "SUBSTITUTION", acoustic_z
    if acoustic_z is not None and abs(acoustic_z) >= z_dis_threshold:
        return "DIS", "DISTORTION", acoustic_z
    return "OK", None, acoustic_z


class VariationClassifier:
    def classify(
        self,
        alignment: list[tuple[str | None, str | None]],
        acoustic_deviations: dict[str, float | None],
    ) -> list[tuple[str, str | None, str, str | None, float | None]]:
        """
        alignment: NW 결과 (tgt, act)
        반환: (target, actual, status, variation, z) 리스트 (phoneme_results 생성용)
        """
        rows: list[tuple[str, str | None, str, str | None, float | None]] = []
        for tgt, act in alignment:
            if tgt is None:
                continue
            key = f"{tgt}:{act}"
            z = acoustic_deviations.get(key) if acoustic_deviations else None
            st, var, zz = classify_alignment_row(tgt, act, z)
            rows.append((tgt, act, st, var, zz))
        return rows
