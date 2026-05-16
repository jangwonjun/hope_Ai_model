from speech_coach.models.pcc import calc_pcc


def test_pcc_all_ok():
    rows = [("s", "s", "OK", None, 0.1), ("a", "a", "OK", None, 0.2)]
    assert calc_pcc(rows) == 100.0


def test_pcc_half():
    rows = [("s", "t", "SUB", "x", None), ("a", "a", "OK", None, 0.0)]
    assert calc_pcc(rows) == 50.0
