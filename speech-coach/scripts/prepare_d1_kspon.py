#!/usr/bin/env python3
"""D1 KsponSpeech manifest (wrapper)."""

from speech_coach.data.prepare_d1 import build_d1_manifests

if __name__ == "__main__":
    print(build_d1_manifests())
