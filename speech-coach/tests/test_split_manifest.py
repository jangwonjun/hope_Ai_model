"""split_manifest speaker-disjoint."""

from __future__ import annotations

import json
from pathlib import Path

from speech_coach.data.split_manifest import split_manifest


def test_split_disjoint_speakers(tmp_path: Path) -> None:
    src = tmp_path / "all.jsonl"
    rows = []
    for spk in ("a", "b", "c", "d", "e"):
        for i in range(3):
            rows.append({"utt_id": f"{spk}_{i}", "speaker_id": spk, "transcript": "사과"})
    src.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8")
    out_dir = tmp_path / "out"
    counts = split_manifest(src, out_dir, train_ratio=0.6, val_ratio=0.2, seed=0)
    assert counts["train"] + counts["val"] + counts["test"] == len(rows)
    train_spks = set()
    for line in (out_dir / "all_train.jsonl").read_text(encoding="utf-8").splitlines():
        train_spks.add(json.loads(line)["speaker_id"])
    val_spks = {
        json.loads(line)["speaker_id"]
        for line in (out_dir / "all_val.jsonl").read_text(encoding="utf-8").splitlines()
        if line
    }
    assert train_spks.isdisjoint(val_spks)
