# Ethics and threat model

The input is an abstract 25-symbol vocabulary with finite class/stage/entity encodings. Labels borrow security-pattern terminology as motivation, but the symbols are not executable instructions, a Linux tokenizer, an exploit recipe, or a production threat feed. No offensive automation, working prompt bypass, external target or real user data is used.

The threat model is rule violation inside the declared toy grammar: wrong order, wrong entity, incomplete chains and irrelevant padding. It excludes semantic paraphrase, adversaries controlling model deployment, unseen real syscalls, operational evasion and production monitoring. An attacker outside the support can defeat the detector; the length counterexample is published for this reason.

Analytic editing can change unrelated outputs. There is no guarantee of safety preservation or zero forgetting. Do not transfer synthetic association results to deployed models without a separate licensed checkpoint, calibration protocol and held-out behavioral evaluation.

Public claims must reference docs/CLAIM_REGISTER.md. Original graphics are code-generated. No third-party music, footage, private data or downloaded model checkpoints are bundled. Social outreach files are drafts only.
