"""D2 AIHub 어린이 음성 (sn=266 JSON 또는 300 샘플 WAV+TXT)."""

from __future__ import annotations

import json
from pathlib import Path

from speech_coach.data.hope_paths import D2_EXTRACTED, HOPE_ROOT
from speech_coach.data.manifest_build import manifest_row, write_jsonl


def _rows_from_aihub_json(
    label_root: Path,
    wav_root: Path,
    *,
    data_source: str = "aihub_kid_266",
) -> list[dict]:
    rows: list[dict] = []
    wav_index: dict[str, Path] = {}
    for wav in wav_root.rglob("*.wav"):
        wav_index[wav.name] = wav

    for jp in sorted(label_root.rglob("*.json")):
        meta = json.loads(jp.read_text(encoding="utf-8"))
        if "발화정보" not in meta:
            continue
        info = meta["발화정보"]
        fn = info.get("fileNm") or ""
        if not fn:
            continue
        wav = wav_index.get(fn)
        if wav is None:
            cand = wav_root / jp.relative_to(label_root).parent / fn
            wav = cand if cand.is_file() else None
        if wav is None:
            matches = list(wav_root.rglob(fn))
            wav = matches[0] if matches else None
        if wav is None:
            continue
        rec = meta.get("녹음자정보", {})
        sex = "M" if rec.get("gender") == "남" else "F"
        rows.append(
            manifest_row(
                utt_id=jp.stem,
                audio_path=wav,
                transcript=info.get("stt") or "",
                data_source=data_source,
                speaker_id=str(rec.get("recorderId", jp.parent.name)),
                age_group="child_g1_g6",
                sex=sex,
                duration_s=float(info.get("recrdTime") or 0),
                repo_root=HOPE_ROOT,
            )
        )
    return rows


def _rows_from_300_sample(extracted: Path) -> list[dict]:
    """어린이_및_일반_음성_데이터셋_300 — transcription.txt 와 wav를 순서로 짝짓기."""
    base = extracted / "어린이_음성데이터셋"
    txt_path = base / "transcription.txt"
    wav_dir = base / "wav"
    if not txt_path.is_file() or not wav_dir.is_dir():
        return []
    lines = [ln.strip() for ln in txt_path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    wavs = sorted(wav_dir.glob("*.wav"))
    if len(lines) != len(wavs):
        n = min(len(lines), len(wavs))
        lines, wavs = lines[:n], wavs[:n]
    rows: list[dict] = []
    for i, (line, wav) in enumerate(zip(lines, wavs, strict=False)):
        parts = line.split(maxsplit=1)
        uid = parts[0] if parts else f"utt_{i}"
        trans = parts[1] if len(parts) > 1 else ""
        rows.append(
            manifest_row(
                utt_id=uid,
                audio_path=wav,
                transcript=trans,
                data_source="aihub_kid_266_sample300",
                speaker_id=uid.split("-")[0] if "-" in uid else uid,
                age_group="child_g1_g6",
                sex="U",
                repo_root=HOPE_ROOT,
            )
        )
    return rows


def build_d2_manifest(
    extracted: Path | None = None,
    out_path: Path | None = None,
    *,
    label_root: Path | None = None,
    wav_root: Path | None = None,
) -> int:
    extracted = extracted or D2_EXTRACTED
    out_path = out_path or (HOPE_ROOT / "data" / "manifests" / "d2_aihub_kid.jsonl")

    if label_root and wav_root:
        rows = _rows_from_aihub_json(label_root, wav_root)
    else:
        label_root = extracted / "라벨링데이터"
        wav_root = extracted / "원천데이터"
        if label_root.is_dir() and wav_root.is_dir():
            rows = _rows_from_aihub_json(label_root, wav_root)
        else:
            rows = _rows_from_300_sample(extracted)
    return write_jsonl(out_path, rows)
