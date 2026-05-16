from speech_coach.models.variation_classifier import VariationClassifier


def test_variation_sub():
    vc = VariationClassifier()
    rows = vc.classify([("s", "t")], {})
    assert rows[0][2] == "SUB"
