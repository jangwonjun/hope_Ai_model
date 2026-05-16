#!/usr/bin/env python3
"""D3 자유대화(sn=108) manifest (wrapper)."""

from speech_coach.data.prepare_d3 import build_d3_manifest

if __name__ == "__main__":
    print(f"rows: {build_d3_manifest()}")
