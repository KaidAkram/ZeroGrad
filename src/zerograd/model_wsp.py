"""Four-block, four-head transformer compilation of the bounded two-stage grammar.

This extension has ordinary causal softmax attention, residuals and ReLU MLPs,
without LayerNorm. Three blocks compute; the fourth is an explicit identity.
It is not a compiler for the original brief's unspecified longer syscall chains.
"""
import torch
from torch import nn
from zerograd.core import Write, digest


def transformer_ir(bound=128):
    """Each assignment is an authored block, including zero-initialized projections."""
    ops = [Write('W_E', (32, 64), tuple((i, i, 1.) for i in range(25)), 'E[t,t]=1 for t<25')]
    for layer in range(4):
        for head in range(4):
            for name, shape in [('W_Q', (64, 16)), ('W_K', (64, 16)), ('W_V', (64, 16)), ('W_O', (16, 64))]:
                coords = []
                if head == 0 and layer == 0:
                    if name == 'W_V': coords = [(1+8*c+e, 4*c+e, 1.) for c in range(3) for e in range(4)]
                    if name == 'W_O': coords = [(j, 32+j, float(bound)) for j in range(12)]
                if head == 0 and layer == 2:
                    if name == 'W_V': coords = [(44+4*c+e, c, 1.) for c in range(3) for e in range(4)]
                    if name == 'W_O': coords = [(c, 56+c, float(bound)) for c in range(3)]
                ops.append(Write(f'L{layer}_H{head}_{name}', shape, tuple(coords),
                                 'uniform routing; Q=K=0; see transformer specification'))
        wi, bi, wo = [], [], []
        if layer == 0:
            wi = [(32+j,j,1.) for j in range(12)]
            bi = [(0,j,-1.) for j in range(12)]
            wo = [(j,32+j,-1.) for j in range(12)]
        if layer == 1:
            wi = [(32+j,j,1.) for j in range(12)] + [(5+8*c+e,4*c+e,1.) for c in range(3) for e in range(4)]
            bi = [(0,j,-1.5) for j in range(12)]
            wo = [(j,44+j,2.) for j in range(12)]
        if layer == 2:
            wi = [(56+c,c,1.) for c in range(3)]
            bi = [(0,c,-1.) for c in range(3)]
            wo = [(c,56+c,-1.) for c in range(3)]
        ops.extend([Write(f'L{layer}_W_in',(64,256),tuple(wi),'read stage bank'),
                    Write(f'L{layer}_b_in',(1,256),tuple(bi),'gate threshold'),
                    Write(f'L{layer}_W_out',(256,64),tuple(wo),'residual correction / AND write'),
                    Write(f'L{layer}_b_out',(1,64),(),'zero bias')])
    ops.extend([Write('W_U',(64,4),tuple((56+c,c+1,float(c+1)) for c in range(3)),'class precedence'),
                Write('b_U',(1,4),((0,0,.5),),'benign threshold')])
    return ops


class CompiledTransformer(nn.Module):
    def __init__(self, bound=128, beta=100.):
        super().__init__()
        if bound < 2 or beta <= 0: raise ValueError('invalid bound or beta')
        self.bound, self.beta = bound, beta
        for op in transformer_ir(bound):
            self.register_buffer(op.tensor, torch.from_numpy(op.materialize()))

    def forward(self, tokens, probe=False):
        if tokens.ndim != 2 or tokens.shape[1] < 2 or torch.any((tokens < 0) | (tokens >= 25)):
            raise ValueError('expected B,L abstract token IDs 0..24, L>=2')
        x = self.W_E[tokens]
        mask = torch.triu(torch.full((tokens.shape[1], tokens.shape[1]), float('-inf'),device=x.device), diagonal=1)
        traces = []
        for layer in range(4):
            a_out = torch.zeros_like(x)
            for head in range(4):
                prefix = f'L{layer}_H{head}_'
                q = x @ getattr(self, prefix+'W_Q')
                k = x @ getattr(self, prefix+'W_K')
                v = x @ getattr(self, prefix+'W_V')
                a = torch.softmax(self.beta*(q @ k.transpose(-1,-2))+mask, dim=-1)
                a_out = a_out + (a @ v) @ getattr(self, prefix+'W_O')
                if probe and head == 0: traces.append(a.detach())
            x = x+a_out
            hidden = torch.relu(x@getattr(self,f'L{layer}_W_in')+getattr(self,f'L{layer}_b_in'))
            x = x+hidden@getattr(self,f'L{layer}_W_out')+getattr(self,f'L{layer}_b_out')
        logits = x[:,-1]@self.W_U+self.b_U
        return (logits, x, traces) if probe else logits

    def export_stream(self):
        events = []
        for i,op in enumerate(transformer_ir(self.bound)):
            a = op.materialize()
            events.append(dict(id=f'transformer-write-{i:03}',type='weight_write',tensor=op.tensor,
                               shape=op.shape,coords=op.coords,formula=op.formula,zero_grad=True,
                               before_sha256=digest(torch.zeros(op.shape)),after_sha256=digest(a)))
        return dict(schema_version='1.0',architecture='bounded-transformer-v1',seed=11,events=events)
