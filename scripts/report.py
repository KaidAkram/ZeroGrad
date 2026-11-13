"""Regenerate evidence-linked report, figures, original cards and career copy."""
import json
import html
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
from scripts.render_video import frame

def write(path,text):
    p=Path(path)
    if p.exists() and p.read_text(encoding='utf-8')==text:return
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8')

def generate():
    d=json.loads(Path('telemetry/benchmark_results.json').read_text());s=json.loads(Path('telemetry/weight_write_stream.json').read_text())
    supported=[r for r in d['results'] if r['study']=='E2' and r['length']<=128]
    stress=[r for r in d['results'] if r['study']=='E2' and r['length']==256]
    correct=sum(r['correct'] for r in supported);n=sum(r['n'] for r in supported)
    mean=float(np.mean([r['accuracy'] for r in stress]));e=d['edits'][2]
    finding=f'The compiled circuit matched the oracle on {correct}/{n} generated examples at lengths 16–128 across three seeds. At length 256, mean accuracy fell to {mean:.1%}; a constructed length-512 example fails.'
    patch=f"The rank-{e['rank']} analytic patch reduced target MSE from {e['before_mse']:.6f} to {e['target_mse']:.6f}, with unrelated-output drift MSE {e['drift']:.6f}."
    limitation='These are synthetic, finite symbolic tasks. The main benchmark and studio replay use the prefix circuit. A separately validated four-block transformer implements the same narrow two-stage grammar; three blocks compute and one is identity. The feature MLP and retrieval baselines are diagnostic and not architecture-matched. No semantic or real pretrained-model claim is supported.'
    table='| Method | Length | Seed | Train N | Accuracy | Macro F1 |\n|---|---:|---:|---:|---:|---:|\n'+'\n'.join(f"| {r['method']} | {r['length']} | {r['seed']} | {r['train_n']} | {r['accuracy']:.4f} | {r['macro_f1']:.4f} |" for r in d['results'])
    report=f'''# ZeroGrad-Sec: bounded weight compilation and analytic edits

Technical report / unreviewed research prototype. Author: Akram Kaid. Affiliation not specified.

## Abstract
{finding} {patch} We expose coefficients, symbolic assumptions, raw predictions and replay checksums. This is an engineering testbed and a limited diagnostic study; no algorithmic novelty claim is made.

## Introduction and research questions
Can explicit sequence rules be expressed as numeric neural operations without optimization? Where does finite support break? Can a ridge-regularized update improve a controlled defect while measuring drift? This study answers these questions only for a finite grammar and a linear synthetic association memory.

## Related work
RASP and Tracr establish programming and compilation approaches for transformers. ROME and MEMIT motivate associative-memory edits; our normalized covariance/ridge objective is derived independently in [the math spec](../specs/ZEROGRAD_MATH_SPEC.md). LoRA trains low-rank updates; this analytic adapter uses a direct solve. Retrieval here has no generator and is not RAG. Verified source metadata and distinctions are in [literature notes](../docs/LITERATURE_NOTES.md).

## Formal task and methods
Tokens encode one of three abstract signatures, one of two stages and one of four entity IDs. A first-stage event must strictly precede the matching second-stage event. Highest matching class takes precedence. The compiler creates E[25,64], S/T[64,12] and U[3,3]; uniform strict causal attention and saturated ReLU gates recover bounded existence. See equations (1)–(4) in the math spec. This is an explicitly changed architecture, not standard four-block compilation.

## Protocol
Frozen protocol: [EXPERIMENT_PROTOCOL.md](../docs/EXPERIMENT_PROTOCOL.md). Seeds 11,22,33; disjoint train/test RNG seeds and exact sequence overlap exclusion. Each E2 cell uses 256 examples. E1 uses 50,200,1000 training examples and a fixed 100-step AdamW feature MLP, with no tuning. Wilson 95% intervals accompany every accuracy in JSON. They do not quantify grammar or model-selection uncertainty. Hard negatives are reversed, wrong-entity or incomplete pairs. The generated distribution is simple and has exploitable shortcuts.

## Results
{finding}

![Length sensitivity](../outputs/figures/length_sensitivity.png)

{table}

## Analytic editing and controls
{patch} All 128 entries of the 8x16 matrix change; the rank-two factors contain 48 parameters. Low rank is not entry sparsity. Calibration and unrelated draws are independent Gaussian samples with deliberately low variance in the first two coordinates. This favorable construction is not real activation evidence. Naive lambda=0, shuffled targets and norm-matched random directions are reported in the JSON. No paraphrase, token KL, or perplexity metric is defined for this linear module.

## Ablations and negative results
Length 256 lies outside the proved support and produces failures. A single late ordered pair at length 512 is rejected. Exact support is a property of the saturation scaling, not of high-temperature softmax. Q=K=0 means beta does not affect this uniform attention variant; the requested content-selector beta sweep remains NOT RUN. Wrong-order/entity near misses are evaluated separately. Full mixture/compositional and skewed-prior studies remain open.

## Threats to validity
{limitation} The synthetic association checkpoint is a linear module, not a full synthetic transformer. The baselines have unequal representations and inductive biases. These data cannot establish superiority over learned semantic models. Accuracy on the simple generator is not security efficacy. No cross-template generalization study, ECE/AUROC suite, latency quantiles or memory profiling was completed.

## Responsible use
Only non-executable abstract tokens are shipped. No syscall capture, exploit payload, real prompt bypass or live target is involved. Do not use this as an intrusion detection system.

## Reproducibility
Run `python run_all.py --mode benchmark --offline --skip-real-llm`, then `python run_all.py --mode paper`. Measured benchmark elapsed time: {d['elapsed_seconds']:.3f} seconds in this environment. CPU-only scientific path; version snapshot in requirements-observed.txt. Raw examples and predictions: telemetry/raw/predictions.json. Checksums: telemetry/manifest.json. Exact write replay is tested. Timing varies by host.

## Conclusion
The useful result is an auditable bounded construction and a visible failure boundary. Next, compare the identical circuit architecture under learning, extend compositional generators, and test calibration shift before attempting a real checkpoint repair.

## References
See references.bib and docs/LITERATURE_NOTES.md. Author/affiliation and archival release identifiers must be supplied before external submission.
'''
    extension_path=Path('telemetry/transformer_validation.json')
    if extension_path.exists():
        extension=json.loads(extension_path.read_text())
        rs=[r for r in extension['results'] if r['length']<=128]
        ext_text=f"The separately evaluated four-block transformer matched the oracle on {sum(r['correct'] for r in rs)}/{sum(r['n'] for r in rs)} examples, including dense mixtures. It uses 4 heads, D=64, head width 16 and MLP width 256. Three blocks perform computation; block four and three heads per block are identity/zero paths. All {extension['buffer_entries']} tensor entries (including zeros) are directly authored; {extension['nonzero_entries']} are nonzero. Extension results and out-of-support failures are in telemetry/transformer_validation.json, with full write replay in transformer_weight_stream.json. This does not implement arbitrary multi-stage security tracking."
        report=report.replace('## Analytic editing and controls','## Four-block transformer extension\n'+ext_text+'\n\nSee [extension derivation](../specs/TRANSFORMER_EXTENSION.md). The main benchmark table and media remain the original prefix-circuit experiment.\n\n## Analytic editing and controls')
    write('paper/zerograd_sec_paper.md',report);write('outputs/PAPER_EVALUATION_REPORT.md',report)
    write('outputs/track_b_edit_report.md','# Synthetic analytic edit\n\n'+patch+'\n\n'+json.dumps(d['edits'],indent=2)+'\n\n'+limitation)
    write('outputs/metrics.tex','% Generated from telemetry/benchmark_results.json\n\\begin{tabular}{lrr}\nMethod & Length & Accuracy \\\\\n'+'\n'.join(f"{r['method'].replace('_',' ')} & {r['length']} & {r['accuracy']:.4f} \\\\" for r in d['results'])+'\n\\end{tabular}\n')
    plt.rcParams.update({'axes.spines.top':False,'axes.spines.right':False,'font.size':12})
    fig,ax=plt.subplots(figsize=(8,4.5));lengths=[16,32,64,128,256]
    for seed in [11,22,33]:
        rs=[r for r in d['results'] if r['study']=='E2' and r['seed']==seed]
        ax.plot([r['length'] for r in rs],[r['accuracy'] for r in rs],'o-',label=f'Seed {seed}')
    ax.axvspan(129,260,color='#f59e0b',alpha=.12,label='Outside proved support');ax.set(xlabel='Sequence length',ylabel='Accuracy',ylim=(0,1.05));ax.legend(fontsize=9);fig.tight_layout()
    for ext in ['svg','png']:fig.savefig(f'outputs/figures/length_sensitivity.{ext}',dpi=220)
    plt.close(fig)
    fig,ax=plt.subplots(figsize=(7,4));es=d['edits'][:4];ax.plot([r['drift'] for r in es],[r['target_mse'] for r in es],'o-',color='#b77900')
    for r in es:ax.annotate(f"λ={r['lambda']}",(r['drift'],r['target_mse']))
    ax.set(xlabel='Unrelated-output drift (MSE)',ylabel='Target residual (MSE)',title='Synthetic efficacy / locality tradeoff');fig.tight_layout()
    for ext in ['svg','png']:fig.savefig(f'outputs/figures/edit_tradeoff.{ext}',dpi=220)
    plt.close(fig)
    claims=f'''# Claim register

| ID | Permitted wording | Evidence | Status / limits |
|---|---|---|---|
| C1 | {finding} | telemetry/benchmark_results.json E2 and E5-boundary; raw/predictions.json | Verified for generated samples only |
| C2 | {patch} | telemetry/benchmark_results.json edits[2] | Verified synthetic linear module only |
| C3 | Direct construction uses zero optimizer/backprop steps | src/zerograd/core.py, tests/test_core.py | Verified frozen buffers; learned baseline does use gradients |
| C4 | Every authored matrix block replays with a matching SHA256 | weight_write_stream.json; test_replay_corruption | Verified four block events, not individual time-stamped writes |
| C5 | Low rank does not imply sparse changed entries | edits[2]: 48 factor parameters, 128 changed / 128 original entries | Verified for this patch only |
| C6 | Within length 128, binary prefix existence is recovered in exact arithmetic | specs/ZEROGRAD_MATH_SPEC.md | Theoretical; FP32 empirical tests supplement proof |

Prohibited: arbitrary-length correctness, full original security-state-machine implementation, zero forgetting, real exploit detection, real pretrained repair, superiority over optimized learned models, peer-reviewed novelty. Media/style numbers (dimensions, frames, dates) require their own file metadata, not benchmark scores.
'''
    if extension_path.exists():claims+='\nC7 (verified, bounded): '+ext_text+'\n'
    write('docs/CLAIM_REGISTER.md',claims);write('docs/KNOWN_LIMITATIONS.md','# Known limitations\n\n'+limitation+'\n\n'+report.split('## Threats to validity')[1].split('## Responsible use')[0]+'\nRemotion network installation blocked; media uses original Pillow/FFmpeg fallback. No package installation outside the workspace. Full acceptance is not claimed.')
    write('career/CV_BULLETS.md',f'''# Evidence-grounded CV options

- Built a PyTorch weight compiler for bounded symbolic sequence detection, with zero optimizer steps in the compiled path, checksum-verified tensor replay and an interactive research studio.
- Evaluated a compiled prefix circuit on {n} generated examples within its declared length support and documented an out-of-support failure; implemented retrieval and fixed-budget AdamW diagnostics.
- Derived and tested covariance-regularized low-rank matrix edits with target efficacy, unrelated-output drift and random/shuffled controls.

Short resume: Built ZeroGrad-Sec, a reproducible PyTorch testbed for bounded weight compilation and analytic editing, with evidence-linked visualizations.

Research CV: {finding} {patch} Scope and provenance: Claim Register C1–C6. Do not describe this as real-model repair or deployed threat detection.
''')
    post=f'''I wrote a small detector's neural weights directly from a rule.
The interesting result was where it stopped working.

I built ZeroGrad-Sec to make weight programming inspectable: a finite symbolic grammar, explicit tensor recipes, an independent oracle, and a studio that replays the actual matrix writes.

{finding}

That boundary matters. The circuit uses bounded prefix averages and ReLU gates; it is not a general semantic security model, and it is not the four-block transformer I originally set out to investigate. Retrieval and a fixed-budget feature MLP provide diagnostics, not a definitive leaderboard.

The second track asks a different question: can an analytic low-rank patch repair a known synthetic association defect while limiting unrelated changes? The report shows both target improvement and nonzero drift. There is no zero-forgetting guarantee.

The code, raw predictions, mathematical assumptions, and failure case are all part of the project. The visuals consume those artifacts rather than a scripted success curve.

I would welcome critique of the bounded construction and suggestions for an architecture-matched baseline. Reproduce the failure before trusting the success.

https://github.com/KaidAkram/ZeroGrad
#MechanisticInterpretability #MachineLearning #ReproducibleResearch
'''
    write('career/LINKEDIN_MAIN_POST.md',post)
    write('career/LINKEDIN_POST_VARIANTS.md',f'# Audience variants\n\nResearchers: {finding} Which compositional counterexamples should an independent evaluation include?\n\nSystems engineers: I built an auditable path from tensor recipes to checksummed replay, benchmark JSON and a local studio. All data are synthetic; the release status makes skipped studies visible.\n\nDevelopers: Can code write a tiny neural network directly? This project does that for a bounded toy grammar, then shows the boundary where it fails.\n\nConcise: Some rules compile. Generalization still needs measurement. Evidence: Claim Register C1–C6; repository link must be configured before posting.')
    write('career/PORTFOLIO_CASE_STUDY.md','# Portfolio case study\n\nChallenge: make direct weight construction auditable rather than anecdotal.\n\nHypothesis: explicit bounded predicates can be compiled without gradient optimization.\n\nArchitecture: a prefix-average circuit and an independent linear analytic editor feed a common artifact pipeline.\n\n'+finding+'\n\n'+patch+'\n\nEngineering: frozen PyTorch buffers, data-driven coordinate IR, checksummed replay, deterministic safe generators, raw predictions, responsive studio and frame-based media.\n\nWhat I learned: an exact-arithmetic bound is a product constraint. More impressive-looking architectures must earn their claims through execution.\n\nNext: architecture-matched training and distribution-shift experiments.\n\n'+limitation)
    write('career/PROJECT_SUMMARY_50_150_300_WORDS.md','# Project summaries\n\n## Short\nZeroGrad-Sec compiles bounded symbolic sequence rules into neural weights and evaluates analytic low-rank edits on synthetic associations. A local research studio and reproducible media expose the coefficients, assumptions, measurements and failures. It is a research prototype, not a production security detector.\n\n## Medium\n'+post.split('[Repository')[0]+'\n## Extended\n'+report.split('## Introduction')[0]+'\n'+limitation+'\n\nRead the mathematical specification before extrapolating beyond the toy grammar. The next research stage needs identical-architecture learning and independent replication; the current result is a transparent engineering demonstration with measured limits, not a replacement for semantic model training.\n\nEditorial note: lengths are approximate, not certified word counts.')
    write('career/RESEARCH_STATEMENT_PARAGRAPH.md','I am interested in the interface between explicit programs and learned representations: which computations can be authored directly, which require data, and how interventions can be audited. ZeroGrad-Sec explores this through bounded weight compilation, covariance-aware matrix edits and artifact-driven visual explanations. The project emphasizes reproducibility and failure boundaries rather than broad claims about replacing learning.')
    write('career/HIRING_MANAGER_README.md','# Two-minute review\n\n1. Read README scope and measured failure.\n2. Inspect src/zerograd/core.py: the forward does not call the oracle.\n3. Run pytest and inspect the normal-equation test.\n4. Open the studio and scrub the write events.\n5. Compare report claims with raw predictions.\n\nEvaluate correctness, clarity of scope, evidence provenance and reproducibility separately from visual polish.')
    write('career/REPRODUCIBILITY_DEMO.md',f'# Reproduce\n\n`python run_all.py --mode benchmark --offline --skip-real-llm`\n\nMeasured benchmark time on authoring host: {d["elapsed_seconds"]:.3f} seconds. Writes telemetry/benchmark_results.json, telemetry/raw/predictions.json, telemetry/manifest.json and outputs/metrics.csv. Python 3.13, CPU protocol; see docs/ENVIRONMENT.md. Next run paper and media modes separately.\n')
    write('career/CONTENT_SERIES_4_WEEKS.md','# Four-week sequence\n\n1. Compilation: poster + write replay. Ask: which bounded predicate should be next? Evidence C3/C4.\n2. Failure: length-sensitivity figure. Ask: which OOD generator would expose shortcuts? Evidence C1.\n3. Editing: spectrum + drift figure. Ask: what calibration shift invalidates locality? Evidence C2/C5.\n4. Reproduction: studio and test walkthrough. Ask for independent replication. Evidence protocol and raw predictions.\n\nOne substantial post per week; respond to critique. No automatic outreach or publishing.')
    write('career/DEMO_DAY_SCRIPT.md','# Walkthrough\n\n90 seconds: (0–20) Explain finite symbols and the zero-gradient construction. (20–45) Open compiler, scrub a real write, inspect its coordinate and checksum. (45–65) Open evidence and show the length-256 degradation. (65–90) Show patch drift and explain what remains untested.\n\nThree minutes: add the oracle/forward separation, normal-equation derivation, baseline architecture mismatch, and a reproducibility command. End with the architecture-matched experiment.\n\nSkeptical questions: Is this a standard transformer? No. Is the editor a real LM repair? No. Does low rank mean few changed entries? No; inspect C5. Is 100% a general security claim? No, it is conditional on this finite generator.')
    write('career/COMMUNITY_OUTREACH.md','# Drafts — not sent\n\nResearch group: I built a bounded weight-compilation testbed with an explicit failure boundary. Would you be willing to critique the scope of the proof and suggest a stronger generalization test? [link]\n\nMaintainer: This small research prototype uses an independent circuit and checksummed telemetry. I would value feedback on reproducibility and test design; no endorsement is implied. [link]\n\nRecruiter: I built a PyTorch research prototype with an interactive evidence studio and measured limitations. The case study links code, tests and artifacts if useful for evaluating my engineering work. [link]')
    write('career/RELEASE_CHECKLIST.md','# Before publishing\n\n- Run release-check; resolve FAIL and read all WARN entries.\n- Configure actual repository URL and author metadata.\n- Inspect mobile studio and video at feed size.\n- Confirm captions, alt text, license inventory and artifact checksums.\n- Publish repository first, then use its real link in the post.\n- Upload actual video/poster, add concise relevant tags and an evidence-linked pinned comment.\n- Never advertise unrun semantic or real-model results.\n- Posting, messaging and deployment remain manual.')
    titles=['NEURAL WEIGHTS — WRITTEN AS CODE?','THE BOUNDED REGISTER MAP','FROM SYMBOLIC RULE TO TENSOR','SURGICAL EDIT / MEASURED DRIFT','WHAT THE BENCHMARKS SHOW','LIMITS / NEXT EXPERIMENTS']
    captions=['An original matrix view introduces direct construction on a synthetic grammar.','25 token/entity product coordinates occupy a 64-dimensional embedding; this differs from the proposed register map.','A true compiled selector writes S[1+8c+e,4c+e]=1; event write-001.','A rank-two synthetic analytic patch improves its target and changes unrelated outputs.',finding,'Architecture-matched training, compositional grammar tests and calibration shift remain next.']
    montage=Image.new('RGB',(1080,900),'#07090e')
    for i,(title,cap) in enumerate(zip(titles,captions)):
        im=frame(13 if i==2 else 10,1080,1350,d,s,i);im.save(f'outputs/carousel_{i+1:02}.png');montage.paste(im.resize((360,450)),((i%3)*360,(i//3)*450))
        # Editable vector illustration, independent of raster card render.
        parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1350" viewBox="0 0 1080 1350"><rect width="1080" height="1350" fill="#07090e"/><g font-family="sans-serif" fill="#f0f3f5"><text x="86" y="120" font-size="24" fill="#10b981">ZEROGRAD-SEC / RESEARCH PROTOTYPE</text>']
        words=title.split();lines=[];line=''
        for word in words:
            if len(line+' '+word)>25:lines.append(line);line=word
            else:line=(line+' '+word).strip()
        lines.append(line)
        for j,line in enumerate(lines):parts.append(f'<text x="86" y="{230+j*70}" font-size="48" font-weight="bold">{html.escape(line)}</text>')
        if i in [0,1,2]:
            for a,b,v in s['events'][1 if i==2 else 0]['coords']:
                parts.append(f'<rect x="{86+(b%16)*50}" y="{480+(a%16)*35}" width="40" height="25" fill="#10b981"/>')
        elif i==3:
            for j,v in enumerate(e['singular_values'][:8]):parts.append(f'<rect x="{86+j*90}" y="{900-v*40}" width="60" height="{max(2,v*40)}" fill="#f59e0b"/>')
        elif i==4:
            for j,r in enumerate(supported[:4]):parts.append(f'<rect x="200" y="{500+j*90}" width="{650*r["accuracy"]}" height="40" fill="#10b981"/><text x="86" y="{530+j*90}" font-size="22">L={r["length"]}</text>')
        else:
            for j,txt in enumerate(['Architecture-matched training','Unseen compositions','Calibration shift','Independent replication']):parts.append(f'<text x="86" y="{550+j*90}" font-size="30">{txt}</text>')
        parts.append('<text x="86" y="1200" font-size="22">Bounded synthetic study. Evidence: Claim Register.</text></g></svg>')
        write(f'design/slides_svg/carousel_{i+1:02}.svg',''.join(parts))
    montage.save('outputs/carousel_montage.png');frame(1,1200,630,d,s,0).save('outputs/opengraph.png')
    write('career/LINKEDIN_CAROUSEL_COPY.md','# Carousel copy and alt text\n\n'+'\n\n'.join(f'{i+1}. **{t}**\n\n{c}\n\nAlt: {c} Asset: outputs/carousel_{i+1:02}.png; editable vector variant: design/slides_svg/carousel_{i+1:02}.svg.' for i,(t,c) in enumerate(zip(titles,captions))))
    script=[('00:00:00,000','00:00:07,000','Can a bounded rule become neural weights?'),('00:00:07,000','00:00:15,000','These authored tensor writes implement a synthetic sequence detector.'),('00:00:15,000','00:00:23,000','Explicit assumptions. Zero optimizer steps in the compiled path.'),('00:00:23,000','00:00:34,000','An analytic patch improves a synthetic target, with nonzero unrelated drift.'),('00:00:34,000','00:00:45,000','Some rules compile. Generalization must be measured.')]
    write('outputs/zerograd_subtitles.srt','\n\n'.join(f'{i+1}\n{a} --> {b}\n{txt}' for i,(a,b,txt) in enumerate(script)))
    write('outputs/zerograd_subtitles.vtt','WEBVTT\n\n'+'\n\n'.join(f'{a.replace(",",".")} --> {b.replace(",",".")}\n{txt}' for a,b,txt in script))
    write('career/LINKEDIN_REEL_CAPTIONS.md','# Reel publishing copy\n\nHook: Some rules compile. Their boundaries matter.\nTitle: ZeroGrad-Sec / weights, evidence, limits\nCover: Neural weights. Written as code?\nPinned comment: Reproduce the length-512 failure and inspect the assumptions before extrapolating. https://github.com/KaidAkram/ZeroGrad\nCTA: What is the strongest next counterexample?\nTags: #MachineLearning #ReproducibleResearch\nAlt: Animated authored matrix coordinates, synthetic patch spectrum and measured length sensitivity.\n\nExact captions:\n\n'+'\n'.join(t for _,_,t in script))
    for name in ['SHOT_LIST','STORYBOARD','VOICEOVER_SCRIPT']:
        write(f'video_studio/{name}.md','# '+name.replace('_',' ')+'\n\n'+'\n\n'.join(f'{a}–{b}: {t}' for a,b,t in script)+'\n\nOriginal deterministic source: scripts/render_video.py. Matrix displays are folded coordinate views, labeled as such; no interpolated benchmark claims. Wide layout is independently positioned. No audio recorded.')
    write('video_studio/MOTION_STYLE_GUIDE.md','# Motion system\n\n60fps deterministic frame time; obsidian ground, emerald writes, amber edit spectrum. Eight-percent safe margins. Slow scan line visualizes replay interpolation, not hardware timing. Event order comes from telemetry; cuts at 7,23,34 seconds. No flashes or stock assets. The fallback has restrained motion and is not a full Remotion composition.')
    write('video_studio/AUDIO_LICENSES.md','# Audio and visual provenance\n\nSilent renders; no music or third-party footage. Original code-generated graphics, MIT. System fonts rendered locally, not redistributed. FFmpeg and Pillow retain upstream licenses. Remotion was inspected but not installed/used because shell network access was denied.')

    from scripts.readme import generate as generate_readme
    generate_readme()

if __name__=='__main__':generate()
