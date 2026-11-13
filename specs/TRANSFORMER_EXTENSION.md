# Four-block bounded transformer extension

This follow-on implements the brief's numeric architecture (4 blocks, 4 heads,
64 features, 16 head features, 256 MLP features, vocabulary capacity 32).
The grammar remains a **two-stage, four-entity abstract grammar**. No claim is made
about arbitrary longer security state machines. The original prefix-circuit
results remain unchanged and are identified separately from this extension.

Tokens 0..24 and embedding registers 0..24 follow the prefix spec. Registers
25..31 are unused. Registers 32..43 hold prefix start-presence; 44..55 hold
12 entity-specific matches; 56..58 hold three pooled class matches; 59..63 unused.
This revised register map is explicit and differs from the brief's target map.

Each head uses WQ,WK,WV[64,16], WO[16,64], A=softmax(beta QKᵀ+mask).
The mask is standard **inclusive causal**. All Q/K are zero, so A[i,j]=1/(i+1)
for j<=i and zero otherwise; beta is mathematically irrelevant. There is no
temperature-based hard-routing claim. Heads 1..3 have zero value/output weights.

Block 0 head 0 selects the 12 first-stage token coordinates into values and
writes 128 times the prefix averages to 32..43. Its MLP writes
`-ReLU(x[32+j]-1)` back to the same coordinate. With residual addition this is
`min(x[32+j],1)` because x>=0. Presence is binary in exact arithmetic for L<=128.

Block 1 has zero attention outputs. Its MLP writes
`2 ReLU(x[32+j]+x[end_token(j)]-1.5)` to 44+j. Current tokens cannot be both
first-stage and second-stage, so inclusive attention does not introduce a
self-match. This establishes the strict ordered-pair predicate.

Block 2 head 0 sums each four-entity gate bank into three value coordinates,
then writes 128 times their causal averages to 56..58. The MLP saturates those
registers with the same residual correction. At the last position, this is
existence of a completed pair anywhere in the sequence. Block 3 is an explicit
identity ablation (all projections/MLPs zero). No claim that four active blocks
are necessary: this construction uses three computational blocks.

Readout WU[64,4] has WU[56+c,c+1]=c+1; output bias bU[0]=0.5.
This implements the oracle's highest-class precedence. No LayerNorm, dropout or
position embedding is used. Softmax rows are finite because each includes itself.
All parameters are frozen buffers, authored by `transformer_ir()`.

The normal forward runs all four heads and all four blocks, including zeros.
Computational complexity is O(B * blocks * heads * L² * d_head) for attention
plus O(B * blocks * L * D * M) for MLPs; dense buffers include authored zeros.
It is an interpretability fixture, not an optimized deployment model.

Tests cover all supported lengths, overlap precedence, mixtures, masks, beta
invariance, frozen tensors and full tensor replay. The original circuit's length
512 counterexample is not automatically the transformer's counterexample;
extension-specific out-of-support behavior is recorded in a separate artifact.
