# Bounded prefix-circuit v1 (architecture decision)

This is a deliberately narrower alternative, not the requested four-block transformer.
No impossibility result about that transformer is claimed. The broader original
security state machine remains unsupported; the narrow four-block extension is separate.
The separately tested follow-on in TRANSFORMER_EXTENSION.md now implements the
numeric four-block architecture for this same narrow grammar. It does not establish
the original brief's broader multi-stage/security/semantic capability.
The executable prefix architecture uses a 64-dimensional embedding, one fixed uniform strict
causal attention operator and ReLU circuits. No LayerNorm, learned Q/K, or semantic tokenizer.

Vocabulary: token 0 is benign; token 1+8*c+4*s+e encodes class c in 0..2,
stage s in 0..1, entity e in 0..3. These are abstract symbols, not syscalls.
Class names are BENIGN, PRIV_ESC_PATTERN, CONTAINER_ESCAPE_PATTERN,
PROMPT_INJECTION_PATTERN; highest numbered matching class wins. An ordered pair
with the same entity is a match. Supported lengths: 2..128. Entity IDs: 0..3.

E[25,64] has E[t,t]=1. S,T[64,12] select first and second stage coordinates:
S[1+8*c+e,4*c+e]=1; T[5+8*c+e,4*c+e]=1.
Register allocation differs from the brief: 0..24 token/entity product symbols;
25..63 unused. Intermediate 12-wide stage banks are explicit tensors, not residual registers.
Input H=E[tokens] has shape B,L,64. A[L,L] has A[i,j]=1/i for j<i,
zero otherwise; row zero is defined as zero (equivalent to an empty-prefix sentinel).
For i>0 this is masked softmax with Q=K=0 at any finite beta. There is no
hard-selection approximation: attention averages every previous token.

(1) p = sat(128 A H S), sat(z)=ReLU(z)-ReLU(z-1).
Within support, any positive average is at least 1/127, so p is binary in exact
arithmetic. This saturation has explicit linear weights 128 and biases 0,-1.
(2) g=2 ReLU(p+HT-1.5). Binary truth table: 00,01,10 ->0; 11 ->1.
(3) h=sat(sum_position g), reshape 3x4 and saturate sum_entity.
(4) logits=[0.5,h_1,2h_2,3h_3]; argmax implements precedence.
The network forward is entirely embedding, matrix multiplication, sums and ReLU.
The oracle is a separate sequential set-state program. It is never called by forward.
FP32 rounding is tested; the exact proof is not a floating-point equality guarantee.
Beyond 128, saturation need not recover binary registers; a late single first-stage
event followed by a last-position second-stage event at length 512 is a counterexample.
Costs: attention O(L²*12) compute/storage O(L²); embedding O(25*64).
Direct construction uses frozen buffers, no optimizer or backward.

## Analytic editor
W: o x d, X: d x n, K: d x m, V: o x m, R=V-WK.
Minimize ||D K-R||_F² + lambda/n ||D X||_F² + epsilon ||D||_F².
Differentiating analytically gives D(KKᵀ+lambda XXᵀ/n+epsilon I)=RKᵀ.
M is positive definite for epsilon>0; solve M Dᵀ=K Rᵀ.
Rank(D)<=m. Truncated SVD D=U diag(s) Vh gives B=U_r diag(s_r), A=Vh_r.
This adapts the associative-memory normal equations discussed in MEMIT §4.2,
with explicit ridge on the update and normalized uncentered calibration covariance.
It is not a reproduction of multilayer MEMIT target optimization or ROME causal tracing.
Exact locality on every vector would require D=0. Ridge does not promise zero forgetting.
