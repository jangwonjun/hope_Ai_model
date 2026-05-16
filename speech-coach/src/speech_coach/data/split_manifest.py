"""manifest.jsonl → train/val/test (speaker-disjoint, 설계서 §4.6)."""

from __future__ import annotations

import json
import random
from pathlib import Path


def split_manifest(
    src: Path,
    out_dir: Path,
    *,
    train_ratio: float = 0.8,
    val_ratio: float = 0.1,
    seed: int = 42,
) -> dict[str, int]:
    """speaker_id 기준으로 분할 (같은 화자는 한 split만)."""
    rows: list[dict] = []
    for line in Path(src).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    by_spk: dict[str, list[dict]] = {}
    for row in rows:
        spk = row.get("speaker_id") or "unknown"
        by_spk.setdefault(spk, []).append(row)

    spks = list(by_spk.keys())
    rng = random.Random(seed)
    rng.shuffle(spks)
    n = len(spks)
    n_train = max(1, int(n * train_ratio))
    n_val = max(0, int(n * val_ratio))
    train_spks = set(spks[:n_train])
    val_spks = set(spks[n_train : n_train + n_val])

    buckets = {"train": [], "val": [], "test": []}
    for spk, items in by_spk.items():
        if spk in train_spks:
            buckets["train"].extend(items)
        elif spk in val_spks:
            buckets["val"].extend(items)
        else:
            buckets["test"].extend(items)

    out_dir.mkdir(parents=True, exist_ok=True)
    counts: dict[str, int] = {}
    stem = src.stem
    for name, items in buckets.items():
        out = out_dir / f"{stem}_{name}.jsonl"
        with out.open("w", encoding="utf-8") as f:
            for row in items:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
        counts[name] = len(items)
    return counts
