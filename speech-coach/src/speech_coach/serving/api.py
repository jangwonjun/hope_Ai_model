"""FastAPI 서버 — §3.4 POST /v1/utterance/analyze."""

from __future__ import annotations

import json

from fastapi import FastAPI, File, Form, HTTPException, UploadFile

from speech_coach import __version__
from speech_coach.serving.pipeline import InferencePipeline

app = FastAPI(title="speech-coach", version=__version__)
_pipeline: InferencePipeline | None = None


def get_pipeline() -> InferencePipeline:
    global _pipeline
    if _pipeline is None:
        _pipeline = InferencePipeline.from_stub()
    return _pipeline


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "version": __version__}


@app.post("/v1/utterance/analyze")
async def analyze(
    audio: UploadFile = File(..., description="16kHz mono WAV, ≤5s"),
    target_word: str = Form(...),
    target_phonemes: str = Form(..., description='JSON 배열 문자열, 예: ["s","a"]'),
    user_id: str | None = Form(None),
):
    _ = user_id
    try:
        phones = json.loads(target_phonemes)
        if not isinstance(phones, list) or not all(isinstance(p, str) for p in phones):
            raise ValueError("target_phonemes must be a JSON array of strings")
    except (json.JSONDecodeError, ValueError) as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    raw = await audio.read()
    if len(raw) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="audio too large")

    try:
        out = get_pipeline()(raw, target_word=target_word, target_phonemes=phones)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    return out.model_dump()
