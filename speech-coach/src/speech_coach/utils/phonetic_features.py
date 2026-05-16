"""음성학 특징 보조 유틸 (추후 확장)."""

from __future__ import annotations


def ipa_token_ok(token: str) -> bool:
    return bool(token and token.strip())
