import numpy as np

from speech_coach.training.audio_io import load_audio_mono_float32


def test_load_kspon_pcm_small():
    from pathlib import Path

    pcm = (
        Path(__file__).resolve().parents[2]
        / "data/raw/kspon/extracted/KsponSpeech_eval/eval_clean/KsponSpeech_E00016.pcm"
    )
    if not pcm.is_file():
        return
    w = load_audio_mono_float32(pcm)
    assert w.ndim == 1
    assert w.dtype == np.float32
    assert len(w) > 0
