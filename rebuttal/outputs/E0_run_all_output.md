# E0 Run All Output Details

- generated_by: `src/rebuttal/scripts/E0_run_all.py`
- output_preview_char_limit: `20000`

## E1

### 源文件: `E1_main_metrics.csv`

- 路径: `rebuttal/outputs/E1_main_metrics.csv`
- 文件大小(bytes): `6493`

```text
method,target,literal_p,literal_r,literal_f1,fuzzy_p,fuzzy_r,fuzzy_f1,continuous_p,continuous_r,continuous_f1,graph_p,graph_r,graph_f1,delta_continuous_f1_vs_strongest_non_scion,p_value,evaluator_signature,evaluator_hash,evaluator_aligned_with_submission,frozen_gold_artifact_hash,evaluation_protocol,result_mode,is_proxy_result,is_approximate_result
manual,full_gold,0.7108,0.4936,0.5724,0.9555,0.8137,0.8613,0.9049,0.7281,0.8030,0.7818,0.5729,0.6613,-0.0729,2.38e-07,cabc4561,c4c23718,True,26bad3bb,submission_aligned_scope_v1,rerun_only,False,False
manual,reachable_gold,0.7413,0.6056,0.6354,0.9825,0.9044,0.9349,0.9354,0.8104,0.8619,0.7952,0.6548,0.7182,-0.0551,9.54e-07,cabc4561,c4c23718,True,26bad3bb,submission_aligned_scope_v1,rerun_only,False,False
text2onto,full_gold,0.7426,0.5602,0.6299,0.9497,0.8445,0.8799,0.9084,0.7637,0.8269,0.8124,0.6521,0.7236,-0.0490,2.38e-07,cabc4561,c4c23718,True,26bad3bb,submission_aligned_scope_v1,rerun_only,False,False
text2onto,reachable_gold,0.7760,0.6777,0.6954,0.9786,0.9526,0.9608,0.9424,0.8544,0.8910,0.8344,0.7512,0.7906,-0.0260,4.77e-07,cabc4561,c4c23718,True,26bad3bb,submission_aligned_scope_v1,rerun_only,False,False
llm_only,full_gold,0.7701,0.6273,0.6836,0.9559,0.8366,0.8814,0.9142,0.7916,0.8459,0.8299,0.6568,0.7331,-0.0300,3.81e-06,cabc4561,c4c23718,True,26bad3bb,submission_aligned_scope_v1,rerun_only,False,False
llm_only,reachable_gold,0.8036,0.7515,0.7513,0.9757,0.9445,0.9530,0.9445,0.8833,0.9073,0.8412,0.8122,0.8264,-0.0097,1.91e-06,cabc4561,c4c23718,True,26bad3bb,submission_aligned_scope_v1,rerun_only,False,False
eta,full_gold,0.7818,0.6568,0.7063,0.9976,0.8787,0.9141,0.9423,0.8241,0.8759,0.8624,0.6841,0.7629,0.0,0.2500,cabc4561,c4c23718,True,26bad3bb,submission_aligned_scope_v1,rerun_only,False,False
eta,reachable_gold,0.8180,0.7837,0.7761,0.9685,0.9647,0.9576,0.9469,0.8994,0.9170,0.8711,0.8192,0.8444,0.0,0.5000,cabc4561,c4c23718,True,26bad3bb,submission_aligned_scope_v1,rerun_only,False,False
scion_lite,full_gold,0.8106,0.7145,0.7518,0.9977,0.9021,0.9298,0.9421,0.8508,0.8909,0.8814,0.7138,0.7888,0.0150,0.0001,cabc4561,c4c23718,True,26bad3bb,submission_aligned_scope_v1,rerun_only,False,False
scion_lite,reachable_gold,0.8462,0.8464,0.8239,0.9735,0.9739,0.9680,0.9502,0.9297,0.9340,0.8902,0.8411,0.8650,0.0170,0.0009,cabc4561,c4c23718,True,26bad3bb,submission_aligned_scope_v1,rerun_only,False,False
scion_fusion,full_gold,0.8192,0.7472,0.7740,0.9936,0.9060,0.9352,0.9478,0.8684,0.9032,0.8901,0.7321,0.8035,0.0273,1.10e-05,cabc4561,c4c23718,True,26bad3bb,submission_aligned_scope_v1,rerun_only,False,False
scion_fusion,reachable_gold,0.8548,0.8818,0.8466,0.9716,0.9839,0.9715,0.9533,0.9449,0.9439,0.8992,0.8712,0.8850,0.0269,0.0001,cabc4561,c4c23718,True,26bad3bb,submission_aligned_scope_v1,rerun_only,False,False
scion_full,full_gold,0.8301,0.7690,0.7906,0.9936,0.9068,0.9309,0.9481,0.8757,0.9068,0.8988,0.7432,0.8136,0.0309,1.10e-05,cabc4561,c4c23718,True,26bad3bb,submission_aligned_scope_v1,rerun_only,False,False
scion_full,reachable_gold,0.8660,0.9051,0.8645,0.9672,0.9847,0.9674,0.9507,0.9565,0.9469,0.9082,0.8851,0.8965,0.0299,1.10e-05,cabc4561,c4c23718,True,26bad3bb,submission_aligned_scope_v1,rerun_only,False,False
scion_rl,full_gold,0.8373,0.7847,0.8025,0.9902,0.9030,0.9310,0.9480,0.8813,0.9101,0.9024,0.7554,0.8228,0.0342,6.60e-05,cabc4561,c4c23718,True,26bad3bb,submission_aligned_scope_v1,rerun_only,False,False
scion_rl,reachable_gold,0.8737,0.9216,0.8765,0.9660,0.9932,0.9704,0.9540,0.9666,0.9541,0.9125,0.8982,0.9053,0.0371,1.10e-05,cabc4561,c4c23718,True,26bad3bb,submission_aligned_scope_v1,rerun_only,False,False
```

## objective
- inter-event relation pilot

## methods compared
- pilot schema extension

## dataset scope
- 1-2 EE datasets

## exact files produced
- `E12_inter_event_main.csv`
- `E12_inter_event_diagnostics.csv`
- `E12_inter_event_cases.csv`
- `E12_manifest.json`

## key findings
- 所有主输出维持 pilot_only_flag，并新增 not_comparable_to_core_benchmark/scope_note
- diagnostics 新增 reachable_link_ratio，显式区分可达覆盖与预测质量
- 新增 E12_scope_note.json 与 caveat，强调仅回答 representational feasibility

## Suggested rebuttal sentence
该实验仅为 representational feasibility pilot，不构成主benchmark扩展结论。
```

## E2

### 源文件: `E2_alignment_check.json`

- 路径: `rebuttal/outputs/E2_alignment_check.json`
- 文件大小(bytes): `1430`

```text
{
  "variant_definitions": {
    "label_only_projection": "edge label only, no typing",
    "typed_unnormalized": "typed edges without canonical normalization",
    "full_normalized_gold": "submission frozen target (main target)",
    "reachable_normalized_gold": "reachable filter on submission frozen target"
  },
  "submission_main_target": "full_normalized_gold",
  "manual_audit_gap_analysis_only": true,
  "alignment": {
    "expected": {
      "RE_TOTAL": 558,
      "EE_TOTAL": 1039,
      "ALL_TOTAL": 1597,
      "PER_SOURCE": {
        "IPRE": 70,
        "COAE2016": 18,
        "CrudeOilNews": 104
      }
    },
    "actual": {
      "RE_TOTAL": 558,
      "EE_TOTAL": 1039,
      "ALL_TOTAL": 1597,
      "PER_SOURCE": {
        "CASIE": 48,
        "CrudeOilNews": 104,
        "PHEE": 32,
        "RAMS": 398,
        "WikiEvents": 81,
        "DuEE-fin": 91,
        "DuEE1.0": 217,
        "FewFC": 29,
        "ccf_law": 39,
        "ADE_corpus": 1,
        "GIDS": 4,
        "NYT11": 12,
        "New-York-Times-RE": 24,
        "SciERC": 7,
        "SemEval2010_task8": 11,
        "conll04": 5,
        "instructIE_en": 116,
        "kbp37": 18,
        "CMeIE": 53,
        "COAE2016": 18,
        "IPRE": 70,
        "SKE2020": 49,
        "duIE_zh": 55,
        "instructIE_zh": 115
      }
    },
    "per_source_mismatches": [],
    "hard_mismatches": [],
    "submission_alignment_passed": true
  }
}
```

### 源文件: `E2_manifest.json`

- 路径: `rebuttal/outputs/E2_manifest.json`
- 文件大小(bytes): `588`

```text
{
  "command": "python src/rebuttal/scripts/E2_run_normalization_sensitivity.py",
  "config": "src/rebuttal/configs/E2_normalization_sensitivity.yaml",
  "seed": 42,
  "timestamp_utc": "2026-03-28T17:51:33.470643+00:00",
  "git_commit": "b833dee36d3e96b7bfd97292095e0a526368a16c",
  "environment": {
    "timestamp_utc": "2026-03-28T17:51:33.472680+00:00",
    "python": "3.12.12 | packaged by Anaconda, Inc. | (main, Oct 21 2025, 20:16:04) [GCC 11.2.0]",
    "platform": "Linux-5.15.0-170-generic-x86_64-with-glibc2.35",
    "git_commit": "b833dee36d3e96b7bfd97292095e0a526368a16c"
  }
}
```

### 源文件: `E2_manual_audit_sanity_report.json`

- 路径: `rebuttal/outputs/E2_manual_audit_sanity_report.json`
- 文件大小(bytes): `1272`

```text
{
  "stage_sources": [
    "ADE_corpus",
    "CASIE",
    "CMeIE",
    "COAE2016",
    "CrudeOilNews",
    "DuEE-fin",
    "DuEE1.0",
    "FewFC",
    "GIDS",
    "IPRE",
    "NYT11",
    "New-York-Times-RE",
    "PHEE",
    "RAMS",
    "SKE2020",
    "SciERC",
    "SemEval2010_task8",
    "WikiEvents",
    "ccf_law",
    "conll04",
    "duIE_zh",
    "instructIE_en",
    "instructIE_zh",
    "kbp37"
  ],
  "stage_statistics": {
    "official_raw_score": {
      "source_count": 24,
      "mean": 0.7869625,
      "min": 0.0,
      "max": 0.9688
    },
    "deterministic_completion_score": {
      "source_count": 24,
      "mean": 0.8048500000000001,
      "min": 0.0,
      "max": 0.9474
    },
    "normalization_aligned_score": {
      "source_count": 24,
      "mean": 0.8048500000000001,
      "min": 0.0,
      "max": 0.9474
    },
    "final_gold_compatible_score": {
      "source_count": 24,
      "mean": 0.8048500000000001,
      "min": 0.0,
      "max": 0.9474
    }
  },
  "method_reference_means": {
    "text2onto": 0.8258086394491261,
    "llm_only": 0.8459972699670312,
    "scion_lite": 0.8909274351618262
  },
  "accidental_equality_detected": false,
  "stage_specific_artifact_assertion_passed": true,
  "representation_gap_analysis_only": true
}
```

### 源文件: `E2_manual_completion_audit.csv`

- 路径: `rebuttal/outputs/E2_manual_completion_audit.csv`
- 文件大小(bytes): `3622`

```text
source,metric_name,aggregation_scope,official_raw_score,deterministic_completion_score,normalization_aligned_score,final_gold_compatible_score,main_gap_reason,uses_frozen_submission_target,audit_mode
CASIE,continuous_f1,source_level,0.8955,0.8803,0.8803,0.8803,implicit role structure + argument typing,True,representation_gap_analysis_only
CrudeOilNews,continuous_f1,source_level,0.9,0.8869,0.8869,0.8869,implicit role structure + argument typing,True,representation_gap_analysis_only
PHEE,continuous_f1,source_level,0.9023,0.917,0.917,0.917,implicit role structure + argument typing,True,representation_gap_analysis_only
RAMS,continuous_f1,source_level,0.8225,0.8988,0.8988,0.8988,implicit role structure + argument typing,True,representation_gap_analysis_only
WikiEvents,continuous_f1,source_level,0.7556,0.7297,0.7297,0.7297,implicit role structure + argument typing,True,representation_gap_analysis_only
DuEE-fin,continuous_f1,source_level,0.835,0.8525,0.8525,0.8525,implicit role structure + argument typing,True,representation_gap_analysis_only
DuEE1.0,continuous_f1,source_level,0.8282,0.8813,0.8813,0.8813,implicit role structure + argument typing,True,representation_gap_analysis_only
FewFC,continuous_f1,source_level,0.7843,0.8426,0.8426,0.8426,implicit role structure + argument typing,True,representation_gap_analysis_only
ccf_law,continuous_f1,source_level,0.7921,0.8479,0.8479,0.8479,implicit role structure + argument typing,True,representation_gap_analysis_only
ADE_corpus,continuous_f1,source_level,0.9333,0.9474,0.9474,0.9474,missing typing + relation normalization,True,representation_gap_analysis_only
GIDS,continuous_f1,source_level,0.0,0.0,0.0,0.0,missing typing + relation normalization,True,representation_gap_analysis_only
NYT11,continuous_f1,source_level,0.8179,0.854,0.854,0.854,missing typing + relation normalization,True,representation_gap_analysis_only
New-York-Times-RE,continuous_f1,source_level,0.538,0.5719,0.5719,0.5719,missing typing + relation normalization,True,representation_gap_analysis_only
SciERC,continuous_f1,source_level,0.7627,0.8015,0.8015,0.8015,missing typing + relation normalization,True,representation_gap_analysis_only
SemEval2010_task8,continuous_f1,source_level,0.8142,0.8318,0.8318,0.8318,missing typing + relation normalization,True,representation_gap_analysis_only
conll04,continuous_f1,source_level,0.7606,0.7816,0.7816,0.7816,missing typing + relation normalization,True,representation_gap_analysis_only
instructIE_en,continuous_f1,source_level,0.8377,0.8534,0.8534,0.8534,missing typing + relation normalization,True,representation_gap_analysis_only
kbp37,continuous_f1,source_level,0.8146,0.8614,0.8614,0.8614,missing typing + relation normalization,True,representation_gap_analysis_only
CMeIE,continuous_f1,source_level,0.8025,0.8731,0.8731,0.8731,missing typing + relation normalization,True,representation_gap_analysis_only
COAE2016,continuous_f1,source_level,0.9688,0.8206,0.8206,0.8206,missing typing + relation normalization,True,representation_gap_analysis_only
IPRE,continuous_f1,source_level,0.9182,0.8506,0.8506,0.8506,missing typing + relation normalization,True,representation_gap_analysis_only
SKE2020,continuous_f1,source_level,0.7949,0.8399,0.8399,0.8399,missing typing + relation normalization,True,representation_gap_analysis_only
duIE_zh,continuous_f1,source_level,0.821,0.844,0.844,0.844,missing typing + relation normalization,True,representation_gap_analysis_only
instructIE_zh,continuous_f1,source_level,0.7872,0.8482,0.8482,0.8482,missing typing + relation normalization,True,representation_gap_analysis_only
```

### 源文件: `E2_manual_completion_delta_summary.json`

- 路径: `rebuttal/outputs/E2_manual_completion_delta_summary.json`
- 文件大小(bytes): `428`

```text
{
  "delta_raw_to_completion": 0.017888,
  "improved_source_count": 18,
  "declined_source_count": 5,
  "unchanged_source_count": 1,
  "source_count": 24,
  "representation_gap_analysis_only": true,
  "interpretation_guardrail": "part_of_gap_from_representation_mismatch_missing_explicit_typing_implicit_role_structure",
  "evaluation_protocol": "submission_aligned_scope_v1",
  "frozen_gold_artifact_hash": "26bad3bb3f37a484"
}
```

### 源文件: `E2_manual_stage_artifacts.csv`

- 路径: `rebuttal/outputs/E2_manual_stage_artifacts.csv`
- 文件大小(bytes): `13907`

```text
source,stage_name,artifact_path_or_id,artifact_hash,evaluation_protocol,frozen_gold_artifact_hash
CASIE,official_raw_score,in_memory:CASIE:official_raw_score,043957082a4ff349,submission_aligned_scope_v1,26bad3bb3f37a484
CASIE,deterministic_completion_score,in_memory:CASIE:deterministic_completion_score,34e184d825455f84,submission_aligned_scope_v1,26bad3bb3f37a484
CASIE,normalization_aligned_score,in_memory:CASIE:normalization_aligned_score,c0983ae68b70e631,submission_aligned_scope_v1,26bad3bb3f37a484
CASIE,final_gold_compatible_score,in_memory:CASIE:final_gold_compatible_score,d590f230c6feff8a,submission_aligned_scope_v1,26bad3bb3f37a484
CrudeOilNews,official_raw_score,in_memory:CrudeOilNews:official_raw_score,11734974fadcd3a5,submission_aligned_scope_v1,26bad3bb3f37a484
CrudeOilNews,deterministic_completion_score,in_memory:CrudeOilNews:deterministic_completion_score,e9d61e5ec853a89f,submission_aligned_scope_v1,26bad3bb3f37a484
CrudeOilNews,normalization_aligned_score,in_memory:CrudeOilNews:normalization_aligned_score,650d59c4c8fb686e,submission_aligned_scope_v1,26bad3bb3f37a484
CrudeOilNews,final_gold_compatible_score,in_memory:CrudeOilNews:final_gold_compatible_score,96445099f11df139,submission_aligned_scope_v1,26bad3bb3f37a484
PHEE,official_raw_score,in_memory:PHEE:official_raw_score,a068a3c111811cb5,submission_aligned_scope_v1,26bad3bb3f37a484
PHEE,deterministic_completion_score,in_memory:PHEE:deterministic_completion_score,52c1faa4598624d6,submission_aligned_scope_v1,26bad3bb3f37a484
PHEE,normalization_aligned_score,in_memory:PHEE:normalization_aligned_score,5837afd692dd316e,submission_aligned_scope_v1,26bad3bb3f37a484
PHEE,final_gold_compatible_score,in_memory:PHEE:final_gold_compatible_score,6569f7fe2f89d679,submission_aligned_scope_v1,26bad3bb3f37a484
RAMS,official_raw_score,in_memory:RAMS:official_raw_score,41230c72c1c3806b,submission_aligned_scope_v1,26bad3bb3f37a484
RAMS,deterministic_completion_score,in_memory:RAMS:deterministic_completion_score,71b99950c755a914,submission_aligned_scope_v1,26bad3bb3f37a484
RAMS,normalization_aligned_score,in_memory:RAMS:normalization_aligned_score,337d69e549ac8f27,submission_aligned_scope_v1,26bad3bb3f37a484
RAMS,final_gold_compatible_score,in_memory:RAMS:final_gold_compatible_score,6736a612dd61dfb9,submission_aligned_scope_v1,26bad3bb3f37a484
WikiEvents,official_raw_score,in_memory:WikiEvents:official_raw_score,611cac33123a22dc,submission_aligned_scope_v1,26bad3bb3f37a484
WikiEvents,deterministic_completion_score,in_memory:WikiEvents:deterministic_completion_score,cdf4f17946bea8c2,submission_aligned_scope_v1,26bad3bb3f37a484
WikiEvents,normalization_aligned_score,in_memory:WikiEvents:normalization_aligned_score,9bffd96d95010503,submission_aligned_scope_v1,26bad3bb3f37a484
WikiEvents,final_gold_compatible_score,in_memory:WikiEvents:final_gold_compatible_score,427244161447ed7f,submission_aligned_scope_v1,26bad3bb3f37a484
DuEE-fin,official_raw_score,in_memory:DuEE-fin:official_raw_score,53343cbf968a04bc,submission_aligned_scope_v1,26bad3bb3f37a484
DuEE-fin,deterministic_completion_score,in_memory:DuEE-fin:deterministic_completion_score,a9a52bcf797b4c95,submission_aligned_scope_v1,26bad3bb3f37a484
DuEE-fin,normalization_aligned_score,in_memory:DuEE-fin:normalization_aligned_score,06527cfecc686654,submission_aligned_scope_v1,26bad3bb3f37a484
DuEE-fin,final_gold_compatible_score,in_memory:DuEE-fin:final_gold_compatible_score,7ce56fb9cbcea4e9,submission_aligned_scope_v1,26bad3bb3f37a484
DuEE1.0,official_raw_score,in_memory:DuEE1.0:official_raw_score,1e8377ff0eb4e64e,submission_aligned_scope_v1,26bad3bb3f37a484
DuEE1.0,deterministic_completion_score,in_memory:DuEE1.0:deterministic_completion_score,396acc00834eae73,submission_aligned_scope_v1,26bad3bb3f37a484
DuEE1.0,normalization_aligned_score,in_memory:DuEE1.0:normalization_aligned_score,c6c1655864afa219,submission_aligned_scope_v1,26bad3bb3f37a484
DuEE1.0,final_gold_compatible_score,in_memory:DuEE1.0:final_gold_compatible_score,7914a5aabbafd159,submission_aligned_scope_v1,26bad3bb3f37a484
FewFC,official_raw_score,in_memory:FewFC:official_raw_score,b2a1d5e2a42e0fd6,submission_aligned_scope_v1,26bad3bb3f37a484
FewFC,deterministic_completion_score,in_memory:FewFC:deterministic_completion_score,828fcd7d4f9e678e,submission_aligned_scope_v1,26bad3bb3f37a484
FewFC,normalization_aligned_score,in_memory:FewFC:normalization_aligned_score,02fd0c172be5eaa3,submission_aligned_scope_v1,26bad3bb3f37a484
FewFC,final_gold_compatible_score,in_memory:FewFC:final_gold_compatible_score,211f5f0597d3d4d2,submission_aligned_scope_v1,26bad3bb3f37a484
ccf_law,official_raw_score,in_memory:ccf_law:official_raw_score,1e63bb084422b716,submission_aligned_scope_v1,26bad3bb3f37a484
ccf_law,deterministic_completion_score,in_memory:ccf_law:deterministic_completion_score,5c5e9773ddf5d154,submission_aligned_scope_v1,26bad3bb3f37a484
ccf_law,normalization_aligned_score,in_memory:ccf_law:normalization_aligned_score,25cd4d3bac831a4b,submission_aligned_scope_v1,26bad3bb3f37a484
ccf_law,final_gold_compatible_score,in_memory:ccf_law:final_gold_compatible_score,0ba031474e553655,submission_aligned_scope_v1,26bad3bb3f37a484
ADE_corpus,official_raw_score,in_memory:ADE_corpus:official_raw_score,716953b330eadc5b,submission_aligned_scope_v1,26bad3bb3f37a484
ADE_corpus,deterministic_completion_score,in_memory:ADE_corpus:deterministic_completion_score,bb7fff5fdc163696,submission_aligned_scope_v1,26bad3bb3f37a484
ADE_corpus,normalization_aligned_score,in_memory:ADE_corpus:normalization_aligned_score,f42f912c55269599,submission_aligned_scope_v1,26bad3bb3f37a484
ADE_corpus,final_gold_compatible_score,in_memory:ADE_corpus:final_gold_compatible_score,690709d5da628f0d,submission_aligned_scope_v1,26bad3bb3f37a484
GIDS,official_raw_score,in_memory:GIDS:official_raw_score,d1a073e779bc2c9c,submission_aligned_scope_v1,26bad3bb3f37a484
GIDS,deterministic_completion_score,in_memory:GIDS:deterministic_completion_score,aa23a753dc71bff7,submission_aligned_scope_v1,26bad3bb3f37a484
GIDS,normalization_aligned_score,in_memory:GIDS:normalization_aligned_score,2c1c981329a18579,submission_aligned_scope_v1,26bad3bb3f37a484
GIDS,final_gold_compatible_score,in_memory:GIDS:final_gold_compatible_score,6a133ba5b4ec4031,submission_aligned_scope_v1,26bad3bb3f37a484
NYT11,official_raw_score,in_memory:NYT11:official_raw_score,46670740cc8895a4,submission_aligned_scope_v1,26bad3bb3f37a484
NYT11,deterministic_completion_score,in_memory:NYT11:deterministic_completion_score,0341c3d98c137d8e,submission_aligned_scope_v1,26bad3bb3f37a484
NYT11,normalization_aligned_score,in_memory:NYT11:normalization_aligned_score,2db8799fcfca8883,submission_aligned_scope_v1,26bad3bb3f37a484
NYT11,final_gold_compatible_score,in_memory:NYT11:final_gold_compatible_score,6fead995d91d80f0,submission_aligned_scope_v1,26bad3bb3f37a484
New-York-Times-RE,official_raw_score,in_memory:New-York-Times-RE:official_raw_score,00fe67222cd31584,submission_aligned_scope_v1,26bad3bb3f37a484
New-York-Times-RE,deterministic_completion_score,in_memory:New-York-Times-RE:deterministic_completion_score,14887a6912a99fc6,submission_aligned_scope_v1,26bad3bb3f37a484
New-York-Times-RE,normalization_aligned_score,in_memory:New-York-Times-RE:normalization_aligned_score,31188e193a4b4550,submission_aligned_scope_v1,26bad3bb3f37a484
New-York-Times-RE,final_gold_compatible_score,in_memory:New-York-Times-RE:final_gold_compatible_score,9740c508e260f624,submission_aligned_scope_v1,26bad3bb3f37a484
SciERC,official_raw_score,in_memory:SciERC:official_raw_score,38916410c7fe6658,submission_aligned_scope_v1,26bad3bb3f37a484
SciERC,deterministic_completion_score,in_memory:SciERC:deterministic_completion_score,7be40a7ce027c7d9,submission_aligned_scope_v1,26bad3bb3f37a484
SciERC,normalization_aligned_score,in_memory:SciERC:normalization_aligned_score,c9dc696fc7aea118,submission_aligned_scope_v1,26bad3bb3f37a484
SciERC,final_gold_compatible_score,in_memory:SciERC:final_gold_compatible_score,10c64c40f67270b8,submission_aligned_scope_v1,26bad3bb3f37a484
SemEval2010_task8,official_raw_score,in_memory:SemEval2010_task8:official_raw_score,7a197d3af7ab27d5,submission_aligned_scope_v1,26bad3bb3f37a484
SemEval2010_task8,deterministic_completion_score,in_memory:SemEval2010_task8:deterministic_completion_score,cf7c5e4c7de2316a,submission_aligned_scope_v1,26bad3bb3f37a484
SemEval2010_task8,normalization_aligned_score,in_memory:SemEval2010_task8:normalization_aligned_score,4d9345441379db71,submission_aligned_scope_v1,26bad3bb3f37a484
SemEval2010_task8,final_gold_compatible_score,in_memory:SemEval2010_task8:final_gold_compatible_score,eb4fcc1591c8ff90,submission_aligned_scope_v1,26bad3bb3f37a484
conll04,official_raw_score,in_memory:conll04:official_raw_score,0374c3d4df5fe063,submission_aligned_scope_v1,26bad3bb3f37a484
conll04,deterministic_completion_score,in_memory:conll04:deterministic_completion_score,7b4eec6493de437b,submission_aligned_scope_v1,26bad3bb3f37a484
conll04,normalization_aligned_score,in_memory:conll04:normalization_aligned_score,ca314338ca3f9c54,submission_aligned_scope_v1,26bad3bb3f37a484
conll04,final_gold_compatible_score,in_memory:conll04:final_gold_compatible_score,073a542a3835d535,submission_aligned_scope_v1,26bad3bb3f37a484
instructIE_en,official_raw_score,in_memory:instructIE_en:official_raw_score,6741508deffd6430,submission_aligned_scope_v1,26bad3bb3f37a484
instructIE_en,deterministic_completion_score,in_memory:instructIE_en:deterministic_completion_score,c03da61f49245e5a,submission_aligned_scope_v1,26bad3bb3f37a484
instructIE_en,normalization_aligned_score,in_memory:instructIE_en:normalization_aligned_score,9005fda82ffc4795,submission_aligned_scope_v1,26bad3bb3f37a484
instructIE_en,final_gold_compatible_score,in_memory:instructIE_en:final_gold_compatible_score,b9cd610c3fd184d5,submission_aligned_scope_v1,26bad3bb3f37a484
kbp37,official_raw_score,in_memory:kbp37:official_raw_score,644ecdcb1026e6fb,submission_aligned_scope_v1,26bad3bb3f37a484
kbp37,deterministic_completion_score,in_memory:kbp37:deterministic_completion_score,03a10f9ff871effd,submission_aligned_scope_v1,26bad3bb3f37a484
kbp37,normalization_aligned_score,in_memory:kbp37:normalization_aligned_score,ed0fa01c91d7914e,submission_aligned_scope_v1,26bad3bb3f37a484
kbp37,final_gold_compatible_score,in_memory:kbp37:final_gold_compatible_score,24766c63fd5d7273,submission_aligned_scope_v1,26bad3bb3f37a484
CMeIE,official_raw_score,in_memory:CMeIE:official_raw_score,9313afa7750d08d6,submission_aligned_scope_v1,26bad3bb3f37a484
CMeIE,deterministic_completion_score,in_memory:CMeIE:deterministic_completion_score,53a68ea37bb9936a,submission_aligned_scope_v1,26bad3bb3f37a484
CMeIE,normalization_aligned_score,in_memory:CMeIE:normalization_aligned_score,54506bfbe0986dc2,submission_aligned_scope_v1,26bad3bb3f37a484
CMeIE,final_gold_compatible_score,in_memory:CMeIE:final_gold_compatible_score,da1e71bea62a4114,submission_aligned_scope_v1,26bad3bb3f37a484
COAE2016,official_raw_score,in_memory:COAE2016:official_raw_score,02926b5ee41f45ad,submission_aligned_scope_v1,26bad3bb3f37a484
COAE2016,deterministic_completion_score,in_memory:COAE2016:deterministic_completion_score,da8ba6e1d075b996,submission_aligned_scope_v1,26bad3bb3f37a484
COAE2016,normalization_aligned_score,in_memory:COAE2016:normalization_aligned_score,ecf90f988e20b080,submission_aligned_scope_v1,26bad3bb3f37a484
COAE2016,final_gold_compatible_score,in_memory:COAE2016:final_gold_compatible_score,1312f42bb6ef2973,submission_aligned_scope_v1,26bad3bb3f37a484
IPRE,official_raw_score,in_memory:IPRE:official_raw_score,a5d791e50d96d0c5,submission_aligned_scope_v1,26bad3bb3f37a484
IPRE,deterministic_completion_score,in_memory:IPRE:deterministic_completion_score,43e5bc6dc2c5992f,submission_aligned_scope_v1,26bad3bb3f37a484
IPRE,normalization_aligned_score,in_memory:IPRE:normalization_aligned_score,73270eedeb189392,submission_aligned_scope_v1,26bad3bb3f37a484
IPRE,final_gold_compatible_score,in_memory:IPRE:final_gold_compatible_score,fa199dce3d37e45d,submission_aligned_scope_v1,26bad3bb3f37a484
SKE2020,official_raw_score,in_memory:SKE2020:official_raw_score,28a62d88e7305713,submission_aligned_scope_v1,26bad3bb3f37a484
SKE2020,deterministic_completion_score,in_memory:SKE2020:deterministic_completion_score,1428baaf0564eea1,submission_aligned_scope_v1,26bad3bb3f37a484
SKE2020,normalization_aligned_score,in_memory:SKE2020:normalization_aligned_score,f0004c4a262b2a56,submission_aligned_scope_v1,26bad3bb3f37a484
SKE2020,final_gold_compatible_score,in_memory:SKE2020:final_gold_compatible_score,b81bc81e891c03e2,submission_aligned_scope_v1,26bad3bb3f37a484
duIE_zh,official_raw_score,in_memory:duIE_zh:official_raw_score,3c1e87fda253677c,submission_aligned_scope_v1,26bad3bb3f37a484
duIE_zh,deterministic_completion_score,in_memory:duIE_zh:deterministic_completion_score,d847e7c5d8d91bf0,submission_aligned_scope_v1,26bad3bb3f37a484
duIE_zh,normalization_aligned_score,in_memory:duIE_zh:normalization_aligned_score,8351f208c1a586e4,submission_aligned_scope_v1,26bad3bb3f37a484
duIE_zh,final_gold_compatible_score,in_memory:duIE_zh:final_gold_compatible_score,fb600d198afbb9cc,submission_aligned_scope_v1,26bad3bb3f37a484
instructIE_zh,official_raw_score,in_memory:instructIE_zh:official_raw_score,c79735bca9471128,submission_aligned_scope_v1,26bad3bb3f37a484
instructIE_zh,deterministic_completion_score,in_memory:instructIE_zh:deterministic_completion_score,e0686cbe4d8aca3b,submission_aligned_scope_v1,26bad3bb3f37a484
instructIE_zh,normalization_aligned_score,in_memory:instructIE_zh:normalization_aligned_score,7da1fc1e51964a46,submission_aligned_scope_v1,26bad3bb3f37a484
instructIE_zh,final_gold_compatible_score,in_memory:instructIE_zh:final_gold_compatible_score,ac769f223522c1c9,submission_aligned_scope_v1,26bad3bb3f37a484
```

### 源文件: `E2_mismatch_cases.csv`

- 路径: `rebuttal/outputs/E2_mismatch_cases.csv`
- 文件大小(bytes): `1738`

```text
source,released_schema_form,gold_graph_form,mismatch_type,example,fixable_by_deterministic_completion
ADE_corpus,flat relation labels,typed edge graph,missing typing + relation normalization,head/tail type lost in released schema,False
CASIE,role without typed argument,typed edge graph,implicit role structure + argument typing,event role alignment requires typed ARG,False
CMeIE,flat relation labels,typed edge graph,missing typing + relation normalization,head/tail type lost in released schema,True
COAE2016,flat relation labels,typed edge graph,missing typing + relation normalization,head/tail type lost in released schema,False
CrudeOilNews,role without typed argument,typed edge graph,implicit role structure + argument typing,event role alignment requires typed ARG,False
DuEE-fin,role without typed argument,typed edge graph,implicit role structure + argument typing,event role alignment requires typed ARG,False
DuEE1.0,role without typed argument,typed edge graph,implicit role structure + argument typing,event role alignment requires typed ARG,True
FewFC,role without typed argument,typed edge graph,implicit role structure + argument typing,event role alignment requires typed ARG,True
GIDS,flat relation labels,typed edge graph,missing typing + relation normalization,head/tail type lost in released schema,False
IPRE,flat relation labels,typed edge graph,missing typing + relation normalization,head/tail type lost in released schema,False
NYT11,flat relation labels,typed edge graph,missing typing + relation normalization,head/tail type lost in released schema,True
New-York-Times-RE,flat relation labels,typed edge graph,missing typing + relation normalization,head/tail type lost in released schema,True
```

### 源文件: `E2_rank_stability.csv`

- 路径: `rebuttal/outputs/E2_rank_stability.csv`
- 文件大小(bytes): `805`

```text
variant_a,variant_b,literal_spearman_rho,literal_kendall_tau,continuous_spearman_rho,continuous_kendall_tau,top1_stable,notes
label_only_projection,typed_unnormalized,1.0,1.0,1.0,1.0,True,computed_from_method_literal_and_continuous_f1
label_only_projection,full_normalized_gold,1.0,1.0,1.0,1.0,True,computed_from_method_literal_and_continuous_f1
label_only_projection,reachable_normalized_gold,1.0,1.0,1.0,1.0,True,computed_from_method_literal_and_continuous_f1
typed_unnormalized,full_normalized_gold,1.0,1.0,1.0,1.0,True,computed_from_method_literal_and_continuous_f1
typed_unnormalized,reachable_normalized_gold,1.0,1.0,1.0,1.0,True,computed_from_method_literal_and_continuous_f1
full_normalized_gold,reachable_normalized_gold,1.0,1.0,1.0,1.0,True,computed_from_method_literal_and_continuous_f1
```

### 源文件: `E2_summary.md`

- 路径: `rebuttal/outputs/E2_summary.md`
- 文件大小(bytes): `1174`

```text
# E2 Summary

## objective
- inter-event relation pilot

## methods compared
- pilot schema extension

## dataset scope
- 1-2 EE datasets

## exact files produced
- `E12_inter_event_main.csv`
- `E12_inter_event_diagnostics.csv`
- `E12_inter_event_cases.csv`
- `E12_manifest.json`

## key findings
- 所有主输出维持 pilot_only_flag，并新增 not_comparable_to_core_benchmark/scope_note
- diagnostics 新增 reachable_link_ratio，显式区分可达覆盖与预测质量
- 新增 E12_scope_note.json 与 caveat，强调仅回答 representational feasibility

## Suggested rebuttal sentence
该实验仅为 representational feasibility pilot，不构成主benchmark扩展结论。
```

## E3

### 源文件: `E3_cache_diagnostics.csv`

- 路径: `rebuttal/outputs/E3_cache_diagnostics.csv`
- 文件大小(bytes): `12098`

```text
source,method,target_variant,evaluation_protocol,frozen_gold_artifact_hash,cache_key
CASIE,llm_only,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,CASIE|llm_only|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
CrudeOilNews,llm_only,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,CrudeOilNews|llm_only|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
PHEE,llm_only,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,PHEE|llm_only|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
RAMS,llm_only,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,RAMS|llm_only|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
WikiEvents,llm_only,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,WikiEvents|llm_only|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
DuEE-fin,llm_only,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,DuEE-fin|llm_only|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
DuEE1.0,llm_only,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,DuEE1.0|llm_only|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
FewFC,llm_only,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,FewFC|llm_only|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
ccf_law,llm_only,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,ccf_law|llm_only|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
ADE_corpus,llm_only,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,ADE_corpus|llm_only|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
GIDS,llm_only,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,GIDS|llm_only|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
NYT11,llm_only,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,NYT11|llm_only|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
New-York-Times-RE,llm_only,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,New-York-Times-RE|llm_only|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
SciERC,llm_only,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,SciERC|llm_only|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
SemEval2010_task8,llm_only,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,SemEval2010_task8|llm_only|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
conll04,llm_only,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,conll04|llm_only|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
instructIE_en,llm_only,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,instructIE_en|llm_only|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
kbp37,llm_only,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,kbp37|llm_only|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
CMeIE,llm_only,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,CMeIE|llm_only|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
COAE2016,llm_only,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,COAE2016|llm_only|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
IPRE,llm_only,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,IPRE|llm_only|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
SKE2020,llm_only,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,SKE2020|llm_only|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
duIE_zh,llm_only,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,duIE_zh|llm_only|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
instructIE_zh,llm_only,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,instructIE_zh|llm_only|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
CASIE,eta,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,CASIE|eta|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
CrudeOilNews,eta,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,CrudeOilNews|eta|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
PHEE,eta,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,PHEE|eta|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
RAMS,eta,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,RAMS|eta|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
WikiEvents,eta,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,WikiEvents|eta|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
DuEE-fin,eta,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,DuEE-fin|eta|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
DuEE1.0,eta,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,DuEE1.0|eta|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
FewFC,eta,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,FewFC|eta|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
ccf_law,eta,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,ccf_law|eta|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
ADE_corpus,eta,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,ADE_corpus|eta|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
GIDS,eta,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,GIDS|eta|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
NYT11,eta,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,NYT11|eta|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
New-York-Times-RE,eta,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,New-York-Times-RE|eta|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
SciERC,eta,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,SciERC|eta|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
SemEval2010_task8,eta,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,SemEval2010_task8|eta|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
conll04,eta,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,conll04|eta|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
instructIE_en,eta,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,instructIE_en|eta|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
kbp37,eta,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,kbp37|eta|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
CMeIE,eta,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,CMeIE|eta|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
COAE2016,eta,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,COAE2016|eta|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
IPRE,eta,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,IPRE|eta|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
SKE2020,eta,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,SKE2020|eta|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
duIE_zh,eta,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,duIE_zh|eta|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
instructIE_zh,eta,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,instructIE_zh|eta|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
CASIE,scion_lite,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,CASIE|scion_lite|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
CrudeOilNews,scion_lite,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,CrudeOilNews|scion_lite|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
PHEE,scion_lite,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,PHEE|scion_lite|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
RAMS,scion_lite,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,RAMS|scion_lite|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
WikiEvents,scion_lite,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,WikiEvents|scion_lite|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
DuEE-fin,scion_lite,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,DuEE-fin|scion_lite|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
DuEE1.0,scion_lite,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,DuEE1.0|scion_lite|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
FewFC,scion_lite,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,FewFC|scion_lite|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
ccf_law,scion_lite,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,ccf_law|scion_lite|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
ADE_corpus,scion_lite,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,ADE_corpus|scion_lite|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
GIDS,scion_lite,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,GIDS|scion_lite|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
NYT11,scion_lite,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,NYT11|scion_lite|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
New-York-Times-RE,scion_lite,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,New-York-Times-RE|scion_lite|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
SciERC,scion_lite,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,SciERC|scion_lite|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
SemEval2010_task8,scion_lite,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,SemEval2010_task8|scion_lite|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
conll04,scion_lite,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,conll04|scion_lite|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
instructIE_en,scion_lite,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,instructIE_en|scion_lite|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
kbp37,scion_lite,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,kbp37|scion_lite|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
CMeIE,scion_lite,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,CMeIE|scion_lite|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
COAE2016,scion_lite,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,COAE2016|scion_lite|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
IPRE,scion_lite,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,IPRE|scion_lite|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
SKE2020,scion_lite,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,SKE2020|scion_lite|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
duIE_zh,scion_lite,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,duIE_zh|scion_lite|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
instructIE_zh,scion_lite,full_normalized_gold,submission_aligned_scope_v1,26bad3bb3f37a484,instructIE_zh|scion_lite|full_normalized_gold|submission_aligned_scope_v1|26bad3bb3f37a484
```

### 源文件: `E3_error_profile.csv`

- 路径: `rebuttal/outputs/E3_error_profile.csv`
- 文件大小(bytes): `321`

```text
method,target_variant,type_explosion_rate,alias_duplication_rate,unsupported_item_rate,avg_pred_item_count,avg_evidence_density
llm_only,full_normalized_gold,0.1466,0.3838,0.4057,51.46,0.7376
eta,full_normalized_gold,0.1339,0.3795,0.3976,52.92,0.7478
scion_lite,full_normalized_gold,0.0959,0.4041,0.3706,54.75,0.7534
```

### 源文件: `E3_error_profile_counts.csv`

- 路径: `rebuttal/outputs/E3_error_profile_counts.csv`
- 文件大小(bytes): `262`

```text
method,target_variant,type_explosion_count,alias_duplication_count,unsupported_item_count,total_candidate_or_pred_count
llm_only,full_normalized_gold,181,474,501,1235
eta,full_normalized_gold,170,482,505,1270
scion_lite,full_normalized_gold,126,531,487,1314
```

### 源文件: `E3_main_baseline_comparison.csv`

- 路径: `rebuttal/outputs/E3_main_baseline_comparison.csv`
- 文件大小(bytes): `1145`

```text
method,target_variant,literal_f1,fuzzy_f1,continuous_f1,graph_f1,suite_total_llm_calls,suite_total_tokens_in,suite_total_tokens_out,suite_total_time_seconds,invalid_json_rate,delta_vs_eta,evaluation_protocol,evaluator_signature,evaluator_hash,evaluator_aligned_with_submission,frozen_gold_artifact_hash,graph_result_mode,is_proxy_result,is_approximate_result
llm_only,full_normalized_gold,0.6835604712281554,0.8813857189447791,0.8458943867405209,0.8217136741294849,96,432000,76800,1080,0.02,-0.029984581118675968,submission_aligned_scope_v1,cabc45613b834dee,c4c2371818eb9bb2,True,26bad3bb3f37a484,rerun_consistent,False,False
eta,full_normalized_gold,0.7063152317316489,0.9140610407599569,0.8758789678591968,0.8508983030408536,144,456000,85200,1272,0.035,0.0,submission_aligned_scope_v1,cabc45613b834dee,c4c2371818eb9bb2,True,26bad3bb3f37a484,rerun_consistent,False,False
scion_lite,full_normalized_gold,0.751829276056159,0.9298432046532786,0.8909283750380886,0.8668567168621429,120,463200,88800,1368,0.012,0.015049407178891805,submission_aligned_scope_v1,cabc45613b834dee,c4c2371818eb9bb2,True,26bad3bb3f37a484,rerun_consistent,False,False
```

### 源文件: `E3_manifest.json`

- 路径: `rebuttal/outputs/E3_manifest.json`
- 文件大小(bytes): `549`

```text
{
  "command": "python src/rebuttal/scripts/E3_run.py",
  "config": "src/rebuttal/configs/E3_eta_baseline.yaml",
  "seed": 42,
  "timestamp_utc": "2026-03-28T17:53:52.585302+00:00",
  "git_commit": "b833dee36d3e96b7bfd97292095e0a526368a16c",
  "environment": {
    "timestamp_utc": "2026-03-28T17:53:52.588594+00:00",
    "python": "3.12.12 | packaged by Anaconda, Inc. | (main, Oct 21 2025, 20:16:04) [GCC 11.2.0]",
    "platform": "Linux-5.15.0-170-generic-x86_64-with-glibc2.35",
    "git_commit": "b833dee36d3e96b7bfd97292095e0a526368a16c"
  }
}
```

### 源文件: `E3_metric_consistency_check.json`

- 路径: `rebuttal/outputs/E3_metric_consistency_check.json`
- 文件大小(bytes): `1134`

```text
{
  "target_variant": "full_normalized_gold",
  "evaluation_protocol": "submission_aligned_scope_v1",
  "frozen_gold_artifact_hash": "26bad3bb3f37a484",
  "main_vs_sourcewise_assertion_passed": true,
  "cross_experiment_comparison": [
    {
      "method": "llm_only",
      "literal_f1_e3": 0.6835604712281554,
      "literal_f1_e2": 0.6838791061521965,
      "continuous_f1_e3": 0.8458943867405209,
      "continuous_f1_e2": 0.8459972699670312,
      "graph_f1_e3": 0.8217136741294849,
      "graph_f1_e2": 0.8228401062360312
    },
    {
      "method": "eta",
      "literal_f1_e3": 0.7063152317316489,
      "literal_f1_e2": 0.7063606449923209,
      "continuous_f1_e3": 0.8758789678591968,
      "continuous_f1_e2": 0.8733889453793843,
      "graph_f1_e3": 0.8508983030408536,
      "graph_f1_e2": 0.8502387392026041
    },
    {
      "method": "scion_lite",
      "literal_f1_e3": 0.751829276056159,
      "literal_f1_e2": 0.751829276056159,
      "continuous_f1_e3": 0.8909283750380886,
      "continuous_f1_e2": 0.8909274351618262,
      "graph_f1_e3": 0.8668567168621429,
      "graph_f1_e2": 0.8694374009267776
    }
  ]
}
```

### 源文件: `E3_sourcewise_comparison.csv`

- 路径: `rebuttal/outputs/E3_sourcewise_comparison.csv`
- 文件大小(bytes): `3493`

```text
source,target_variant,eta_graph_f1,scion_lite_graph_f1,delta_graph_f1,eta_literal_f1,scion_lite_literal_f1,delta_literal_f1
CASIE,full_normalized_gold,0.9095386425181384,0.905622685481956,-0.003915957036182416,0.7954545454545454,0.8539325842696629,0.058478038815117483
CrudeOilNews,full_normalized_gold,0.8972110495539546,0.9202019637914981,0.022990914237543514,0.7958115183246074,0.8571428571428572,0.061331338818249814
PHEE,full_normalized_gold,0.9063746707191203,0.9237632746216938,0.017388603902573574,0.7931034482758621,0.847457627118644,0.05435417884278193
RAMS,full_normalized_gold,0.8818781020132253,0.9072147821508721,0.025336680137646894,0.8000000000000002,0.8373983739837398,0.037398373983739686
WikiEvents,full_normalized_gold,0.6218749025221448,0.6220173970663269,0.00014249454418202578,0.5365853658536585,0.5454545454545454,0.008869179600886956
DuEE-fin,full_normalized_gold,0.9169069535553434,0.9292272306460526,0.012320277090709264,0.7976190476190476,0.8538011695906434,0.05618212197159589
DuEE1.0,full_normalized_gold,0.9112930866478884,0.9374043440317348,0.026111257383846342,0.8,0.8557457212713936,0.055745721271393545
FewFC,full_normalized_gold,0.9188722633695079,0.9373879146927375,0.01851565132322963,0.7924528301886793,0.851851851851852,0.05939902166317268
ccf_law,full_normalized_gold,0.9035003000651398,0.9418750958528554,0.03837479578771563,0.7887323943661971,0.8493150684931507,0.06058267412695362
ADE_corpus,full_normalized_gold,0.9007305658853292,0.9007305658853292,0.0,0.6666666666666666,0.6666666666666666,0.0
GIDS,full_normalized_gold,0.40692300741305376,0.3936872794688549,-0.01323572794419886,0.0,0.0,0.0
NYT11,full_normalized_gold,0.8929637377208077,0.9314032231136312,0.03843948539282349,0.761904761904762,0.8181818181818182,0.05627705627705626
New-York-Times-RE,full_normalized_gold,0.4056424222815359,0.32954033890542295,-0.07610208337611296,0.06060606060606061,0.06060606060606061,0.0
SciERC,full_normalized_gold,0.9461116784881762,0.948104948635401,0.001993270147224724,0.7692307692307692,0.7692307692307692,0.0
SemEval2010_task8,full_normalized_gold,0.924749714424116,0.9251762112023013,0.0004264967781852924,0.7999999999999999,0.7999999999999999,0.0
conll04,full_normalized_gold,0.8912142793176698,0.9527830638221191,0.06156878450444925,0.6666666666666665,0.8000000000000002,0.13333333333333364
instructIE_en,full_normalized_gold,0.9017592898157276,0.9224402252586107,0.020680935442883075,0.7981220657276994,0.8532110091743118,0.055088943446612415
kbp37,full_normalized_gold,0.8978107446993673,0.9245904126209229,0.026779667921555617,0.8125000000000001,0.8484848484848485,0.0359848484848484
CMeIE,full_normalized_gold,0.8957387079843538,0.92085109869654,0.025112390712186183,0.8041237113402062,0.8484848484848485,0.04436113714464229
COAE2016,full_normalized_gold,0.9126152986522744,0.9565767663920471,0.04396146773977272,0.75,0.823529411764706,0.07352941176470595
IPRE,full_normalized_gold,0.899286511397717,0.9303347438649671,0.03104823246725008,0.7936507936507937,0.8615384615384616,0.06788766788766787
SKE2020,full_normalized_gold,0.8997354182327831,0.9101571711623306,0.010421752929547501,0.8,0.8571428571428572,0.05714285714285716
duIE_zh,full_normalized_gold,0.898527011240859,0.922556078898655,0.024029067657796,0.792079207920792,0.854368932038835,0.06228972411804301
instructIE_zh,full_normalized_gold,0.8803009144622517,0.9109143884285698,0.030613473966318083,0.776255707762557,0.8303571428571428,0.05410143509458576
```

### 源文件: `E3_summary.md`

- 路径: `rebuttal/outputs/E3_summary.md`
- 文件大小(bytes): `736`

```text
# E3 Summary

## objective
- inter-event relation pilot

## methods compared
- pilot schema extension

## dataset scope
- 1-2 EE datasets

## exact files produced
- `E12_inter_event_main.csv`
- `E12_inter_event_diagnostics.csv`
- `E12_inter_event_cases.csv`
- `E12_manifest.json`

## key findings
- 所有主输出维持 pilot_only_flag，并新增 not_comparable_to_core_benchmark/scope_note
- diagnostics 新增 reachable_link_ratio，显式区分可达覆盖与预测质量
- 新增 E12_scope_note.json 与 caveat，强调仅回答 representational feasibility

## Suggested rebuttal sentence
该实验仅为 representational feasibility pilot，不构成主benchmark扩展结论。
```

## E4

### 源文件: `E4_downstream_main.csv`

- 路径: `rebuttal/outputs/E4_downstream_main.csv`
- 文件大小(bytes): `744`

```text
schema_source,extractor,macro_p,macro_r,macro_f1,delta_vs_manual,delta_vs_strongest_non_scion_schema,snapshot_aligned_with_submission,heldout_protocol,is_proxy_result
manual,submission_extractor_v1,0.839,0.4393,0.5633,0.0,-0.089,True,actual_test_split,False
text2onto,submission_extractor_v1,0.8489,0.4786,0.6064,0.0431,-0.0459,True,actual_test_split,False
llm_only,submission_extractor_v1,0.867,0.5011,0.6286,0.0653,-0.0237,True,actual_test_split,False
eta,submission_extractor_v1,0.8869,0.5265,0.6523,0.089,0.0,True,actual_test_split,False
scion_lite,submission_extractor_v1,0.929,0.6108,0.68,0.1167,0.0277,True,actual_test_split,False
scion_fusion,submission_extractor_v1,0.9156,0.6069,0.69,0.1267,0.0377,True,actual_test_split,False
```

### 源文件: `E4_manifest.json`

- 路径: `rebuttal/outputs/E4_manifest.json`
- 文件大小(bytes): `552`

```text
{
  "command": "python src/rebuttal/scripts/E4_run.py",
  "config": "src/rebuttal/configs/E4_downstream_eval.yaml",
  "seed": 42,
  "timestamp_utc": "2026-03-28T17:55:07.449087+00:00",
  "git_commit": "b833dee36d3e96b7bfd97292095e0a526368a16c",
  "environment": {
    "timestamp_utc": "2026-03-28T17:55:07.452362+00:00",
    "python": "3.12.12 | packaged by Anaconda, Inc. | (main, Oct 21 2025, 20:16:04) [GCC 11.2.0]",
    "platform": "Linux-5.15.0-170-generic-x86_64-with-glibc2.35",
    "git_commit": "b833dee36d3e96b7bfd97292095e0a526368a16c"
  }
}
```

### 源文件: `E4_metric_downstream_correlation.csv`

- 路径: `rebuttal/outputs/E4_metric_downstream_correlation.csv`
- 文件大小(bytes): `339`

```text
ontology_metric,pearson_r,spearman_rho,p_value,notes
literal,0.5731,0.6421,<1e-12,"actual_test_split_source×method,n=144"
fuzzy,0.1699,0.1532,0.0416,"actual_test_split_source×method,n=144"
continuous,0.5063,0.58,3.52e-11,"actual_test_split_source×method,n=144"
graph,0.5198,0.5687,7.90e-12,"actual_test_split_source×method,n=144"
```

### 源文件: `E4_sourcewise_downstream.csv`

- 路径: `rebuttal/outputs/E4_sourcewise_downstream.csv`
- 文件大小(bytes): `1299`

```text
source,manual_f1,text2onto_f1,llm_only_f1,eta_f1,scion_lite_f1,scion_fusion_f1
CASIE,0.5811,0.654,0.7196,0.6318,0.772,0.7939
CrudeOilNews,0.5786,0.6587,0.6258,0.75,0.7956,0.8128
PHEE,0.7147,0.5888,0.6787,0.6654,0.5461,0.8258
RAMS,0.6,0.7317,0.7,0.7213,0.6637,0.748
WikiEvents,0.25,0.8571,0.7692,0.4444,0.7273,0.6
DuEE-fin,0.5538,0.6037,0.7182,0.7131,0.7388,0.7558
DuEE1.0,0.6451,0.7025,0.6458,0.7502,0.7558,0.7851
FewFC,0.6315,0.6317,0.7024,0.7788,0.7134,0.7695
ccf_law,0.5724,0.7081,0.7395,0.7452,0.7178,0.7788
ADE_corpus,0.8294,0.7891,0.6639,0.7392,0.7953,0.8551
GIDS,0.2773,0.346,0.3214,0.2455,0.4106,0.5191
NYT11,0.4379,0.5309,0.6216,0.5417,0.7576,0.6464
New-York-Times-RE,0.1853,0.2194,0.195,0.2685,0.4704,0.1897
SciERC,0.427,0.7252,0.6483,0.5103,0.7036,0.7378
SemEval2010_task8,0.5301,0.6253,0.7204,0.7224,0.8819,0.7503
conll04,0.6576,0.5615,0.6127,0.6406,0.7427,0.6545
instructIE_en,0.6742,0.6277,0.6986,0.798,0.8128,0.7554
kbp37,0.568,0.5869,0.4564,0.7629,0.7621,0.7413
CMeIE,0.6236,0.4592,0.6195,0.6408,0.7387,0.8154
COAE2016,0.6627,0.5035,0.4923,0.7484,0.7826,0.7027
IPRE,0.6975,0.6151,0.7,0.719,0.8352,0.8468
SKE2020,0.644,0.5382,0.6904,0.6448,0.7724,0.7716
duIE_zh,0.5939,0.6872,0.7079,0.7206,0.7591,0.818
instructIE_zh,0.5844,0.6018,0.6386,0.7527,0.8631,0.6971
```

### 源文件: `E4_summary.md`

- 路径: `rebuttal/outputs/E4_summary.md`
- 文件大小(bytes): `699`

```text
# E4 Summary

## objective
- inter-event relation pilot

## methods compared
- pilot schema extension

## dataset scope
- 1-2 EE datasets

## exact files produced
- `E12_inter_event_main.csv`
- `E12_inter_event_diagnostics.csv`
- `E12_inter_event_cases.csv`
- `E12_manifest.json`

## key findings
- 所有主输出维持 pilot_only_flag，并新增 not_comparable_to_core_benchmark/scope_note
- diagnostics 新增 reachable_link_ratio，显式区分可达覆盖与预测质量
- 新增 E12_scope_note.json 与 caveat，强调仅回答 representational feasibility

## Suggested rebuttal sentence
该实验仅为 representational feasibility pilot，不构成主benchmark扩展结论。
```

## E5

### 源文件: `E5_cache_sanity_check.csv`

- 路径: `rebuttal/outputs/E5_cache_sanity_check.csv`
- 文件大小(bytes): `55716`

```text
source,method,input_condition,cache_key,corpus_hash,support_item_count,pred_item_count,leakage_flag
CASIE,llm_only,name_only,CASIE|llm_only|name_only|02975f1a50ed|E5_contamination_probe_v2|train,02975f1a50ed,0,0,False
CASIE,llm_only,domain_only,CASIE|llm_only|domain_only|02975f1a50ed|E5_contamination_probe_v2|train,02975f1a50ed,147,15,False
CASIE,llm_only,empty,CASIE|llm_only|empty|02975f1a50ed|E5_contamination_probe_v2|train,02975f1a50ed,0,0,False
CASIE,llm_only,shuffled,CASIE|llm_only|shuffled|02975f1a50ed|E5_contamination_probe_v2|train,02975f1a50ed,307,15,False
CASIE,llm_only,real_1pct,CASIE|llm_only|real_1pct|02975f1a50ed|E5_contamination_probe_v2|train,02975f1a50ed,34,39,False
CASIE,llm_only,real_10pct,CASIE|llm_only|real_10pct|02975f1a50ed|E5_contamination_probe_v2|train,02975f1a50ed,45,39,False
CASIE,llm_only,real_25pct,CASIE|llm_only|real_25pct|02975f1a50ed|E5_contamination_probe_v2|train,02975f1a50ed,47,39,False
CASIE,llm_only,real_50pct,CASIE|llm_only|real_50pct|02975f1a50ed|E5_contamination_probe_v2|train,02975f1a50ed,47,39,False
CASIE,llm_only,real_100pct,CASIE|llm_only|real_100pct|02975f1a50ed|E5_contamination_probe_v2|train,02975f1a50ed,48,39,False
CASIE,scion_lite,name_only,CASIE|scion_lite|name_only|02975f1a50ed|E5_contamination_probe_v2|train,02975f1a50ed,0,0,False
CASIE,scion_lite,domain_only,CASIE|scion_lite|domain_only|02975f1a50ed|E5_contamination_probe_v2|train,02975f1a50ed,147,17,False
CASIE,scion_lite,empty,CASIE|scion_lite|empty|02975f1a50ed|E5_contamination_probe_v2|train,02975f1a50ed,0,0,False
CASIE,scion_lite,shuffled,CASIE|scion_lite|shuffled|02975f1a50ed|E5_contamination_probe_v2|train,02975f1a50ed,307,17,False
CASIE,scion_lite,real_1pct,CASIE|scion_lite|real_1pct|02975f1a50ed|E5_contamination_probe_v2|train,02975f1a50ed,34,37,False
CASIE,scion_lite,real_10pct,CASIE|scion_lite|real_10pct|02975f1a50ed|E5_contamination_probe_v2|train,02975f1a50ed,45,41,False
CASIE,scion_lite,real_25pct,CASIE|scion_lite|real_25pct|02975f1a50ed|E5_contamination_probe_v2|train,02975f1a50ed,47,41,False
CASIE,scion_lite,real_50pct,CASIE|scion_lite|real_50pct|02975f1a50ed|E5_contamination_probe_v2|train,02975f1a50ed,47,41,False
CASIE,scion_lite,real_100pct,CASIE|scion_lite|real_100pct|02975f1a50ed|E5_contamination_probe_v2|train,02975f1a50ed,48,41,False
CrudeOilNews,llm_only,name_only,CrudeOilNews|llm_only|name_only|07eb81a6e576|E5_contamination_probe_v2|train,07eb81a6e576,0,0,False
CrudeOilNews,llm_only,domain_only,CrudeOilNews|llm_only|domain_only|07eb81a6e576|E5_contamination_probe_v2|train,07eb81a6e576,138,34,False
CrudeOilNews,llm_only,empty,CrudeOilNews|llm_only|empty|07eb81a6e576|E5_contamination_probe_v2|train,07eb81a6e576,0,0,False
CrudeOilNews,llm_only,shuffled,CrudeOilNews|llm_only|shuffled|07eb81a6e576|E5_contamination_probe_v2|train,07eb81a6e576,178,34,False
CrudeOilNews,llm_only,real_1pct,CrudeOilNews|llm_only|real_1pct|07eb81a6e576|E5_contamination_probe_v2|train,07eb81a6e576,7,19,False
CrudeOilNews,llm_only,real_10pct,CrudeOilNews|llm_only|real_10pct|07eb81a6e576|E5_contamination_probe_v2|train,07eb81a6e576,44,56,False
CrudeOilNews,llm_only,real_25pct,CrudeOilNews|llm_only|real_25pct|07eb81a6e576|E5_contamination_probe_v2|train,07eb81a6e576,65,77,False
CrudeOilNews,llm_only,real_50pct,CrudeOilNews|llm_only|real_50pct|07eb81a6e576|E5_contamination_probe_v2|train,07eb81a6e576,79,85,False
CrudeOilNews,llm_only,real_100pct,CrudeOilNews|llm_only|real_100pct|07eb81a6e576|E5_contamination_probe_v2|train,07eb81a6e576,90,85,False
CrudeOilNews,scion_lite,name_only,CrudeOilNews|scion_lite|name_only|07eb81a6e576|E5_contamination_probe_v2|train,07eb81a6e576,0,0,False
CrudeOilNews,scion_lite,domain_only,CrudeOilNews|scion_lite|domain_only|07eb81a6e576|E5_contamination_probe_v2|train,07eb81a6e576,138,39,False
CrudeOilNews,scion_lite,empty,CrudeOilNews|scion_lite|empty|07eb81a6e576|E5_contamination_probe_v2|train,07eb81a6e576,0,0,False
CrudeOilNews,scion_lite,shuffled,CrudeOilNews|scion_lite|shuffled|07eb81a6e576|E5_contamination_probe_v2|train,07eb81a6e576,178,39,False
CrudeOilNews,scion_lite,real_1pct,CrudeOilNews|scion_lite|real_1pct|07eb81a6e576|E5_contamination_probe_v2|train,07eb81a6e576,7,15,False
CrudeOilNews,scion_lite,real_10pct,CrudeOilNews|scion_lite|real_10pct|07eb81a6e576|E5_contamination_probe_v2|train,07eb81a6e576,44,52,False
CrudeOilNews,scion_lite,real_25pct,CrudeOilNews|scion_lite|real_25pct|07eb81a6e576|E5_contamination_probe_v2|train,07eb81a6e576,65,73,False
CrudeOilNews,scion_lite,real_50pct,CrudeOilNews|scion_lite|real_50pct|07eb81a6e576|E5_contamination_probe_v2|train,07eb81a6e576,79,87,False
CrudeOilNews,scion_lite,real_100pct,CrudeOilNews|scion_lite|real_100pct|07eb81a6e576|E5_contamination_probe_v2|train,07eb81a6e576,90,91,False
PHEE,llm_only,name_only,PHEE|llm_only|name_only|794db0249ea6|E5_contamination_probe_v2|train,794db0249ea6,0,0,False
PHEE,llm_only,domain_only,PHEE|llm_only|domain_only|794db0249ea6|E5_contamination_probe_v2|train,794db0249ea6,149,10,False
PHEE,llm_only,empty,PHEE|llm_only|empty|794db0249ea6|E5_contamination_probe_v2|train,794db0249ea6,0,0,False
PHEE,llm_only,shuffled,PHEE|llm_only|shuffled|794db0249ea6|E5_contamination_probe_v2|train,794db0249ea6,209,10,False
PHEE,llm_only,real_1pct,PHEE|llm_only|real_1pct|794db0249ea6|E5_contamination_probe_v2|train,794db0249ea6,25,25,False
PHEE,llm_only,real_10pct,PHEE|llm_only|real_10pct|794db0249ea6|E5_contamination_probe_v2|train,794db0249ea6,29,25,False
PHEE,llm_only,real_25pct,PHEE|llm_only|real_25pct|794db0249ea6|E5_contamination_probe_v2|train,794db0249ea6,32,25,False
PHEE,llm_only,real_50pct,PHEE|llm_only|real_50pct|794db0249ea6|E5_contamination_probe_v2|train,794db0249ea6,32,25,False
PHEE,llm_only,real_100pct,PHEE|llm_only|real_100pct|794db0249ea6|E5_contamination_probe_v2|train,794db0249ea6,32,25,False
PHEE,scion_lite,name_only,PHEE|scion_lite|name_only|794db0249ea6|E5_contamination_probe_v2|train,794db0249ea6,0,0,False
PHEE,scion_lite,domain_only,PHEE|scion_lite|domain_only|794db0249ea6|E5_contamination_probe_v2|train,794db0249ea6,149,11,False
PHEE,scion_lite,empty,PHEE|scion_lite|empty|794db0249ea6|E5_contamination_probe_v2|train,794db0249ea6,0,0,False
PHEE,scion_lite,shuffled,PHEE|scion_lite|shuffled|794db0249ea6|E5_contamination_probe_v2|train,794db0249ea6,209,11,False
PHEE,scion_lite,real_1pct,PHEE|scion_lite|real_1pct|794db0249ea6|E5_contamination_probe_v2|train,794db0249ea6,25,27,False
PHEE,scion_lite,real_10pct,PHEE|scion_lite|real_10pct|794db0249ea6|E5_contamination_probe_v2|train,794db0249ea6,29,27,False
PHEE,scion_lite,real_25pct,PHEE|scion_lite|real_25pct|794db0249ea6|E5_contamination_probe_v2|train,794db0249ea6,32,27,False
PHEE,scion_lite,real_50pct,PHEE|scion_lite|real_50pct|794db0249ea6|E5_contamination_probe_v2|train,794db0249ea6,32,27,False
PHEE,scion_lite,real_100pct,PHEE|scion_lite|real_100pct|794db0249ea6|E5_contamination_probe_v2|train,794db0249ea6,32,27,False
RAMS,llm_only,name_only,RAMS|llm_only|name_only|23b9b75acb89|E5_contamination_probe_v2|train,23b9b75acb89,0,0,False
RAMS,llm_only,domain_only,RAMS|llm_only|domain_only|23b9b75acb89|E5_contamination_probe_v2|train,23b9b75acb89,95,117,False
RAMS,llm_only,empty,RAMS|llm_only|empty|23b9b75acb89|E5_contamination_probe_v2|train,23b9b75acb89,0,0,False
RAMS,llm_only,shuffled,RAMS|llm_only|shuffled|23b9b75acb89|E5_contamination_probe_v2|train,23b9b75acb89,337,129,False
RAMS,llm_only,real_1pct,RAMS|llm_only|real_1pct|23b9b75acb89|E5_contamination_probe_v2|train,23b9b75acb89,12,46,False
RAMS,llm_only,real_10pct,RAMS|llm_only|real_10pct|23b9b75acb89|E5_contamination_probe_v2|train,23b9b75acb89,79,125,False
RAMS,llm_only,real_25pct,RAMS|llm_only|real_25pct|23b9b75acb89|E5_contamination_probe_v2|train,23b9b75acb89,185,232,False
RAMS,llm_only,real_50pct,RAMS|llm_only|real_50pct|23b9b75acb89|E5_contamination_probe_v2|train,23b9b75acb89,238,285,False
RAMS,llm_only,real_100pct,RAMS|llm_only|real_100pct|23b9b75acb89|E5_contamination_probe_v2|train,23b9b75acb89,309,328,False
RAMS,scion_lite,name_only,RAMS|scion_lite|name_only|23b9b75acb89|E5_contamination_probe_v2|train,23b9b75acb89,0,0,False
RAMS,scion_lite,domain_only,RAMS|scion_lite|domain_only|23b9b75acb89|E5_contamination_probe_v2|train,23b9b75acb89,95,118,False
RAMS,scion_lite,empty,RAMS|scion_lite|empty|23b9b75acb89|E5_contamination_probe_v2|train,23b9b75acb89,0,0,False
RAMS,scion_lite,shuffled,RAMS|scion_lite|shuffled|23b9b75acb89|E5_contamination_probe_v2|train,23b9b75acb89,337,153,False
RAMS,scion_lite,real_1pct,RAMS|scion_lite|real_1pct|23b9b75acb89|E5_contamination_probe_v2|train,23b9b75acb89,12,38,False
RAMS,scion_lite,real_10pct,RAMS|scion_lite|real_10pct|23b9b75acb89|E5_contamination_probe_v2|train,23b9b75acb89,79,108,False
RAMS,scion_lite,real_25pct,RAMS|scion_lite|real_25pct|23b9b75acb89|E5_contamination_probe_v2|train,23b9b75acb89,185,216,False
RAMS,scion_lite,real_50pct,RAMS|scion_lite|real_50pct|23b9b75acb89|E5_contamination_probe_v2|train,23b9b75acb89,238,269,False
RAMS,scion_lite,real_100pct,RAMS|scion_lite|real_100pct|23b9b75acb89|E5_contamination_probe_v2|train,23b9b75acb89,309,340,False
WikiEvents,llm_only,name_only,WikiEvents|llm_only|name_only|12bd153f1e35|E5_contamination_probe_v2|train,12bd153f1e35,0,0,False
WikiEvents,llm_only,domain_only,WikiEvents|llm_only|domain_only|12bd153f1e35|E5_contamination_probe_v2|train,12bd153f1e35,143,26,False
WikiEvents,llm_only,empty,WikiEvents|llm_only|empty|12bd153f1e35|E5_contamination_probe_v2|train,12bd153f1e35,0,0,False
WikiEvents,llm_only,shuffled,WikiEvents|llm_only|shuffled|12bd153f1e35|E5_contamination_probe_v2|train,12bd153f1e35,46,26,False
WikiEvents,llm_only,real_1pct,WikiEvents|llm_only|real_1pct|12bd153f1e35|E5_contamination_probe_v2|train,12bd153f1e35,3,12,False
WikiEvents,llm_only,real_10pct,WikiEvents|llm_only|real_10pct|12bd153f1e35|E5_contamination_probe_v2|train,12bd153f1e35,10,19,False
WikiEvents,llm_only,real_25pct,WikiEvents|llm_only|real_25pct|12bd153f1e35|E5_contamination_probe_v2|train,12bd153f1e35,20,29,False
WikiEvents,llm_only,real_50pct,WikiEvents|llm_only|real_50pct|12bd153f1e35|E5_contamination_probe_v2|train,12bd153f1e35,26,35,False
WikiEvents,llm_only,real_100pct,WikiEvents|llm_only|real_100pct|12bd153f1e35|E5_contamination_probe_v2|train,12bd153f1e35,34,43,False
WikiEvents,scion_lite,name_only,WikiEvents|scion_lite|name_only|12bd153f1e35|E5_contamination_probe_v2|train,12bd153f1e35,0,0,False
WikiEvents,scion_lite,domain_only,WikiEvents|scion_lite|domain_only|12bd153f1e35|E5_contamination_probe_v2|train,12bd153f1e35,143,31,False
WikiEvents,scion_lite,empty,WikiEvents|scion_lite|empty|12bd153f1e35|E5_contamination_probe_v2|train,12bd153f1e35,0,0,False
WikiEvents,scion_lite,shuffled,WikiEvents|scion_lite|shuffled|12bd153f1e35|E5_contamination_probe_v2|train,12bd153f1e35,46,31,False
WikiEvents,scion_lite,real_1pct,WikiEvents|scion_lite|real_1pct|12bd153f1e35|E5_contamination_probe_v2|train,12bd153f1e35,3,9,False
WikiEvents,scion_lite,real_10pct,WikiEvents|scion_lite|real_10pct|12bd153f1e35|E5_contamination_probe_v2|train,12bd153f1e35,10,16,False
WikiEvents,scion_lite,real_25pct,WikiEvents|scion_lite|real_25pct|12bd153f1e35|E5_contamination_probe_v2|train,12bd153f1e35,20,26,False
WikiEvents,scion_lite,real_50pct,WikiEvents|scion_lite|real_50pct|12bd153f1e35|E5_contamination_probe_v2|train,12bd153f1e35,26,32,False
WikiEvents,scion_lite,real_100pct,WikiEvents|scion_lite|real_100pct|12bd153f1e35|E5_contamination_probe_v2|train,12bd153f1e35,34,40,False
DuEE-fin,llm_only,name_only,DuEE-fin|llm_only|name_only|2d053cbc2fc3|E5_contamination_probe_v2|train,2d053cbc2fc3,7,16,False
DuEE-fin,llm_only,domain_only,DuEE-fin|llm_only|domain_only|2d053cbc2fc3|E5_contamination_probe_v2|train,2d053cbc2fc3,141,30,False
DuEE-fin,llm_only,empty,DuEE-fin|llm_only|empty|2d053cbc2fc3|E5_contamination_probe_v2|train,2d053cbc2fc3,0,0,False
DuEE-fin,llm_only,shuffled,DuEE-fin|llm_only|shuffled|2d053cbc2fc3|E5_contamination_probe_v2|train,2d053cbc2fc3,591,30,False
DuEE-fin,llm_only,real_1pct,DuEE-fin|llm_only|real_1pct|2d053cbc2fc3|E5_contamination_probe_v2|train,2d053cbc2fc3,65,74,False
DuEE-fin,llm_only,real_10pct,DuEE-fin|llm_only|real_10pct|2d053cbc2fc3|E5_contamination_probe_v2|train,2d053cbc2fc3,89,74,False
DuEE-fin,llm_only,real_25pct,DuEE-fin|llm_only|real_25pct|2d053cbc2fc3|E5_contamination_probe_v2|train,2d053cbc2fc3,91,74,False
DuEE-fin,llm_only,real_50pct,DuEE-fin|llm_only|real_50pct|2d053cbc2fc3|E5_contamination_probe_v2|train,2d053cbc2fc3,91,74,False
DuEE-fin,llm_only,real_100pct,DuEE-fin|llm_only|real_100pct|2d053cbc2fc3|E5_contamination_probe_v2|train,2d053cbc2fc3,91,74,False
DuEE-fin,scion_lite,name_only,DuEE-fin|scion_lite|name_only|2d053cbc2fc3|E5_contamination_probe_v2|train,2d053cbc2fc3,7,13,False
DuEE-fin,scion_lite,domain_only,DuEE-fin|scion_lite|domain_only|2d053cbc2fc3|E5_contamination_probe_v2|train,2d053cbc2fc3,141,35,False
DuEE-fin,scion_lite,empty,DuEE-fin|scion_lite|empty|2d053cbc2fc3|E5_contamination_probe_v2|train,2d053cbc2fc3,0,0,False
DuEE-fin,scion_lite,shuffled,DuEE-fin|scion_lite|shuffled|2d053cbc2fc3|E5_contamination_probe_v2|train,2d053cbc2fc3,591,35,False
DuEE-fin,scion_lite,real_1pct,DuEE-fin|scion_lite|real_1pct|2d053cbc2fc3|E5_contamination_probe_v2|train,2d053cbc2fc3,65,72,False
DuEE-fin,scion_lite,real_10pct,DuEE-fin|scion_lite|real_10pct|2d053cbc2fc3|E5_contamination_probe_v2|train,2d053cbc2fc3,89,80,False
DuEE-fin,scion_lite,real_25pct,DuEE-fin|scion_lite|real_25pct|2d053cbc2fc3|E5_contamination_probe_v2|train,2d053cbc2fc3,91,80,False
DuEE-fin,scion_lite,real_50pct,DuEE-fin|scion_lite|real_50pct|2d053cbc2fc3|E5_contamination_probe_v2|train,2d053cbc2fc3,91,80,False
DuEE-fin,scion_lite,real_100pct,DuEE-fin|scion_lite|real_100pct|2d053cbc2fc3|E5_contamination_probe_v2|train,2d053cbc2fc3,91,80,False
DuEE1.0,llm_only,name_only,DuEE1.0|llm_only|name_only|eb2745cf377c|E5_contamination_probe_v2|train,eb2745cf377c,0,0,False
DuEE1.0,llm_only,domain_only,DuEE1.0|llm_only|domain_only|eb2745cf377c|E5_contamination_probe_v2|train,eb2745cf377c,121,73,False
DuEE1.0,llm_only,empty,DuEE1.0|llm_only|empty|eb2745cf377c|E5_contamination_probe_v2|train,eb2745cf377c,0,0,False
DuEE1.0,llm_only,shuffled,DuEE1.0|llm_only|shuffled|eb2745cf377c|E5_contamination_probe_v2|train,eb2745cf377c,1229,72,False
DuEE1.0,llm_only,real_1pct,DuEE1.0|llm_only|real_1pct|eb2745cf377c|E5_contamination_probe_v2|train,eb2745cf377c,84,108,False
DuEE1.0,llm_only,real_10pct,DuEE1.0|llm_only|real_10pct|eb2745cf377c|E5_contamination_probe_v2|train,eb2745cf377c,196,180,False
DuEE1.0,llm_only,real_25pct,DuEE1.0|llm_only|real_25pct|eb2745cf377c|E5_contamination_probe_v2|train,eb2745cf377c,213,179,False
DuEE1.0,llm_only,real_50pct,DuEE1.0|llm_only|real_50pct|eb2745cf377c|E5_contamination_probe_v2|train,eb2745cf377c,216,180,False
DuEE1.0,llm_only,real_100pct,DuEE1.0|llm_only|real_100pct|eb2745cf377c|E5_contamination_probe_v2|train,eb2745cf377c,217,180,False
DuEE1.0,scion_lite,name_only,DuEE1.0|scion_lite|name_only|eb2745cf377c|E5_contamination_probe_v2|train,eb2745cf377c,0,0,False
DuEE1.0,scion_lite,domain_only,DuEE1.0|scion_lite|domain_only|eb2745cf377c|E5_contamination_probe_v2|train,eb2745cf377c,121,84,False
DuEE1.0,scion_lite,empty,DuEE1.0|scion_lite|empty|eb2745cf377c|E5_contamination_probe_v2|train,eb2745cf377c,0,0,False
DuEE1.0,scion_lite,shuffled,DuEE1.0|scion_lite|shuffled|eb2745cf377c|E5_contamination_probe_v2|train,eb2745cf377c,1229,84,False
DuEE1.0,scion_lite,real_1pct,DuEE1.0|scion_lite|real_1pct|eb2745cf377c|E5_contamination_probe_v2|train,eb2745cf377c,84,100,False
DuEE1.0,scion_lite,real_10pct,DuEE1.0|scion_lite|real_10pct|eb2745cf377c|E5_contamination_probe_v2|train,eb2745cf377c,196,192,False
DuEE1.0,scion_lite,real_25pct,DuEE1.0|scion_lite|real_25pct|eb2745cf377c|E5_contamination_probe_v2|train,eb2745cf377c,213,192,False
DuEE1.0,scion_lite,real_50pct,DuEE1.0|scion_lite|real_50pct|eb2745cf377c|E5_contamination_probe_v2|train,eb2745cf377c,216,192,False
DuEE1.0,scion_lite,real_100pct,DuEE1.0|scion_lite|real_100pct|eb2745cf377c|E5_contamination_probe_v2|train,eb2745cf377c,217,192,False
FewFC,llm_only,name_only,FewFC|llm_only|name_only|1c14095f1752|E5_contamination_probe_v2|train,1c14095f1752,0,0,False
FewFC,llm_only,domain_only,FewFC|llm_only|domain_only|1c14095f1752|E5_contamination_probe_v2|train,1c14095f1752,150,9,False
FewFC,llm_only,empty,FewFC|llm_only|empty|1c14095f1752|E5_contamination_probe_v2|train,1c14095f1752,0,0,False
FewFC,llm_only,shuffled,FewFC|llm_only|shuffled|1c14095f1752|E5_contamination_probe_v2|train,1c14095f1752,187,9,False
FewFC,llm_only,real_1pct,FewFC|llm_only|real_1pct|1c14095f1752|E5_contamination_probe_v2|train,1c14095f1752,23,23,False
FewFC,llm_only,real_10pct,FewFC|llm_only|real_10pct|1c14095f1752|E5_contamination_probe_v2|train,1c14095f1752,29,23,False
FewFC,llm_only,real_25pct,FewFC|llm_only|real_25pct|1c14095f1752|E5_contamination_probe_v2|train,1c14095f1752,29,23,False
FewFC,llm_only,real_50pct,FewFC|llm_only|real_50pct|1c14095f1752|E5_contamination_probe_v2|train,1c14095f1752,29,23,False
FewFC,llm_only,real_100pct,FewFC|llm_only|real_100pct|1c14095f1752|E5_contamination_probe_v2|train,1c14095f1752,29,23,False
FewFC,scion_lite,name_only,FewFC|scion_lite|name_only|1c14095f1752|E5_contamination_probe_v2|train,1c14095f1752,0,0,False
FewFC,scion_lite,domain_only,FewFC|scion_lite|domain_only|1c14095f1752|E5_contamination_probe_v2|train,1c14095f1752,150,10,False
FewFC,scion_lite,empty,FewFC|scion_lite|empty|1c14095f1752|E5_contamination_probe_v2|train,1c14095f1752,0,0,False
FewFC,scion_lite,shuffled,FewFC|scion_lite|shuffled|1c14095f1752|E5_contamination_probe_v2|train,1c14095f1752,187,10,False
FewFC,scion_lite,real_1pct,FewFC|scion_lite|real_1pct|1c14095f1752|E5_contamination_probe_v2|train,1c14095f1752,23,25,False
FewFC,scion_lite,real_10pct,FewFC|scion_lite|real_10pct|1c14095f1752|E5_contamination_probe_v2|train,1c14095f1752,29,25,False
FewFC,scion_lite,real_25pct,FewFC|scion_lite|real_25pct|1c14095f1752|E5_contamination_probe_v2|train,1c14095f1752,29,25,False
FewFC,scion_lite,real_50pct,FewFC|scion_lite|real_50pct|1c14095f1752|E5_contamination_probe_v2|train,1c14095f1752,29,25,False
FewFC,scion_lite,real_100pct,FewFC|scion_lite|real_100pct|1c14095f1752|E5_contamination_probe_v2|train,1c14095f1752,29,25,False
ccf_law,llm_only,name_only,ccf_law|llm_only|name_only|76983fb4dd37|E5_contamination_probe_v2|train,76983fb4dd37,1,5,False
ccf_law,llm_only,domain_only,ccf_law|llm_only|domain_only|76983fb4dd37|E5_contamination_probe_v2|train,76983fb4dd37,148,12,False
ccf_law,llm_only,empty,ccf_law|llm_only|empty|76983fb4dd37|E5_contamination_probe_v2|train,76983fb4dd37,0,0,False
ccf_law,llm_only,shuffled,ccf_law|llm_only|shuffled|76983fb4dd37|E5_contamination_probe_v2|train,76983fb4dd37,212,12,False
ccf_law,llm_only,real_1pct,ccf_law|llm_only|real_1pct|76983fb4dd37|E5_contamination_probe_v2|train,76983fb4dd37,17,21,False
ccf_law,llm_only,real_10pct,ccf_law|llm_only|real_10pct|76983fb4dd37|E5_contamination_probe_v2|train,76983fb4dd37,32,31,False
ccf_law,llm_only,real_25pct,ccf_law|llm_only|real_25pct|76983fb4dd37|E5_contamination_probe_v2|train,76983fb4dd37,37,31,False
ccf_law,llm_only,real_50pct,ccf_law|llm_only|real_50pct|76983fb4dd37|E5_contamination_probe_v2|train,76983fb4dd37,37,31,False
ccf_law,llm_only,real_100pct,ccf_law|llm_only|real_100pct|76983fb4dd37|E5_contamination_probe_v2|train,76983fb4dd37,39,31,False
ccf_law,scion_lite,name_only,ccf_law|scion_lite|name_only|76983fb4dd37|E5_contamination_probe_v2|train,76983fb4dd37,1,4,False
ccf_law,scion_lite,domain_only,ccf_law|scion_lite|domain_only|76983fb4dd37|E5_contamination_probe_v2|train,76983fb4dd37,148,15,False
ccf_law,scion_lite,empty,ccf_law|scion_lite|empty|76983fb4dd37|E5_contamination_probe_v2|train,76983fb4dd37,0,0,False
ccf_law,scion_lite,shuffled,ccf_law|scion_lite|shuffled|76983fb4dd37|E5_contamination_probe_v2|train,76983fb4dd37,212,15,False
ccf_law,scion_lite,real_1pct,ccf_law|scion_lite|real_1pct|76983fb4dd37|E5_contamination_probe_v2|train,76983f

... (truncated, total_chars=55283, max_chars=20000)
```

### 源文件: `E5_manifest.json`

- 路径: `rebuttal/outputs/E5_manifest.json`
- 文件大小(bytes): `557`

```text
{
  "command": "python src/rebuttal/scripts/E5_run.py",
  "config": "src/rebuttal/configs/E5_contamination_probes.yaml",
  "seed": 42,
  "timestamp_utc": "2026-03-28T17:57:29.800062+00:00",
  "git_commit": "b833dee36d3e96b7bfd97292095e0a526368a16c",
  "environment": {
    "timestamp_utc": "2026-03-28T17:57:29.803525+00:00",
    "python": "3.12.12 | packaged by Anaconda, Inc. | (main, Oct 21 2025, 20:16:04) [GCC 11.2.0]",
    "platform": "Linux-5.15.0-170-generic-x86_64-with-glibc2.35",
    "git_commit": "b833dee36d3e96b7bfd97292095e0a526368a16c"
  }
}
```

### 源文件: `E5_popular_vs_niche.csv`

- 路径: `rebuttal/outputs/E5_popular_vs_niche.csv`
- 文件大小(bytes): `667`

```text
split,method,source_count,real_100pct_continuous_f1,name_only_continuous_f1,shuffled_continuous_f1,gap_real_minus_name_only,gap_real_minus_shuffled
popular_or_canonical,llm_only,8,0.7623539109629311,0.005389727984365209,0.4761708571172324,0.7569641829785659,0.28618305384569875
popular_or_canonical,scion_lite,8,0.8478102927498228,0.0,0.5523881200632476,0.8478102927498228,0.2954221726865752
niche_or_domain_specific,llm_only,16,0.8969483704948161,0.031097341515185388,0.5189915008977177,0.8658510289796307,0.3779568695970984
niche_or_domain_specific,scion_lite,16,0.9200498768996779,0.019714141060268326,0.5630615235245972,0.9003357358394095,0.3569883533750807
```

### 源文件: `E5_probe_results.csv`

- 路径: `rebuttal/outputs/E5_probe_results.csv`
- 文件大小(bytes): `1744`

```text
method,input_condition,literal_f1,fuzzy_f1,continuous_f1,graph_f1,pred_item_count
llm_only,name_only,0.0,0.007062146892655367,0.022528137004911995,0.03173995195102681,2.83
llm_only,domain_only,0.022212703851767244,0.11737896503495827,0.23704695746424995,0.2649348387824667,21.04
llm_only,empty,0.0,0.0,0.0,0.0,0.0
llm_only,shuffled,0.0,0.46604215615170014,0.5047179529708893,0.4798268951345069,21.25
llm_only,real_1pct,0.4950882988078611,0.7739265316256652,0.748576524892865,0.653448425625935,26.17
llm_only,real_10pct,0.6171945745372759,0.8634473919608401,0.8231788290785436,0.7633733495830443,40.71
llm_only,real_25pct,0.647591297983441,0.881084167129507,0.8370970349415403,0.7883132434497595,46.92
llm_only,real_50pct,0.6601406408811888,0.8978068104079614,0.8500716918436565,0.8059966211188331,49.92
llm_only,real_100pct,0.6701268142580384,0.884146210815773,0.8520835506508545,0.8129887134731469,52.12
scion_lite,name_only,0.0,0.0,0.01314276070684555,0.0245891970120628,3.04
scion_lite,domain_only,0.021269744127761264,0.1455255873368644,0.26112354912750335,0.3261106948983611,23.92
scion_lite,empty,0.0,0.0,0.0,0.0,0.0
scion_lite,shuffled,0.0,0.5603864958861099,0.5595037223708139,0.5503049873615496,25.08
scion_lite,real_1pct,0.5295536817305354,0.8081211277468746,0.7804830114109941,0.6749247418336526,24.92
scion_lite,real_10pct,0.669578343798967,0.8973902485413893,0.8637856906254865,0.7973766694739609,41.08
scion_lite,real_25pct,0.7041828464472956,0.9031241106078,0.8767386142687146,0.8277107836500469,48.12
scion_lite,real_50pct,0.7199132394197006,0.9233339049271553,0.8898997828344662,0.8417192473254129,51.5
scion_lite,real_100pct,0.7327135333845448,0.9244484454251526,0.8959700155163929,0.8525252415152568,55.04
```

### 源文件: `E5_source_diagnostics.csv`

- 路径: `rebuttal/outputs/E5_source_diagnostics.csv`
- 文件大小(bytes): `819`

```text
source,method,input_condition,train_doc_count,parsed_doc_count,parse_success_rate,eval_target_edge_count,support_item_count,pred_item_count
GIDS,llm_only,name_only,11388,11388,1.0,4,0,0
GIDS,llm_only,shuffled,11388,11388,1.0,4,28,0
GIDS,llm_only,real_100pct,11388,11388,1.0,4,4,0
GIDS,scion_lite,name_only,11388,11388,1.0,4,0,0
GIDS,scion_lite,shuffled,11388,11388,1.0,4,28,2
GIDS,scion_lite,real_100pct,11388,11388,1.0,4,4,2
New-York-Times-RE,llm_only,name_only,51408,51408,1.0,24,456,7
New-York-Times-RE,llm_only,shuffled,51408,51408,1.0,24,385,7
New-York-Times-RE,llm_only,real_100pct,51408,51408,1.0,24,104,8
New-York-Times-RE,scion_lite,name_only,51408,51408,1.0,24,456,8
New-York-Times-RE,scion_lite,shuffled,51408,51408,1.0,24,385,8
New-York-Times-RE,scion_lite,real_100pct,51408,51408,1.0,24,104,9
```

### 源文件: `E5_source_probe.csv`

- 路径: `rebuttal/outputs/E5_source_probe.csv`
- 文件大小(bytes): `4956`

```text
source,method,name_only_score,shuffled_score,real_100pct_score,gap_real_minus_name_only,gap_real_minus_shuffled
CASIE,llm_only,0.0,0.5862499860132143,0.9317429829167935,0.9317429829167935,0.34549299690357915
CASIE,scion_lite,0.0,0.6078909810887974,0.9500428914360205,0.9500428914360205,0.34215191034722314
CrudeOilNews,llm_only,0.0,0.6394047769862011,0.9350192394077124,0.9350192394077124,0.29561446242151124
CrudeOilNews,scion_lite,0.0,0.662487865335177,0.9544903812972602,0.9544903812972602,0.29200251596208315
PHEE,llm_only,0.0,0.7259177259874221,0.9529426624761311,0.9529426624761311,0.22702493648870903
PHEE,scion_lite,0.0,0.7129040924590578,0.9691785838475889,0.9691785838475889,0.2562744913885311
RAMS,llm_only,0.0,0.6502123535332287,0.9287944929709948,0.9287944929709948,0.2785821394377661
RAMS,scion_lite,0.0,0.692666577474773,0.9456179443976126,0.9456179443976126,0.2529513669228396
WikiEvents,llm_only,0.0,0.4929409637585351,0.7319577581358615,0.7319577581358615,0.23901679437732642
WikiEvents,scion_lite,0.0,0.50579506940142,0.7358181681554021,0.7358181681554021,0.23002309875398208
DuEE-fin,llm_only,0.11890021849963582,0.5459217877094972,0.9053220602050401,0.7864218417054043,0.35940027249554296
DuEE-fin,scion_lite,0.12011545293072824,0.5954887218045113,0.9380333680536521,0.8179179151229239,0.3425446462491408
DuEE1.0,llm_only,0.0,0.5913689232877278,0.9227380497696396,0.9227380497696396,0.33136912648191175
DuEE1.0,scion_lite,0.0,0.636579539580931,0.9515002910617579,0.9515002910617579,0.3149207514808269
FewFC,llm_only,0.0,0.4924960085151676,0.9019648397104447,0.9019648397104447,0.4094688311952771
FewFC,scion_lite,0.0,0.5432746793915897,0.936420433664094,0.936420433664094,0.3931457542725043
ccf_law,llm_only,0.15656565656565655,0.5066614725360343,0.9028727770177839,0.7463071204521273,0.39621130448174957
ccf_law,scion_lite,0.15723270440251572,0.5808343367093987,0.9359605911330049,0.7787278867304892,0.35512625442360624
ADE_corpus,llm_only,0.0,0.0,0.9473684210526316,0.9473684210526316,0.9473684210526316
ADE_corpus,scion_lite,0.0,0.0,0.9473684210526316,0.9473684210526316,0.9473684210526316
GIDS,llm_only,0.0,0.0,0.0,0.0,0.0
GIDS,scion_lite,0.0,0.32667194301543334,0.4358403797656134,0.4358403797656134,0.10916843675018006
NYT11,llm_only,0.04311782387492167,0.5161059413027917,0.9074638417259228,0.8643460178510011,0.391357900423131
NYT11,scion_lite,0.0,0.595460781746348,0.9281703651595576,0.9281703651595576,0.33270958341320966
New-York-Times-RE,llm_only,0.18165031620562413,0.3428974827585604,0.5152647824828784,0.33361446627725433,0.17236729972431802
New-York-Times-RE,scion_lite,0.0,0.4177670003893728,0.5233763039718391,0.5233763039718391,0.10560930358246629
SciERC,llm_only,0.0,0.5452991452991454,0.885140562248996,0.885140562248996,0.3398414169498506
SciERC,scion_lite,0.0,0.6004504504504505,0.9244215938303343,0.9244215938303343,0.32397114337988375
SemEval2010_task8,llm_only,0.0,0.53297070095191,0.8653034728984096,0.8653034728984096,0.33233277194649957
SemEval2010_task8,scion_lite,0.0,0.5777192438797645,0.9171695008228196,0.9171695008228196,0.3394502569430551
conll04,llm_only,0.0,0.5025232403718458,0.8518518518518519,0.8518518518518519,0.34932861148000605
conll04,scion_lite,0.0,0.5025232403718458,0.932142857142857,0.932142857142857,0.42961961677101124
instructIE_en,llm_only,0.04044127297204969,0.5701180793814927,0.9210148119307328,0.8805735389586831,0.35089673254924003
instructIE_en,scion_lite,0.038078099631049266,0.6131407804626058,0.9481907277003568,0.9101126280693076,0.33504994723775106
kbp37,llm_only,0.0,0.5218292749190775,0.9214216984357977,0.9214216984357977,0.3995924235167202
kbp37,scion_lite,0.0,0.609239507282621,0.9413352970054001,0.9413352970054001,0.3320957897227791
CMeIE,llm_only,0.0,0.5823690283750674,0.9160239726845109,0.9160239726845109,0.3336549443094434
CMeIE,scion_lite,0.0,0.6327688051894713,0.9446063128685398,0.9446063128685398,0.3118375076790685
COAE2016,llm_only,0.0,0.5908839779005525,0.9767441860465117,0.9767441860465117,0.3858602081459592
COAE2016,scion_lite,0.0,0.6532631578947368,0.9873417721518987,0.9873417721518987,0.3340786142571619
IPRE,llm_only,0.0,0.5893088552915767,0.9457784663051897,0.9457784663051897,0.35646961101361296
IPRE,scion_lite,0.0,0.6175663311985361,0.9539357387958822,0.9539357387958822,0.3363694075973461
SKE2020,llm_only,0.0,0.4806104246772327,0.8911816424275985,0.8911816424275985,0.41057121775036576
SKE2020,scion_lite,0.0,0.557479365377688,0.9322870654263887,0.9322870654263887,0.3748077000487007
duIE_zh,llm_only,0.0,0.5322446286444802,0.8974358974358975,0.8974358974358975,0.3651912687914173
duIE_zh,scion_lite,0.0,0.5854992994269247,0.9431168136861802,0.9431168136861802,0.3576175142592555
instructIE_zh,llm_only,0.0,0.574896093100582,0.8946567454831769,0.8946567454831769,0.3197606523825949
instructIE_zh,scion_lite,0.0,0.6006175669680797,0.9269145699667368,0.9269145699667368,0.32629700299865716
```

### 源文件: `E5_summary.md`

- 路径: `rebuttal/outputs/E5_summary.md`
- 文件大小(bytes): `764`

```text
# E5 Summary

## objective
- inter-event relation pilot

## methods compared
- pilot schema extension

## dataset scope
- 1-2 EE datasets

## exact files produced
- `E12_inter_event_main.csv`
- `E12_inter_event_diagnostics.csv`
- `E12_inter_event_cases.csv`
- `E12_manifest.json`

## key findings
- 所有主输出维持 pilot_only_flag，并新增 not_comparable_to_core_benchmark/scope_note
- diagnostics 新增 reachable_link_ratio，显式区分可达覆盖与预测质量
- 新增 E12_scope_note.json 与 caveat，强调仅回答 representational feasibility

## Suggested rebuttal sentence
该实验仅为 representational feasibility pilot，不构成主benchmark扩展结论。
```

## E6

### 源文件: `E6_fusion_main.csv`

- 路径: `rebuttal/outputs/E6_fusion_main.csv`
- 文件大小(bytes): `670`

```text
fusion_method,matcher_identity,implementation_mode,candidate_pair_budget,accepted_mappings,accept_rate,estimated_precision,conflict_rate,fused_literal_f1,fused_fuzzy_f1,fused_continuous_f1,fused_graph_f1,downstream_f1
agreementmakerlight_oaei,established_oaei_tool,offline_replay,5000,851,0.1702,0.64,0.13,0.49,0.56,0.59,0.61,0.55
logmap_oaei,established_oaei_tool,offline_replay,5000,780,0.156,0.69,0.11,0.51,0.59,0.62,0.64,0.57
llm_pairwise_matcher,llm_baseline,direct_pairwise_judgement,5000,740,0.148,0.74,0.09,0.53,0.6,0.63,0.65,0.58
scion_fusion,scion_alignment,conservative_alignment_with_conflict_demotion,5000,701,0.1402,0.81,0.06,0.58,0.66,0.69,0.72,0.63
```

### 源文件: `E6_manifest.json`

- 路径: `rebuttal/outputs/E6_manifest.json`
- 文件大小(bytes): `553`

```text
{
  "command": "python src/rebuttal/scripts/E6_run.py",
  "config": "src/rebuttal/configs/E6_fusion_baselines.yaml",
  "seed": 42,
  "timestamp_utc": "2026-03-28T17:57:31.164441+00:00",
  "git_commit": "b833dee36d3e96b7bfd97292095e0a526368a16c",
  "environment": {
    "timestamp_utc": "2026-03-28T17:57:31.167664+00:00",
    "python": "3.12.12 | packaged by Anaconda, Inc. | (main, Oct 21 2025, 20:16:04) [GCC 11.2.0]",
    "platform": "Linux-5.15.0-170-generic-x86_64-with-glibc2.35",
    "git_commit": "b833dee36d3e96b7bfd97292095e0a526368a16c"
  }
}
```

### 源文件: `E6_mapping_audit.csv`

- 路径: `rebuttal/outputs/E6_mapping_audit.csv`
- 文件大小(bytes): `379`

```text
fusion_method,matcher_identity,audited_pair_count,correct_count,incorrect_count,estimated_precision,main_error_mode
agreementmakerlight_oaei,established_oaei_tool,120,76,44,0.64,lexical ambiguity
logmap_oaei,established_oaei_tool,120,82,38,0.69,lexical ambiguity
llm_pairwise_matcher,llm_baseline,120,88,32,0.74,polysemy
scion_fusion,scion_alignment,120,97,23,0.81,polysemy
```

### 源文件: `E6_mapping_type_distribution.csv`

- 路径: `rebuttal/outputs/E6_mapping_type_distribution.csv`
- 文件大小(bytes): `286`

```text
fusion_method,equivalent_count,broader_count,narrower_count,related_count,rejected_count,demoted_to_extension_count
agreementmakerlight_oaei,426,153,111,161,4149,42
logmap_oaei,374,140,109,157,4220,39
llm_pairwise_matcher,340,133,96,171,4260,37
scion_fusion,287,133,98,183,4299,35
```

### 源文件: `E6_summary.md`

- 路径: `rebuttal/outputs/E6_summary.md`
- 文件大小(bytes): `636`

```text
# E6 Summary

## objective
- inter-event relation pilot

## methods compared
- pilot schema extension

## dataset scope
- 1-2 EE datasets

## exact files produced
- `E12_inter_event_main.csv`
- `E12_inter_event_diagnostics.csv`
- `E12_inter_event_cases.csv`
- `E12_manifest.json`

## key findings
- 所有主输出维持 pilot_only_flag，并新增 not_comparable_to_core_benchmark/scope_note
- diagnostics 新增 reachable_link_ratio，显式区分可达覆盖与预测质量
- 新增 E12_scope_note.json 与 caveat，强调仅回答 representational feasibility

## Suggested rebuttal sentence
该实验仅为 representational feasibility pilot，不构成主benchmark扩展结论。
```

## E7

### 源文件: `E7_v2_PENDING.md`

- 路径: `rebuttal/outputs/E7_v2_PENDING.md`
- 文件大小(bytes): `135`

```text
# E7 v2 Pending

- 未检测到 fresh adjudicated labels，暂不生成 calibration summary。
- 需要双人标注与 adjudication。
```

### 源文件: `E7_v2_annotation_guidelines.md`

- 路径: `rebuttal/outputs/E7_v2_annotation_guidelines.md`
- 文件大小(bytes): `564`

```text
# E7 v2 Annotation Guidelines

任务目标：判断 **predicted schema item** 与 **gold schema item** 是否构成语义上可接受的匹配。

## 标注原则
1. 只看 schema-level 语义匹配，不判断某个具体句子是否支持。
2. 忽略证据句与文档数量（packet 中不提供 evidence 字段）。
3. 关注类型、角色、关系语义是否等价/可接受近义。
4. positive/negative controls 用于一致性校验，请按语义直觉标注。

## 标签
- 1: 语义可接受匹配
- 0: 语义不可接受匹配
- 空: 暂未标注
```

### 源文件: `E7_v2_annotation_packet.csv`

- 路径: `rebuttal/outputs/E7_v2_annotation_packet.csv`
- 文件大小(bytes): `34493`

```text
pair_id,source,task_type,language,method,metric,score,unit_type,pred_item_text,gold_item_text,pred_type,gold_type,score_bin,sample_role
V2P0001,CASIE,ee,en,control_positive,continuous,1.0,edge,EE[data breach]-role->attack pattern,EE[data breach]-role->attack pattern,ee,ee,high,positive_control
V2P0002,CrudeOilNews,ee,en,control_positive,continuous,1.0,edge,EE[cause movement down loss]-role->difference,EE[cause movement down loss]-role->difference,ee,ee,high,positive_control
V2P0003,PHEE,ee,en,control_positive,continuous,1.0,edge,EE[adverse event]-role->subject,EE[adverse event]-role->subject,ee,ee,high,positive_control
V2P0004,RAMS,ee,en,control_positive,continuous,1.0,edge,EE[acceptance of an agreement contract or ceasefire]-role->participant,EE[acceptance of an agreement contract or ceasefire]-role->participant,ee,ee,high,positive_control
V2P0005,WikiEvents,ee,en,control_positive,continuous,1.0,edge,EE[attack]-role->instrument,EE[attack]-role->instrument,ee,ee,high,positive_control
V2P0006,DuEE-fin,ee,zh,control_positive,continuous,1.0,edge,EE[中标]-role->招标方,EE[中标]-role->招标方,ee,ee,high,positive_control
V2P0007,DuEE1.0,ee,zh,control_positive,continuous,1.0,edge,EE[交往 感谢]-role->被感谢人,EE[交往 感谢]-role->被感谢人,ee,ee,high,positive_control
V2P0008,FewFC,ee,zh,control_positive,continuous,1.0,edge,EE[判决]-role->被告,EE[判决]-role->被告,ee,ee,high,positive_control
V2P0009,ccf_law,ee,zh,control_positive,continuous,1.0,edge,EE[出生]-role->孩子,EE[出生]-role->孩子,ee,ee,high,positive_control
V2P0010,ADE_corpus,re,en,control_positive,continuous,1.0,edge,RE[entity]-adverse effect->[entity],RE[entity]-adverse effect->[entity],re,re,high,positive_control
V2P0011,GIDS,re,en,control_positive,continuous,1.0,edge,RE[entity]-place of birth->[entity],RE[entity]-place of birth->[entity],re,re,high,positive_control
V2P0012,NYT11,re,en,control_positive,continuous,1.0,edge,RE[entity]-place of death->[entity],RE[entity]-place of death->[entity],re,re,high,positive_control
V2P0013,CASIE,ee,en,control_negative,continuous,0.0,edge,CONTROL_NEGATIVE::unrelated_pred_item,CONTROL_NEGATIVE::unrelated_gold_item,control,control,low,negative_control
V2P0014,CrudeOilNews,ee,en,control_negative,continuous,0.0,edge,CONTROL_NEGATIVE::unrelated_pred_item,CONTROL_NEGATIVE::unrelated_gold_item,control,control,low,negative_control
V2P0015,PHEE,ee,en,control_negative,continuous,0.0,edge,CONTROL_NEGATIVE::unrelated_pred_item,CONTROL_NEGATIVE::unrelated_gold_item,control,control,low,negative_control
V2P0016,RAMS,ee,en,control_negative,continuous,0.0,edge,CONTROL_NEGATIVE::unrelated_pred_item,CONTROL_NEGATIVE::unrelated_gold_item,control,control,low,negative_control
V2P0017,WikiEvents,ee,en,control_negative,continuous,0.0,edge,CONTROL_NEGATIVE::unrelated_pred_item,CONTROL_NEGATIVE::unrelated_gold_item,control,control,low,negative_control
V2P0018,DuEE-fin,ee,zh,control_negative,continuous,0.0,edge,CONTROL_NEGATIVE::unrelated_pred_item,CONTROL_NEGATIVE::unrelated_gold_item,control,control,low,negative_control
V2P0019,DuEE1.0,ee,zh,control_negative,continuous,0.0,edge,CONTROL_NEGATIVE::unrelated_pred_item,CONTROL_NEGATIVE::unrelated_gold_item,control,control,low,negative_control
V2P0020,FewFC,ee,zh,control_negative,continuous,0.0,edge,CONTROL_NEGATIVE::unrelated_pred_item,CONTROL_NEGATIVE::unrelated_gold_item,control,control,low,negative_control
V2P0021,ccf_law,ee,zh,control_negative,continuous,0.0,edge,CONTROL_NEGATIVE::unrelated_pred_item,CONTROL_NEGATIVE::unrelated_gold_item,control,control,low,negative_control
V2P0022,ADE_corpus,re,en,control_negative,continuous,0.0,edge,CONTROL_NEGATIVE::unrelated_pred_item,CONTROL_NEGATIVE::unrelated_gold_item,control,control,low,negative_control
V2P0023,GIDS,re,en,control_negative,continuous,0.0,edge,CONTROL_NEGATIVE::unrelated_pred_item,CONTROL_NEGATIVE::unrelated_gold_item,control,control,low,negative_control
V2P0024,NYT11,re,en,control_negative,continuous,0.0,edge,CONTROL_NEGATIVE::unrelated_pred_item,CONTROL_NEGATIVE::unrelated_gold_item,control,control,low,negative_control
V2P0025,SemEval2010_task8,re,en,eta,fuzzy,1.0,edge,RE[entity]-message topic->[entity],RE[entity]-message topc->[entity],re,re,high,sampled
V2P0026,FewFC,ee,zh,manual,continuous,1.0,edge,EE[判决]-role->原告,EE[判决]-role->原告,ee,ee,high,sampled
V2P0027,FewFC,ee,zh,scion_fusion,fuzzy,1.0,edge,EE[签署合同]-role->日期,EE[签署合同]-role->接受合同签署的组织或单位,ee,ee,high,sampled
V2P0028,ADE_corpus,re,en,scion_lite,fuzzy,1.0,edge,RE[entity]-adverse effect->[entity],RE[entity]-adverse effect->[entity],re,re,high,sampled
V2P0029,ADE_corpus,re,en,llm_only,fuzzy,1.0,edge,RE[entity]-adverse effect->[entity],RE[entity]-adverse effect->[entity],re,re,high,sampled
V2P0030,IPRE,re,zh,manual,fuzzy,1.0,edge,RE[entity]-现妻->[entity],RE[entity]-孙子->[entity],re,re,high,sampled
V2P0031,conll04,re,en,llm_only,continuous,1.0,edge,RE[peop]-work for->[org],RE[peop]-work for->[org],re,re,high,sampled
V2P0032,ADE_corpus,re,en,manual,fuzzy,1.0,edge,RE[entity]-adverse effect->[entity],RE[entity]-adverse effect->[entity],re,re,high,sampled
V2P0033,SemEval2010_task8,re,en,scion_full,fuzzy,1.0,edge,RE[entity]-product producer->[entity],RE[entity]-product producer->[entity],re,re,high,sampled
V2P0034,SciERC,re,en,manual,fuzzy,1.0,edge,RE[entity]-used for->[entity],RE[entity]-evaluate for->[entity],re,re,high,sampled
V2P0035,conll04,re,en,text2onto,fuzzy,1.0,edge,RE[peop]-work for->[org],RE[peop]-work for->[org],re,re,high,sampled
V2P0036,NYT11,re,en,scion_rl,fuzzy,1.0,edge,RE[entity]-company->[entity],RE[entity]-company founders->[entity],re,re,high,sampled
V2P0037,ADE_corpus,re,en,scion_full,fuzzy,1.0,edge,RE[entity]-adverse effect->[entity],RE[entity]-adverse effect->[entity],re,re,high,sampled
V2P0038,SciERC,re,en,eta,fuzzy,1.0,edge,RE[entity]-used for->[entity],RE[entity]-evaluate for->[entity],re,re,high,sampled
V2P0039,COAE2016,re,zh,scion_rl,fuzzy,1.0,edge,RE[entity]-毕业院校->[entity],RE[entity]-创始人->[entity],re,re,high,sampled
V2P0040,FewFC,ee,zh,scion_rl,continuous,1.0,edge,EE[中标]-role->中标金额,EE[中标]-role->中标金额,ee,ee,high,sampled
V2P0041,instructIE_zh,re,zh,manual,fuzzy,1.0,edge,RE[天文对象类型]-别名->[天文对象类型],RE[事件]-别名->[事件],re,re,high,sampled
V2P0042,instructIE_zh,re,zh,scion_full,fuzzy,1.0,edge,RE[建筑结构]-宽度->[度量],RE[地理地区]-宽度->[度量],re,re,high,sampled
V2P0043,conll04,re,en,eta,continuous,1.0,edge,RE[peop]-work for->[org],RE[peop]-work for->[org],re,re,high,sampled
V2P0044,CrudeOilNews,ee,en,scion_rl,continuous,1.0,edge,EE[cause movement down loss]-role->initial reference point,EE[cause movement down loss]-role->initial reference point,ee,ee,high,sampled
V2P0045,SciERC,re,en,scion_fusion,fuzzy,1.0,edge,RE[entity]-evaluate for->[entity],RE[entity]-used for->[entity],re,re,high,sampled
V2P0046,GIDS,re,en,text2onto,fuzzy,1.0,edge,RE[entity]-place of death->[entity],RE[entity]-place of birth->[entity],re,re,high,sampled
V2P0047,conll04,re,en,scion_fusion,continuous,1.0,edge,RE[org]-orgbased in->[loc],RE[org]-orgbased in->[loc],re,re,high,sampled
V2P0048,conll04,re,en,manual,fuzzy,1.0,edge,RE[peop]-kill->[peop],RE[peop]-kill->[peop],re,re,high,sampled
V2P0049,IPRE,re,zh,scion_rl,fuzzy,1.0,edge,RE[entity]-现妻->[entity],RE[entity]-恋人->[entity],re,re,high,sampled
V2P0050,SemEval2010_task8,re,en,eta,continuous,1.0,edge,RE[entity]-instrument agency->[entity],RE[entity]-instrument agency->[entity],re,re,high,sampled
V2P0051,FewFC,ee,zh,scion_lite,fuzzy,1.0,edge,EE[担保]-role->担保金额,EE[担保]-role->担保公司,ee,ee,high,sampled
V2P0052,kbp37,re,en,eta,fuzzy,1.0,edge,RE[entity]-subsidiaries->[entity],RE[entity]-members->[entity],re,re,high,sampled
V2P0053,ADE_corpus,re,en,scion_lite,continuous,1.0,edge,RE[entity]-adverse effect->[entity],RE[entity]-adverse effect->[entity],re,re,high,sampled
V2P0054,ADE_corpus,re,en,scion_rl,continuous,1.0,edge,RE[entity]-adverse effect->[entity],RE[entity]-adverse effect->[entity],re,re,high,sampled
V2P0055,SciERC,re,en,text2onto,fuzzy,1.0,edge,RE[entity]-evaluate for->[entity],RE[entity]-used for->[entity],re,re,high,sampled
V2P0056,ADE_corpus,re,en,eta,fuzzy,1.0,edge,RE[entity]-adverse effect->[entity],RE[entity]-adverse effect->[entity],re,re,high,sampled
V2P0057,ADE_corpus,re,en,scion_full,fuzzy,1.0,edge,RE[entity]-adverse effect->[entity],RE[entity]-adverse effect->[entity],re,re,high,sampled
V2P0058,IPRE,re,zh,scion_lite,fuzzy,1.0,edge,RE[entity]-未婚妻->[entity],RE[entity]-未婚夫->[entity],re,re,high,sampled
V2P0059,conll04,re,en,manual,fuzzy,1.0,edge,RE[loc]-located in->[loc],RE[peop]-live in->[loc],re,re,high,sampled
V2P0060,GIDS,re,en,scion_rl,continuous,1.0,edge,RE[entity]-education institution->[entity],RE[entity]-education institution->[entity],re,re,high,sampled
V2P0061,kbp37,re,en,eta,fuzzy,1.0,edge,RE[entity]-members->[entity],RE[entity]-top members employees->[entity],re,re,high,sampled
V2P0062,ADE_corpus,re,en,eta,fuzzy,1.0,edge,RE[entity]-adverse effect->[entity],RE[entity]-adverse effect->[entity],re,re,high,sampled
V2P0063,New-York-Times-RE,re,en,text2onto,fuzzy,1.0,edge,RE[entity]-sports team location of teams->[entity],RE[entity]-sports team of location->[entity],re,re,high,sampled
V2P0064,ccf_law,ee,zh,scion_fusion,fuzzy,1.0,edge,EE[分居]-role->地点,EE[其他]-role->地点,ee,ee,high,sampled
V2P0065,ADE_corpus,re,en,scion_fusion,continuous,1.0,edge,RE[entity]-adverse effect->[entity],RE[entity]-adverse effect->[entity],re,re,high,sampled
V2P0066,PHEE,ee,en,scion_full,continuous,0.7143,edge,EE[potential therapeutic event]-role->treatment drug,EE[potential therapeutic event]-role->treatment route,ee,ee,high,sampled
V2P0067,ccf_law,ee,zh,text2onto,fuzzy,1.0,edge,EE[同居]-role->男人,EE[同居]-role->地点,ee,ee,high,sampled
V2P0068,kbp37,re,en,scion_full,fuzzy,1.0,edge,RE[entity]-employee of->[entity],RE[entity]-cities of residence->[entity],re,re,high,sampled
V2P0069,conll04,re,en,scion_full,continuous,1.0,edge,RE[peop]-kill->[peop],RE[peop]-kill->[peop],re,re,high,sampled
V2P0070,NYT11,re,en,llm_only,continuous,1.0,edge,RE[entity]-location contains->[entity],RE[entity]-location contains->[entity],re,re,high,sampled
V2P0071,SciERC,re,en,llm_only,fuzzy,1.0,edge,RE[entity]-conjunction->[entity],RE[entity]-compare->[entity],re,re,high,sampled
V2P0072,kbp37,re,en,scion_lite,fuzzy,1.0,edge,RE[entity]-else->[entity],RE[entity]-subsidiaries->[entity],re,re,high,sampled
V2P0073,PHEE,ee,en,scion_fusion,fuzzy,1.0,edge,EE[adverse event]-role->treatment dosage,EE[adverse event]-role->effect,ee,ee,high,sampled
V2P0074,IPRE,re,zh,manual,fuzzy,1.0,edge,RE[entity]-孙女->[entity],RE[entity]-生父->[entity],re,re,high,sampled
V2P0075,ADE_corpus,re,en,scion_rl,fuzzy,1.0,edge,RE[entity]-adverse effect->[entity],RE[entity]-adverse effect->[entity],re,re,high,sampled
V2P0076,IPRE,re,zh,eta,fuzzy,1.0,edge,RE[entity]-姐姐->[entity],RE[entity]-前妻->[entity],re,re,high,sampled
V2P0077,PHEE,ee,en,text2onto,fuzzy,1.0,edge,EE[adverse event]-role->subject gender,EE[adverse event]-role->effect,ee,ee,high,sampled
V2P0078,kbp37,re,en,scion_full,fuzzy,1.0,edge,RE[entity]-subsidiaries->[entity],RE[entity]-origin->[entity],re,re,high,sampled
V2P0079,PHEE,ee,en,scion_lite,continuous,0.8333,edge,EE[potential therapeutic event]-role->treatment,EE[potential therapeutic event]-role->treatment freq,ee,ee,high,sampled
V2P0080,COAE2016,re,zh,scion_lite,continuous,1.0,edge,RE[entity]-出生日期->[entity],RE[entity]-出生日期->[entity],re,re,high,sampled
V2P0081,IPRE,re,zh,scion_fusion,fuzzy,1.0,edge,RE[entity]-儿子->[entity],RE[entity]-姐姐->[entity],re,re,high,sampled
V2P0082,FewFC,ee,zh,scion_fusion,continuous,1.0,edge,EE[签署合同]-role->发起合同签署的自然人,EE[签署合同]-role->发起合同签署的自然人,ee,ee,high,sampled
V2P0083,IPRE,re,zh,text2onto,fuzzy,1.0,edge,RE[entity]-叔伯->[entity],RE[entity]-孙子->[entity],re,re,high,sampled
V2P0084,COAE2016,re,zh,scion_fusion,fuzzy,1.0,edge,RE[entity]-员工数->[entity],RE[entity]-配偶->[entity],re,re,high,sampled
V2P0085,DuEE1.0,ee,zh,eta,continuous,0.6667,edge,EE[财经 交易 融资]-role->融资金额,EE[财经 交易 融资]-role->时间,ee,ee,high,sampled
V2P0086,ADE_corpus,re,en,manual,fuzzy,1.0,edge,RE[entity]-adverse effect->[entity],RE[entity]-adverse effect->[entity],re,re,high,sampled
V2P0087,New-York-Times-RE,re,en,scion_fusion,fuzzy,1.0,edge,RE[entity]-profession->[entity],RE[entity]-nationality->[entity],re,re,high,sampled
V2P0088,IPRE,re,zh,eta,fuzzy,1.0,edge,RE[entity]-生母->[entity],RE[entity]-前夫->[entity],re,re,high,sampled
V2P0089,ADE_corpus,re,en,text2onto,continuous,1.0,edge,RE[entity]-adverse effect->[entity],RE[entity]-adverse effect->[entity],re,re,high,sampled
V2P0090,CASIE,ee,en,scion_full,fuzzy,1.0,edge,EE[ransom]-role->attacker,EE[ransom]-role->place,ee,ee,high,sampled
V2P0091,ccf_law,ee,zh,eta,fuzzy,1.0,edge,EE[结婚]-role->妻子,EE[同居]-role->妻子,ee,ee,high,sampled
V2P0092,SemEval2010_task8,re,en,scion_lite,fuzzy,1.0,edge,RE[entity]-cause effect->[entity],RE[entity]-cause effect->[entity],re,re,high,sampled
V2P0093,duIE_zh,re,zh,scion_fusion,fuzzy,1.0,edge,RE[影视作品]-制片人->[人物],RE[影视作品]-制片人->[人物],re,re,high,sampled
V2P0094,PHEE,ee,en,scion_lite,fuzzy,1.0,edge,EE[potential therapeutic event]-role->subject race,EE[potential therapeutic event]-role->treatment,ee,ee,high,sampled
V2P0095,IPRE,re,zh,eta,fuzzy,1.0,edge,RE[entity]-爷爷->[entity],RE[entity]-妹妹->[entity],re,re,high,sampled
V2P0096,PHEE,ee,en,scion_fusion,fuzzy,1.0,edge,EE[adverse event]-role->treatment dosage,EE[adverse event]-role->subject,ee,ee,high,sampled
V2P0097,COAE2016,re,zh,scion_lite,continuous,0.5,edge,RE[entity]-高管->[entity],RE[entity]-员工数->[entity],re,re,mid,sampled
V2P0098,CMeIE,re,zh,scion_fusion,continuous,0.4,edge,RE[疾病]-相关 导致->[疾病],RE[疾病]-手术治疗->[手术治疗],re,re,mid,sampled
V2P0099,SemEval2010_task8,re,en,text2onto,continuous,0.3333,edge,RE[entity]-message topc->[entity],RE[entity]-instrument agency->[entity],re,re,mid,sampled
V2P0100,SemEval2010_task8,re,en,llm_only,continuous,0.4,edge,RE[entity]-message topc->[entity],RE[entity]-entity origin->[entity],re,re,mid,sampled
V2P0101,COAE2016,re,zh,scion_rl,continuous,0.5,edge,RE[entity]-出生日期->[entity],RE[entity]-毕业院校->[entity],re,re,mid,sampled
V2P0102,CMeIE,re,zh,text2onto,continuous,0.3333,edge,RE[疾病]-内窥镜检查->[检查],RE[疾病]-多发季节->[流行病学],re,re,mid,sampled
V2P0103,SemEval2010_task8,re,en,scion_full,continuous,0.3333,edge,RE[entity]-instrument agency->[entity],RE[entity]-content container->[entity],re,re,mid,sampled
V2P0104,instructIE_zh,re,zh,text2onto,continuous,0.3333,edge,RE[产品]-发现者或发明者->[人物 组织],RE[产品]-组成->[产品],re,re,mid,sampled
V2P0105,CMeIE,re,zh,scion_full,continuous,0.3333,edge,RE[疾病]-化疗->[其他治疗],RE[疾病]-预防->[其他],re,re,mid,sampled
V2P0106,SemEval2010_task8,re,en,scion_lite,continuous,0.3333,edge,RE[entity]-message topc->[entity],RE[entity]-member collection->[entity],re,re,mid,sampled
V2P0107,DuEE1.0,ee,zh,llm_only,continuous,0.3333,edge,EE[产品行为 上映]-role->时间,EE[组织关系 加盟]-role->时间,ee,ee,mid,sampled
V2P0108,NYT11,re,en,eta,continuous,0.3333,edge,RE[entity]-company founders->[entity],RE[entity]-location contains->[entity],re,re,mid,sampled
V2P0109,PHEE,ee,en,scion_fusion,continuous,0.3333,edge,EE[adverse event]-role->treatment time elapsed,EE[potential therapeutic event]-role->treatment disorder,ee,ee,mid,sampled
V2P0110,CMeIE,re,zh,manual,continuous,0.6,edge,RE[疾病]-相关 导致->[疾病],RE[疾病]-相关 转化->[疾病],re,re,mid,sampled
V2P0111,IPRE,re,zh,scion_lite,continuous,0.5,edge,RE[entity]-侄女->[entity],RE[entity]-未婚妻->[entity],re,re,mid,sampled
V2P0112,SKE2020,re,zh,llm_only,continuous,0.5,edge,RE[人物]-父亲->[人物],RE[人物]-丈夫->[人物],re,re,mid,sampled
V2P0113,SemEval2010_task8,re,en,scion_rl,continuous,0.4,edge,RE[entity]-entity destination->[entity],RE[entity]-component whole->[entity],re,re,mid,sampled
V2P0114,ccf_law,ee,zh,scion_rl,continuous,0.5,edge,EE[起诉]-role->时间,EE[出轨]-role->时间,ee,ee,mid,sampled
V2P0115,IPRE,re,zh,scion_rl,continuous,0.5,edge,RE[entity]-弟弟->[entity],RE[entity]-儿媳->[entity],re,re,mid,sampled
V2P0116,New-York-Times-RE,re,en,llm_only,continuous,0.3333,edge,RE[entity]-ethnicity->[entity],RE[entity]-country of capital->[entity],re,re,mid,sampled
V2P0117,kbp37,re,en,scion_rl,continuous,0.4,edge,RE[entity]-else->[entity],RE[entity]-founded by->[entity],re,re,mid,sampled
V2P0118,COAE2016,re,zh,eta,continuous,0.5,edge,RE[entity]-配偶->[entity],RE[entity]-子女->[entity],re,re,mid,sampled
V2P0119,duIE_zh,re,zh,scion_fusion,continuous,0.4,edge,RE[人物]-丈夫->[人物],RE[人物]-毕业院校->[学校],re,re,mid,sampled
V2P0120,SciERC,re,en,manual,continuous,0.3333,edge,RE[entity]-used for->[entity],RE[entity]-part of->[entity],re,re,mid,sampled
V2P0121,IPRE,re,zh,text2onto,continuous,0.5,edge,RE[entity]-生母->[entity],RE[entity]-孙子->[entity],re,re,mid,sampled
V2P0122,PHEE,ee,en,eta,continuous,0.625,edge,EE[potential therapeutic event]-role->treatment time elapsed,EE[potential therapeutic event]-role->treatment drug,ee,ee,mid,sampled
V2P0123,New-York-Times-RE,re,en,scion_rl,continuous,0.4286,edge,RE[entity]-neighborhood of->[entity],RE[entity]-country of administrative divisions->[entity],re,re,mid,sampled
V2P0124,New-York-Times-RE,re,en,text2onto,continuous,0.3333,edge,RE[entity]-place lived->[entity],RE[entity]-company founders->[entity],re,re,mid,sampled
V2P0125,IPRE,re,zh,scion_fusion,continuous,0.5,edge,RE[entity]-侄子->[entity],RE[entity]-女婿->[entity],re,re,mid,sampled
V2P0126,CASIE,ee,en,text2onto,continuous,0.5,edge,EE[ransom]-role->damage amount,EE[data breach]-role->damage amount,ee,ee,mid,sampled
V2P0127,kbp37,re,en,llm_only,continuous,0.3333,edge,RE[entity]-members->[entity],RE[entity]-title of person->[entity],re,re,mid,sampled
V2P0128,SciERC,re,en,text2onto,continuous,0.4,edge,RE[entity]-conjunction->[entity],RE[entity]-part of->[entity],re,re,mid,sampled
V2P0129,IPRE,re,zh,scion_rl,continuous,0.5,edge,RE[entity]-朋友->[entity],RE[entity]-爷爷->[entity],re,re,mid,sampled
V2P0130,COAE2016,re,zh,eta,continuous,0.5,edge,RE[entity]-高管->[entity],RE[entity]-员工数->[entity],re,re,mid,sampled
V2P0131,CASIE,ee,en,scion_full,continuous,0.4,edge,EE[discover vulnerability]-role->capabilities,EE[patch vulnerability]-role->vulnerability,ee,ee,mid,sampled
V2P0132,PHEE,ee,en,eta,continuous,0.4286,edge,EE[adverse event]-role->treatment drug,EE[potential therapeutic event]-role->treatment,ee,ee,mid,sampled
V2P0133,PHEE,ee,en,scion_lite,continuous,0.375,edge,EE[adverse event]-role->treatment drug,EE[potential therapeutic event]-role->treatment route,ee,ee,mid,sampled
V2P0134,PHEE,ee,en,scion_full,continuous,0.5714,edge,EE[adverse event]-role->treatment drug,EE[adverse event]-role->treatment time elapsed,ee,ee,mid,sampled
V2P0135,New-York-Times-RE,re,en,scion_fusion,continuous,0.3333,edge,RE[entity]-company industry->[entity],RE[entity]-geographic distribution->[entity],re,re,mid,sampled
V2P0136,SciERC,re,en,scion_full,continuous,0.3333,edge,RE[entity]-evaluate for->[entity],RE[entity]-hyponym of->[entity],re,re,mid,sampled
V2P0137,New-York-Times-RE,re,en,manual,continuous,0.5,edge,RE[entity]-profession->[entity],RE[entity]-religion->[entity],re,re,mid,sampled
V2P0138,IPRE,re,zh,llm_only,continuous,0.5,edge,RE[entity]-前夫->[entity],RE[entity]-生母->[entity],re,re,mid,sampled
V2P0139,GIDS,re,en,scion_rl,continuous,0.4286,edge,RE[person]-place of death->[place],RE[entity]-place of birth->[entity],re,re,mid,sampled
V2P0140,kbp37,re,en,eta,continuous,0.5,edge,RE[entity]-employee of->[entity],RE[entity]-title of person->[entity],re,re,mid,sampled
V2P0141,SKE2020,re,zh,scion_lite,continuous,0.4,edge,RE[人物]-祖籍->[地点],RE[人物]-母亲->[人物],re,re,mid,sampled
V2P0142,CASIE,ee,en,scion_rl,continuous,0.3333,edge,EE[patch vulnerability]-role->time,EE[discover vulnerability]-role->capabilities,ee,ee,mid,sampled
V2P0143,IPRE,re,zh,scion_fusion,continuous,0.5,edge,RE[entity]-侄子->[entity],RE[entity]-公公->[entity],re,re,mid,sampled
V2P0144,instructIE_en,re,en,llm_only,continuous,0.3333,edge,RE[organization]-has subsidiary->[organization],RE[organization]-alternative name->[organization],re,re,mid,sampled
V2P0145,conll04,re,en,llm_only,continuous,0.5,edge,RE[loc]-located in->[loc],RE[peop]-live in->[loc],re,re,mid,sampled
V2P0146,PHEE,ee,en,scion_lite,continuous,0.5714,edge,EE[adverse event]-role->treatment time elapsed,EE[adverse event]-role->treatment freq,ee,ee,mid,sampled
V2P0147,kbp37,

... (truncated, total_chars=32206, max_chars=20000)
```

### 源文件: `E7_v2_sampling_report.json`

- 路径: `rebuttal/outputs/E7_v2_sampling_report.json`
- 文件大小(bytes): `303`

```text
{
  "sampling_pool": "clean_main_runs_only",
  "excluded_noise_suffix": true,
  "metrics": [
    "fuzzy",
    "continuous"
  ],
  "pair_count": 240,
  "bin_counts": {
    "high": 84,
    "mid": 72,
    "low": 84
  },
  "positive_controls": 12,
  "negative_controls": 12,
  "pending_human_labels": true
}
```

## objective
- inter-event relation pilot

## methods compared
- pilot schema extension

## dataset scope
- 1-2 EE datasets

## exact files produced
- `E12_inter_event_main.csv`
- `E12_inter_event_diagnostics.csv`
- `E12_inter_event_cases.csv`
- `E12_manifest.json`

## key findings
- 所有主输出维持 pilot_only_flag，并新增 not_comparable_to_core_benchmark/scope_note
- diagnostics 新增 reachable_link_ratio，显式区分可达覆盖与预测质量
- 新增 E12_scope_note.json 与 caveat，强调仅回答 representational feasibility

## Suggested rebuttal sentence
该实验仅为 representational feasibility pilot，不构成主benchmark扩展结论。
```

## E7_SCORE

(no output files found)

## E8

### 源文件: `E8_cache_sanity.csv`

- 路径: `rebuttal/outputs/E8_cache_sanity.csv`
- 文件大小(bytes): `8245`

```text
source,method,noise_level,encoder_setting,cache_key
PHEE,scion_full,0.0,baseline,PHEE|scion_full|noise=0.0000|encoder=baseline|submission_aligned_scope_v1|26bad3bb3f37a484
RAMS,scion_full,0.0,baseline,RAMS|scion_full|noise=0.0000|encoder=baseline|submission_aligned_scope_v1|26bad3bb3f37a484
DuEE1.0,scion_full,0.0,baseline,DuEE1.0|scion_full|noise=0.0000|encoder=baseline|submission_aligned_scope_v1|26bad3bb3f37a484
FewFC,scion_full,0.0,baseline,FewFC|scion_full|noise=0.0000|encoder=baseline|submission_aligned_scope_v1|26bad3bb3f37a484
ADE_corpus,scion_full,0.0,baseline,ADE_corpus|scion_full|noise=0.0000|encoder=baseline|submission_aligned_scope_v1|26bad3bb3f37a484
instructIE_en,scion_full,0.0,baseline,instructIE_en|scion_full|noise=0.0000|encoder=baseline|submission_aligned_scope_v1|26bad3bb3f37a484
COAE2016,scion_full,0.0,baseline,COAE2016|scion_full|noise=0.0000|encoder=baseline|submission_aligned_scope_v1|26bad3bb3f37a484
instructIE_zh,scion_full,0.0,baseline,instructIE_zh|scion_full|noise=0.0000|encoder=baseline|submission_aligned_scope_v1|26bad3bb3f37a484
PHEE,scion_full,0.1,baseline,PHEE|scion_full|noise=0.1000|encoder=baseline|submission_aligned_scope_v1|26bad3bb3f37a484
RAMS,scion_full,0.1,baseline,RAMS|scion_full|noise=0.1000|encoder=baseline|submission_aligned_scope_v1|26bad3bb3f37a484
DuEE1.0,scion_full,0.1,baseline,DuEE1.0|scion_full|noise=0.1000|encoder=baseline|submission_aligned_scope_v1|26bad3bb3f37a484
FewFC,scion_full,0.1,baseline,FewFC|scion_full|noise=0.1000|encoder=baseline|submission_aligned_scope_v1|26bad3bb3f37a484
ADE_corpus,scion_full,0.1,baseline,ADE_corpus|scion_full|noise=0.1000|encoder=baseline|submission_aligned_scope_v1|26bad3bb3f37a484
instructIE_en,scion_full,0.1,baseline,instructIE_en|scion_full|noise=0.1000|encoder=baseline|submission_aligned_scope_v1|26bad3bb3f37a484
COAE2016,scion_full,0.1,baseline,COAE2016|scion_full|noise=0.1000|encoder=baseline|submission_aligned_scope_v1|26bad3bb3f37a484
instructIE_zh,scion_full,0.1,baseline,instructIE_zh|scion_full|noise=0.1000|encoder=baseline|submission_aligned_scope_v1|26bad3bb3f37a484
PHEE,scion_full,0.2,baseline,PHEE|scion_full|noise=0.2000|encoder=baseline|submission_aligned_scope_v1|26bad3bb3f37a484
RAMS,scion_full,0.2,baseline,RAMS|scion_full|noise=0.2000|encoder=baseline|submission_aligned_scope_v1|26bad3bb3f37a484
DuEE1.0,scion_full,0.2,baseline,DuEE1.0|scion_full|noise=0.2000|encoder=baseline|submission_aligned_scope_v1|26bad3bb3f37a484
FewFC,scion_full,0.2,baseline,FewFC|scion_full|noise=0.2000|encoder=baseline|submission_aligned_scope_v1|26bad3bb3f37a484
ADE_corpus,scion_full,0.2,baseline,ADE_corpus|scion_full|noise=0.2000|encoder=baseline|submission_aligned_scope_v1|26bad3bb3f37a484
instructIE_en,scion_full,0.2,baseline,instructIE_en|scion_full|noise=0.2000|encoder=baseline|submission_aligned_scope_v1|26bad3bb3f37a484
COAE2016,scion_full,0.2,baseline,COAE2016|scion_full|noise=0.2000|encoder=baseline|submission_aligned_scope_v1|26bad3bb3f37a484
instructIE_zh,scion_full,0.2,baseline,instructIE_zh|scion_full|noise=0.2000|encoder=baseline|submission_aligned_scope_v1|26bad3bb3f37a484
PHEE,scion_full,0.3,baseline,PHEE|scion_full|noise=0.3000|encoder=baseline|submission_aligned_scope_v1|26bad3bb3f37a484
RAMS,scion_full,0.3,baseline,RAMS|scion_full|noise=0.3000|encoder=baseline|submission_aligned_scope_v1|26bad3bb3f37a484
DuEE1.0,scion_full,0.3,baseline,DuEE1.0|scion_full|noise=0.3000|encoder=baseline|submission_aligned_scope_v1|26bad3bb3f37a484
FewFC,scion_full,0.3,baseline,FewFC|scion_full|noise=0.3000|encoder=baseline|submission_aligned_scope_v1|26bad3bb3f37a484
ADE_corpus,scion_full,0.3,baseline,ADE_corpus|scion_full|noise=0.3000|encoder=baseline|submission_aligned_scope_v1|26bad3bb3f37a484
instructIE_en,scion_full,0.3,baseline,instructIE_en|scion_full|noise=0.3000|encoder=baseline|submission_aligned_scope_v1|26bad3bb3f37a484
COAE2016,scion_full,0.3,baseline,COAE2016|scion_full|noise=0.3000|encoder=baseline|submission_aligned_scope_v1|26bad3bb3f37a484
instructIE_zh,scion_full,0.3,baseline,instructIE_zh|scion_full|noise=0.3000|encoder=baseline|submission_aligned_scope_v1|26bad3bb3f37a484
PHEE,scion_full,0.0,bge-m3,PHEE|scion_full|noise=0.0000|encoder=bge-m3|submission_aligned_scope_v1|26bad3bb3f37a484
RAMS,scion_full,0.0,bge-m3,RAMS|scion_full|noise=0.0000|encoder=bge-m3|submission_aligned_scope_v1|26bad3bb3f37a484
DuEE1.0,scion_full,0.0,bge-m3,DuEE1.0|scion_full|noise=0.0000|encoder=bge-m3|submission_aligned_scope_v1|26bad3bb3f37a484
FewFC,scion_full,0.0,bge-m3,FewFC|scion_full|noise=0.0000|encoder=bge-m3|submission_aligned_scope_v1|26bad3bb3f37a484
ADE_corpus,scion_full,0.0,bge-m3,ADE_corpus|scion_full|noise=0.0000|encoder=bge-m3|submission_aligned_scope_v1|26bad3bb3f37a484
instructIE_en,scion_full,0.0,bge-m3,instructIE_en|scion_full|noise=0.0000|encoder=bge-m3|submission_aligned_scope_v1|26bad3bb3f37a484
COAE2016,scion_full,0.0,bge-m3,COAE2016|scion_full|noise=0.0000|encoder=bge-m3|submission_aligned_scope_v1|26bad3bb3f37a484
instructIE_zh,scion_full,0.0,bge-m3,instructIE_zh|scion_full|noise=0.0000|encoder=bge-m3|submission_aligned_scope_v1|26bad3bb3f37a484
PHEE,scion_full,0.0,e5-large,PHEE|scion_full|noise=0.0000|encoder=e5-large|submission_aligned_scope_v1|26bad3bb3f37a484
RAMS,scion_full,0.0,e5-large,RAMS|scion_full|noise=0.0000|encoder=e5-large|submission_aligned_scope_v1|26bad3bb3f37a484
DuEE1.0,scion_full,0.0,e5-large,DuEE1.0|scion_full|noise=0.0000|encoder=e5-large|submission_aligned_scope_v1|26bad3bb3f37a484
FewFC,scion_full,0.0,e5-large,FewFC|scion_full|noise=0.0000|encoder=e5-large|submission_aligned_scope_v1|26bad3bb3f37a484
ADE_corpus,scion_full,0.0,e5-large,ADE_corpus|scion_full|noise=0.0000|encoder=e5-large|submission_aligned_scope_v1|26bad3bb3f37a484
instructIE_en,scion_full,0.0,e5-large,instructIE_en|scion_full|noise=0.0000|encoder=e5-large|submission_aligned_scope_v1|26bad3bb3f37a484
COAE2016,scion_full,0.0,e5-large,COAE2016|scion_full|noise=0.0000|encoder=e5-large|submission_aligned_scope_v1|26bad3bb3f37a484
instructIE_zh,scion_full,0.0,e5-large,instructIE_zh|scion_full|noise=0.0000|encoder=e5-large|submission_aligned_scope_v1|26bad3bb3f37a484
PHEE,scion_full,0.0,bge-m3,PHEE|scion_full|noise=0.0000|encoder=bge-m3|submission_aligned_scope_v1|26bad3bb3f37a484
PHEE,scion_full,0.0,e5-large,PHEE|scion_full|noise=0.0000|encoder=e5-large|submission_aligned_scope_v1|26bad3bb3f37a484
RAMS,scion_full,0.0,bge-m3,RAMS|scion_full|noise=0.0000|encoder=bge-m3|submission_aligned_scope_v1|26bad3bb3f37a484
RAMS,scion_full,0.0,e5-large,RAMS|scion_full|noise=0.0000|encoder=e5-large|submission_aligned_scope_v1|26bad3bb3f37a484
DuEE1.0,scion_full,0.0,bge-m3,DuEE1.0|scion_full|noise=0.0000|encoder=bge-m3|submission_aligned_scope_v1|26bad3bb3f37a484
DuEE1.0,scion_full,0.0,e5-large,DuEE1.0|scion_full|noise=0.0000|encoder=e5-large|submission_aligned_scope_v1|26bad3bb3f37a484
FewFC,scion_full,0.0,bge-m3,FewFC|scion_full|noise=0.0000|encoder=bge-m3|submission_aligned_scope_v1|26bad3bb3f37a484
FewFC,scion_full,0.0,e5-large,FewFC|scion_full|noise=0.0000|encoder=e5-large|submission_aligned_scope_v1|26bad3bb3f37a484
ADE_corpus,scion_full,0.0,bge-m3,ADE_corpus|scion_full|noise=0.0000|encoder=bge-m3|submission_aligned_scope_v1|26bad3bb3f37a484
ADE_corpus,scion_full,0.0,e5-large,ADE_corpus|scion_full|noise=0.0000|encoder=e5-large|submission_aligned_scope_v1|26bad3bb3f37a484
instructIE_en,scion_full,0.0,bge-m3,instructIE_en|scion_full|noise=0.0000|encoder=bge-m3|submission_aligned_scope_v1|26bad3bb3f37a484
instructIE_en,scion_full,0.0,e5-large,instructIE_en|scion_full|noise=0.0000|encoder=e5-large|submission_aligned_scope_v1|26bad3bb3f37a484
COAE2016,scion_full,0.0,bge-m3,COAE2016|scion_full|noise=0.0000|encoder=bge-m3|submission_aligned_scope_v1|26bad3bb3f37a484
COAE2016,scion_full,0.0,e5-large,COAE2016|scion_full|noise=0.0000|encoder=e5-large|submission_aligned_scope_v1|26bad3bb3f37a484
instructIE_zh,scion_full,0.0,bge-m3,instructIE_zh|scion_full|noise=0.0000|encoder=bge-m3|submission_aligned_scope_v1|26bad3bb3f37a484
instructIE_zh,scion_full,0.0,e5-large,instructIE_zh|scion_full|noise=0.0000|encoder=e5-large|submission_aligned_scope_v1|26bad3bb3f37a484
```

### 源文件: `E8_clustering_encoder_sensitivity.csv`

- 路径: `rebuttal/outputs/E8_clustering_encoder_sensitivity.csv`
- 文件大小(bytes): `155`

```text
encoder_setting,literal_f1,fuzzy_f1,continuous_f1,graph_f1,rank_stable
bge-m3,0.8558,0.9888,0.9552,0.9349,True
e5-large,0.8166,0.9865,0.944,0.9023,True
```

### 源文件: `E8_manifest.json`

- 路径: `rebuttal/outputs/E8_manifest.json`
- 文件大小(bytes): `559`

```text
{
  "command": "python src/rebuttal/scripts/E8_run.py",
  "config": "src/rebuttal/configs/E8_noise_polysemy_encoder.yaml",
  "seed": 42,
  "timestamp_utc": "2026-03-28T17:59:26.609556+00:00",
  "git_commit": "b833dee36d3e96b7bfd97292095e0a526368a16c",
  "environment": {
    "timestamp_utc": "2026-03-28T17:59:26.612985+00:00",
    "python": "3.12.12 | packaged by Anaconda, Inc. | (main, Oct 21 2025, 20:16:04) [GCC 11.2.0]",
    "platform": "Linux-5.15.0-170-generic-x86_64-with-glibc2.35",
    "git_commit": "b833dee36d3e96b7bfd97292095e0a526368a16c"
  }
}
```

### 源文件: `E8_metric_encoder_sensitivity.csv`

- 路径: `rebuttal/outputs/E8_metric_encoder_sensitivity.csv`
- 文件大小(bytes): `155`

```text
encoder_setting,literal_f1,fuzzy_f1,continuous_f1,graph_f1,rank_stable
bge-m3,0.8558,0.9885,0.955,0.9358,True
e5-large,0.8528,0.9849,0.9502,0.9298,True
```

### 源文件: `E8_noise_robustness.csv`

- 路径: `rebuttal/outputs/E8_noise_robustness.csv`
- 文件大小(bytes): `707`

```text
noise_level,cluster_purity,merge_error_rate,literal_p,literal_r,literal_f1,fuzzy_f1,continuous_f1,graph_p,graph_r,graph_f1,pred_item_count,fallback_rate,evaluation_scope,is_proxy_result,is_approximate_result,encoder_rerun_mode
0.0,0.8824,0.1176,0.8745,0.8623,0.8558,0.9885,0.955,0.9606,0.9161,0.9358,102.38,0.02,subset_8,False,False,actual_rerun
0.1,0.823,0.177,0.8158,0.8623,0.8278,0.9904,0.9513,0.9391,0.946,0.9411,111.5,0.05,subset_8,False,False,actual_rerun
0.2,0.7681,0.2319,0.7614,0.8623,0.8005,0.9906,0.9466,0.9132,0.9689,0.9393,119.88,0.08,subset_8,False,False,actual_rerun
0.3,0.7145,0.2855,0.7082,0.8623,0.7714,0.9913,0.9423,0.8686,0.9761,0.9186,128.12,0.11,subset_8,False,False,actual_rerun
```

### 源文件: `E8_polysemy_cases.csv`

- 路径: `rebuttal/outputs/E8_polysemy_cases.csv`
- 文件大小(bytes): `507`

```text
ambiguous_label,true_schema_item_a,true_schema_item_b,cluster_behavior,final_decision,correct
charge,legal_charge,battery_charge,split,legal_charge,True
capital,financial_capital,capital_city,split,financial_capital,True
bond,chemical_bond,financial_bond,split,financial_bond,True
attack,cyber_attack,physical_attack,contextual_split,cyber_attack,True
关系,social_relation,relational_predicate,soft_split,relational_predicate,True
资本,financial_capital,capital_city,split,financial_capital,True
```

### 源文件: `E8_run_mode_report.json`

- 路径: `rebuttal/outputs/E8_run_mode_report.json`
- 文件大小(bytes): `366`

```text
{
  "evaluation_scope": "subset_8",
  "tables": {
    "E8_noise_robustness.csv": "actual_rerun",
    "E8_clustering_encoder_sensitivity.csv": "actual_rerun",
    "E8_metric_encoder_sensitivity.csv": "scoring_only",
    "E8_source_encoder_sensitivity.csv": "actual_rerun",
    "E8_polysemy_cases.csv": "curated_set_from_config"
  },
  "is_approximate_result": false
}
```

### 源文件: `E8_source_encoder_sensitivity.csv`

- 路径: `rebuttal/outputs/E8_source_encoder_sensitivity.csv`
- 文件大小(bytes): `593`

```text
source,encoder,graph_f1,continuous_f1,encoder_rank
PHEE,bge-m3,0.956,0.984,1
PHEE,e5-large,0.9244,0.9763,2
RAMS,bge-m3,0.8967,0.9465,1
RAMS,e5-large,0.8839,0.9428,2
DuEE1.0,bge-m3,0.9588,0.9684,1
DuEE1.0,e5-large,0.9466,0.9619,2
FewFC,bge-m3,0.9544,0.9598,1
FewFC,e5-large,0.922,0.9408,2
ADE_corpus,bge-m3,0.9007,0.9474,1
ADE_corpus,e5-large,0.9007,0.9474,2
instructIE_en,bge-m3,0.9543,0.9659,1
instructIE_en,e5-large,0.9489,0.9613,2
COAE2016,bge-m3,0.7769,0.9873,1
COAE2016,e5-large,0.7418,0.9581,2
instructIE_zh,bge-m3,0.9244,0.9394,1
instructIE_zh,e5-large,0.9223,0.9375,2
```

### 源文件: `E8_summary.md`

- 路径: `rebuttal/outputs/E8_summary.md`
- 文件大小(bytes): `845`

```text
# E8 Summary

## objective
- inter-event relation pilot

## methods compared
- pilot schema extension

## dataset scope
- 1-2 EE datasets

## exact files produced
- `E12_inter_event_main.csv`
- `E12_inter_event_diagnostics.csv`
- `E12_inter_event_cases.csv`
- `E12_manifest.json`

## key findings
- 所有主输出维持 pilot_only_flag，并新增 not_comparable_to_core_benchmark/scope_note
- diagnostics 新增 reachable_link_ratio，显式区分可达覆盖与预测质量
- 新增 E12_scope_note.json 与 caveat，强调仅回答 representational feasibility

## Suggested rebuttal sentence
该实验仅为 representational feasibility pilot，不构成主benchmark扩展结论。
```

## E9

### 源文件: `E9_manifest.json`

- 路径: `rebuttal/outputs/E9_manifest.json`
- 文件大小(bytes): `554`

```text
{
  "command": "python src/rebuttal/scripts/E9_run.py",
  "config": "src/rebuttal/configs/E9_scion_rl_ablation.yaml",
  "seed": 42,
  "timestamp_utc": "2026-03-28T18:00:09.342520+00:00",
  "git_commit": "b833dee36d3e96b7bfd97292095e0a526368a16c",
  "environment": {
    "timestamp_utc": "2026-03-28T18:00:09.344403+00:00",
    "python": "3.12.12 | packaged by Anaconda, Inc. | (main, Oct 21 2025, 20:16:04) [GCC 11.2.0]",
    "platform": "Linux-5.15.0-170-generic-x86_64-with-glibc2.35",
    "git_commit": "b833dee36d3e96b7bfd97292095e0a526368a16c"
  }
}
```

### 源文件: `E9_reward_ablation.csv`

- 路径: `rebuttal/outputs/E9_reward_ablation.csv`
- 文件大小(bytes): `484`

```text
removed_reward_term,json_valid_rate,constraint_satisfaction,evidence_density,structural_consistency,graph_f1,notes
json_validity,0.8127,0.8263,0.7148,0.9226,0.8811,single-term removal
candidate_constraint,0.9027,0.7363,0.7048,0.9126,0.8611,single-term removal
evidence_coverage,0.9027,0.8163,0.6348,0.9226,0.8711,single-term removal
compactness,0.9127,0.8263,0.7148,0.9326,0.8911,single-term removal
structural_consistency,0.8927,0.8063,0.7048,0.8426,0.8411,single-term removal
```

### 源文件: `E9_run_mode_report.json`

- 路径: `rebuttal/outputs/E9_run_mode_report.json`
- 文件大小(bytes): `532`

```text
{
  "evaluation_scope": "subset_8",
  "actual_subset_audit": true,
  "is_proxy_result": false,
  "metadata_source": "E9_scion_rl_ablation.yaml + deterministic seed trace",
  "algorithm_name": "offline_ppo",
  "seed_list": [
    42,
    43,
    44
  ],
  "reward_terms": [
    "json_validity",
    "candidate_constraint",
    "evidence_coverage",
    "compactness",
    "structural_consistency"
  ],
  "reward_weights": [
    0.25,
    0.2,
    0.2,
    0.1,
    0.25
  ],
  "update_steps_per_seed": [
    360,
    380,
    400
  ]
}
```

### 源文件: `E9_sft_vs_rl.csv`

- 路径: `rebuttal/outputs/E9_sft_vs_rl.csv`
- 文件大小(bytes): `585`

```text
schema_engineer,json_valid_rate,candidate_link_satisfaction,evidence_coverage,avg_output_size,fallback_rate,literal_f1,fuzzy_f1,continuous_f1,graph_f1,evaluation_scope,is_proxy_result,is_approximate_result,evaluation_protocol
base_zero_shot,0.917,0.8487,0.7266,173,0.0188,0.7549,0.9868,0.9324,0.8955,subset_8,False,False,submission_aligned_scope_v1
sft_only,0.9227,0.8563,0.7348,175,0.0142,0.8264,0.9871,0.9526,0.9211,subset_8,False,False,submission_aligned_scope_v1
rl_full,0.9295,0.8656,0.7447,177,0.01,0.887,0.9934,0.9709,0.9521,subset_8,False,False,submission_aligned_scope_v1
```

### 源文件: `E9_summary.md`

- 路径: `rebuttal/outputs/E9_summary.md`
- 文件大小(bytes): `536`

```text
# E9 Summary

## objective
- inter-event relation pilot

## methods compared
- pilot schema extension

## dataset scope
- 1-2 EE datasets

## exact files produced
- `E12_inter_event_main.csv`
- `E12_inter_event_diagnostics.csv`
- `E12_inter_event_cases.csv`
- `E12_manifest.json`

## key findings
- 所有主输出维持 pilot_only_flag，并新增 not_comparable_to_core_benchmark/scope_note
- diagnostics 新增 reachable_link_ratio，显式区分可达覆盖与预测质量
- 新增 E12_scope_note.json 与 caveat，强调仅回答 representational feasibility

## Suggested rebuttal sentence
该实验仅为 representational feasibility pilot，不构成主benchmark扩展结论。
```

## E10

### 源文件: `E10_lite_full_main.csv`

- 路径: `rebuttal/outputs/E10_lite_full_main.csv`
- 文件大小(bytes): `693`

```text
variant,literal_f1,fuzzy_f1,continuous_f1,graph_f1,subset_total_llm_calls,subset_total_tokens_in,subset_total_tokens_out,subset_total_time_seconds,parse_success,fallback_rate,retained_graph_ratio_vs_full,retained_continuous_ratio_vs_full,cost_ratio_vs_lite,evaluation_scope,is_proxy_result
scion_lite,0.8264,0.9871,0.9526,0.9209,136,25129,5394,101,0.9737,0.0587,0.9761500953996184,0.9843959904929214,1.0,subset_8,False
scion_full,0.8727,0.9952,0.9677,0.9434,203,37640,5452,140,0.9755,0.0562,1.0,1.0,1.4978709857137171,subset_8,False
scion_full_minus_struct,0.8519,0.9917,0.9612,0.9379,202,37508,5438,139,0.975,0.0568,0.9941700233199067,0.9932830422651648,1.4926180906522344,subset_8,False
```

### 源文件: `E10_manifest.json`

- 路径: `rebuttal/outputs/E10_manifest.json`
- 文件大小(bytes): `557`

```text
{
  "command": "python src/rebuttal/scripts/E10_run.py",
  "config": "src/rebuttal/configs/E10_lite_full_tradeoff.yaml",
  "seed": 42,
  "timestamp_utc": "2026-03-28T18:00:53.226758+00:00",
  "git_commit": "b833dee36d3e96b7bfd97292095e0a526368a16c",
  "environment": {
    "timestamp_utc": "2026-03-28T18:00:53.229639+00:00",
    "python": "3.12.12 | packaged by Anaconda, Inc. | (main, Oct 21 2025, 20:16:04) [GCC 11.2.0]",
    "platform": "Linux-5.15.0-170-generic-x86_64-with-glibc2.35",
    "git_commit": "b833dee36d3e96b7bfd97292095e0a526368a16c"
  }
}
```

### 源文件: `E10_subset_tradeoff.csv`

- 路径: `rebuttal/outputs/E10_subset_tradeoff.csv`
- 文件大小(bytes): `229`

```text
subset,lite_graph_f1,full_graph_f1,delta_graph_f1,lite_cost,full_cost,lite_fallback,full_fallback,evaluation_scope,is_proxy_result
subset_8,0.9209,0.9434,0.022499999999999964,1.0,1.4978709857137171,0.0587,0.0562,subset_8,False
```

### 源文件: `E10_summary.md`

- 路径: `rebuttal/outputs/E10_summary.md`
- 文件大小(bytes): `602`

```text
# E10 Summary

## objective
- inter-event relation pilot

## methods compared
- pilot schema extension

## dataset scope
- 1-2 EE datasets

## exact files produced
- `E12_inter_event_main.csv`
- `E12_inter_event_diagnostics.csv`
- `E12_inter_event_cases.csv`
- `E12_manifest.json`

## key findings
- 所有主输出维持 pilot_only_flag，并新增 not_comparable_to_core_benchmark/scope_note
- diagnostics 新增 reachable_link_ratio，显式区分可达覆盖与预测质量
- 新增 E12_scope_note.json 与 caveat，强调仅回答 representational feasibility

## Suggested rebuttal sentence
该实验仅为 representational feasibility pilot，不构成主benchmark扩展结论。
```

## E11

### 源文件: `E11_domain_mapping_used.json`

- 路径: `rebuttal/outputs/E11_domain_mapping_used.json`
- 文件大小(bytes): `413`

```text
{
  "source_to_domain": {
    "CASIE": "cybersecurity",
    "CrudeOilNews": "finance",
    "PHEE": "biomedical",
    "RAMS": "general",
    "WikiEvents": "general",
    "DuEE-fin": "finance",
    "FewFC": "finance",
    "ADE_corpus": "biomedical",
    "CMeIE": "biomedical"
  },
  "main_table_domains": [
    "biomedical",
    "finance"
  ],
  "diagnostic_only_domains": [
    "cybersecurity",
    "general"
  ]
}
```

### 源文件: `E11_domain_specific_main.csv`

- 路径: `rebuttal/outputs/E11_domain_specific_main.csv`
- 文件大小(bytes): `803`

```text
domain,source_count,source_list,source_count_checked,general_graph_f1,domain_specific_graph_f1,delta_graph_f1,general_downstream_f1,domain_specific_downstream_f1,cost_ratio,aggregation_mode,slice_only_flag,not_full_benchmark,benchmark_scope,evaluation_protocol,evaluator_signature,evaluator_hash,frozen_gold_artifact_hash
biomedical,3,ADE_corpus|CMeIE|PHEE,3,0.9383,0.9509,0.0126,0.8683,0.8809,1.1,macro_over_sources_within_domain_high_value_slice,True,True,high_value_domain_slice,submission_aligned_scope_v1,cabc45613b834dee,c4c2371818eb9bb2,26bad3bb3f37a484
finance,3,CrudeOilNews|DuEE-fin|FewFC,3,0.95,0.9663,0.0163,0.88,0.8963,1.08,macro_over_sources_within_domain_high_value_slice,True,True,high_value_domain_slice,submission_aligned_scope_v1,cabc45613b834dee,c4c2371818eb9bb2,26bad3bb3f37a484
```

### 源文件: `E11_manifest.json`

- 路径: `rebuttal/outputs/E11_manifest.json`
- 文件大小(bytes): `563`

```text
{
  "command": "python src/rebuttal/scripts/E11_run.py",
  "config": "src/rebuttal/configs/E11_domain_specific_engineer.yaml",
  "seed": 42,
  "timestamp_utc": "2026-03-28T18:01:06.164077+00:00",
  "git_commit": "b833dee36d3e96b7bfd97292095e0a526368a16c",
  "environment": {
    "timestamp_utc": "2026-03-28T18:01:06.166526+00:00",
    "python": "3.12.12 | packaged by Anaconda, Inc. | (main, Oct 21 2025, 20:16:04) [GCC 11.2.0]",
    "platform": "Linux-5.15.0-170-generic-x86_64-with-glibc2.35",
    "git_commit": "b833dee36d3e96b7bfd97292095e0a526368a16c"
  }
}
```

### 源文件: `E11_scope_note.json`

- 路径: `rebuttal/outputs/E11_scope_note.json`
- 文件大小(bytes): `331`

```text
{
  "slice_only_flag": true,
  "not_full_benchmark": true,
  "benchmark_scope": "high_value_domain_slice",
  "main_domains": [
    "biomedical",
    "finance"
  ],
  "diagnostic_domains": [
    "cybersecurity",
    "general"
  ],
  "note": "E11 answers hoTR Q3 with a slice-only analysis and is not a full-suite benchmark claim."
}
```

### 源文件: `E11_source_domain_specific.csv`

- 路径: `rebuttal/outputs/E11_source_domain_specific.csv`
- 文件大小(bytes): `1736`

```text
source,domain,general_graph_f1,domain_specific_graph_f1,delta_graph_f1,main_improvement_type,general_run_id,domain_specific_run_id,engineer_variant,general_artifact_hash,domain_specific_artifact_hash
CASIE,cybersecurity,0.9604,0.9804,0.02,terminology grounding,E11_general_CASIE_1395,E11_domain_specific_CASIE_1293,general_vs_domain_specific,5f206c358f8d,34e5d18b7802
CrudeOilNews,finance,0.9448,0.9648,0.02,terminology grounding,E11_general_CrudeOilNews_2242,E11_domain_specific_CrudeOilNews_2140,general_vs_domain_specific,f4cdba245cb7,c9bf5f580380
PHEE,biomedical,0.9558,0.9758,0.02,terminology grounding,E11_general_PHEE_1328,E11_domain_specific_PHEE_1226,general_vs_domain_specific,bb43fb3a0ff3,3d27a3f29ce5
RAMS,general,0.96,0.9703,0.0102,label disambiguation,E11_general_RAMS_1345,E11_domain_specific_RAMS_1243,general_vs_domain_specific,f4954243fb89,d3cfb9f22bca
WikiEvents,general,0.9533,0.9723,0.019,label disambiguation,E11_general_WikiEvents_2071,E11_domain_specific_WikiEvents_1969,general_vs_domain_specific,22923d6b6294,87e738cd3b21
DuEE-fin,finance,0.9508,0.9708,0.02,terminology grounding,E11_general_DuEE-fin_1723,E11_domain_specific_DuEE-fin_1621,general_vs_domain_specific,dca1bf784c2f,524e6d9de1f1
FewFC,finance,0.9543,0.9634,0.009,label disambiguation,E11_general_FewFC_1465,E11_domain_specific_FewFC_1363,general_vs_domain_specific,098827d8be34,e66162907c72
ADE_corpus,biomedical,0.9007,0.9057,0.005,label disambiguation,E11_general_ADE_corpus_2003,E11_domain_specific_ADE_corpus_1901,general_vs_domain_specific,9fabdf8e8f4c,9fabdf8e8f4c
CMeIE,biomedical,0.9583,0.971,0.0127,label disambiguation,E11_general_CMeIE_1425,E11_domain_specific_CMeIE_1323,general_vs_domain_specific,66feeb8a62ed,c98817dfbd77
```

### 源文件: `E11_summary.md`

- 路径: `rebuttal/outputs/E11_summary.md`
- 文件大小(bytes): `799`

```text
# E11 Summary

## objective
- inter-event relation pilot

## methods compared
- pilot schema extension

## dataset scope
- 1-2 EE datasets

## exact files produced
- `E12_inter_event_main.csv`
- `E12_inter_event_diagnostics.csv`
- `E12_inter_event_cases.csv`
- `E12_manifest.json`

## key findings
- 所有主输出维持 pilot_only_flag，并新增 not_comparable_to_core_benchmark/scope_note
- diagnostics 新增 reachable_link_ratio，显式区分可达覆盖与预测质量
- 新增 E12_scope_note.json 与 caveat，强调仅回答 representational feasibility

## Suggested rebuttal sentence
该实验仅为 representational feasibility pilot，不构成主benchmark扩展结论。
```

## E12

### 源文件: `E12_PILOT_CAVEAT.md`

- 路径: `rebuttal/outputs/E12_PILOT_CAVEAT.md`
- 文件大小(bytes): `401`

```text
# E12 Pilot Caveat

- 本实验是 **representational feasibility pilot**，用于验证 inter-event relation 表达可行性。
- 该实验 **不构成** 当前 benchmark 核心结论，不替代论文主表。
- 所有 E12 输出均带 `pilot_only_flag=true` 与 `not_comparable_to_core_benchmark=true`。
- E12 只回答 “representation feasibility”，不与主 benchmark 表格并列比较。
```

### 源文件: `E12_inter_event_cases.csv`

- 路径: `rebuttal/outputs/E12_inter_event_cases.csv`
- 文件大小(bytes): `267`

```text
dataset,event_pair,predicted_link,gold_link,correct,failure_reason,error_category,ambiguity_type
RAMS,attack->evacuation,causal,causal,True,,none,none
WikiEvents,meeting->statement,overlap,temporal,False,temporal ambiguity,label_confusion,temporal_scope_ambiguity
```

### 源文件: `E12_inter_event_diagnostics.csv`

- 路径: `rebuttal/outputs/E12_inter_event_diagnostics.csv`
- 文件大小(bytes): `318`

```text
dataset,gold_link_count,reachable_link_count,reachable_link_ratio,pred_link_count,correct_link_count,link_type_inventory,evaluation_mode,pilot_only_flag
RAMS,42,29,0.6905,36,16,"causal,temporal,coreference",pilot_offline_replay,True
WikiEvents,37,24,0.6486,32,13,"causal,temporal,overlap",pilot_offline_replay,True
```

### 源文件: `E12_inter_event_main.csv`

- 路径: `rebuttal/outputs/E12_inter_event_main.csv`
- 文件大小(bytes): `730`

```text
dataset,inter_event_link_type_count,representation,literal_f1,graph_f1,mapping_precision,pilot_only_flag,not_comparable_to_core_benchmark,scope_note,evaluation_scope,result_interpretation,evaluation_protocol,evaluator_signature,evaluator_hash,frozen_gold_artifact_hash,notes
RAMS,3,event_pair_edges,0.31,0.39,0.52,True,True,feasibility_only,pilot_slice_not_full_benchmark,feasibility_only_not_core_benchmark,submission_aligned_scope_v1,cabc45613b834dee,c4c2371818eb9bb2,26bad3bb3f37a484,pilot only
WikiEvents,3,event_pair_edges,0.29,0.36,0.49,True,True,feasibility_only,pilot_slice_not_full_benchmark,feasibility_only_not_core_benchmark,submission_aligned_scope_v1,cabc45613b834dee,c4c2371818eb9bb2,26bad3bb3f37a484,pilot only
```

### 源文件: `E12_manifest.json`

- 路径: `rebuttal/outputs/E12_manifest.json`
- 文件大小(bytes): `556`

```text
{
  "command": "python src/rebuttal/scripts/E12_run.py",
  "config": "src/rebuttal/configs/E12_inter_event_pilot.yaml",
  "seed": 42,
  "timestamp_utc": "2026-03-28T18:01:07.572287+00:00",
  "git_commit": "b833dee36d3e96b7bfd97292095e0a526368a16c",
  "environment": {
    "timestamp_utc": "2026-03-28T18:01:07.573862+00:00",
    "python": "3.12.12 | packaged by Anaconda, Inc. | (main, Oct 21 2025, 20:16:04) [GCC 11.2.0]",
    "platform": "Linux-5.15.0-170-generic-x86_64-with-glibc2.35",
    "git_commit": "b833dee36d3e96b7bfd97292095e0a526368a16c"
  }
}
```

### 源文件: `E12_scope_note.json`

- 路径: `rebuttal/outputs/E12_scope_note.json`
- 文件大小(bytes): `238`

```text
{
  "pilot_only_flag": true,
  "not_comparable_to_core_benchmark": true,
  "scope_note": "feasibility_only",
  "note": "E12 only addresses representational feasibility and should not be compared side-by-side with core benchmark tables."
}
```

### 源文件: `E12_summary.md`

- 路径: `rebuttal/outputs/E12_summary.md`
- 文件大小(bytes): `687`

```text
# E12 Summary

## objective
- inter-event relation pilot

## methods compared
- pilot schema extension

## dataset scope
- 1-2 EE datasets

## exact files produced
- `E12_inter_event_main.csv`
- `E12_inter_event_diagnostics.csv`
- `E12_inter_event_cases.csv`
- `E12_manifest.json`

## key findings
- 所有主输出维持 pilot_only_flag，并新增 not_comparable_to_core_benchmark/scope_note
- diagnostics 新增 reachable_link_ratio，显式区分可达覆盖与预测质量
- 新增 E12_scope_note.json 与 caveat，强调仅回答 representational feasibility

## Suggested rebuttal sentence
该实验仅为 representational feasibility pilot，不构成主benchmark扩展结论。
```
