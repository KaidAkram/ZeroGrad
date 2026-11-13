"""Fixed-budget diagnostic suite; measurements only, explicit missing methods."""
import csv
import hashlib
import json
import time
from pathlib import Path
import numpy as np
import torch
from sklearn.metrics import f1_score, confusion_matrix, balanced_accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from zerograd.core import CompiledCircuit,dataset,analytic_edit,compile_stream,replay

def save(path,obj):
    p=Path(path);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,indent=2),encoding='utf-8')

def features(x,ordered=True):
    bins=np.array_split(x,4 if ordered else 1,axis=1)
    return np.concatenate([np.stack([(b==i).mean(1) for i in range(25)],1) for b in bins],1).astype('float32')

def score(y,p):
    n=len(y);k=int((y==p).sum()); a=k/n;z=1.96;den=1+z*z/n
    mid=(a+z*z/(2*n))/den;half=z*np.sqrt(a*(1-a)/n+z*z/(4*n*n))/den
    return dict(accuracy=a,macro_f1=float(f1_score(y,p,labels=range(4),average='macro',zero_division=0)),
      balanced_accuracy=float(balanced_accuracy_score(y,p)),correct=k,n=n,ci=[mid-half,mid+half],
      confusion_matrix=confusion_matrix(y,p,labels=range(4)).tolist())

def run(seed=11,smoke=False):
    started=time.perf_counter();torch.set_num_threads(2)
    rows=[]; raw=[];m=CompiledCircuit();seeds=[seed] if smoke else [11,22,33]
    for s in seeds:
        for length in ([16] if smoke else [16,32,64,128,256]):
            x,y=dataset(64 if smoke else 256,length,10000+s)
            t=time.perf_counter()
            with torch.no_grad(): p=m(torch.tensor(x)).argmax(-1).numpy()
            elapsed=time.perf_counter()-t
            row=dict(id=f'E2-compiled-{length}-{s}',study='E2',method='WSP-Compiled',length=length,seed=s,status='measured',train_n=0,seconds=elapsed,**score(y,p))
            rows.append(row);raw.append(dict(id=row['id'],x=x.tolist(),y=y.tolist(),prediction=p.tolist()))
        if smoke: continue
        x,y=dataset(256,32,10000+s);test_set={tuple(r) for r in x};ft=features(x)
        for n in [50,200,1000]:
            tr,ty=dataset(n+100,32,20000+s)
            keep=np.array([tuple(r) not in test_set for r in tr]);tr,ty=tr[keep][:n],ty[keep][:n]
            assert not test_set.intersection(map(tuple,tr))
            for ordered in [False,True]:
                name='retrieval-position' if ordered else 'retrieval-histogram'
                t=time.perf_counter();knn=KNeighborsClassifier(3).fit(features(tr,ordered),ty)
                p=knn.predict(features(x,ordered));elapsed=time.perf_counter()-t
                result_id=f'E1-{name}-{n}-{s}'
                rows.append(dict(id=result_id,study='E1',method=name,length=32,seed=s,train_n=len(tr),status='measured',seconds=elapsed,**score(y,p)))
                raw.append(dict(id=result_id,x=x.tolist(),y=y.tolist(),prediction=p.tolist()))
            torch.manual_seed(s);net=torch.nn.Sequential(torch.nn.Linear(100,64),torch.nn.ReLU(),torch.nn.Linear(64,4))
            opt=torch.optim.AdamW(net.parameters(),lr=.01);train=torch.tensor(features(tr));target=torch.tensor(ty)
            t=time.perf_counter()
            for step in range(100):
                opt.zero_grad();loss=torch.nn.functional.cross_entropy(net(train),target);loss.backward();opt.step()
            with torch.no_grad(): p=net(torch.tensor(ft)).argmax(-1).numpy()
            result_id=f'E1-mlp-{n}-{s}'
            rows.append(dict(id=result_id,study='E1',method='AdamW-feature-MLP',architecture_mismatch=True,length=32,seed=s,train_n=len(tr),optimizer_steps=100,status='measured',seconds=time.perf_counter()-t,**score(y,p)))
            raw.append(dict(id=result_id,x=x.tolist(),y=y.tolist(),prediction=p.tolist()))
    # All finite wrong-entity/reversed pairs, at multiple distances.
    xx=[]
    for c in range(3):
        for e in range(4):
            for gap in [1,7,30]:
                for a,b in [(5+8*c+e,1+8*c+e),(1+8*c+e,5+8*c+(e+1)%4)]:
                    r=np.zeros(32,dtype='int64');r[0],r[gap]=a,b;xx.append(r)
    xx=np.array(xx); yy=np.zeros(len(xx),dtype=int); pp=m(torch.tensor(xx)).argmax(-1).numpy()
    rows.append(dict(id='E3-near-miss',study='E3',method='WSP-Compiled',length=32,seed=seed,train_n=0,status='measured',**score(yy,pp)))
    raw.append(dict(id='E3-near-miss',x=xx.tolist(),y=yy.tolist(),prediction=pp.tolist()))
    counter=np.zeros((1,512),dtype='int64');counter[0,-2:]=[1,5]
    pred=int(m(torch.tensor(counter)).argmax(-1).item())
    rows.append(dict(id='E5-boundary',study='E5',method='WSP-Compiled',length=512,seed=seed,train_n=0,status='measured',**score(np.array([1]),np.array([pred]))))
    raw.append(dict(id='E5-boundary',x=counter.tolist(),y=[1],prediction=[pred]))
    rng=np.random.default_rng(seed);ideal=rng.normal(size=(8,16));k=np.eye(16)[:,:2];w=ideal.copy();w[:,:2]+=rng.normal(size=(8,2))*2
    cal=rng.normal(size=(16,256))*np.array([.1,.1]+[1]*14)[:,None]
    hold=rng.normal(size=(16,256))*np.array([.1,.1]+[1]*14)[:,None];v=ideal@k
    edits=[];before=float(np.mean((w@k-v)**2))
    for lam in [0.,.1,1.,10.]:
        d,meta=analytic_edit(w,cal,k,v,lam=lam,rank=2)
        edits.append(dict(method='analytic',lambda_=lam,**{'lambda':lam},target_mse=float(np.mean(((w+d)@k-v)**2)),before_mse=before,drift=float(np.mean((d@hold)**2)),patch_norm=float(np.linalg.norm(d)),**meta))
    for name in ['random-direction','shuffled-target']:
        if name=='random-direction':
            d=rng.normal(size=w.shape);d*=edits[2]['patch_norm']/np.linalg.norm(d)
        else: d,_=analytic_edit(w,cal,k,v[:,::-1],rank=2)
        edits.append(dict(method=name,**{'lambda':1.},target_mse=float(np.mean(((w+d)@k-v)**2)),before_mse=before,drift=float(np.mean((d@hold)**2)),rank=int(np.linalg.matrix_rank(d)),singular_values=np.linalg.svd(d,compute_uv=False).tolist()))
    statuses=[dict(study='E1',method=meth,status='not_run',reason=reason) for meth,reason in [('WSP-Hybrid','No training protocol for saturated circuit yet'),('LoRA-trained','No shared pretrained checkpoint; comparison would be misleading'),('architecture-matched AdamW','Feature MLP is diagnostic only')]]
    statuses += [dict(study='E5',method='semantic-model',status='not_run',reason='No semantic dataset/model protocol implemented'),dict(study='B2',method='real-LLM',status='not_run',reason='No licensed checkpoint downloaded or evaluated')]
    result=dict(schema_version='1.0',profile='smoke' if smoke else 'bounded-diagnostic',seed=seed,results=rows,edits=edits,statuses=statuses,elapsed_seconds=time.perf_counter()-started,
      caveats=['Fixed-budget feature baselines are not architecture-matched','Wilson intervals are conditional on generated samples','No pretrained language model evaluated'])
    prefix='telemetry/smoke' if smoke else 'telemetry'
    save(prefix+'/benchmark_results.json',result);save(prefix+'/raw/predictions.json',raw)
    stream=compile_stream(seed);replay(stream);save('telemetry/weight_write_stream.json',stream)
    save(prefix+'/manifest.json',dict(data_sha256=hashlib.sha256(json.dumps(raw,sort_keys=True).encode()).hexdigest(),seed_schedule=seeds))
    if not smoke:
        keys=['id','study','method','length','seed','train_n','n','accuracy','macro_f1','status']
        with open('outputs/metrics.csv','w',newline='',encoding='utf-8') as f:
            writer=csv.DictWriter(f,fieldnames=keys,extrasaction='ignore');writer.writeheader();writer.writerows(rows)
    return result
