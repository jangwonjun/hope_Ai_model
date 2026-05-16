#!/usr/bin/env python3
"""D4 한국어아동(sn=540) manifest (wrapper)."""

from speech_coach.data.prepare_d4 import build_d4_manifest

if __name__ == "__main__":
    print(f"rows: {build_d4_manifest()}")
