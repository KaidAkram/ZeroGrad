# Project summaries

## Short
ZeroGrad-Sec compiles bounded symbolic sequence rules into neural weights and evaluates analytic low-rank edits on synthetic associations. A local research studio and reproducible media expose the coefficients, assumptions, measurements and failures. It is a research prototype, not a production security detector.

## Medium
I wrote a small detector's neural weights directly from a rule.
The interesting result was where it stopped working.

I built ZeroGrad-Sec to make weight programming inspectable: a finite symbolic grammar, explicit tensor recipes, an independent oracle, and a studio that replays the actual matrix writes.

The compiled circuit matched the oracle on 3072/3072 generated examples at lengths 16–128 across three seeds. At length 256, mean accuracy fell to 70.7%; a constructed length-512 example fails.

That boundary matters. The circuit uses bounded prefix averages and ReLU gates; it is not a general semantic security model, and it is not the four-block transformer I originally set out to investigate. Retrieval and a fixed-budget feature MLP provide diagnostics, not a definitive leaderboard.

The second track asks a different question: can an analytic low-rank patch repair a known synthetic association defect while limiting unrelated changes? The report shows both target improvement and nonzero drift. There is no zero-forgetting guarantee.

The code, raw predictions, mathematical assumptions, and failure case are all part of the project. The visuals consume those artifacts rather than a scripted success curve.

I would welcome critique of the bounded construction and suggestions for an architecture-matched baseline. Reproduce the failure before trusting the success.

https://github.com/KaidAkram/ZeroGrad
#MechanisticInterpretability #MachineLearning #ReproducibleResearch

## Extended
# ZeroGrad-Sec: bounded weight compilation and analytic edits

Technical report / unreviewed research prototype. Author: Akram Kaid. Affiliation not specified.

## Abstract
The compiled circuit matched the oracle on 3072/3072 generated examples at lengths 16–128 across three seeds. At length 256, mean accuracy fell to 70.7%; a constructed length-512 example fails. The rank-2 analytic patch reduced target MSE from 3.640517 to 0.000334, with unrelated-output drift MSE 0.073793. We expose coefficients, symbolic assumptions, raw predictions and replay checksums. This is an engineering testbed and a limited diagnostic study; no algorithmic novelty claim is made.


These are synthetic, finite symbolic tasks. The main benchmark and studio replay use the prefix circuit. A separately validated four-block transformer implements the same narrow two-stage grammar; three blocks compute and one is identity. The feature MLP and retrieval baselines are diagnostic and not architecture-matched. No semantic or real pretrained-model claim is supported.

Read the mathematical specification before extrapolating beyond the toy grammar. The next research stage needs identical-architecture learning and independent replication; the current result is a transparent engineering demonstration with measured limits, not a replacement for semantic model training.

Editorial note: lengths are approximate, not certified word counts.