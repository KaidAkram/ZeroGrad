# Frozen protocol — 2026-11-10

Before execution: seed schedule 11,22,33; test seeds 10011,10022,10033;
training seeds 20011,20022,20033. Four balanced labels, random positions and
entities, benign reversed/wrong-entity/incomplete pairs. No model selection on test.
Train/test exact sequences are checked for overlap and removed from training.
E1 quick profile: N=50,200,1000; test 256, L=32. N=0 only compiled.
N=5000,20000 deferred; no full sample-efficiency conclusions.
M1 compiled prefix circuit. M5 nearest neighbor over token histograms and ordered
position-bin counts (representation mismatch disclosed). M3 MLP on position-bin
counts is a diagnostic learned baseline, NOT architecture-matched transformer.
M2 and M4 are unsupported in this first bounded study and explicitly reported.
E2 lengths 16,32,64,128,256; E3 reversed pairs and wrong entity pairs.
E4 synthetic linear associative checkpoint, lambda=0,0.1,1,10; naive,
random-direction and shuffled-target controls. Independent calibration/holdout draws.
E5 length-512 counterexample; fuzzy semantics NOT RUN.
Accuracy uses Wilson 95% binomial intervals (not uncertainty over all possible grammars).
Macro F1 uses all four labels with zero_division=0. Save predictions and data hashes.
Exploratory diagnostics are labeled; fixed 100 AdamW steps, no tuning or early stopping,
therefore learned results are a fixed-budget diagnostic and not an optimized baseline.
