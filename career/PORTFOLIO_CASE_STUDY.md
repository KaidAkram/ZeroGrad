# Portfolio case study

Challenge: make direct weight construction auditable rather than anecdotal.

Hypothesis: explicit bounded predicates can be compiled without gradient optimization.

Architecture: a prefix-average circuit and an independent linear analytic editor feed a common artifact pipeline.

The compiled circuit matched the oracle on 3072/3072 generated examples at lengths 16–128 across three seeds. At length 256, mean accuracy fell to 70.7%; a constructed length-512 example fails.

The rank-2 analytic patch reduced target MSE from 3.640517 to 0.000334, with unrelated-output drift MSE 0.073793.

Engineering: frozen PyTorch buffers, data-driven coordinate IR, checksummed replay, deterministic safe generators, raw predictions, responsive studio and frame-based media.

What I learned: an exact-arithmetic bound is a product constraint. More impressive-looking architectures must earn their claims through execution.

Next: architecture-matched training and distribution-shift experiments.

These are synthetic, finite symbolic tasks. The main benchmark and studio replay use the prefix circuit. A separately validated four-block transformer implements the same narrow two-stage grammar; three blocks compute and one is identity. The feature MLP and retrieval baselines are diagnostic and not architecture-matched. No semantic or real pretrained-model claim is supported.