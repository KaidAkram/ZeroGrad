import numpy as np
import pytest
from zerograd.core import analytic_edit

def test_rank_cutoff_changes_reconstruction_and_counts():
    rng=np.random.default_rng(61)
    w=np.zeros((5,8));x=rng.normal(size=(8,64));k=rng.normal(size=(8,3));v=rng.normal(size=(5,3))
    d,meta=analytic_edit(w,x,k,v,rank=1)
    assert meta['rank']==1
    assert meta['reconstruction_error']>0
    assert np.linalg.matrix_rank(d,tol=1e-8)==1

def test_locality_regularization_tradeoff():
    w=np.zeros((3,4));x=np.eye(4);k=np.eye(4)[:,:1];v=np.ones((3,1))
    naive,_=analytic_edit(w,x,k,v,lam=0)
    regular,_=analytic_edit(w,x,k,v,lam=10)
    assert np.linalg.norm(regular@x)<np.linalg.norm(naive@x)
    assert np.linalg.norm(regular@k-v)>np.linalg.norm(naive@k-v)
    # Exact preservation of all inputs would force this nonzero update to vanish.
    assert np.linalg.norm(regular)>0

@pytest.mark.parametrize('lam,eps',[(np.nan,1e-6),(1,np.inf),(-1,1e-6),(1,0)])
def test_invalid_regularization(lam,eps):
    with pytest.raises(ValueError):analytic_edit(np.zeros((2,3)),np.eye(3),np.ones((3,1)),np.ones((2,1)),lam=lam,eps=eps)

def test_no_gradient_compilation(monkeypatch):
    import torch
    from zerograd.core import CompiledCircuit
    from zerograd.model_wsp import CompiledTransformer
    def forbidden(*args,**kwargs):raise AssertionError('gradient path called')
    monkeypatch.setattr(torch.Tensor,'backward',forbidden)
    monkeypatch.setattr(torch.optim.AdamW,'step',forbidden)
    for cls in [CompiledCircuit,CompiledTransformer]:
        assert cls()(torch.tensor([[1,0,5]])).argmax(-1).item()==1
