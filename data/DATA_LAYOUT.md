# HOPE data/ 레이아웃 (D1~D4)

## 1. 형(4080) 워크플로 — 3단계

```text
① data/incoming/          ← zip만 넣기 (README 참고)
② data/raw/*/extracted/   ← python scripts/extract_hope_data.py
③ data/manifests/         ← python scripts/prepare_all_manifests.py
                           ← python scripts/split_manifests.py (train/val/test)
④ 학습                    ← python -m speech_coach.training.train_ctc ...
```

## 2. incoming (zip 드롭 존)

| 폴더 | 파일 |
|------|------|
| `incoming/d1_kspon_scripts/` | `KsponSpeech_scripts.zip` |
| `incoming/d1_kspon_eval/` | `KsponSpeech_eval.zip` |
| `incoming/d1_kspon_train/` | `KsponSpeech_01.zip` … `05.zip` |
| `incoming/d2_aihub_266/` | `어린이_음성데이터셋.zip` (본편) |
| `incoming/d3_free_dialog/` | `자유대화음성샘플.zip` (옵션) |
| `incoming/d4_kor_child/` | `한국아동음성데이터.zip` (옵션) |

## 3. extract 후 (raw)

| ID | 경로 |
|----|------|
| D1 | `raw/d1_kspon/extracted/` + `KsponSpeech_eval/`, `KsponSpeech_01/` … |
| D2 | `raw/d2_aihub_266/extracted/` (`라벨링데이터`, `원천데이터`) |
| D3 | `raw/d3_free_dialog/extracted/` |
| D4 | `raw/d4_kor_child/extracted/` |

## 4. manifest

| 파일 | 용도 |
|------|------|
| `d1_train.jsonl` / `d1_eval_clean.jsonl` | D1 |
| `d2_aihub_kid.jsonl` | D2 |
| `stage1b_d1_60_d2_40.jsonl` | Stage 1-B |
| `stage2_d1_50_d2_50.jsonl` | Stage 2 |
| `*_train.jsonl`, `*_val.jsonl`, `*_test.jsonl` | split 후 |

**split (설계 §4.6):**

```bash
python scripts/split_manifests.py --manifest ../data/manifests/d2_aihub_kid.jsonl
```

## 5. 학습 시간 (설계 §5.1.1, 4080 + XLS-R base)

- **대략 3~4일 / Stage** (effective batch 32, 데이터 ~100h급 가정)
- **총 오디오 시간·max_steps·Stage 수**에 비례
- D1 train 01~05 전부 + D2 본편이면 **1주일 이상** 가능

## 6. 주의

- **eval_clean만으로 본학습 금지** → 과대평가
- **manifest-smoke/final** 은 연결 테스트용, 형에게 받을 산출물 아님
- 대용량은 Git 제외 — incoming zip + raw 는 로컬/드라이브만
