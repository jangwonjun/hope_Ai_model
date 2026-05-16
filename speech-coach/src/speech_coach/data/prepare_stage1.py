"""Stage1 manifest: D1 50% + D2 50% (설계서 §4.2, 옵션 D3/D4)."""

from __future__ import annotations

from pathlib import Path

from speech_coach.data.hope_paths import MANIFESTS_DIR
from speech_coach.data.manifest_build import merge_manifests
from speech_coach.data.prepare_d1 import build_d1_manifests
from speech_coach.data.prepare_d2 import build_d2_manifest
from speech_coach.data.prepare_d3 import build_d3_manifest
from speech_coach.data.prepare_d4 import build_d4_manifest


def build_stage1_train_manifest(
    out_path: Path | None = None,
    *,
    d1_weight: float = 0.5,
    d2_weight: float = 0.5,
    include_d3: bool = False,
    include_d4: bool = False,
    d3_weight: float = 0.0,
    d4_weight: float = 0.0,
    max_rows: int | None = None,
) -> int:
    mdir = MANIFESTS_DIR
    build_d1_manifests(out_dir=mdir)
    build_d2_manifest(out_path=mdir / "d2_aihub_kid.jsonl")

    inputs: list[tuple[Path, float]] = [
        (mdir / "d1_eval_clean.jsonl", d1_weight),
        (mdir / "d2_aihub_kid.jsonl", d2_weight),
    ]
    if include_d3 or d3_weight > 0:
        build_d3_manifest(out_path=mdir / "d3_free_dialog.jsonl")
        inputs.append((mdir / "d3_free_dialog.jsonl", d3_weight if d3_weight > 0 else 0.1))
    if include_d4 or d4_weight > 0:
        build_d4_manifest(out_path=mdir / "d4_kor_child.jsonl")
        inputs.append((mdir / "d4_kor_child.jsonl", d4_weight if d4_weight > 0 else 0.1))

    # train.trn 이 있으면 d1_train 을 eval 대신/추가로 쓸 수 있음
    train_m = mdir / "d1_train.jsonl"
    if train_m.is_file() and train_m.stat().st_size > 0:
        inputs = [(train_m, d1_weight), (mdir / "d2_aihub_kid.jsonl", d2_weight)] + inputs[2:]

    out_path = out_path or (mdir / "stage1_train.jsonl")
    return merge_manifests(inputs, out_path, max_rows=max_rows)
