"""g2p: 사과 같은 대표 예뿐 아니라 받침·희귀 음절·Kspon 마커 등 회귀용 샘플."""

import pytest

from speech_coach.data.g2p_ko import g2p_sentence, g2p_word, normalize_kspon_transcript


def test_g2p_sagwa():
    # ㄱ onset → vocab의 k (§5.2에 별도 ɡ 없음)
    assert g2p_word("사과") == ["s", "a", "k", "w", "a"]


@pytest.mark.parametrize(
    "word,expected",
    [
        # 받침 ㄺ 등은 규칙 단순화 — 손으로 역산하기 어려운 케이스
        ("닭", ["t", "a", "l"]),
        ("값", ["k", "a", "p"]),
        # 희귀·낯선 음절 (코드포인트만 맞으면 동일 규칙 적용)
        ("쀍", ["p͈", "w", "e", "l"]),
        ("힣", ["h", "i", "t"]),
    ],
)
def test_g2p_unlikely_syllables(word: str, expected: list[str]) -> None:
    assert g2p_word(word) == expected


def test_g2p_long_compound_verb() -> None:
    """여러 음절·된소리·받침이 섞인 동사 — 한 줄로 기대열을 외우기 어려움."""
    assert g2p_word("꿰뚫다") == ["k͈", "w", "e", "t͈", "u", "l", "t", "a"]


def test_normalize_kspon_strips_markers() -> None:
    assert normalize_kspon_transcript("b/ 오늘은 o/ 날씨") == "오늘은 날씨"


def test_g2p_sentence_after_kspon_normalize() -> None:
    raw = "b/ 오늘은 o/ 좋다"
    assert g2p_sentence(raw) == g2p_sentence("오늘은 좋다")
