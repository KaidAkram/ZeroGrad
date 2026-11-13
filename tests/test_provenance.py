import copy
import numpy as np
import pytest
from pydantic import ValidationError
from zerograd.core import compile_stream
from zerograd.telemetry import WeightStream
from zerograd.patch_io import save_patch,apply_patch

def test_schema_rejects_invalid_coordinate():
    stream=compile_stream(); WeightStream.model_validate(stream)
    bad=copy.deepcopy(stream);bad['events'][0]['coords']=[(25,0,1.)]
    with pytest.raises(ValidationError):WeightStream.model_validate(bad)

def test_schema_rejects_duplicate_and_false_zero_grad():
    stream=compile_stream();stream['events'][0]['zero_grad']=False
    with pytest.raises(ValidationError):WeightStream.model_validate(stream)
    stream=compile_stream();stream['events'].append(stream['events'][0])
    with pytest.raises(ValidationError):WeightStream.model_validate(stream)

def test_exact_patch_roundtrip(tmp_path):
    rng=np.random.default_rng(99);w=rng.normal(size=(8,16));d=rng.normal(size=w.shape)/10
    path=tmp_path/'patch.npz';save_patch(path,w,d)
    after=apply_patch(path,w)
    assert np.array_equal(apply_patch(path,after,undo=True),w)
    with pytest.raises(ValueError):apply_patch(path,w+1)
