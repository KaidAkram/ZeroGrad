# Falsifiable questions

## RQ1

Question: Can bounded rules compile without SGD?

H0: the proposed construction or protocol provides no reliable advantage for this observable. H1: it satisfies its declared bounded invariant or measured tradeoff.

Observable: Oracle disagreement rate within L<=128.

Controls: Compiled weights vs independent oracle; wrong-order/entity negatives.

Failure criterion: Any supported disagreement falsifies the exact construction hypothesis.

Why it matters: makes the scope of a weight-programming claim empirically auditable.

## RQ2

Question: How does robustness vary with length and bindings?

H0: the proposed construction or protocol provides no reliable advantage for this observable. H1: it satisfies its declared bounded invariant or measured tradeoff.

Observable: Accuracy by length and entity; explicit late-pair failure.

Controls: Same compiler, length sweep, finite IDs.

Failure criterion: No degradation outside support would challenge the proposed failure mechanism, not prove unbounded correctness.

Why it matters: makes the scope of a weight-programming claim empirically auditable.

## RQ3

Question: Can analytic edits balance target repair and locality?

H0: the proposed construction or protocol provides no reliable advantage for this observable. H1: it satisfies its declared bounded invariant or measured tradeoff.

Observable: Target MSE, unrelated-output MSE, update rank/norm.

Controls: Naive, random-direction and shuffled-target patches on identical checkpoint.

Failure criterion: Failure to improve target or drift above the predeclared application tolerance rejects usefulness; no production tolerance is claimed here.

Why it matters: makes the scope of a weight-programming claim empirically auditable.

## RQ4

Question: Where does compilation fail relative to learned semantic methods?

H0: the proposed construction or protocol provides no reliable advantage for this observable. H1: it satisfies its declared bounded invariant or measured tradeoff.

Observable: Matched task accuracy and semantic held-out performance.

Controls: Identical-architecture trained model and semantic model; NOT RUN yet.

Failure criterion: A compiled win on this symbolic generator does not answer semantic generalization.

Why it matters: makes the scope of a weight-programming claim empirically auditable.

## RQ5

Question: Can event-sourced weight changes support faithful visualization?

H0: the proposed construction or protocol provides no reliable advantage for this observable. H1: it satisfies its declared bounded invariant or measured tradeoff.

Observable: Replay checksum equality, schema violations, UI evidence binding.

Controls: Tampered checksum/coordinate negative tests.

Failure criterion: Any mismatched reconstructed tensor or unsupported displayed metric rejects fidelity.

Why it matters: makes the scope of a weight-programming claim empirically auditable.