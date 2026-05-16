"""§3.4 API Contract — 요청/응답 스키마."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class PhonemeResult(BaseModel):
    target: str
    actual: str | None = None
    status: str  # OK | SUB | DEL | DIS
    variation: str | None = None
    acoustic_deviation_z: float | None = None


class FeedbackBlock(BaseModel):
    kid_text: str
    practice_word_next: str | None = None


class AnalyzeResponse(BaseModel):
    pcc: float
    phoneme_results: list[PhonemeResult]
    feedback: FeedbackBlock
    latency_ms: int
    model_version: str


# multipart 필드는 FastAPI에서 개별 인자로 받음; 이 모델은 문서화용
class AnalyzeFormFields(BaseModel):
    """폼 필드 이름 참고용."""

    audio: Any = Field(description="wav ≤5s, 16kHz mono 권장")
    target_word: str
    target_phonemes: str  # JSON 배열 문자열로 전달 권장 — API에서 파싱
    user_id: str | None = None
