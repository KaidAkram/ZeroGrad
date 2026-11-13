"""Evidence consistency checks, not a general natural-language truth verifier."""
import json
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from zerograd.telemetry import validate_stream

def validate():
    d=json.loads(Path('telemetry/benchmark_results.json').read_text())
    ids=[r['id'] for r in d['results']]
    assert len(ids)==len(set(ids)),'duplicate result IDs'
    for r in d['results']:
        assert r['status']=='measured'
        assert 0<=r['correct']<=r['n'] and r['n']>0
        assert abs(r['accuracy']-r['correct']/r['n'])<1e-12
        assert 0<=r['macro_f1']<=1
        assert r['ci'][0]<=r['accuracy']<=r['ci'][1]
    raw_path=Path('telemetry/raw/predictions.json')
    raw=json.loads(raw_path.read_text())
    lookup={r['id']:r for r in d['results']}
    assert {r['id'] for r in raw}==set(lookup),'raw/result ID coverage mismatch'
    for row in raw:
        result=lookup[row['id']]
        assert len(row['x'])==len(row['y'])==len(row['prediction'])==result['n']
        assert sum(y==p for y,p in zip(row['y'],row['prediction']))==result['correct']
    validate_stream('telemetry/weight_write_stream.json')
    claim=Path('docs/CLAIM_REGISTER.md').read_text(encoding='utf-8')
    rows=[r for r in d['results'] if r['study']=='E2' and r['length']<=128]
    assert f"{sum(r['correct'] for r in rows)}/{sum(r['n'] for r in rows)}" in claim
    e=d['edits'][2]
    for value in [e['before_mse'],e['target_mse'],e['drift']]:assert f'{value:.6f}' in claim
    for path in ['README.md','paper/zerograd_sec_paper.md','career/LINKEDIN_MAIN_POST.md']:
        text=Path(path).read_text(encoding='utf-8')
        assert 'synthetic' in text.lower(),f'{path} omits synthetic scope'
    if Path('telemetry/transformer_weight_stream.json').exists():validate_stream('telemetry/transformer_weight_stream.json')
    if Path('telemetry/transformer_validation.json').exists():
        extension=json.loads(Path('telemetry/transformer_validation.json').read_text())
        rows=[r for r in extension['results'] if r['length']<=128]
        assert f"{sum(r['correct'] for r in rows)}/{sum(r['n'] for r in rows)}" in claim,'C7 extension count mismatch'
    return dict(status='PASS',checks=['metric arithmetic','unique result IDs','Wilson interval containment','weight schema/checksum replay','C1 sample totals','C2 edit values','synthetic scope labels'],
                limitations='This targeted linter does not semantically verify every sentence or every public number. Manual claim review remains necessary.')

if __name__=='__main__':
    result=validate();print(json.dumps(result,indent=2))
