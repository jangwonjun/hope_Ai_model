#!/usr/bin/env python3
"""D2 AIHub 어린이 음성 manifest (wrapper)."""

from __future__ import annotations

import argparse
from pathlib import Path

from speech_coach.data.prepare_d2 import build_d2_manifest


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--label-root", type=Path, default=None, help="sn=266 라벨링데이터 루트")
    p.add_argument("--wav-root", type=Path, default=None, help="sn=266 원천데이터 루트")
    p.add_argument("--out", type=Path, default=None)
    args = p.parse_args()
    n = build_d2_manifest(
        out_path=args.out,
        label_root=args.label_root,
        wav_root=args.wav_root,
    )
    print(f"Wrote {n} rows")


if __name__ == "__main__":
    main()
