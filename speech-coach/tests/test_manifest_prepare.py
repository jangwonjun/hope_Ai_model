"""manifest 경로·Kspon trn 파싱 단위 테스트."""

from __future__ import annotations

from pathlib import Path

from speech_coach.data.prepare_d1 import resolve_kspon_audio


def test_resolve_kspon_audio_eval_layout(tmp_path: Path) -> None:
    root = tmp_path
    pcm = root / "KsponSpeech_eval" / "eval_clean" / "KsponSpeech_E00001.pcm"
    pcm.parent.mkdir(parents=True)
    pcm.write_bytes(b"\x00\x00" * 100)
    rel = "KsponSpeech_eval/eval_clean/KsponSpeech_E00001.pcm"
    assert resolve_kspon_audio(root, rel) == pcm
