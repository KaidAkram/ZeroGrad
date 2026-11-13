# Synthetic analytic edit

The rank-2 analytic patch reduced target MSE from 3.640517 to 0.000334, with unrelated-output drift MSE 0.073793.

[
  {
    "method": "analytic",
    "lambda_": 0.0,
    "lambda": 0.0,
    "target_mse": 3.6405100347523926e-12,
    "before_mse": 3.6405173169036074,
    "drift": 0.07065668251365692,
    "patch_norm": 7.63204825548675,
    "singular_values": [
      7.067618831478588,
      2.8804382699526085,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0
    ],
    "rank": 2,
    "reconstruction_error": 2.3023747694351215e-15,
    "adapter_parameters": 48,
    "modified_entries": 16,
    "original_parameters": 128
  },
  {
    "method": "analytic",
    "lambda_": 0.1,
    "lambda": 0.1,
    "target_mse": 3.4063705225918364e-06,
    "before_mse": 3.6405173169036074,
    "drift": 0.07508075250504985,
    "patch_norm": 7.627242510904702,
    "singular_values": [
      7.0631455535054695,
      2.8786808107443544,
      2.283919395272759e-17,
      1.39547568515448e-17,
      8.968121044788054e-18,
      7.017541285625718e-18,
      5.57789994494096e-18,
      1.4959272387149361e-18
    ],
    "rank": 2,
    "reconstruction_error": 3.472419797170628e-15,
    "adapter_parameters": 48,
    "modified_entries": 128,
    "original_parameters": 128
  },
  {
    "method": "analytic",
    "lambda_": 1.0,
    "lambda": 1.0,
    "target_mse": 0.0003341526299500032,
    "before_mse": 3.6405173169036074,
    "drift": 0.07379283409118395,
    "patch_norm": 7.56153806843999,
    "singular_values": [
      7.00164478779881,
      2.8554908905400076,
      2.9156333950192415e-17,
      2.0283716082567727e-17,
      1.0437209175092888e-17,
      4.882194046874539e-18,
      3.740073510397871e-18,
      2.5250585755736177e-18
    ],
    "rank": 2,
    "reconstruction_error": 3.956129304044559e-15,
    "adapter_parameters": 48,
    "modified_entries": 128,
    "original_parameters": 128
  },
  {
    "method": "analytic",
    "lambda_": 10.0,
    "lambda": 10.0,
    "target_mse": 0.028305983881345333,
    "before_mse": 3.6405173169036074,
    "drift": 0.06255361743308455,
    "patch_norm": 6.96193802519666,
    "singular_values": [
      6.440907191459937,
      2.6425925939650248,
      3.2964430409182454e-17,
      1.5267591049915836e-17,
      1.4169975658755422e-17,
      5.4331222969592845e-18,
      4.8610750480611744e-18,
      1.7399195354126043e-18
    ],
    "rank": 2,
    "reconstruction_error": 4.22980435788346e-15,
    "adapter_parameters": 48,
    "modified_entries": 128,
    "original_parameters": 128
  },
  {
    "method": "random-direction",
    "lambda": 1.0,
    "target_mse": 3.857409225132179,
    "before_mse": 3.6405173169036074,
    "drift": 6.724336025320696,
    "rank": 8,
    "singular_values": [
      3.9033523404421637,
      3.5638349106659075,
      2.9533604330065644,
      2.6374015747248594,
      2.3629885585665242,
      2.1678703977274885,
      1.4398481526350346,
      1.0977315659280984
    ]
  },
  {
    "method": "shuffled-target",
    "lambda": 1.0,
    "target_mse": 2.162318383097449,
    "before_mse": 3.6405173169036074,
    "drift": 0.1101194499669015,
    "rank": 2,
    "singular_values": [
      6.896577345041466,
      6.0612223209367135,
      2.507761440079105e-17,
      1.7722603100189287e-17,
      5.781278567424573e-18,
      5.4976622885566175e-18,
      2.167470549598544e-18,
      4.579756379716187e-19
    ]
  }
]

These are synthetic, finite symbolic tasks. The main benchmark and studio replay use the prefix circuit. A separately validated four-block transformer implements the same narrow two-stage grammar; three blocks compute and one is identity. The feature MLP and retrieval baselines are diagnostic and not architecture-matched. No semantic or real pretrained-model claim is supported.