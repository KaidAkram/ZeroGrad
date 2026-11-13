"""Repository documentation and research governance assets; no fabricated results."""
import json
import platform
import importlib.metadata
from datetime import datetime,timezone
from pathlib import Path
from scripts.report import write

REFERENCES=[
('takehi2026','Rikiya Takehi and Jayden Teoh and Alex Zhang and Omar Khattab','Sparks of Weight-Space Programming: LLMs can natively read & write neural network weights','2026','https://rikiyat.github.io/blog/weight-space-programming/','Authors research blog, 2026-11-02; not assumed peer reviewed'),
('ahmed2026','Nazmus Sakib Ahmed','Can an LLM Actually Reason and Program about Neural Network\'s Weights or is it just memorization on steroids? Exploring Weight-Space Programming','2026','https://arxiv.org/abs/2611.08070','v1, submitted 2026-11-05; preprint'),
('aixiv2026','Cluade Science and Codex','Is Weight-Space Programming More Than a Loop Fix?','2026','https://aixiv.science/abs/aixiv.261103.000004','Site displays AI authorship, v1.1, 2026-11-04; identity and claims not independently validated; context only'),
('weiss2021','Gail Weiss and Yoav Goldberg and Eran Yahav','Thinking Like Transformers','2021','https://arxiv.org/abs/2106.06981','v2, revised 2021-07-19; ICML 2021'),
('lindner2023','David Lindner and Janos Kramar and Sebastian Farquhar and Matthew Rahtz and Thomas McGrath and Vladimir Mikulik','Tracr: Compiled Transformers as a Laboratory for Interpretability','2023','https://arxiv.org/abs/2301.05062','v5, revised 2023-11-03; NeurIPS 2023'),
('meng2022rome','Kevin Meng and David Bau and Alex Andonian and Yonatan Belinkov','Locating and Editing Factual Associations in GPT','2022','https://arxiv.org/abs/2202.05262','v5, revised 2023-01-13'),
('meng2022memit','Kevin Meng and Arnab Sen Sharma and Alex Andonian and Yonatan Belinkov and David Bau','Mass-Editing Memory in a Transformer','2022','https://arxiv.org/abs/2210.07229','v2, revised 2023-08-01; HTML section 4.2 inspected'),
('hu2021','Edward J. Hu and Yelong Shen and Phillip Wallis and Zeyuan Allen-Zhu and Yuanzhi Li and Shean Wang and Lu Wang and Weizhu Chen','LoRA: Low-Rank Adaptation of Large Language Models','2021','https://arxiv.org/abs/2106.09685','v2, revised 2021-10-16'),
('dettmers2023','Tim Dettmers and Artidoro Pagnoni and Ari Holtzman and Luke Zettlemoyer','QLoRA: Efficient Finetuning of Quantized LLMs','2023','https://arxiv.org/abs/2305.14314','Submitted 2023-05-23'),
('sheng2023','Ying Sheng and others','S-LoRA: Serving Thousands of Concurrent LoRA Adapters','2023','https://arxiv.org/abs/2311.03285','v3, revised 2024-06-05'),
('ha2016','David Ha and Andrew Dai and Quoc V. Le','HyperNetworks','2016','https://arxiv.org/abs/1609.09106','v4, revised 2016-12-01'),
('hotsko2026','Liliana Hotsko and Yinxi Li and Yuntian Deng and Pengyu Nie','Code2LoRA: Hypernetwork-Generated Adapters for Code Language Models under Software Evolution','2026','https://arxiv.org/abs/2606.06492','v2, revised 2026-10-27; preprint'),
('augenstein2026','Sean Augenstein and Li Ding and Jihwan Lee and Keith Rush and Andrey Zhmoginov','LoRA-generating hypernetworks for efficient on-device LLM generative personalization','2026','https://arxiv.org/abs/2609.24979','Submitted 2026-09-21; preprint'),
('lewis2020','Patrick Lewis and others','Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks','2020','https://arxiv.org/abs/2005.11401','v4, revised 2021-04-12')]

def main():
    now=datetime.now(timezone.utc).isoformat()
    notes='# Literature and provenance notes\n\nPrimary pages were opened through the available web tool on 2026-11-10. Metadata below reflects those accessible pages, not an exhaustive peer review. No external scores are claimed as ZeroGrad-Sec results. Shell network access is separately blocked.\n\n'
    for key,authors,title,year,url,status in REFERENCES:
        notes+=f'## {key}\n\n[{title}]({url}) — {authors}. {status}.\n\n'
    notes+='''## Related-work / difference matrix

| Prior family | What this project uses | What it does not claim |
|---|---|---|
| RASP / Tracr | Inspiration for transparent compiled sequence programs | Novelty of program-to-transformer compilation |
| ROME / MEMIT | Associative-memory view and analytic update motivation | Reproducing causal tracing, target optimization, or large-LM factual edits |
| LoRA / QLoRA | Low-rank factor vocabulary, distinct gradient baseline target | Quantization support, trained LoRA results, or equivalence of analytic and trained adapters |
| S-LoRA | Context for adapter-serving systems | A multi-adapter serving implementation |
| HyperNetworks / Code2LoRA / personalization | Related generated-weight approaches | A trained hypernetwork or inference-time personalization evaluation |
| RAG | Context for nonparametric evidence retrieval | Retrieval-only nearest neighbors are not generation |
| 2026 WSP reports | Motivation and the need for controlled tests | Reproduction of their models, scores, sparse edit fractions, or LLM autonomous discovery |

The original engineering contribution is the local combination of explicit coefficients, a proof/test fixture, checksummed replay, reproducible diagnostic evaluations and visual explanations. Priority and algorithmic novelty are unestablished. The AI-authored aiXiv item is not relied on for technical guarantees. The editor formula is derived in the spec; its objective adds explicit ridge and uses a normalized uncentered calibration covariance. It is not labeled the complete MEMIT algorithm.

## Skills and license checks

Official OpenAI skill documentation inspected: https://developers.openai.com/plugins/concepts/skills and https://learn.chatgpt.com/docs/build-skills . Local skill-installer and skill-creator instructions were read. Three concise project-specific skills were authored rather than installing unverified community packages.

Official Remotion skill documentation: https://www.remotion.dev/docs/ai/skills ; repository: https://github.com/remotion-dev/skills . The repository page was inspected. The attempted raw SKILL.md and LICENSE URLs returned 404; no license provenance was established for a local copy. Shell GitHub/npm requests were denied by the host. No Remotion skill or executable was installed or represented as installed. Remotion software licensing was inspected at https://www.remotion.pro/license (individual/small-team terms shown there); the fallback render uses no Remotion code. Future installation should pin a verified commit and inspect the actual license and entrypoint first.
'''
    write('docs/LITERATURE_NOTES.md',notes)
    write('references.bib','\n\n'.join(f'@misc{{{key},\n  author = {{{a}}},\n  title = {{{t}}},\n  year = {{{y}}},\n  url = {{{url}}},\n  note = {{{status}; accessed 2026-11-10}}\n}}' for key,a,t,y,url,status in REFERENCES))
    versions={p:importlib.metadata.version(p) for p in ['numpy','torch','scipy','scikit-learn','matplotlib','pydantic','Pillow','pytest','psutil']}
    write('requirements-observed.txt','# Exact versions observed; clean network install not verified. Python 3.13 on authoring host.\n'+'\n'.join(f'{k}=={v}' for k,v in versions.items())+'\n')
    cpu_versions={**versions,'torch':versions['torch'].split('+')[0]}
    write('requirements-cpu.txt','# Reproduction pins; torch uses the public version, not the authoring host CUDA build tag.\n# Install torch from the official CPU index first if a CPU-only wheel is needed. Clean install unverified here.\n'+'\n'.join(f'{k}=={v}' for k,v in cpu_versions.items())+'\n')
    write('docs/ENVIRONMENT.md',f'''# Audited environment

Updated {now}. Initial workspace contained only the master brief; it was not a Git repository. No existing source was overwritten or Git history reinitialized. Source revision is therefore `unversioned`; a release commit must be created by the owner.

- OS: Windows, PowerShell; Python {platform.python_version()}.
- Node 24.14.1; npm.cmd used because npm.ps1 is blocked by PowerShell execution policy. No execution-policy changes made.
- CPU: 20 logical processors; approximately 15.7 GiB system RAM and 55.8 GiB free disk at initial audit. CUDA reported available, but all science uses CPU with two PyTorch threads; no GPU benchmark claim.
- FFmpeg/ffprobe 8.1.2 available; system Arial font rendered but not redistributed.
- Python versions: {json.dumps(versions)}.
- `.venv` created with system-site-packages for the available trusted scientific stack. No global package changes. A clean environment install remains unverified because shell network sockets are blocked (WinError 10013 / EACCES).
- Official references could be read through the web tool. Shell GitHub/npm requests failed; no privileged retry.
- React/TypeScript/Vite dependencies were recovered from the existing read-only npm cache. studio/package-lock.json contains pinned integrity hashes. Production build succeeds locally.
- Installed Microsoft Edge/Playwright enabled local browser QA. No external hosting, account access, publishing or messaging performed.
- Skills applied: installed skill-installer, skill-creator, openai-docs and Sites instructions. Remotion installation blocked; original Pillow/FFmpeg fallback used.

Machine names, account secrets and unique hardware identifiers are intentionally excluded.
''')
    write('docs/ETHICS_AND_THREAT_MODEL.md','''# Ethics and threat model

The input is an abstract 25-symbol vocabulary with finite class/stage/entity encodings. Labels borrow security-pattern terminology as motivation, but the symbols are not executable instructions, a Linux tokenizer, an exploit recipe, or a production threat feed. No offensive automation, working prompt bypass, external target or real user data is used.

The threat model is rule violation inside the declared toy grammar: wrong order, wrong entity, incomplete chains and irrelevant padding. It excludes semantic paraphrase, adversaries controlling model deployment, unseen real syscalls, operational evasion and production monitoring. An attacker outside the support can defeat the detector; the length counterexample is published for this reason.

Analytic editing can change unrelated outputs. There is no guarantee of safety preservation or zero forgetting. Do not transfer synthetic association results to deployed models without a separate licensed checkpoint, calibration protocol and held-out behavioral evaluation.

Public claims must reference docs/CLAIM_REGISTER.md. Original graphics are code-generated. No third-party music, footage, private data or downloaded model checkpoints are bundled. Social outreach files are drafts only.
''')
    qs=[('RQ1','Can bounded rules compile without SGD?','Oracle disagreement rate within L<=128','Compiled weights vs independent oracle; wrong-order/entity negatives','Any supported disagreement falsifies the exact construction hypothesis'),('RQ2','How does robustness vary with length and bindings?','Accuracy by length and entity; explicit late-pair failure','Same compiler, length sweep, finite IDs','No degradation outside support would challenge the proposed failure mechanism, not prove unbounded correctness'),('RQ3','Can analytic edits balance target repair and locality?','Target MSE, unrelated-output MSE, update rank/norm','Naive, random-direction and shuffled-target patches on identical checkpoint','Failure to improve target or drift above the predeclared application tolerance rejects usefulness; no production tolerance is claimed here'),('RQ4','Where does compilation fail relative to learned semantic methods?','Matched task accuracy and semantic held-out performance','Identical-architecture trained model and semantic model; NOT RUN yet','A compiled win on this symbolic generator does not answer semantic generalization'),('RQ5','Can event-sourced weight changes support faithful visualization?','Replay checksum equality, schema violations, UI evidence binding','Tampered checksum/coordinate negative tests','Any mismatched reconstructed tensor or unsupported displayed metric rejects fidelity')]
    write('docs/RESEARCH_QUESTIONS.md','# Falsifiable questions\n\n'+'\n\n'.join(f'## {q}\n\nQuestion: {question}\n\nH0: the proposed construction or protocol provides no reliable advantage for this observable. H1: it satisfies its declared bounded invariant or measured tradeoff.\n\nObservable: {obs}.\n\nControls: {ctrl}.\n\nFailure criterion: {fail}.\n\nWhy it matters: makes the scope of a weight-programming claim empirically auditable.' for q,question,obs,ctrl,fail in qs))
    write('docs/RESEARCH_POSITIONING.md','''# Positioning

Demonstrated engineering: bounded coefficient recipes, independent oracle tests, ridge/SVD diagnostics and a shared artifact pipeline. This does not establish a new learning algorithm, general neural programmability or real security detection. RASP/Tracr and ROME/MEMIT are acknowledged as prior work.

The four-block extension compiles the same narrow two-stage grammar into ordinary masked-softmax/ReLU residual operations; three blocks compute and one is identity. Its results are separate from the original prefix-circuit study.

Before submission: (1) train and compare the exact same architecture with a validation-tuned budget; (2) evaluate disjoint compositional templates, dense mixtures and unseen entity encodings; (3) test calibration distribution shift and noisy edit keys with preregistered drift tolerances. An independent replication should precede broad performance claims.
''')
    write('docs/RESEARCH_ROADMAP.md','''# 30 / 60 / 90-day research roadmap

30 days: architecture-matched initialization/training controls, complete baseline tuning protocol, dense compositional splits, latency/memory and calibration metrics. Freeze the evaluation before tuning.

60 days: expanded three-stage circuits, stronger entity/generalization tests, causal ablations of authored registers, noisy keys and covariance-shift edit controls. Release an independently reviewed benchmark specification.

90 days: independent replication and a small licensed pretrained-checkpoint study only if the synthetic controls justify it. Consider a workshop submission after full evidence review; no acceptance or novelty claim is made.
''')
    write('docs/RESEARCH_PITCH_ONE_PAGER.md','''# ZeroGrad-Sec / a laboratory for auditable weight programs

**Question:** Which bounded computations can be written into neural weights, and what evidence is needed before calling a direct edit useful?

**Artifact:** A CPU-first PyTorch compiler with an independent oracle, a separately validated four-block bounded transformer, a covariance-aware analytic editor and a local React research studio. JSON evidence drives original figures and deterministic media.

**Initial evidence:** The prefix circuit agrees on 3,072 generated examples within lengths 16–128 and degrades beyond its proved support. The synthetic rank-two association edit improves target MSE while measurably changing unrelated outputs. See Claim Register C1/C2 for exact values and scope.

**Research value:** Explicit weights make intervention ground truth available; negative results expose where representational assumptions enter the computation. Shared telemetry makes visual explanations inspectable rather than anecdotal.

**Limits:** Toy symbols, favorable synthetic covariance, incomplete architecture-matched/semantic baselines, no real-model repair or production security claim. This is an unreviewed prototype.

**Next collaboration:** Design and independently run the architecture-matched comparison and a compositional split. Seeking critique and replication, not affiliation or endorsement.
''')
    write('specs/SYMBOLIC_CIRCUIT_IR.md','''# Symbolic circuit IR and telemetry contract

`Write(tensor, shape, coords, formula)` is a typed authored matrix block. Coordinates are exact float32 assignments to a zero-initialized tensor. `circuit_ir()` emits the four prefix operations; `transformer_ir()` emits every transformer matrix, including authored zeros. Their forward passes consume the resulting tensors and never call the oracle.

The implemented IR is intentionally smaller than a general REGISTER/SELECT/AGGREGATE language. It represents assignment recipes and their provenance, not arbitrary automatic program synthesis. The human-readable spec supplies the dependency graph. Supported operations are embedding selection, fixed causal averaging, residual ReLU gates and linear readout.

Each stream event records ID, tensor shape, exact COO coordinates, equation label, before/after SHA256 and a zero-gradient flag. Empty coordinate lists represent a real zero block, not fictitious individual writes. Replay reconstructs the full arrays and validates both checksums. Pydantic rejects duplicate IDs/coordinates, out-of-range indices and false zero-gradient declarations. JSON schema is generated by src/zerograd/telemetry.py. Frame interpolation is purely visual.

The minimal implemented event schema is for weight writes. Register/attention/SVD probes are stored as experiment artifacts where available; this release does not claim the complete richer event taxonomy in the original brief. Run metadata and result IDs remain separate JSON records.
''')
    write('AGENTS.md','''# ZeroGrad-Sec repository instructions

Read ZEROGRAD_SEC_MASTER_PROMPT.txt for the authoritative brief. Preserve existing artifacts and label scope reductions explicitly. Run CPU tests after scientific changes. Public quantitative claims must match telemetry/benchmark_results.json or the separately named transformer extension artifact. Update docs/CLAIM_REGISTER.md and regenerate reports when results change. Never imply real-world threat detection or pretrained repair from synthetic tests. Do not publish or send outreach without explicit authorization.
''')
    write('.gitignore','''.venv/
__pycache__/
*.py[cod]
.pytest_cache/
node_modules/
.npm-cache/
*.log
.env
.env.*
!.env.example
*.safetensors
*.pt
*.pth
*.ckpt
studio/dist/
studio/public/data/
studio/public/media/
.publish/
''')
    write('LICENSE','''MIT License

Copyright (c) 2026 ZeroGrad-Sec contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
''')
    write('CITATION.cff','''cff-version: 1.2.0
message: "Please cite this unreviewed research software prototype; source and evidence are available in the linked repository."
title: "ZeroGrad-Sec: bounded weight compilation and analytic editing"
type: software
version: 0.1.0
date-released: 2026-11-11
license: MIT
authors:
  - family-names: "Kaid"
    given-names: "Akram"
repository-code: "https://github.com/KaidAkram/ZeroGrad"
url: "https://github.com/KaidAkram/ZeroGrad"
abstract: "A synthetic CPU-first testbed with explicit assumptions and evidence-linked visualizations."
''')
    write('CONTRIBUTING.md','# Contributing\n\nRun `python -m pytest -q`, smoke, and studio build/browser checks before proposing a change. Preserve frozen test seeds; disclose any tuning. Add raw evidence and claim-register entries for scientific results. Avoid large checkpoints and offensive payloads. Changes to the proof or grammar require independent oracle tests and documented scope. Use issues for reproducibility reports; no affiliation is implied by a contribution.')
    write('CODE_OF_CONDUCT.md','# Code of conduct\n\nParticipate respectfully, critique evidence rather than people, protect private information, and avoid harassment or discriminatory conduct. Maintainers may remove harmful content or restrict participation. Report conduct concerns privately through a repository maintainer contact once configured; no personal address is invented here.')
    write('SECURITY.md','# Security\n\nThis prototype is not a deployed security detector. It processes safe abstract tokens only. Do not attach credentials, live exploit payloads, private logs or model checkpoints with unclear licenses. Use GitHub private vulnerability reporting when enabled by the owner; otherwise request a private contact without posting sensitive details publicly. No production security guarantee is offered.')
    write('assets/LICENSES.md','# Asset licenses\n\nOriginal diagrams, SVGs, motion source and carousel illustrations: MIT under repository LICENSE. System Arial fonts are rendered locally and are not redistributed; Linux fallback is installed DejaVu Sans. No downloaded music, photography, footage or model weights. Runtime software retains its own upstream licenses. React/Vite/TypeScript/Playwright package licenses are in their installed distributions. Python dependencies and FFmpeg are external runtime dependencies, not relicensed by this repository.')
    write('.github/ISSUE_TEMPLATE/reproducibility.md','---\nname: Reproducibility report\nabout: Report a failed command or inconsistent scientific artifact\n---\n\nCommand, OS/Python/Node versions, expected artifact, actual error, and relevant claim/result ID. Remove secrets before sharing logs.\n')
    write('.github/workflows/ci.yml','''name: CPU research checks
on: [push, pull_request]
jobs:
  science:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: python -m pip install . pytest psutil
      - run: python -m pytest -q
      - run: python run_all.py --mode smoke --offline --skip-real-llm
      - run: python scripts/validate_claims.py
  studio:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '24'
      - run: npm ci
        working-directory: studio
      - run: npm run build
        working-directory: studio
''')
    write('scripts/bootstrap.ps1','''$ErrorActionPreference = 'Stop'
python -m venv .venv
& ./.venv/Scripts/python.exe -m pip install -r requirements-cpu.txt
& ./.venv/Scripts/python.exe -m pip install -e . --no-deps
Push-Location studio
try { npm.cmd ci } finally { Pop-Location }
''')
    write('scripts/bootstrap.sh','''#!/bin/sh
set -eu
python3 -m venv .venv
.venv/bin/python -m pip install -e . pytest psutil
cd studio
npm ci
''')
    skills={
      'research-repro-audit':('Audit ZeroGrad-Sec benchmark reproducibility, split leakage and claim evidence when scientific artifacts change.', 'Read docs/EXPERIMENT_PROTOCOL.md and docs/CLAIM_REGISTER.md. Compare result IDs and raw predictions, verify train/test sequence exclusion, seed schedules, uncertainty denominators and method comparability. Run tests and scripts/validate_claims.py. Keep the transformer extension distinct from prefix results. Report missing comparisons as unrun; never infer semantic efficacy from these tokens.'),
      'weight-telemetry-visuals':('Regenerate faithful ZeroGrad-Sec figures and motion from validated telemetry when visual assets or measurements change.', 'Validate telemetry with src/zerograd/telemetry.py and replay checksums. Use scripts/report.py for figures/cards and scripts/render_video.py for frame-based media. Never invent compilation accuracy checkpoints. Preserve folded-coordinate and schematic-geometry labels. Inspect portrait and wide frames, then run scripts/verify_media.py. Exact SVG variants are editable sources, not claims of identical raster composition.'),
      'release-and-career-kit':('Refresh ZeroGrad-Sec career copy and release evidence after verified scientific changes.', 'Read the claim register, release status and authoritative results. Regenerate via python run_all.py --mode paper, then inspect README and career copy for scope drift. Check actual asset links, author metadata, license provenance and hashes with release-check. Repository URLs and affiliations must be supplied by the owner. Publishing or sending outreach is a separate authorized action.')}
    for name,(description,body) in skills.items():
        write(f'.agents/skills/{name}/SKILL.md',f'---\nname: {name}\ndescription: {description}\n---\n\n# {name.replace("-"," ").title()}\n\n{body}\n')
    write('design/brand_tokens.json',json.dumps(dict(obsidian='#07090E',carbon='#0F141C',border='#1E293B',text='#F0F3F5',muted='#94A3B8',compiled='#10B981',routing='#06B6D4',edit='#F59E0B',anomaly='#F43F5E',spacing=[8,16,24,32,48,64,96]),indent=2))

if __name__=='__main__':main()
