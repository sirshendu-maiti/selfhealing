import json
from pathlib import Path
from selfheal.scorer.scorer import score_pair
FIXTURES = Path(__file__).parent / "fixtures" / "scorer_pairs.json"
def test_fixture_count_is_twenty():
    assert len(json.loads(FIXTURES.read_text(encoding="utf-8"))) == 20
def test_scores_are_bounded():
    for case in json.loads(FIXTURES.read_text(encoding="utf-8")):
        score = score_pair(case["original"], case["candidate"])["score"]
        assert 0.0 <= score <= 1.0
def test_exact_match_scores_one():
    el = {"tag_name":"button","text":"Save","classes":["primary"],"attributes":{"type":"submit"},"role":"button","parent_tag":"form","parent_text":"Profile","x":10,"y":20,"width":100,"height":40}
    assert score_pair(el, el)["score"] == 1.0
