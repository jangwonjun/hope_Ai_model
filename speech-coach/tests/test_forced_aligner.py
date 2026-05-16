import torch

from speech_coach.models.forced_aligner import ForcedAligner


def test_forced_aligner_stub():
    fa = ForcedAligner()
    logits = torch.zeros(1, 10, 40)
    idx = torch.zeros(1, 3, dtype=torch.long)
    assert fa(logits, idx) == []
