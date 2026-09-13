# Topic Scoring Model

Score every dimension from 1 (weak) to 5 (exceptional):

| Dimension | Weight | Question |
|---|---:|---|
| Audience fit | 25% | Does this solve a real problem or answer a live question for the target reader? |
| Why now | 20% | Is there a verified event, change, or conversation window? |
| Insight potential | 20% | Can the account add a defensible, non-obvious judgment? |
| Evidence depth | 15% | Are credible primary and independent sources available? |
| Share/save value | 10% | Will readers want to forward, discuss, or retain it? |
| Competition gap | 10% | Is there room beyond existing coverage? |

Calculate:

`weighted_score = sum(score / 5 * weight)`

Interpretation: 80–100 prioritize; 65–79 viable with refinement; 50–64 develop only for strategic reasons; below 50 reject. A score above 80 cannot have evidence confidence `low` without an explicit warning.

Penalize clickbait/claim mismatch, dependence on one unverified source, weak fit with account positioning, and a topic whose useful window will close before publication.
