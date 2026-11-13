"""CPU-first resumable stage runner. Each mode writes independent artifacts."""
import argparse
import sys
import json
import hashlib
import subprocess
from datetime import datetime,timezone
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent/'src'))
from evaluation.run_benchmarks import run

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--mode',choices=['smoke','benchmark','full','media','paper','release-check'],default='smoke')
    p.add_argument('--device',choices=['auto','cpu','cuda'],default='cpu')
    p.add_argument('--seed',type=int,default=11)
    p.add_argument('--offline',action='store_true');p.add_argument('--skip-real-llm',action='store_true')
    p.add_argument('--quality',choices=['preview','final'],default='preview')
    p.add_argument('--resume',action='store_true',help='Reuse scientific artifacts when their source/seed fingerprint matches the saved checkpoint')
    a=p.parse_args()
    if a.device=='cuda': p.error('This v1 protocol is CPU-only; CUDA comparisons are not implemented.')
    if a.mode in ['smoke','benchmark','full']:
        files=sorted(Path('src').rglob('*.py'))+sorted(Path('evaluation').glob('*.py'))
        fingerprint=hashlib.sha256(b''.join(f.read_bytes() for f in files)+str((a.seed,a.mode=='smoke')).encode()).hexdigest()
        checkpoint=Path('outputs/science_checkpoint.json')
        cached=json.loads(checkpoint.read_text()) if checkpoint.exists() else {}
        result_path=Path('telemetry/smoke/benchmark_results.json' if a.mode=='smoke' else 'telemetry/benchmark_results.json')
        if a.resume and cached.get('fingerprint')==fingerprint and result_path.exists():
            result=json.loads(result_path.read_text());print('Reused science checkpoint with matching source fingerprint')
        else:
            result=run(a.seed,a.mode=='smoke');print(f"Measured {len(result['results'])} rows in {result['elapsed_seconds']:.3f}s")
            if a.mode!='smoke':
                from evaluation.transformer_validation import run as validate_transformer
                validate_transformer()
            checkpoint.write_text(json.dumps(dict(fingerprint=fingerprint,result_path=str(result_path),timestamp=datetime.now(timezone.utc).isoformat()),indent=2))
        from zerograd.telemetry import export_schema,validate_stream
        export_schema();validate_stream('telemetry/weight_write_stream.json')
        if a.mode=='smoke':
            import matplotlib
            matplotlib.use('Agg')
            import matplotlib.pyplot as plt
            r=result['results'][0];fig,ax=plt.subplots(figsize=(5,3))
            ax.bar(['Correct','Incorrect'],[r['correct'],r['n']-r['correct']],color=['#10b981','#f43f5e'])
            ax.set(ylabel='Generated examples',title='CPU smoke / synthetic grammar')
            fig.tight_layout();fig.savefig('outputs/smoke.png');fig.savefig('outputs/smoke.svg');plt.close(fig)
    if a.mode in ['paper','full']:
        from scripts.report import generate
        generate()
        from scripts.finalize_docs import main as documentation
        documentation()
    if a.mode in ['media','full']:
        from scripts.render_video import render
        render(a.quality)
    if a.mode in ['release-check','full']:
        if a.mode=='full':
            subprocess.run([sys.executable,'-m','pytest','-q','--junitxml=outputs/test_results.xml'],check=True,timeout=180)
            npm='npm.cmd' if sys.platform=='win32' else 'npm'
            subprocess.run([npm,'run','build'],cwd='studio',check=True,timeout=180)
            subprocess.run([npm,'test'],cwd='studio',check=True,timeout=180)
            from scripts.verify_media import verify
            verify()
        from scripts.release_check import check
        return check()
    return 0
if __name__=='__main__': sys.exit(main())
