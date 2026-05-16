from speech_coach.models.aligner import needleman_wunsch_align


def test_nw_identical():
    a = ["s", "a"]
    assert needleman_wunsch_align(a, a) == [("s", "s"), ("a", "a")]


def test_nw_substitution():
    al = needleman_wunsch_align(["s", "a"], ["t", "a"])
    assert ("s", "t") in al or ("t", "s") in al
