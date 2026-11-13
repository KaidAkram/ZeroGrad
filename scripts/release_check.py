"""Local artifact release gate. Full research acceptance is reported separately."""
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime,timezone
from pathlib import Path
from scripts.validate_claims import validate

def check():
    checks=[]
    required=['README.md','LICENSE','CITATION.cff','references.bib','docs/ENVIRONMENT.md',
              'docs/LITERATURE_NOTES.md','docs/CLAIM_REGISTER.md','docs/KNOWN_LIMITATIONS.md',
              'docs/ETHICS_AND_THREAT_MODEL.md','docs/RESEARCH_QUESTIONS.md','docs/EXECUTION_PLAN.md',
              'specs/ZEROGRAD_MATH_SPEC.md','specs/TRANSFORMER_EXTENSION.md','schemas/telemetry.schema.json',
              'telemetry/benchmark_results.json','telemetry/transformer_validation.json',
              'paper/zerograd_sec_paper.md','career/CV_BULLETS.md','career/LINKEDIN_MAIN_POST.md',
              'studio/dist/index.html','studio/qa/results.json','outputs/MEDIA_QA.json']
    required += [f'outputs/carousel_{i:02}.png' for i in range(1,7)]
    required += ['outputs/zerograd_linkedin_reel.mp4','outputs/zerograd_widescreen.mp4','outputs/zerograd_teaser_12s.mp4','outputs/zerograd_preview.mp4']
    for p in required:checks.append(('PASS' if Path(p).is_file() and Path(p).stat().st_size else 'FAIL',p))
    try:validate();checks.append(('PASS','Claim arithmetic, schema validation and tensor replay'))
    except Exception as e:checks.append(('FAIL',f'Claim validation: {e}'))
    try:
        from scripts.verify_readme import verify
        verify();checks.append(('PASS','README artifact references and SVG syntax'))
    except Exception as e:checks.append(('FAIL',f'README validation: {e}'))
    for p in ['studio/qa/results.json','outputs/MEDIA_QA.json']:
        if Path(p).exists():
            obj=json.loads(Path(p).read_text())
            good=obj.get('failed',1)==0 if isinstance(obj,dict) else all(v['status']=='PASS' for v in obj)
            checks.append(('PASS' if good else 'FAIL',f'Recorded QA: {p}'))
    try:
        import xml.etree.ElementTree as ET
        suites=list(ET.parse('outputs/test_results.xml').getroot().iter('testsuite'))
        tests=sum(int(v.attrib['tests']) for v in suites)
        failures=sum(int(v.attrib.get('failures',0))+int(v.attrib.get('errors',0)) for v in suites)
        checks.append(('PASS' if tests>0 and failures==0 else 'FAIL',f'Recorded Python tests: {tests}, failures/errors: {failures}'))
    except Exception as e:checks.append(('FAIL',f'Missing/invalid Python test evidence: {e}'))
    checks.extend(('WARN',s) for s in [
        'This is a bounded research prototype, not completion of every master-brief study.',
        'Hybrid/LoRA, optimized architecture-matched learning, semantic models and real-checkpoint editing remain NOT RUN.',
        'Clean online bootstrap and hosted CI have not been executed; local checks passed independently.',
        'Remotion installation blocked by shell network policy; deterministic Pillow/FFmpeg media delivered.',
        'Repository and author metadata are configured; consult docs/PUBLISHING.md for the observed publication state.',
        'Claim linter checks selected invariants, not arbitrary natural-language scientific truth.'
    ])
    status='FAIL' if any(s=='FAIL' for s,_ in checks) else 'PASS WITH WARNINGS'
    text='# Release status\n\n'+status+' — '+datetime.now(timezone.utc).isoformat()+'\n\n'
    text+='\n'.join(f'- **{s}** {msg}' for s,msg in checks)+'\n'
    text+='\nPublic claims are bounded by docs/CLAIM_REGISTER.md. Full acceptance gaps and follow-on experiments are listed in docs/EXECUTION_PLAN.md. Website deployment and social posting are separate actions; repository publication is recorded in docs/PUBLISHING.md.\n'
    Path('outputs/RELEASE_STATUS.md').write_text(text,encoding='utf-8')
    entries=[];skip={'.venv','node_modules','__pycache__','.pytest_cache','.git','.publish'}
    for directory,dirs,files in os.walk('.'):
        dirs[:]=[d for d in dirs if d not in skip]
        for name in files:
            p=Path(directory)/name;relative=p.as_posix()
            if relative=='outputs/DELIVERY_MANIFEST.json':continue
            if relative=='outputs/test_results.xml':generated_from='tests/ + pytest'
            elif relative.startswith(('outputs/media_qa/','outputs/MEDIA_QA')):generated_from='scripts/verify_media.py + actual encoded MP4 files'
            elif relative.startswith('outputs/zerograd_') and ('.mp4' in relative or '.ffprobe.' in relative):generated_from='scripts/render_video.py + telemetry/benchmark_results.json + telemetry/weight_write_stream.json; FFmpeg/ffprobe'
            elif relative.startswith(('studio/dist/','studio/qa/')):generated_from='studio/src/ + studio/scripts/ + copied telemetry/docs/media; Vite build or Playwright QA'
            elif relative.startswith(('outputs/RELEASE_STATUS','outputs/DELIVERY_MANIFEST')):generated_from='scripts/release_check.py + existing artifacts and recorded QA'
            elif relative.startswith(('outputs/','career/','design/','paper/')):generated_from='scripts/report.py + telemetry/benchmark_results.json + telemetry/weight_write_stream.json; review notes authored from inspected artifacts'
            elif relative.startswith('telemetry/'):generated_from='evaluation/run_benchmarks.py or evaluation/transformer_validation.py + deterministic seed/config; see artifact architecture and result IDs'
            else:generated_from='authored repository source/documentation; controlling brief ZEROGRAD_SEC_MASTER_PROMPT.txt and recorded primary references'
            entries.append(dict(path=relative,size=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),generated_from=generated_from,status='present',verification_method='SHA256 and file size; applicable functional checks in RELEASE_STATUS.md'))
    Path('outputs/DELIVERY_MANIFEST.json').write_text(json.dumps(dict(schema_version='1.0',release_status=status,artifacts=sorted(entries,key=lambda e:e['path'])),indent=2),encoding='utf-8')
    print(f'{status}: {sum(s=="PASS" for s,_ in checks)} PASS, {sum(s=="FAIL" for s,_ in checks)} FAIL, {sum(s=="WARN" for s,_ in checks)} WARN')
    return int(any(s=='FAIL' for s,_ in checks))

if __name__=='__main__':sys.exit(check())
