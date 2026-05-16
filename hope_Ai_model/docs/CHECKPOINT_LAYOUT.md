# 체크포인트 `final/` 폴더 구조 (요약)

`train_ctc` 가 `trainer.save_model` / `processor.save_pretrained` 로 저장한 결과입니다.

| 파일 | 역할 |
|------|------|
| `model.safetensors` | `Wav2Vec2ForCTC` 가중치 |
| `config.json` | `vocab_size`, `pad_token_id`, 레이어 수 등 |
| `vocab.json` | IPA(및 특수) 토큰 → id |
| `tokenizer_config.json` | `Wav2Vec2CTCTokenizer` 로드용 |
| `processor_config.json` | 16 kHz 등 feature extractor 설정 요약 |
| `training_args.bin` | 당시 `TrainingArguments` 스냅샷 (추론 필수 아님) |

스모크로 몇 스텝만 돌린 폴더는 **품질 검증용이 아니라 파이프라인 검증용**입니다.
