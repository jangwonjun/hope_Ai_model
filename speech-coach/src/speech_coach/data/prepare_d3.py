"""D3 AIHub 자유대화 7~10세 (sn=108) → manifest."""

from __future__ import annotations

import json
from pathlib import Path

from speech_coach.data.hope_paths import D3_EXTRACTED, HOPE_ROOT
from speech_coach.data.manifest_build import manifest_row, write_jsonl


def build_d3_manifest(
    extracted: Path | None = None,
    out_path: Path | None = None,
) -> int:
    extracted = extracted or D3_EXTRACTED
    out_path = out_path or (HOPE_ROOT / "data" / "manifests" / "d3_free_dialog.jsonl")
    label_root = extracted / "라벨링데이터"
    wav_root = extracted / "원천데이터"
    if not label_root.is_dir():
        raise FileNotFoundError(f"D3 label root missing: {label_root} (run extract first)")

    wav_index: dict[str, Path] = {}
    if wav_root.is_dir():
        for wav in wav_root.rglob("*.wav"):
            wav_index[wav.name] = wav

    rows: list[dict] = []
    for jp in sorted(label_root.rglob("*.json")):
        meta = json.loads(jp.read_text(encoding="utf-8"))
        info = meta.get("발화정보") or {}
        fn = info.get("fileNm") or ""
        if not fn:
            continue
        wav = wav_index.get(fn)
        if wav is None and wav_root.is_dir():
            hits = list(wav_root.rglob(fn))
            wav = hits[0] if hits else None
        if wav is None or not wav.is_file():
            continue
        rec = meta.get("녹음자정보", {})
        sex = "M" if rec.get("gender") == "남" else "F"
        rows.append(
            manifest_row(
                utt_id=jp.stem,
                audio_path=wav,
                transcript=info.get("stt") or "",
                data_source="aihub_kid_108",
                speaker_id=str(rec.get("recorderId", jp.parent.name)),
                age_group="child_g7_g10",
                sex=sex,
                duration_s=float(info.get("recrdTime") or 0),
                repo_root=HOPE_ROOT,
            )
        )
    return write_jsonl(out_path, rows)
