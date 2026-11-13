"""Executable prefix circuit; all task-dependent coefficients live in compiled tensors."""
import hashlib
import json
from dataclasses import dataclass
import numpy as np
import torch
from torch import nn

LABELS = ['BENIGN', 'PRIV_ESC_PATTERN', 'CONTAINER_ESCAPE_PATTERN', 'PROMPT_INJECTION_PATTERN']

def digest(a):
    return hashlib.sha256(np.asarray(a, dtype='<f4').tobytes()).hexdigest()

def oracle(tokens):
    seen, matches = set(), set()
    for t in tokens:
        if not 0 <= int(t) < 25:
            raise ValueError('abstract vocabulary is 0..24')
        if t:
            c, rem = divmod(int(t)-1, 8)
            s, e = divmod(rem, 4)
            if s and (c,e) in seen:
                matches.add(c+1)
            if not s:
                seen.add((c,e))
    return max(matches, default=0)

@dataclass(frozen=True)
class Write:
    tensor: str
    shape: tuple
    coords: tuple
    formula: str
    def materialize(self):
        a = np.zeros(self.shape, dtype=np.float32)
        for i,j,v in self.coords:
            if not (0 <= i < self.shape[0] and 0 <= j < self.shape[1]):
                raise ValueError('IR coordinate out of bounds')
            a[i,j] = v
        return a

def circuit_ir():
    return [Write('embedding',(25,64),tuple((i,i,1.) for i in range(25)), 'E[t,t]=1'),
            Write('start',(64,12),tuple((1+8*c+e,4*c+e,1.) for c in range(3) for e in range(4)), 'S[1+8c+e,4c+e]=1'),
            Write('end',(64,12),tuple((5+8*c+e,4*c+e,1.) for c in range(3) for e in range(4)), 'T[5+8c+e,4c+e]=1'),
            Write('readout',(3,3),tuple((c,c,float(c+1)) for c in range(3)), 'U[c,c]=c+1')]

def sat(x):
    return torch.relu(x)-torch.relu(x-1)

class CompiledCircuit(nn.Module):
    def __init__(self, bound=128):
        super().__init__()
        self.bound = bound
        for op in circuit_ir():
            self.register_buffer(op.tensor,torch.from_numpy(op.materialize()))
    def forward(self,tokens,probe=False):
        if tokens.ndim != 2 or tokens.shape[1] < 2:
            raise ValueError('expected B,L with L>=2')
        if torch.any((tokens<0)|(tokens>=25)):
            raise ValueError('token outside finite vocabulary')
        h=self.embedding[tokens]
        n=tokens.shape[1]
        a=torch.tril(torch.ones(n,n,device=h.device),diagonal=-1)
        a=a/a.sum(-1,keepdim=True).clamp_min(1)
        p=sat(self.bound*(a@(h@self.start)))
        g=2*torch.relu(p+h@self.end-1.5)
        hits=sat(sat(g.sum(1)).reshape(-1,3,4).sum(-1))
        logits=torch.cat([torch.full((len(tokens),1),.5,device=h.device),hits@self.readout],-1)
        return (logits, a,p,g) if probe else logits

def compile_stream(seed=11):
    events=[]
    for i,op in enumerate(circuit_ir()):
        events.append(dict(id=f'write-{i:03}',type='weight_write',tensor=op.tensor,
          shape=op.shape,coords=op.coords,formula=op.formula,zero_grad=True,
          before_sha256=digest(np.zeros(op.shape)),after_sha256=digest(op.materialize())))
    return dict(schema_version='1.0',seed=seed,architecture='prefix-circuit-v1',events=events)

def replay(stream):
    out={}
    for e in stream['events']:
        if e['type']!='weight_write': continue
        a=Write(e['tensor'],tuple(e['shape']),tuple(e['coords']),e['formula']).materialize()
        if digest(a)!=e['after_sha256'] or digest(np.zeros(e['shape']))!=e['before_sha256']:
            raise ValueError('telemetry checksum mismatch')
        out[e['tensor']]=a
    return out

def dataset(n,length,seed):
    rng=np.random.default_rng(seed)
    x=np.zeros((n,length),dtype=np.int64)
    for i in range(n):
        label=i%4; c=int(rng.integers(3)) if label==0 else label-1
        e=int(rng.integers(4)); p,q=sorted(rng.choice(length,2,replace=False))
        a,b=1+8*c+e,5+8*c+e
        if label==0:
            mode=i//4%3
            if mode==0: a,b=b,a
            elif mode==1: b=5+8*c+(e+1)%4
            else: b=0
        x[i,p],x[i,q]=a,b
    y=np.array([oracle(row) for row in x])
    return x,y

def analytic_edit(w,x,k,v,lam=1.,eps=1e-6,rank=None):
    if not np.isfinite(eps) or not np.isfinite(lam) or eps<=0 or lam<0: raise ValueError('positive finite ridge and nonnegative finite locality required')
    if not all(np.isfinite(a).all() for a in [w,x,k,v]): raise ValueError('nonfinite input')
    if any(a.ndim!=2 for a in [w,x,k,v]) or x.shape[1]==0 or k.shape[1]==0 or x.shape[0]!=w.shape[1] or k.shape[0]!=w.shape[1] or v.shape!=(w.shape[0],k.shape[1]):
        raise ValueError('shape mismatch')
    r=v-w@k
    m=lam*x@x.T/x.shape[1]+k@k.T+eps*np.eye(w.shape[1])
    d=np.linalg.solve(m,k@r.T).T
    u,s,vh=np.linalg.svd(d,full_matrices=False)
    rank=len(s) if rank is None else rank
    if not 1<=rank<=len(s): raise ValueError('invalid rank')
    b=u[:,:rank]*s[:rank]; a=vh[:rank]
    applied=b@a
    return applied,dict(singular_values=s.tolist(),rank=int(np.linalg.matrix_rank(applied,tol=1e-8)),
                   reconstruction_error=float(np.linalg.norm(d-b@a)),adapter_parameters=int(b.size+a.size),
                   modified_entries=int(np.count_nonzero(applied)),original_parameters=int(w.size))
