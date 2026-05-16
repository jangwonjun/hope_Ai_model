#!/usr/bin/env python3
"""AI Hub / Kspon zip (data/incoming/) → data/raw/*/extracted."""

from __future__ import annotations

import argparse

from speech_coach.data.extract_archives import extract_all
from speech_coach.data.hope_paths import (
    INCOMING,
    INCOMING_D1_EVAL,
    INCOMING_D1_SCRIPTS,
    INCOMING_D1_TRAIN,
    INCOMING_D2,
    INCOMING_D3,
    INCOMING_D4,
)


def _check_incoming() -> None:
    checks = [
        ("D1 scripts", INCOMING_D1_SCRIPTS / "KsponSpeech_scripts.zip"),
        ("D1 eval", INCOMING_D1_EVAL / "KsponSpeech_eval.zip"),
        ("D1 train", list(INCOMING_D1_TRAIN.glob("KsponSpeech_*.zip")) or list(INCOMING_D1_TRAIN.glob("*.zip"))),
        ("D2", list(INCOMING_D2.glob("*.zip"))),
        ("D3", list(INCOMING_D3.glob("*.zip"))),
        ("D4", list(INCOMING_D4.glob("*.zip"))),
    ]
    print(f"incoming root: {INCOMING}")
    for label, item in checks:
        if isinstance(item, list):
            ok = len(item) > 0
            detail = ", ".join(p.name for p in item[:3]) or "(empty)"
        else:
            ok = item.is_file()
            detail = item.name if ok else "(missing)"
        mark = "OK" if ok else "—"
        print(f"  [{mark}] {label}: {detail}")


def main() -> None:
    p = argparse.ArgumentParser(description="Extract HOPE D1~D4 from data/incoming/ → data/raw/")
    p.add_argument("--skip-d1", action="store_true")
    p.add_argument("--skip-d2", action="store_true")
    p.add_argument("--skip-d3", action="store_true")
    p.add_argument("--skip-d4", action="store_true")
    p.add_argument("--check-only", action="store_true", help="incoming zip 존재만 출력")
    args = p.parse_args()

    _check_incoming()
    if args.check_only:
        return

    paths = extract_all(
        d1=not args.skip_d1,
        d2=not args.skip_d2,
        d3=not args.skip_d3,
        d4=not args.skip_d4,
    )
    print("extracted:")
    for key, path in paths.items():
        print(f"  {key}: {path}")


if __name__ == "__main__":
    main()
