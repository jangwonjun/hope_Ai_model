#!/usr/bin/env python3
from speech_coach.eval.metrics import phoneme_error_rate

if __name__ == "__main__":
    per = phoneme_error_rate([["s", "a"]], [["s", "t"]])
    print("stub PER:", per)
