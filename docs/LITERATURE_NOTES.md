# Literature and provenance notes

Primary pages were opened through the available web tool on 2026-11-10. Metadata below reflects those accessible pages, not an exhaustive peer review. No external scores are claimed as ZeroGrad-Sec results. Shell network access is separately blocked.

## takehi2026

[Sparks of Weight-Space Programming: LLMs can natively read & write neural network weights](https://rikiyat.github.io/blog/weight-space-programming/) — Rikiya Takehi and Jayden Teoh and Alex Zhang and Omar Khattab. Authors research blog, 2026-11-02; not assumed peer reviewed.

## ahmed2026

[Can an LLM Actually Reason and Program about Neural Network's Weights or is it just memorization on steroids? Exploring Weight-Space Programming](https://arxiv.org/abs/2611.08070) — Nazmus Sakib Ahmed. v1, submitted 2026-11-05; preprint.

## aixiv2026

[Is Weight-Space Programming More Than a Loop Fix?](https://aixiv.science/abs/aixiv.261103.000004) — Cluade Science and Codex. Site displays AI authorship, v1.1, 2026-11-04; identity and claims not independently validated; context only.

## weiss2021

[Thinking Like Transformers](https://arxiv.org/abs/2106.06981) — Gail Weiss and Yoav Goldberg and Eran Yahav. v2, revised 2021-07-19; ICML 2021.

## lindner2023

[Tracr: Compiled Transformers as a Laboratory for Interpretability](https://arxiv.org/abs/2301.05062) — David Lindner and Janos Kramar and Sebastian Farquhar and Matthew Rahtz and Thomas McGrath and Vladimir Mikulik. v5, revised 2023-11-03; NeurIPS 2023.

## meng2022rome

[Locating and Editing Factual Associations in GPT](https://arxiv.org/abs/2202.05262) — Kevin Meng and David Bau and Alex Andonian and Yonatan Belinkov. v5, revised 2023-01-13.

## meng2022memit

[Mass-Editing Memory in a Transformer](https://arxiv.org/abs/2210.07229) — Kevin Meng and Arnab Sen Sharma and Alex Andonian and Yonatan Belinkov and David Bau. v2, revised 2023-08-01; HTML section 4.2 inspected.

## hu2021

[LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685) — Edward J. Hu and Yelong Shen and Phillip Wallis and Zeyuan Allen-Zhu and Yuanzhi Li and Shean Wang and Lu Wang and Weizhu Chen. v2, revised 2021-10-16.

## dettmers2023

[QLoRA: Efficient Finetuning of Quantized LLMs](https://arxiv.org/abs/2305.14314) — Tim Dettmers and Artidoro Pagnoni and Ari Holtzman and Luke Zettlemoyer. Submitted 2023-05-23.

## sheng2023

[S-LoRA: Serving Thousands of Concurrent LoRA Adapters](https://arxiv.org/abs/2311.03285) — Ying Sheng and others. v3, revised 2024-06-05.

## ha2016

[HyperNetworks](https://arxiv.org/abs/1609.09106) — David Ha and Andrew Dai and Quoc V. Le. v4, revised 2016-12-01.

## hotsko2026

[Code2LoRA: Hypernetwork-Generated Adapters for Code Language Models under Software Evolution](https://arxiv.org/abs/2606.06492) — Liliana Hotsko and Yinxi Li and Yuntian Deng and Pengyu Nie. v2, revised 2026-10-27; preprint.

## augenstein2026

[LoRA-generating hypernetworks for efficient on-device LLM generative personalization](https://arxiv.org/abs/2609.24979) — Sean Augenstein and Li Ding and Jihwan Lee and Keith Rush and Andrey Zhmoginov. Submitted 2026-09-21; preprint.

## lewis2020

[Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401) — Patrick Lewis and others. v4, revised 2021-04-12.

## Related-work / difference matrix

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
