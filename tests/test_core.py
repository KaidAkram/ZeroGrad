import itertools
import numpy as np
import pytest
import torch
from zerograd.core import *

@pytest.mark.parametrize('length',[16,32,64,128])
def test_oracle_consistency(length):
    x,y=dataset(256,length,91)
    m=CompiledCircuit()
    assert np.array_equal(m(torch.tensor(x)).argmax(-1).numpy(),y)
    assert not list(m.parameters())
    assert all(not b.requires_grad for b in m.buffers())

def test_exhaustive_short():
    x=np.array(list(itertools.product([0,1,2,5,6,9,13],repeat=4)))
    assert np.array_equal(CompiledCircuit()(torch.tensor(x)).argmax(-1),[oracle(r) for r in x])

def test_gates():
    for a,b in itertools.product([0.,1.],repeat=2):
        assert 2*max(a+b-1.5,0)==a*b

def test_replay_corruption():
    s=compile_stream(); replay(s)
    s['events'][0]['after_sha256']='bad'
    with pytest.raises(ValueError): replay(s)

def test_attention_and_shift():
    m=CompiledCircuit(); x=torch.tensor([[1,0,5,0],[0,1,0,5]])
    logits,a,_,_=m(x,True)
    assert logits.argmax(-1).tolist()==[1,1]
    assert torch.all(torch.triu(a)==0)
    assert torch.allclose(a.sum(-1)[1:],torch.ones(3))

def test_out_of_support_negative_result():
    x=torch.zeros((1,512),dtype=torch.long); x[0,-2:]=torch.tensor([1,5])
    assert oracle(x[0])==1
    assert CompiledCircuit()(x).argmax(-1).item()==0

def test_edit_normal_equation():
    rng=np.random.default_rng(3); w=rng.normal(size=(5,8)); x=rng.normal(size=(8,50)); k=rng.normal(size=(8,2)); v=rng.normal(size=(5,2))
    d,meta=analytic_edit(w,x,k,v,rank=2)
    m=x@x.T/50+k@k.T+1e-6*np.eye(8)
    assert np.allclose(d@m,(v-w@k)@k.T)
    assert meta['rank']<=2
    assert meta['reconstruction_error']<1e-10

def test_singular_covariance_and_guards():
    w=np.zeros((2,3));x=np.zeros((3,8));k=np.ones((3,1));v=np.ones((2,1))
    assert np.isfinite(analytic_edit(w,x,k,v)[0]).all()
    with pytest.raises(ValueError): analytic_edit(w,x,k,v,eps=0)
    with pytest.raises(ValueError): analytic_edit(w,x,k,v*np.nan)
