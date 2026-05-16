"""Module B-1 — Needleman–Wunsch 음소 정렬."""

from __future__ import annotations


def needleman_wunsch_align(
    target: list[str],
    predicted: list[str],
    match: int = 2,
    mismatch: int = -1,
    gap: int = -2,
) -> list[tuple[str | None, str | None]]:
    """글로벌 정렬. (target 토큰, predicted 토큰), gap은 None."""
    na, nb = len(target), len(predicted)
    dp: list[list[int]] = [[0] * (nb + 1) for _ in range(na + 1)]
    for i in range(1, na + 1):
        dp[i][0] = dp[i - 1][0] + gap
    for j in range(1, nb + 1):
        dp[0][j] = dp[0][j - 1] + gap
    for i in range(1, na + 1):
        for j in range(1, nb + 1):
            s = match if target[i - 1] == predicted[j - 1] else mismatch
            dp[i][j] = max(
                dp[i - 1][j - 1] + s,
                dp[i - 1][j] + gap,
                dp[i][j - 1] + gap,
            )
    i, j = na, nb
    out: list[tuple[str | None, str | None]] = []
    while i > 0 or j > 0:
        if i > 0 and j > 0:
            s = match if target[i - 1] == predicted[j - 1] else mismatch
            if dp[i][j] == dp[i - 1][j - 1] + s:
                out.append((target[i - 1], predicted[j - 1]))
                i -= 1
                j -= 1
                continue
        if i > 0 and dp[i][j] == dp[i - 1][j] + gap:
            out.append((target[i - 1], None))
            i -= 1
            continue
        if j > 0 and dp[i][j] == dp[i][j - 1] + gap:
            out.append((None, predicted[j - 1]))
            j -= 1
            continue
        break
    out.reverse()
    return out


class NeedlemanWunschAligner:
    def align(self, target: list[str], predicted: list[str]) -> list[tuple[str | None, str | None]]:
        return needleman_wunsch_align(target, predicted)
