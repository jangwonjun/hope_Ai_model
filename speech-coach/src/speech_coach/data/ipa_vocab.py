"""설계서 v0.8 §5.2 한국어 IPA 35 토큰 (CTC blank = <pad>)."""

from __future__ import annotations

import json
from pathlib import Path

# 설계서 순서 유지 (id 0..34). multi-character IPA는 단일 토큰.
PHONEME_ORDER: list[str] = [
    "<pad>",
    "<unk>",
    "k",
    "k͈",
    "n",
    "t",
    "t͈",
    "l",
    "m",
    "p",
    "p͈",
    "s",
    "s͈",
    "ŋ",
    "tɕ",
    "tɕ͈",
    "tɕʰ",
    "kʰ",
    "tʰ",
    "pʰ",
    "h",
    "w",
    "j",
    "a",
    "ɛ",
    "ʌ",
    "e",
    "o",
    "ø",
    "u",
    "y",
    "ɯ",
    "i",
    "<sil>",
    "<eos>",
]

PHONEME_TO_ID: dict[str, int] = {p: i for i, p in enumerate(PHONEME_ORDER)}
ID_TO_PHONEME: dict[int, str] = {i: p for i, p in enumerate(PHONEME_ORDER)}
VOCAB_SIZE = len(PHONEME_ORDER)


def build_vocab_json(out_path: Path) -> None:
    """Wav2Vec2CTCTokenizer용 vocab.json (token -> id)."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(PHONEME_TO_ID, ensure_ascii=False, indent=2), encoding="utf-8")


def filter_to_vocab(tokens: list[str]) -> list[str]:
    """어휘 밖 토큰은 <unk>로 치환."""
    unk = "<unk>"
    return [t if t in PHONEME_TO_ID else unk for t in tokens]
