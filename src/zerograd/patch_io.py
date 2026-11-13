"""Safe numeric patch archive, checked apply/rollback. No pickle deserialization."""
import hashlib
import json
from pathlib import Path
import numpy as np

def checksum(w):
    return hashlib.sha256(np.ascontiguousarray(w).tobytes()).hexdigest()

def save_patch(path,w,delta):
    if w.shape!=delta.shape or not np.isfinite(delta).all():raise ValueError('invalid patch')
    after=w+delta
    meta=dict(version='1.0',shape=list(w.shape),dtype=str(w.dtype),before=checksum(w),after=checksum(after),delta=checksum(delta))
    # Exact snapshots make rollback independent of floating-point subtraction error.
    np.savez_compressed(path,before=w,after=after,delta=delta,metadata=np.array(json.dumps(meta)))
    return meta

def load_patch(path):
    with np.load(Path(path),allow_pickle=False) as a:
        before,after,delta=[a[k].copy() for k in ['before','after','delta']]
        meta=json.loads(str(a['metadata']))
    if any(checksum(v)!=meta[k] for k,v in [('before',before),('after',after),('delta',delta)]):
        raise ValueError('patch checksum mismatch')
    if before.shape!=delta.shape or not np.array_equal(before+delta,after):raise ValueError('patch inconsistency')
    return before,after,meta

def apply_patch(path,w,undo=False):
    before,after,meta=load_patch(path)
    expected=meta['after'] if undo else meta['before']
    if checksum(w)!=expected:raise ValueError('patch targets a different checkpoint')
    return before.copy() if undo else after.copy()
