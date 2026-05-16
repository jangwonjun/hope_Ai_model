HOPE data/ — 요약 (상세: DATA_LAYOUT.md, incoming/README.md)

본학습 필수: D1 (Kspon) + D2 (AIHub sn=266). D3/D4는 옵션.

형(4080): zip → data/incoming/ (압축 풀지 말 것) → extract → prepare → split → train

명령 (hope/speech-coach):
  python scripts/extract_hope_data.py --check-only
  python scripts/extract_hope_data.py
  python scripts/prepare_all_manifests.py --stage1b
  python scripts/split_manifests.py --manifest ../data/manifests/stage1b_d1_60_d2_40.jsonl
  python -m speech_coach.training.train_ctc --repo_root .. --manifest ... --bf16  # --smoke 없음

학습 가이드: hope/이주석형님께 드리는 부탁.md (A.12)
