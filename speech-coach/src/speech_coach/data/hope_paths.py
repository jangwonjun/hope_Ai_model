"""HOPE 저장소 data/ 경로 (D1~D4, incoming, manifest)."""

from __future__ import annotations

from pathlib import Path

# speech-coach/src/speech_coach/data/hope_paths.py → hope 루트
HOPE_ROOT = Path(__file__).resolve().parents[4]
DATA_ROOT = HOPE_ROOT / "data"
MANIFESTS_DIR = DATA_ROOT / "manifests"
INCOMING = DATA_ROOT / "incoming"

RAW = DATA_ROOT / "raw"
D1_EXTRACTED = RAW / "d1_kspon" / "extracted"
D2_EXTRACTED = RAW / "d2_aihub_266" / "extracted"
D3_EXTRACTED = RAW / "d3_free_dialog" / "extracted"
D4_EXTRACTED = RAW / "d4_kor_child" / "extracted"

# 형(4080): zip 을 여기에 넣고 extract_hope_data.py 실행
INCOMING_D1_SCRIPTS = INCOMING / "d1_kspon_scripts"
INCOMING_D1_EVAL = INCOMING / "d1_kspon_eval"
INCOMING_D1_TRAIN = INCOMING / "d1_kspon_train"
INCOMING_D2 = INCOMING / "d2_aihub_266"
INCOMING_D3 = INCOMING / "d3_free_dialog"
INCOMING_D4 = INCOMING / "d4_kor_child"

# 레거시(팀 Mac 샘플) — incoming 없을 때 fallback
LEGACY_D1_SCRIPTS_ZIP = DATA_ROOT / "한국어 음성" / "전시문_통합_스크립트" / "KsponSpeech_scripts.zip"
LEGACY_D1_EVAL_ZIP = DATA_ROOT / "한국어 음성" / "평가용_데이터" / "KsponSpeech_eval.zip"
LEGACY_D2_SAMPLE_ZIP = (
    DATA_ROOT / "어린이 음성 데이터셋" / "어린이_및_일반_음성_데이터셋_300(WAV_TXT).zip"
)
LEGACY_D3_ZIP = DATA_ROOT / "자유대화음성샘플.zip"


def d4_zip_candidates() -> list[Path]:
    return [
        INCOMING_D4 / "한국어아동음성데이터.zip",
        INCOMING_D4 / "한국아동음성데이터.zip",
        DATA_ROOT / "한국어아동음성데이터.zip",
        DATA_ROOT / "한국아동음성데이터.zip",
    ]


def d2_full_zip_candidates() -> list[Path]:
    return [
        INCOMING_D2 / "어린이_음성데이터셋.zip",
        INCOMING_D2 / "어린이_음성데이터셋.zip",
    ]


def d2_sample_zip_candidates() -> list[Path]:
    return [
        INCOMING_D2 / "어린이_및_일반_음성_데이터셋_300(WAV_TXT).zip",
        LEGACY_D2_SAMPLE_ZIP,
    ]


def first_existing(paths: list[Path]) -> Path | None:
    for p in paths:
        if p.is_file():
            return p
    return None


DEFAULT_MANIFEST = MANIFESTS_DIR / "stage1_train.jsonl"
DEFAULT_KSPON_TRN = D1_EXTRACTED / "eval_clean.trn"
DEFAULT_KSPON_AUDIO_ROOT = D1_EXTRACTED
