"""PCM / WAV 로드 (KsponSpeech eval_clean.pcm = 16kHz mono s16le)."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import soundfile as sf


def load_audio_mono_float32(path: str | Path, target_sr: int = 16000) -> np.ndarray:
    path = Path(path)
    if path.suffix.lower() == ".pcm":
        raw = np.fromfile(path, dtype="<i2")
        wav = raw.astype(np.float32) / 32768.0
        return wav
    wav, sr = sf.read(str(path), dtype="float32", always_2d=False)
    if wav.ndim > 1:
        wav = wav.mean(axis=-1)
    if sr != target_sr:
        raise ValueError(f"{path}: expected sr={target_sr}, got {sr}")
    return np.asarray(wav, dtype=np.float32)
