#!/usr/bin/env python3
"""§6.4 정상 분포 reference — 추후 forced_align + OpenSMILE 연동."""

from pathlib import Path

from speech_coach.eval.normal_distribution import build_reference_placeholder

if __name__ == "__main__":
    out = Path(__file__).resolve().parents[1] / "data" / "normal_distribution_ref.json"
    build_reference_placeholder(out)
    print(f"Wrote placeholder {out}")
