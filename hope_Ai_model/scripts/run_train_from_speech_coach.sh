#!/usr/bin/env bash
# hope_Ai_model/scripts → 기본으로 형제 디렉터리 ../speech-coach 를 사용합니다.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
SC="${SPEECH_COACH_ROOT:-${REPO_ROOT}/../speech-coach}"
if [[ ! -d "${SC}" ]]; then
  echo "speech-coach not found at: ${SC}" >&2
  echo "Set SPEECH_COACH_ROOT to the speech-coach package root." >&2
  exit 1
fi
cd "${SC}"
exec python -m speech_coach.training.train_ctc "$@"
