"""Module D — 템플릿 피드백 (설계서: LLM 없음)."""

from __future__ import annotations


class FeedbackGenerator:
    def generate(
        self,
        target_word: str,
        classifications: list[tuple[str, str | None, str, str | None, float | None]],
        pcc_score: float,
    ) -> dict[str, str | None]:
        subs = [c for c in classifications if c[2] == "SUB"]
        if subs:
            t0, a0 = subs[0][0], subs[0][1]
            kid = f"'{target_word}'에서 {t0} 대신 {a0}로 들렸어. 천천히 다시 말해볼래?"
        else:
            kid = f"'{target_word}' 잘했어! 계속 연습해보자."
        return {"kid_text": kid, "practice_word_next": None}
