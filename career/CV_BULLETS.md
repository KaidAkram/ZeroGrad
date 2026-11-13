# Evidence-grounded CV options

- Built a PyTorch weight compiler for bounded symbolic sequence detection, with zero optimizer steps in the compiled path, checksum-verified tensor replay and an interactive research studio.
- Evaluated a compiled prefix circuit on 3072 generated examples within its declared length support and documented an out-of-support failure; implemented retrieval and fixed-budget AdamW diagnostics.
- Derived and tested covariance-regularized low-rank matrix edits with target efficacy, unrelated-output drift and random/shuffled controls.

Short resume: Built ZeroGrad-Sec, a reproducible PyTorch testbed for bounded weight compilation and analytic editing, with evidence-linked visualizations.

Research CV: The compiled circuit matched the oracle on 3072/3072 generated examples at lengths 16–128 across three seeds. At length 256, mean accuracy fell to 70.7%; a constructed length-512 example fails. The rank-2 analytic patch reduced target MSE from 3.640517 to 0.000334, with unrelated-output drift MSE 0.073793. Scope and provenance: Claim Register C1–C6. Do not describe this as real-model repair or deployed threat detection.
