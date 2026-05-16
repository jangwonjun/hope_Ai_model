from speech_coach.models.opensmile_analyzer import OpenSmileAnalyzer


def test_opensmile_loads_empty_ref(tmp_path):
    p = tmp_path / "ref.json"
    p.write_text("{}", encoding="utf-8")
    an = OpenSmileAnalyzer(p)
    assert an.analyze(None, []) == {}
