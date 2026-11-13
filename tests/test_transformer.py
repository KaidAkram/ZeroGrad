import numpy as np
import pytest
import torch
from zerograd.core import dataset, oracle, replay
from zerograd.model_wsp import CompiledTransformer, transformer_ir

@pytest.mark.parametrize('length',[16,32,64,128])
def test_transformer_consistency(length):
    torch.set_num_threads(2)
    x,y=dataset(64,length,108)
    model=CompiledTransformer()
    with torch.no_grad(): prediction=model(torch.tensor(x)).argmax(-1).numpy()
    assert np.array_equal(y,prediction)
    assert not list(model.parameters())
    assert all(not b.requires_grad for b in model.buffers())

@pytest.mark.parametrize('beta',[.25,10.,30.,100.])
def test_uniform_attention_beta_and_precedence(beta):
    model=CompiledTransformer(beta=beta)
    tokens=torch.tensor([[1,9,17,5,13,21],[5,13,21,1,9,17]])
    logits,x,attention=model(tokens,probe=True)
    assert logits.argmax(-1).tolist()==[3,0]
    for a in attention:
        assert torch.allclose(a.sum(-1),torch.ones_like(a.sum(-1)))
        assert torch.count_nonzero(torch.triu(a,diagonal=1))==0
    assert x.shape==(2,6,64)

def test_full_weight_replay():
    model=CompiledTransformer()
    arrays=replay(model.export_stream())
    assert len(arrays)==len(transformer_ir())
    for name,a in arrays.items(): assert np.array_equal(a,getattr(model,name).numpy())

def test_mixture_property():
    rng=np.random.default_rng(104)
    x=rng.integers(0,25,size=(128,32))
    with torch.no_grad(): pred=CompiledTransformer()(torch.tensor(x)).argmax(-1).numpy()
    assert np.array_equal(pred,[oracle(row) for row in x])
