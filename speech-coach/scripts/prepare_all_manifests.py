#!/usr/bin/env python3
"""D1~D4 manifest 생성 + stage1_train.jsonl 병합."""

from __future__ import annotations

import argparse
import sys

from speech_coach.data.hope_paths import MANIFESTS_DIR
from speech_coach.data.prepare_d1 import build_d1_manifests
from speech_coach.data.prepare_d2 import build_d2_manifest
from speech_coach.data.prepare_d3 import build_d3_manifest
from speech_coach.data.prepare_d4 import build_d4_manifest
from speech_coach.data.prepare_stage1 import build_stage1_train_manifest


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--d1-only", action="store_true")
    p.add_argument("--include-d3", action="store_true", help="자유대화(sn=108) manifest 포함·병합")
    p.add_argument("--include-d4", action="store_true", help="한국어아동(sn=540) manifest 포함·병합")
    p.add_argument(
        "--stage1b",
        action="store_true",
        help="설계서 §6.1 Stage1-B: D1 60%% + D2 40%% → stage1b_d1_60_d2_40.jsonl",
    )
    p.add_argument(
        "--stage2-mix",
        action="store_true",
        help="설계서 §6.1 Stage2: D1 50%% + D2 50%% → stage2_d1_50_d2_50.jsonl",
    )
    p.add_argument("--max-rows", type=int, default=None)
    args = p.parse_args()

    d1_counts = build_d1_manifests()
    print("D1 manifests:", d1_counts)

    if args.d1_only:
        return

    n2 = build_d2_manifest()
    print(f"D2: {n2} rows -> {MANIFESTS_DIR / 'd2_aihub_kid.jsonl'}")

    if args.include_d3:
        n3 = build_d3_manifest()
        print(f"D3: {n3} rows")

    if args.include_d4:
        n4 = build_d4_manifest()
        print(f"D4: {n4} rows")

    if args.stage1b:
        out = MANIFESTS_DIR / "stage1b_d1_60_d2_40.jsonl"
        n = build_stage1_train_manifest(
            out_path=out,
            d1_weight=0.6,
            d2_weight=0.4,
            max_rows=args.max_rows,
        )
        print(f"stage1b: {n} rows -> {out}")
    elif args.stage2_mix:
        out = MANIFESTS_DIR / "stage2_d1_50_d2_50.jsonl"
        n = build_stage1_train_manifest(
            out_path=out,
            d1_weight=0.5,
            d2_weight=0.5,
            max_rows=args.max_rows,
        )
        print(f"stage2 mix: {n} rows -> {out}")
    else:
        n = build_stage1_train_manifest(
            include_d3=args.include_d3,
            include_d4=args.include_d4,
            max_rows=args.max_rows,
        )
        out = MANIFESTS_DIR / "stage1_train.jsonl"
        print(f"stage1_train: {n} rows -> {out}")
    if n == 0:
        sys.exit(
            "No rows — run: python scripts/extract_hope_data.py "
            "then prepare_all_manifests.py again"
        )


if __name__ == "__main__":
    main()
