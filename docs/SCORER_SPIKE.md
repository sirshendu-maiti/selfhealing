# Scorer spike — 20 hand-made pairs

- Dataset: `tests/fixtures/scorer_pairs.json` (10 same-target, 10 different-target cases).
- Weighting follows the project report: text 30%, class 20%, attributes 15%, position 15%, parent context 10%, ARIA role 10%.
- Prototype threshold: 0.75 (inherited from project plan; not calibrated).
- Position feature: linear decay to zero over 300 CSS px; if geometry is unknown, use neutral 0.5.
- Text and scalar feature similarity use normalized `SequenceMatcher`; attribute maps average per-key similarities.

## Caveats
This is a hand-authored smoke test, not an unbiased evaluation. It may contain ambiguous or unrealistic cases, and the score does not enforce tag-name equality, locator uniqueness, visibility, enabled state, or action postconditions. Review every false positive. Do not enable automatic healing based on this spike alone.

Run `python -m selfheal.scorer.spike` to regenerate the confusion matrix and per-pair score listing.
