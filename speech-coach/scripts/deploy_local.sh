#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
exec uvicorn speech_coach.serving.api:app --host 0.0.0.0 --port 8000
