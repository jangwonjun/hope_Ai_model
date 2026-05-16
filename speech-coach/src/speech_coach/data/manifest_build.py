"""manifest.jsonl 생성·병합 (설계서 §4.5)."""

from __future__ import annotations

import json
import random
from collections.abc import Iterable
from pathlib import Path
from typing import Any


def manifest_row(
    *,
    utt_id: str,
    audio_path: str | Path,
    transcript: str,
    data_source: str,
    speaker_id: str = "unknown",
    age_group: str = "adult",
    sex: str = "U",
    target_word: str = "",
    target_phonemes: list[str] | None = None,
    duration_s: float = 0.0,
    snr_db: float = 30.0,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    ap = Path(audio_path)
    if repo_root is not None:
        try:
            ap = ap.relative_to(repo_root)
        except ValueError:
            pass
    row: dict[str, Any] = {
        "utt_id": utt_id,
        "audio_path": ap.as_posix(),
        "speaker_id": speaker_id,
        "speaker_meta": {"age_group": age_group, "sex": sex},
        "target_word": target_word,
        "target_phonemes": target_phonemes or [],
        "data_source": data_source,
        "duration_s": duration_s,
        "snr_db": snr_db,
        "transcript": transcript.strip(),
    }
    return row


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
            n += 1
    return n


def merge_manifests(
    inputs: list[tuple[Path, float]],
    out_path: Path,
    *,
    seed: int = 42,
    max_rows: int | None = None,
) -> int:
    """여러 manifest를 가중치 비율로 섞어 하나의 train manifest 생성."""
    rng = random.Random(seed)
    pools: list[list[dict[str, Any]]] = []
    weights: list[float] = []
    for path, w in inputs:
        if not path.is_file() or w <= 0:
            continue
        rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
        if rows:
            pools.append(rows)
            weights.append(w)
    if not pools:
        write_jsonl(out_path, [])
        return 0

    total_w = sum(weights)
    norm = [w / total_w for w in weights]
    # 목표: 가장 큰 풀 크기에 맞춰 비율 샘플
    target_n = max(len(p) for p in pools)
    merged: list[dict[str, Any]] = []
    for pool, frac in zip(pools, norm, strict=True):
        k = max(1, int(target_n * frac))
        if k >= len(pool):
            merged.extend(pool)
        else:
            merged.extend(rng.sample(pool, k))
    rng.shuffle(merged)
    if max_rows is not None:
        merged = merged[:max_rows]
    return write_jsonl(out_path, merged)
