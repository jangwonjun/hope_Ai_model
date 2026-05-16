"""AI Hub / Kspon zip → hope/data/raw/.../extracted (incoming 우선)."""

from __future__ import annotations

import zipfile
from pathlib import Path

from speech_coach.data.hope_paths import (
    D1_EXTRACTED,
    D2_EXTRACTED,
    D3_EXTRACTED,
    D4_EXTRACTED,
    INCOMING_D1_EVAL,
    INCOMING_D1_SCRIPTS,
    INCOMING_D1_TRAIN,
    INCOMING_D3,
    LEGACY_D1_EVAL_ZIP,
    LEGACY_D1_SCRIPTS_ZIP,
    LEGACY_D3_ZIP,
    d2_full_zip_candidates,
    d2_sample_zip_candidates,
    d4_zip_candidates,
    first_existing,
)


def _unzip(zip_path: Path, dest: Path) -> None:
    if not zip_path.is_file():
        raise FileNotFoundError(zip_path)
    dest.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path) as zf:
        zf.extractall(dest)


def _extract_trn_from_scripts(scripts_zip: Path, root: Path) -> None:
    if not scripts_zip.is_file():
        return
    with zipfile.ZipFile(scripts_zip) as zf:
        for name in ("eval_clean.trn", "eval_other.trn", "train.trn", "dev.trn"):
            if name in zf.namelist():
                zf.extract(name, root)


def extract_d1_kspon() -> Path:
    """scripts + eval + train(01~05) zip → extracted."""
    root = D1_EXTRACTED
    root.mkdir(parents=True, exist_ok=True)

    scripts_zip = first_existing(
        [
            INCOMING_D1_SCRIPTS / "KsponSpeech_scripts.zip",
            LEGACY_D1_SCRIPTS_ZIP,
        ]
    )
    eval_zip = first_existing(
        [
            INCOMING_D1_EVAL / "KsponSpeech_eval.zip",
            LEGACY_D1_EVAL_ZIP,
        ]
    )

    if scripts_zip:
        _extract_trn_from_scripts(scripts_zip, root)
    if eval_zip:
        eval_parent = root / "KsponSpeech_eval"
        eval_parent.mkdir(parents=True, exist_ok=True)
        _unzip(eval_zip, eval_parent)

    train_zips = sorted(INCOMING_D1_TRAIN.glob("KsponSpeech_*.zip"))
    if not train_zips:
        train_zips = sorted(INCOMING_D1_TRAIN.glob("*.zip"))
    for z in train_zips:
        _unzip(z, root)

    return root


def extract_d2() -> Path:
    """D2 본편(라벨+wav) 우선, 없으면 300 샘플."""
    root = D2_EXTRACTED
    root.mkdir(parents=True, exist_ok=True)

    full_zip = first_existing(d2_full_zip_candidates())
    if full_zip:
        _unzip(full_zip, root)
        return root

    sample_zip = first_existing(d2_sample_zip_candidates())
    if sample_zip:
        _unzip(sample_zip, root)
        sample_root = root / "어린이_음성데이터셋"
        inner = sample_root / "300wav.zip"
        if inner.is_file():
            wav_dir = sample_root / "wav"
            wav_dir.mkdir(parents=True, exist_ok=True)
            _unzip(inner, wav_dir)
        return root

    raise FileNotFoundError(
        "D2 zip not found. Put 어린이_음성데이터셋.zip (본편) or "
        "어린이_및_일반_음성_데이터셋_300(WAV_TXT).zip under data/incoming/d2_aihub_266/"
    )


def extract_d3_free_dialog() -> Path:
    root = D3_EXTRACTED
    root.mkdir(parents=True, exist_ok=True)
    z = first_existing(
        [
            INCOMING_D3 / "자유대화음성샘플.zip",
            INCOMING_D3 / "자유대화.zip",
            LEGACY_D3_ZIP,
        ]
    )
    if not z:
        raise FileNotFoundError("D3 zip not found under data/incoming/d3_free_dialog/")
    _unzip(z, root)
    return root


def extract_d4_kor_child() -> Path:
    root = D4_EXTRACTED
    root.mkdir(parents=True, exist_ok=True)
    z = first_existing(d4_zip_candidates())
    if not z:
        raise FileNotFoundError("D4 zip not found under data/incoming/d4_kor_child/")
    _unzip(z, root)
    return root


def extract_all(*, d1: bool = True, d2: bool = True, d3: bool = True, d4: bool = True) -> dict[str, Path]:
    out: dict[str, Path] = {}
    if d1:
        out["d1"] = extract_d1_kspon()
    if d2:
        try:
            out["d2"] = extract_d2()
        except FileNotFoundError as e:
            print(f"skip d2: {e}")
    if d3:
        try:
            out["d3"] = extract_d3_free_dialog()
        except FileNotFoundError as e:
            print(f"skip d3: {e}")
    if d4:
        try:
            out["d4"] = extract_d4_kor_child()
        except FileNotFoundError as e:
            print(f"skip d4: {e}")
    return out
