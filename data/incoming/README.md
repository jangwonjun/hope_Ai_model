# HOPE 데이터 incoming (형/4080: zip만 여기에 넣기)

**본학습 필수: D1 + D2만.** D3/D4 폴더는 비워 둬도 됩니다.

AI Hub에서 받은 **zip 파일**을 아래 폴더에 넣은 뒤, `hope/speech-coach`에서:

```bash
python scripts/extract_hope_data.py --check-only   # zip 확인
python scripts/extract_hope_data.py
python scripts/prepare_all_manifests.py --stage1b   # 또는 --stage2-mix
```

AI Hub에서 받은 zip 이름이 다르면 표의 **파일명으로 rename** 하세요.

## 폴더별 넣을 파일

| 폴더 | 넣을 zip (파일명 그대로 권장) | 설계 |
|------|------------------------------|------|
| `d1_kspon_scripts/` | `KsponSpeech_scripts.zip` | D1 전사 |
| `d1_kspon_eval/` | `KsponSpeech_eval.zip` | D1 eval (~536MB) |
| `d1_kspon_train/` | `KsponSpeech_01.zip` … `05.zip` | D1 **본학습** (~14GB×5) |
| `d2_aihub_266/` | `어린이_음성데이터셋.zip` (**본편**) | D2 sn=266 |
| `d2_aihub_266/` | (대안) `어린이_및_일반_음성_데이터셋_300(WAV_TXT).zip` | 샘플만 |
| `d3_free_dialog/` | `자유대화음성샘플.zip` | D3 옵션 |
| `d4_kor_child/` | `한국아동음성데이터.zip` | D4 옵션 |

## 압축 해제 결과 (건드리지 말 것)

`data/raw/d1_kspon/extracted/` … `data/manifests/*.jsonl` 은 스크립트가 생성합니다.

## Git

- zip/pcm/wav 는 **커밋하지 않음** (.gitignore)
- 이 README와 `.gitkeep` 만 추적

자세한 학습·배치·split: `../DATA_LAYOUT.md`, `../../이주석형님께 드리는 부탁.md`
