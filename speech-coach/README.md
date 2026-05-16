# speech-coach (HOPE AI 엔진 골격)

[AI 설계서 v0.8](../AI설계서_v0.8.txt) §8의 저장소 구조와 모듈 경계를 따릅니다.  
현재 단계는 **import·API·테스트가 돌아가는 스켈레톤**이며, 실제 Wav2Vec2 학습 체크포인트와 D1/D2 전체 데이터는 별도로 연결합니다.

## 빠른 시작

```bash
cd speech-coach
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
pytest tests/ -q
uvicorn speech_coach.serving.api:app --reload --host 0.0.0.0 --port 8000
```

- 헬스: `GET http://127.0.0.1:8000/health`
- 분석(스텁): `POST http://127.0.0.1:8000/v1/utterance/analyze` (multipart, 필드는 `schemas` 참고)

## 데이터 (설계서 §4)

프로젝트 **루트(`hope/`)** 에 공용 데이터를 둡니다. 자세한 경로는 [`../data/DATA_README.txt`](../data/DATA_README.txt) 를 참고하세요.

| 경로 (hope 기준) | 용도 |
|------------------|------|
| `data/incoming/` | **형: zip 드롭 존** (README per D1~D4) |
| `data/raw/d1_kspon/extracted/` | D1 Kspon (extract 후) |
| `data/raw/d2_aihub_266/extracted/` | D2 어린이 음성 |
| `data/raw/d3_free_dialog/extracted/` | D3 자유대화 |
| `data/raw/d4_kor_child/extracted/` | D4 한국어 아동 |
| `data/manifests/stage1_train.jsonl` | Stage1 병합 manifest (`train_ctc` 기본) |
| `speech-coach/data/d1_kspon/` 등 | 패키지 내 placeholder (실데이터는 위 `data/raw/` 권장) |
| `speech-coach/data/manifest.example.jsonl` | 스키마 예시 |
| `speech-coach/data/normal_distribution_ref.json` | OpenSMILE 정상 분포 reference (학습 후 채움) |

## 학습 (Wav2Vec2 CTC)

- 라벨: [AI 설계서 v0.8](../AI설계서_v0.8.txt) §5.2 **IPA 35음소** (전사는 `g2p_ko`로 음소열로 변환, manifest에 `target_phonemes`가 있으면 우선 사용)
- 엔트리: `python -m speech_coach.training.train_ctc` 또는 `python scripts/train_stage1.py` (동일)
- 기본 데이터: `hope/data/manifests/stage1_train.jsonl` (`extract_hope_data.py` → `prepare_all_manifests.py` 후)
- 로컬 스모크: `--smoke` (가벼운 base 모델 + 짧은 스텝)
- 설계서 Stage1-A 본학습: `--smoke` 없이 GPU에서 `--model_name facebook/wav2vec2-xls-r-300m` 등으로 실행 (의존성: `accelerate`)

자세한 경로는 [`../data/DATA_README.txt`](../data/DATA_README.txt) 참고.

## 스크립트

- `scripts/extract_hope_data.py` — `data/incoming/*.zip` → `data/raw/*/extracted`
- `scripts/prepare_all_manifests.py` — manifest (`--stage1b`, `--stage2-mix`)
- `scripts/split_manifests.py` — train/val/test (speaker-disjoint)
- `scripts/prepare_d1_kspon.py` / `prepare_d2_aihub_kid.py` / `prepare_d3_free_dialog.py` / `prepare_d4_kor_child.py`
- `scripts/train_stage1.py` / `train_stage2.py` — CTC 학습 (`train_ctc` CLI)
- `scripts/build_normal_distribution.py` — §6.4 통계 추출(플레이스홀더)
- `scripts/eval_test.py` — PER 등 평가(플레이스홀더)

## 라이선스

학습 데이터는 각 AI Hub / KsponSpeech 이용약관을 따릅니다.
