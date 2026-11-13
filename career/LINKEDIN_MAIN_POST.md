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
