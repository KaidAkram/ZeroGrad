# Claim register

| ID | Permitted wording | Evidence | Status / limits |
|---|---|---|---|
| C1 | The compiled circuit matched the oracle on 3072/3072 generated examples at lengths 16–128 across three seeds. At length 256, mean accuracy fell to 70.7%; a constructed length-512 example fails. | telemetry/benchmark_results.json E2 and E5-boundary; raw/predictions.json | Verified for generated samples only |
| C2 | The rank-2 analytic patch reduced target MSE from 3.640517 to 0.000334, with unrelated-output drift MSE 0.073793. | telemetry/benchmark_results.json edits[2] | Verified synthetic linear module only |
| C3 | Direct construction uses zero optimizer/backprop steps | src/zerograd/core.py, tests/test_core.py | Verified frozen buffers; learned baseline does use gradients |
| C4 | Every authored matrix block replays with a matching SHA256 | weight_write_stream.json; test_replay_corruption | Verified four block events, not individual time-stamped writes |
| C5 | Low rank does not imply sparse changed entries | edits[2]: 48 factor parameters, 128 changed / 128 original entries | Verified for this patch only |
| C6 | Within length 128, binary prefix existence is recovered in exact arithmetic | specs/ZEROGRAD_MATH_SPEC.md | Theoretical; FP32 empirical tests supplement proof |

Prohibited: arbitrary-length correctness, full original security-state-machine implementation, zero forgetting, real exploit detection, real pretrained repair, superiority over optimized learned models, peer-reviewed novelty. Media/style numbers (dimensions, frames, dates) require their own file metadata, not benchmark scores.

C7 (verified, bounded): The separately evaluated four-block transformer matched the oracle on 1792/1792 examples, including dense mixtures. It uses 4 heads, D=64, head width 16 and MLP width 256. Three blocks perform computation; block four and three heads per block are identity/zero paths. All 200196 tensor entries (including zeros) are directly authored; 161 are nonzero. Extension results and out-of-support failures are in telemetry/transformer_validation.json, with full write replay in transformer_weight_stream.json. This does not implement arbitrary multi-stage security tracking.

C8 (verified, synthetic): At λ=1, held-out unrelated-output drift MSE is 0.073793; at λ=0 it is 0.070657. Covariance regularization does not guarantee lower held-out drift. Evidence: telemetry/benchmark_results.json edits[2] and edits[0]. This is one favorable synthetic covariance setup, not real model activations.
