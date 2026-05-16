"""오디오 전처리 (설계서 Module preprocess)."""

from __future__ import annotations

import io
from typing import BinaryIO

import numpy as np
import soundfile as sf
import torch


def load_wav_bytes(data: bytes, target_sr: int = 16000) -> torch.Tensor:
    """WAV 바이트를 float32 텐서 (1, T)로 로드. 리샘플은 추후 torchaudio로 확장."""
    buf: BinaryIO = io.BytesIO(data)
    wav, sr = sf.read(buf, dtype="float32", always_2d=False)
    if wav.ndim > 1:
        wav = wav.mean(axis=-1)
    if sr != target_sr:
        # 최소 구현: 정수비 리샘플이 아니면 경고 없이 단순 보간도 비용 큼 → 그대로 두고 호출측에서 맞추도록
        raise ValueError(f"expected sample rate {target_sr}, got {sr}")
    t = torch.from_numpy(np.asarray(wav, dtype=np.float32)).unsqueeze(0)
    return t


def preprocess(audio_bytes: bytes, target_sr: int = 16000) -> torch.Tensor:
    """§8.2: raw bytes → (1, T) float waveform."""
    return load_wav_bytes(audio_bytes, target_sr=target_sr)


def normalize_peak(wave: torch.Tensor, peak: float = 0.9) -> torch.Tensor:
    m = wave.abs().max().clamp(min=1e-8)
    return wave / m * peak
