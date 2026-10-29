from __future__ import annotations
import json
from pathlib import Path
from statistics import mean
from selfheal.scorer.scorer import score_pair

FIXTURES = Path(__file__).resolve().parents[3] / "tests" / "fixtures" / "scorer_pairs.json"
THRESHOLD = 0.75

def main() -> None:
    cases = json.loads(FIXTURES.read_text(encoding="utf-8"))
    rows = []
    tp = fp = tn = fn = 0
    for c in cases:
        result = score_pair(c["original"], c["candidate"])
        predicted = result["score"] >= THRESHOLD
        actual = c["same_target"]
        tp += predicted and actual
        fp += predicted and not actual
        tn += (not predicted) and (not actual)
        fn += (not predicted) and actual
        rows.append((c["id"], c["same_target"], result["score"], predicted, c["note"]))
    print(f"Scorer spike: {len(rows)} hand-authored pairs | threshold={THRESHOLD:.2f}")
    print("id   truth  score  predicted  note")
    for ident, truth, score, pred, note in rows:
        print(f"{ident:<4} {str(truth):<6} {score:>5.3f}  {str(pred):<9}  {note}")
    accuracy = (tp + tn) / len(rows) if rows else 0
    precision = tp / (tp + fp) if tp + fp else 0
    recall = tp / (tp + fn) if tp + fn else 0
    print(f"\nTP={tp} FP={fp} TN={tn} FN={fn}")
    print(f"accuracy={accuracy:.3f} precision={precision:.3f} recall={recall:.3f}")
    print(f"mean score={mean(r[2] for r in rows):.3f}")
    print("NOTE: hand-made smoke benchmark only; threshold and feature handling require calibration on real DOM captures.")

if __name__ == "__main__":
    main()
