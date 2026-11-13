# Execution record and acceptance status

Authoritative brief: ZEROGRAD_SEC_MASTER_PROMPT.txt. Initial execution began
2026-11-10; completion/review continued 2026-11-11. The entire 500-line brief was
read with the terminal in chunks before implementation. Only the brief existed
initially; no unrelated repository or user source was overwritten.

| Gate | Actual work / command | Status and remaining acceptance gap |
|---|---|---|
| 0 Audit | Python/Node/FFmpeg, memory/disk/GPU audit; official reference pages; installed skill docs; isolated local venv | Complete local audit. Shell package network denied. Remotion license/source provenance insufficient for installation; no install claimed. |
| 1 Math | specs/ZEROGRAD_MATH_SPEC.md and TRANSFORMER_EXTENSION.md | Bounded two-stage proof and numeric tensor recipes; no arbitrary-length or semantic proof. |
| 2 CPU slice | core.py; independent oracle; data-driven IR; frozen tensors; `python -m pytest -q` | Working prefix circuit and separately validated four-block transformer. Exact coordinate replay and negative tests. |
| 3 Experiments | `python run_all.py --mode benchmark --offline --skip-real-llm` | 44 prefix/diagnostic rows, 3 seeds. Retrieval + fixed-budget feature MLP are explicitly not architecture-matched. Full tuning/sample-size/semantic suites deferred. |
| 4 Editor | analytic normal-equation solve, SVD, controls, patch save/apply/undo tests | Synthetic linear association module completed. Full synthetic transformer editing and real checkpoint editing remain unsupported. |
| 5 Studio | `npm.cmd run build`, `npm.cmd test` in studio | React/TypeScript static build and 12 browser checks pass, including actual film and caption loading. Desktop/mobile screenshots inspected. Diagram geometry/register strip labeled schematic. Live browser-side inference and full attention explorer remain absent. |
| 6 Media | `python run_all.py --mode media --quality preview` then `--quality final`; `python scripts/verify_media.py` | Real 60fps 5s preview, 45s portrait, 45s widescreen and 12s teaser. FFprobe metadata and full decode pass. Original restrained Pillow/FFmpeg fallback; no Remotion composition or audio. |
| 7 Communication | `python run_all.py --mode paper`; generated report, SVG/PNG figures, 6 carousel cards, README, CV and LinkedIn kit | Completed local prototype kit. Manuscript is Markdown technical report, not accepted paper; author/repo URL not invented. No LaTeX/PDF compilation claimed. |
| 8 QA | pytest XML, schema/claim validation, browser results, media decode, release-check and manifest | Local delivery gate with transparent research warnings. Hosted CI and clean network installation not executed. |

## Executed extension

The follow-on transformer uses four blocks, four heads, d_model=64, d_head=16,
d_mlp=256, vocabulary capacity=32, ReLU MLPs and masked-softmax attention.
Three blocks compute and one is identity; only head zero routes nonzero values.
It compiles the **same narrow two-stage grammar**, not the original brief's full
security state machine. `python -m evaluation.transformer_validation` (with
PYTHONPATH=src) wrote 16 separate evaluation rows and the complete tensor stream.
The standard benchmark runner now invokes this extension automatically.

## Reproduction and checkpoints

- `python run_all.py --mode smoke --offline`: CPU, no network; separate tiny result,
  JSON validation and real-data PNG/SVG.
- `python run_all.py --mode benchmark --offline --skip-real-llm`: bounded diagnostic
  science + extension; source/seed checkpoint in outputs/science_checkpoint.json.
- Add `--resume` to reuse science only if source/seed fingerprints match. Figures,
  docs, studio and video are separate stages and can be regenerated independently.
- `python run_all.py --mode paper`: reports/cards/career assets and repository docs.
- `python run_all.py --mode media --quality final`: sequential bounded render jobs.
- `python run_all.py --mode release-check`: artifacts, selected claims and recorded QA.
- `python run_all.py --mode full --quality final`: science, documents, media, Python
  tests, studio build/browser QA, media validation, release gate.

## Explicit deferred work (not environment excuses)

The full research program exceeds this prototype: architecture-matched trained
baselines with validation tuning, Hybrid/LoRA training, semantic classification,
full class calibration/ROC/PR and latency/memory profiling, larger N grid,
disjoint compositional templates, realistic skew priors, noisy/distribution-shift
editing studies, causal defect localization and real licensed checkpoint repair.
These are unimplemented studies, not successful or merely hidden results. Their
machine-readable statuses and limitations prevent broader public claims.

No external site deployment, GitHub push, social publishing, email or DM was
performed. Source Git history was absent at audit; creating an archival release
and assigning author metadata remain owner actions.
