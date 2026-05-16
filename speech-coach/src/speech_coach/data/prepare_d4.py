"""D4 AIHub 한국어 아동 음성 (sn=540, kor_free JSON) → manifest."""

from __future__ import annotations

import json
from pathlib import Path

from speech_coach.data.hope_paths import D4_EXTRACTED, HOPE_ROOT
from speech_coach.data.manifest_build import manifest_row, write_jsonl


def build_d4_manifest(
    extracted: Path | None = None,
    out_path: Path | None = None,
) -> int:
    extracted = extracted or D4_EXTRACTED
    out_path = out_path or (HOPE_ROOT / "data" / "manifests" / "d4_kor_child.jsonl")
    label_root = extracted / "라벨링데이터"
    wav_root = extracted / "원천데이터"
    if not label_root.is_dir() or not wav_root.is_dir():
        raise FileNotFoundError(f"D4 extracted layout missing under {extracted}")

    wav_index: dict[str, Path] = {p.name: p for p in wav_root.rglob("*.wav")}
    rows: list[dict] = []
    for jp in sorted(label_root.rglob("*.json")):
        meta = json.loads(jp.read_text(encoding="utf-8"))
        file_info = meta.get("File") or {}
        fn = file_info.get("FileName") or ""
        if not fn:
            continue
        wav = wav_index.get(fn) or next(iter(wav_root.rglob(fn)), None)
        if wav is None or not wav.is_file():
            continue
        spk = meta.get("Speaker") or {}
        sex_raw = (spk.get("Gender") or "U").upper()
        sex = "M" if sex_raw.startswith("M") else "F" if sex_raw.startswith("F") else "U"
        age = spk.get("Age")
        try:
            age_i = int(age) if age is not None else 0
        except (TypeError, ValueError):
            age_i = 0
        age_group = "child_g1_g6" if age_i <= 12 else "child_g7_g10"
        trans = (meta.get("Transcription") or {}).get("LabelText") or ""
        rows.append(
            manifest_row(
                utt_id=jp.stem,
                audio_path=wav,
                transcript=trans,
                data_source="aihub_kid_540",
                speaker_id=str(spk.get("SpeakerName") or jp.parent.name),
                age_group=age_group,
                sex=sex,
                duration_s=float(file_info.get("FileLength") or 0),
                repo_root=HOPE_ROOT,
            )
        )
    return write_jsonl(out_path, rows)
