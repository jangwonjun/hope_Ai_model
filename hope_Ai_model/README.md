# hope_Ai_model

HOPE 프로젝트 **음소( IPA ) CTC 모델** 관련 메타·스크립트·문서를 두는 저장소입니다.  
**학습 코드의 소스 오브 트루스**는 [`speech-coach`](../speech-coach) 패키지입니다.  
**인수인계:** 저장소 루트 [`이주석형님께 드리는 부탁.md`](../이주석형님께%20드리는%20부탁.md) A.12.

## 이 레포에 두면 좋은 것

| 올려도 되는 것 | 올리지 말 것 |
|----------------|--------------|
| README, 학습/배포 문서 | `*.safetensors`, 대용량 `checkpoints/` |
| 실행 예시 스크립트 (`scripts/`) | 데이터셋 원본·PCM 대량 |
| 작은 설정 예시·실험 메모 | API 키·개인정보 |

가중치는 [Hugging Face Hub](https://huggingface.co/docs/hub/repositories) 또는 팀 스토리지에 올리고, 여기에는 **다운로드 경로·버전·학습 하이퍼파라미터**만 적어 두는 것을 권장합니다.

## 로컬 디렉터리 관계 (권장)

`hope` 루트를 한 번에 클론해 두었다고 가정합니다.

```text
hope/
  speech-coach/     # 학습 엔트리·g2p·ipa_vocab
  hope_Ai_model/    # 본 레포 (문서·스크립트)
  data/             # Kspon 등 (별도 준비, Git 미포함 권장)
```

## 스모크 (연결만 확인)

```bash
export SPEECH_COACH_ROOT="$(cd "$(dirname "$0")/../speech-coach" && pwd)"
cd "$(dirname "$0")"
./scripts/run_train_from_speech_coach.sh --smoke --output_dir /tmp/ctc-smoke
```

## GPU 본학습 (예시)

```bash
export SPEECH_COACH_ROOT="$(cd "$(dirname "$0")/../speech-coach" && pwd)"
cd "$(dirname "$0")"
./scripts/run_train_from_speech_coach.sh \
  --output_dir ./outputs/ctc-stage1-ipa \
  --model_name facebook/wav2vec2-xls-r-300m \
  --max_steps 50000 \
  --train_batch_size 8 \
  --gradient_accumulation_steps 2
```

데이터가 기본 경로에 없으면 `hope/speech-coach` README대로 `--manifest` / `--repo_root` 를 추가합니다.

## 체크포인트 해석

학습이 끝나면 `.../final` 에 `model.safetensors`, `config.json`, `vocab.json`, `tokenizer_config.json`, `processor_config.json` 등이 생깁니다.  
`vocab_size` 가 설계서 §5.2의 35보다 클 수 있는데, Hugging Face `Wav2Vec2CTCTokenizer`가 `|`, `<s>`, `</s>` 등을 추가하기 때문입니다. CTC blank는 보통 `pad_token_id`(0, `<pad>`)에 맞춥니다.

## 원격 저장소

https://github.com/jangwonjun/hope_Ai_model
