#!/usr/bin/env python3
"""d1/d2 manifest → train/val/test (speaker-disjoint 80/10/10)."""

from __future__ import annotations

import argparse
from pathlib import Path

from speech_coach.data.hope_paths import MANIFESTS_DIR
from speech_coach.data.split_manifest import split_manifest


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--manifest", type=Path, required=True)
    p.add_argument("--out-dir", type=Path, default=MANIFESTS_DIR)
    p.add_argument("--seed", type=int, default=42)
    args = p.parse_args()
    counts = split_manifest(args.manifest, args.out_dir, seed=args.seed)
    print(f"split {args.manifest.name}:", counts)


if __name__ == "__main__":
    main()
