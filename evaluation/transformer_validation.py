"""Separate artifact: bounded transformer extension; preserves original study."""
import json
import time
from pathlib import Path
import numpy as np
import torch
from zerograd.core import dataset,oracle
from zerograd.model_wsp import CompiledTransformer
from zerograd.telemetry import validate_stream
from evaluation.run_benchmarks import score

def run():
    torch.set_num_threads(2);model=CompiledTransformer();rows=[];started=time.perf_counter()
    for seed in [11,22,33]:
        for length in [16,32,64,128,256]:
            x,y=dataset(128,length,30000+seed)
            with torch.no_grad():p=model(torch.tensor(x)).argmax(-1).numpy()
            rows.append(dict(id=f'T4-{seed}-{length}',method='WSP-Transformer',seed=seed,length=length,**score(y,p)))
    rng=np.random.default_rng(905);x=rng.integers(0,25,size=(256,64));y=np.array([oracle(row) for row in x])
    with torch.no_grad():p=model(torch.tensor(x)).argmax(-1).numpy()
    rows.append(dict(id='T4-mixtures',method='WSP-Transformer',seed=905,length=64,**score(y,p)))
    obj=dict(architecture='bounded-transformer-v1',status='measured',results=rows,
             elapsed_seconds=time.perf_counter()-started,zero_optimizer_steps=True,
             buffer_entries=sum(b.numel() for b in model.buffers()),
             nonzero_entries=sum(int(torch.count_nonzero(b)) for b in model.buffers()),
             caveat='Four blocks, but three computational blocks and three inactive heads per block; same two-stage abstract grammar only.')
    Path('telemetry/transformer_validation.json').write_text(json.dumps(obj,indent=2),encoding='utf-8')
    Path('telemetry/transformer_weight_stream.json').write_text(json.dumps(model.export_stream(),indent=2),encoding='utf-8')
    validate_stream('telemetry/transformer_weight_stream.json')
    print(f"Transformer: {len(rows)} evaluations, {obj['elapsed_seconds']:.3f}s")
    return obj

if __name__=='__main__':run()
