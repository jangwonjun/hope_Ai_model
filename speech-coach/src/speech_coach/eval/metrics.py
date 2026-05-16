"""PER 등 (스켈레톤)."""

from __future__ import annotations


def phoneme_error_rate(ref: list[list[str]], hyp: list[list[str]]) -> float:
    """편집거리 기반 PER (0~1)."""
    if len(ref) != len(hyp):
        raise ValueError("ref/hyp length mismatch")
    total, errs = 0, 0
    for r, h in zip(ref, hyp, strict=True):
        total += len(r) + 1
        errs += _edit_distance(r, h)
    return errs / max(total, 1)


def _edit_distance(a: list[str], b: list[str]) -> int:
    na, nb = len(a), len(b)
    dp = [[0] * (nb + 1) for _ in range(na + 1)]
    for i in range(na + 1):
        dp[i][0] = i
    for j in range(nb + 1):
        dp[0][j] = j
    for i in range(1, na + 1):
        for j in range(1, nb + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + cost)
    return dp[na][nb]
