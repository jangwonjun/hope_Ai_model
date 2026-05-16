"""D1 KsponSpeech → manifest.jsonl."""

from __future__ import annotations

from pathlib import Path

from speech_coach.data.hope_paths import D1_EXTRACTED, HOPE_ROOT
from speech_coach.data.manifest_build import manifest_row, write_jsonl


def resolve_kspon_audio(audio_root: Path, rel: str) -> Path | None:
    rel = rel.strip().replace("\\", "/")
    candidates = [
        audio_root / rel,
        audio_root / Path(rel).name,
    ]
    if "KsponSpeech_eval/" in rel:
        suffix = rel.split("KsponSpeech_eval/", 1)[1]
        candidates.append(audio_root / "KsponSpeech_eval" / suffix)
        candidates.append(audio_root / suffix)
    for c in candidates:
        if c.is_file():
            return c
    return None


def parse_kspon_trn(trn_path: Path, audio_root: Path, *, data_source: str = "kspon") -> list[dict]:
    rows: list[dict] = []
    for i, line in enumerate(trn_path.read_text(encoding="utf-8").splitlines()):
        line = line.strip()
        if not line or "::" not in line:
            continue
        rel, trans = line.split("::", 1)
        rel = rel.strip()
        trans = trans.strip()
        ap = resolve_kspon_audio(audio_root, rel)
        if ap is None:
            continue
        utt_id = f"kspon_{trn_path.stem}_{i:06d}"
        spk = Path(rel).stem.split("_")[0] if "_" in Path(rel).stem else "unknown"
        rows.append(
            manifest_row(
                utt_id=utt_id,
                audio_path=ap,
                transcript=trans,
                data_source=data_source,
                speaker_id=spk,
                age_group="adult",
                sex="U",
                repo_root=HOPE_ROOT,
            )
        )
    return rows


def build_d1_manifests(
    extracted: Path | None = None,
    out_dir: Path | None = None,
) -> dict[str, int]:
    extracted = extracted or D1_EXTRACTED
    out_dir = out_dir or (HOPE_ROOT / "data" / "manifests")
    counts: dict[str, int] = {}
    for trn_name in ("eval_clean", "eval_other", "train", "dev"):
        trn = extracted / f"{trn_name}.trn"
        if not trn.is_file():
            continue
        rows = parse_kspon_trn(trn, extracted)
        out = out_dir / f"d1_{trn_name}.jsonl"
        counts[trn_name] = write_jsonl(out, rows)
    return counts
