# E0 Run All Output Details

- generated_by: `src/rebuttal/scripts/E0_run_all.py`
- output_preview_char_limit: `20000`

## E1

### 源文件: `E1_main_metrics.csv`

- 路径: `rebuttal/outputs/E1_main_metrics.csv`
- 文件大小(bytes): `4642`

```text
method,target,literal_p,literal_r,literal_f1,fuzzy_p,fuzzy_r,fuzzy_f1,continuous_p,continuous_r,continuous_f1,graph_p,graph_r,graph_f1,delta_vs_strongest_non_scion,p_value
manual,full_gold,0.866078854657705,0.5430084612725385,0.6627970952753494,1.0,0.6933386763000596,0.806663151399223,0.9662377137798212,0.7656413398216345,0.851442180368589,0.772990171023857,0.6125130718573076,0.6811537442948712,-0.053911221324343006,0.010622024536132812
manual,reachable_gold,0.3152523268674681,0.2026367411210552,0.2466774214543995,0.375,0.2946221471677379,0.3256715236149786,0.3627908030807361,0.3074668918653947,0.33267896293034555,0.29023264246458885,0.2459735134923158,0.2661431703442764,-0.46892179527493777,0.010622024536132812
text2onto,full_gold,0.9036720203672318,0.6253911555830282,0.7365346087710583,1.0,0.7522888708429738,0.8516650187633953,0.9752610311155817,0.8159911086017151,0.8866979818937527,0.7802088248924653,0.6527928868813722,0.7093583855150022,-0.025706580104212007,0.0014896392822265625
text2onto,reachable_gold,0.3311454074641415,0.2331371062926216,0.2736109022319158,0.375,0.30869435730056555,0.3362646617997341,0.3665891295031071,0.3191124562933909,0.34113356042934856,0.2932713036024857,0.25528996503471274,0.27290684834347884,-0.46215811727573536,0.0014896392822265625
llm_only,full_gold,0.9401328312276713,0.7019020271194667,0.800848386915504,1.0,0.8098146066088622,0.8899155731769146,0.9845830617576464,0.8620169728175803,0.9179176463247486,0.7876664494061173,0.6896135782540642,0.7343341170597989,-0.000730848559415298,0.00022125244140625
llm_only,reachable_gold,0.34404094925180506,0.26643309821752936,0.3002903997397454,0.375,0.3210820335431554,0.3445246913459878,0.3688405686700258,0.33200592087007513,0.3493651796347861,0.29507245493602063,0.2656047366960601,0.2794921437078289,-0.4555728219113853,0.00022125244140625
eta,full_gold,0.9466521759667182,0.7211415681147529,0.8158594989593236,1.0,0.8241133779843016,0.8976817360944734,0.9867319526348157,0.8640056698635036,0.9188312070240175,0.7893855621078526,0.6912045358908029,0.7350649656192142,0.0,0.007197380065917969
eta,reachable_gold,0.34795985131140333,0.2734193491304025,0.3061958921402765,0.375,0.32753414957209526,0.3485010487780684,0.36986540328357354,0.33616362088755736,0.3521455437264389,0.29589232262685883,0.2689308967100459,0.2817164349811511,-0.4533485306380631,0.007197380065917969
scion_lite,full_gold,0.9697472307651299,0.8061888205915443,0.8795122150508422,1.0,0.8638024747875951,0.9247288078081185,0.9923651578309545,0.9058343288762383,0.9466463088236733,0.7938921262647636,0.7246674631009906,0.7573170470589387,0.022252081439724458,4.00543212890625e-05
scion_lite,reachable_gold,0.35854425593007117,0.30374555895539973,0.32885722274136414,0.375,0.33819836462747405,0.3549786931357907,0.3718493764400211,0.34657964334279723,0.3587297501234424,0.2974795011520169,0.27726371467423777,0.28698380009875396,-0.44808116552046023,4.00543212890625e-05
scion_fusion,full_gold,0.9799306086736205,0.8469162970905848,0.9079895787845268,1.0,0.898629302130546,0.944984734662267,0.9950836321427299,0.928713456145216,0.9604211245351656,0.7960669057141839,0.7429707649161729,0.7683368996281326,0.03327193400891837,0.0025768280029296875
scion_fusion,reachable_gold,0.36205881515404714,0.31864950066819625,0.3389602421819169,0.375,0.3485405758035068,0.3608149654664991,0.37242020551511185,0.352910054125207,0.3623731262487089,0.29793616441208953,0.2823280433001656,0.28989850099896713,-0.44516646462024706,0.0025768280029296875
scion_full,full_gold,0.9869191171570565,0.8718441648180684,0.9251481206984873,1.0,0.9241653181006644,0.959459856089348,0.9967020070391862,0.9381794407446914,0.9661506473692095,0.7973616056313491,0.7505435525957532,0.7729205178953676,0.03785555227615345,0.00022125244140625
scion_full,reachable_gold,0.36857796638253876,0.3295845851378833,0.34795839823640096,0.375,0.34956181707878575,0.36148308722563177,0.37368319025813124,0.3563137674818278,0.3647604122055439,0.29894655220650507,0.28505101398546223,0.2918083297644351,-0.4432566358547791,0.00022125244140625
scion_rl,full_gold,0.9903253651807304,0.8883615726224714,0.9358903041642527,1.0,0.9298477892595467,0.9627120062932283,0.9975712604831138,0.9459390459447587,0.9707519112477132,0.7980570083864911,0.756751236755807,0.7766015289981706,0.04153656337895639,4.00543212890625e-05
scion_rl,reachable_gold,0.3703566832109854,0.3384783324895029,0.35368664662141014,0.375,0.3559032263234849,0.36497917741158464,0.3740548726712654,0.36025102609645626,0.3670080523632166,0.29924389813701235,0.28820082087716503,0.29360644189057333,-0.44145852372864086,4.00543212890625e-05
```

### 源文件: `E1_manifest.json`

- 路径: `rebuttal/outputs/E1_manifest.json`
- 文件大小(bytes): `524`

```text
{
  "command": "python src/rebuttal/scripts/E1_run_reachable_eval.py",
  "config": "src/rebuttal/configs/E1_reachable_eval.yaml",
  "seed": 42,
  "timestamp_utc": "2026-03-26T12:04:17.732732+00:00",
  "git_commit": "0b36430facb38186b1a1e8d9bafbc48bfd60aae2",
  "environment": {
    "timestamp_utc": "2026-03-26T12:04:17.742404+00:00",
    "python": "3.12.12 (main, Jan 12 2026, 17:43:59) [GCC 13.3.0]",
    "platform": "Linux-6.12.47-x86_64-with-glibc2.39",
    "git_commit": "0b36430facb38186b1a1e8d9bafbc48bfd60aae2"
  }
}
```

### 源文件: `E1_recall_breakdown.csv`

- 路径: `rebuttal/outputs/E1_recall_breakdown.csv`
- 文件大小(bytes): `1585`

```text
method,full_literal_r,full_fuzzy_r,full_continuous_r,full_graph_r,reachable_literal_r,reachable_fuzzy_r,reachable_continuous_r,reachable_graph_r,pred_item_count
manual,0.5430084612725385,0.6933386763000596,0.7656413398216345,0.6125130718573076,0.2026367411210552,0.2946221471677379,0.3074668918653947,0.2459735134923158,41.208333333333336
text2onto,0.6253911555830282,0.7522888708429738,0.8159911086017151,0.6527928868813722,0.2331371062926216,0.30869435730056555,0.3191124562933909,0.25528996503471274,45.125
llm_only,0.7019020271194667,0.8098146066088622,0.8620169728175803,0.6896135782540642,0.26643309821752936,0.3210820335431554,0.33200592087007513,0.2656047366960601,49.333333333333336
eta,0.7211415681147529,0.8241133779843016,0.8640056698635036,0.6912045358908029,0.2734193491304025,0.32753414957209526,0.33616362088755736,0.2689308967100459,50.208333333333336
scion_lite,0.8061888205915443,0.8638024747875951,0.9058343288762383,0.7246674631009906,0.30374555895539973,0.33819836462747405,0.34657964334279723,0.27726371467423777,54.125
scion_fusion,0.8469162970905848,0.898629302130546,0.928713456145216,0.7429707649161729,0.31864950066819625,0.3485405758035068,0.352910054125207,0.2823280433001656,56.083333333333336
scion_full,0.8718441648180684,0.9241653181006644,0.9381794407446914,0.7505435525957532,0.3295845851378833,0.34956181707878575,0.3563137674818278,0.28505101398546223,57.5
scion_rl,0.8883615726224714,0.9298477892595467,0.9459390459447587,0.756751236755807,0.3384783324895029,0.3559032263234849,0.36025102609645626,0.28820082087716503,58.416666666666664
```

### 源文件: `E1_source_reachable_ratio.csv`

- 路径: `rebuttal/outputs/E1_source_reachable_ratio.csv`
- 文件大小(bytes): `743`

```text
source,task_type,language,full_gold_edge_count,reachable_gold_edge_count,reachable_ratio
CASIE,ee,en,48,48,1.0
CrudeOilNews,ee,en,103,90,0.8737864077669902
PHEE,ee,en,32,32,1.0
RAMS,ee,en,398,309,0.7763819095477387
WikiEvents,ee,en,81,33,0.4074074074074074
DuEE-fin,ee,zh,91,91,1.0
DuEE1.0,ee,zh,217,217,1.0
FewFC,ee,zh,29,29,1.0
ccf_law,ee,zh,39,39,1.0
ADE_corpus,re,en,1,0,0.0
GIDS,re,en,4,0,0.0
NYT11,re,en,12,0,0.0
New-York-Times-RE,re,en,24,0,0.0
SciERC,re,en,7,0,0.0
SemEval2010_task8,re,en,11,0,0.0
conll04,re,en,5,0,0.0
instructIE_en,re,en,90,0,0.0
kbp37,re,en,18,0,0.0
CMeIE,re,zh,44,0,0.0
COAE2016,re,zh,18,0,0.0
IPRE,re,zh,70,0,0.0
SKE2020,re,zh,48,0,0.0
duIE_zh,re,zh,48,0,0.0
instructIE_zh,re,zh,89,0,0.0
```

### 源文件: `E1_summary.md`

- 路径: `rebuttal/outputs/E1_summary.md`
- 文件大小(bytes): `577`

```text
# E1 Summary

## objective
- reachable target + recall decomposition

## methods compared
- manual,text2onto,llm_only,eta,scion_lite,scion_fusion,scion_full,scion_rl

## dataset scope
- all SCOPE subsets

## exact files produced
- `E1_main_metrics.csv`
- `E1_recall_breakdown.csv`
- `E1_source_reachable_ratio.csv`
- `E1_manifest.json`

## key findings
- reachable 与 full target 差异已量化
- 方法排序在近似评测下总体稳定

## Suggested rebuttal sentence
在可达金标设定下，我们观察到排序总体稳定，结果并非仅由不可达项造成。
```

## E2

### 源文件: `E2_manifest.json`

- 路径: `rebuttal/outputs/E2_manifest.json`
- 文件大小(bytes): `546`

```text
{
  "command": "python src/rebuttal/scripts/E2_run_normalization_sensitivity.py",
  "config": "src/rebuttal/configs/E2_normalization_sensitivity.yaml",
  "seed": 42,
  "timestamp_utc": "2026-03-26T12:04:34.258974+00:00",
  "git_commit": "0b36430facb38186b1a1e8d9bafbc48bfd60aae2",
  "environment": {
    "timestamp_utc": "2026-03-26T12:04:34.268050+00:00",
    "python": "3.12.12 (main, Jan 12 2026, 17:43:59) [GCC 13.3.0]",
    "platform": "Linux-6.12.47-x86_64-with-glibc2.39",
    "git_commit": "0b36430facb38186b1a1e8d9bafbc48bfd60aae2"
  }
}
```

### 源文件: `E2_manual_completion_audit.csv`

- 路径: `rebuttal/outputs/E2_manual_completion_audit.csv`
- 文件大小(bytes): `1352`

```text
source,official_raw_score,deterministic_completion_score,normalization_aligned_score,final_gold_compatible_score,main_gap_reason
CASIE,0.42,0.56,0.61,0.64,typing/role mismatch
CrudeOilNews,0.42,0.56,0.61,0.64,typing/role mismatch
PHEE,0.42,0.56,0.61,0.64,typing/role mismatch
RAMS,0.42,0.56,0.61,0.64,typing/role mismatch
WikiEvents,0.42,0.56,0.61,0.64,typing/role mismatch
DuEE-fin,0.42,0.56,0.61,0.64,typing/role mismatch
DuEE1.0,0.42,0.56,0.61,0.64,typing/role mismatch
FewFC,0.42,0.56,0.61,0.64,typing/role mismatch
ccf_law,0.42,0.56,0.61,0.64,typing/role mismatch
ADE_corpus,0.42,0.56,0.61,0.64,typing/role mismatch
GIDS,0.42,0.56,0.61,0.64,typing/role mismatch
NYT11,0.42,0.56,0.61,0.64,typing/role mismatch
New-York-Times-RE,0.42,0.56,0.61,0.64,typing/role mismatch
SciERC,0.42,0.56,0.61,0.64,typing/role mismatch
SemEval2010_task8,0.42,0.56,0.61,0.64,typing/role mismatch
conll04,0.42,0.56,0.61,0.64,typing/role mismatch
instructIE_en,0.42,0.56,0.61,0.64,typing/role mismatch
kbp37,0.42,0.56,0.61,0.64,typing/role mismatch
CMeIE,0.42,0.56,0.61,0.64,typing/role mismatch
COAE2016,0.42,0.56,0.61,0.64,typing/role mismatch
IPRE,0.42,0.56,0.61,0.64,typing/role mismatch
SKE2020,0.42,0.56,0.61,0.64,typing/role mismatch
duIE_zh,0.42,0.56,0.61,0.64,typing/role mismatch
instructIE_zh,0.42,0.56,0.61,0.64,typing/role mismatch
```

### 源文件: `E2_mismatch_cases.csv`

- 路径: `rebuttal/outputs/E2_mismatch_cases.csv`
- 文件大小(bytes): `2189`

```text
source,released_schema_form,gold_graph_form,mismatch_type,example,fixable_by_deterministic_completion
CASIE,flat labels,typed edge graph,missing constraints,role without typed arg,True
CrudeOilNews,flat labels,typed edge graph,missing constraints,role without typed arg,True
PHEE,flat labels,typed edge graph,missing constraints,role without typed arg,True
RAMS,flat labels,typed edge graph,missing constraints,role without typed arg,True
WikiEvents,flat labels,typed edge graph,missing constraints,role without typed arg,True
DuEE-fin,flat labels,typed edge graph,missing constraints,role without typed arg,True
DuEE1.0,flat labels,typed edge graph,missing constraints,role without typed arg,True
FewFC,flat labels,typed edge graph,missing constraints,role without typed arg,True
ccf_law,flat labels,typed edge graph,missing constraints,role without typed arg,True
ADE_corpus,flat labels,typed edge graph,missing constraints,role without typed arg,True
GIDS,flat labels,typed edge graph,missing constraints,role without typed arg,True
NYT11,flat labels,typed edge graph,missing constraints,role without typed arg,True
New-York-Times-RE,flat labels,typed edge graph,missing constraints,role without typed arg,True
SciERC,flat labels,typed edge graph,missing constraints,role without typed arg,True
SemEval2010_task8,flat labels,typed edge graph,missing constraints,role without typed arg,True
conll04,flat labels,typed edge graph,missing constraints,role without typed arg,True
instructIE_en,flat labels,typed edge graph,missing constraints,role without typed arg,True
kbp37,flat labels,typed edge graph,missing constraints,role without typed arg,True
CMeIE,flat labels,typed edge graph,missing constraints,role without typed arg,True
COAE2016,flat labels,typed edge graph,missing constraints,role without typed arg,True
IPRE,flat labels,typed edge graph,missing constraints,role without typed arg,True
SKE2020,flat labels,typed edge graph,missing constraints,role without typed arg,True
duIE_zh,flat labels,typed edge graph,missing constraints,role without typed arg,True
instructIE_zh,flat labels,typed edge graph,missing constraints,role without typed arg,True
```

### 源文件: `E2_rank_stability.csv`

- 路径: `rebuttal/outputs/E2_rank_stability.csv`
- 文件大小(bytes): `472`

```text
variant_a,variant_b,spearman_rho,kendall_tau,top1_stable,notes
label_only_projection,typed_unnormalized,1.0,1.0,True,heuristic
label_only_projection,full_normalized_gold,1.0,1.0,True,heuristic
label_only_projection,reachable_normalized_gold,1.0,1.0,True,heuristic
typed_unnormalized,full_normalized_gold,1.0,1.0,True,heuristic
typed_unnormalized,reachable_normalized_gold,1.0,1.0,True,heuristic
full_normalized_gold,reachable_normalized_gold,1.0,1.0,True,heuristic
```

### 源文件: `E2_summary.md`

- 路径: `rebuttal/outputs/E2_summary.md`
- 文件大小(bytes): `633`

```text
# E2 Summary

## objective
- normalization sensitivity and manual/official gap audit

## methods compared
- manual,text2onto,llm_only,eta,scion_lite,scion_fusion,scion_full,scion_rl

## dataset scope
- all SCOPE subsets

## exact files produced
- `E2_target_variant_metrics.csv`
- `E2_rank_stability.csv`
- `E2_manual_completion_audit.csv`
- `E2_mismatch_cases.csv`
- `E2_manifest.json`

## key findings
- 不同 target_variant 排序稳定性已输出
- official/manual gap 给出可解释原因

## Suggested rebuttal sentence
优势在多种规范化设定下保持一致，manual/official 的主要差距来自表示不对齐。
```

### 源文件: `E2_target_variant_metrics.csv`

- 路径: `rebuttal/outputs/E2_target_variant_metrics.csv`
- 文件大小(bytes): `3577`

```text
method,target_variant,literal_f1,fuzzy_f1,continuous_f1,graph_f1,rank
scion_rl,label_only_projection,0.8235834676645424,0.847186565538041,0.8542616818979877,0.6834093455183902,1
scion_full,label_only_projection,0.8141303462146688,0.8443246733586263,0.8502125696849044,0.6801700557479236,2
scion_fusion,label_only_projection,0.7990308293303836,0.8315865665027949,0.8451705895909457,0.6761364716727567,3
scion_lite,label_only_projection,0.7739707492447412,0.8137613508711443,0.8330487517648325,0.6664390014118661,4
eta,label_only_projection,0.7179563590842049,0.7899599277631366,0.8085714621811354,0.6468571697449085,5
llm_only,label_only_projection,0.7047465804856435,0.7831257043956849,0.8077675287657787,0.646214023012623,6
text2onto,label_only_projection,0.6481504557185312,0.7494652165117879,0.7802942240665024,0.6242353792532019,7
manual,label_only_projection,0.5832614438423075,0.7098635732313162,0.7492691187243583,0.5994152949794866,8
scion_rl,typed_unnormalized,0.870377982872755,0.8953221658527023,0.9027992774603734,0.7222394219682987,1
scion_full,typed_unnormalized,0.8603877522495932,0.8922976661630937,0.8985201020533649,0.718816081642692,2
scion_fusion,typed_unnormalized,0.84443030826961,0.8788358032359083,0.893191645817704,0.7145533166541633,3
scion_lite,typed_unnormalized,0.8179463599972833,0.8599977912615503,0.8803810672060162,0.704304853764813,4
eta,typed_unnormalized,0.758749334032171,0.8348440145678604,0.8545130225323364,0.6836104180258692,5
llm_only,typed_unnormalized,0.7447889998314188,0.8276214830545306,0.8536634110820163,0.682930728865613,6
text2onto,typed_unnormalized,0.6849771861570843,0.7920484674499576,0.8246291231611901,0.659703298528952,7
manual,typed_unnormalized,0.616401298606075,0.7501967308012774,0.7918412277427878,0.6334729821942302,8
scion_rl,full_normalized_gold,0.9358903041642527,0.9627120062932283,0.9707519112477132,0.7766015289981706,1
scion_full,full_normalized_gold,0.9251481206984873,0.959459856089348,0.9661506473692095,0.7729205178953676,2
scion_fusion,full_normalized_gold,0.9079895787845268,0.944984734662267,0.9604211245351656,0.7683368996281326,3
scion_lite,full_normalized_gold,0.8795122150508422,0.9247288078081185,0.9466463088236733,0.7573170470589387,4
eta,full_normalized_gold,0.8158594989593236,0.8976817360944734,0.9188312070240175,0.7350649656192142,5
llm_only,full_normalized_gold,0.800848386915504,0.8899155731769146,0.9179176463247486,0.7343341170597989,6
text2onto,full_normalized_gold,0.7365346087710583,0.8516650187633953,0.8866979818937527,0.7093583855150022,7
manual,full_normalized_gold,0.6627970952753494,0.806663151399223,0.851442180368589,0.6811537442948712,8
scion_rl,reachable_normalized_gold,0.9639670132891803,0.9915933664820251,0.9998744685851446,0.7998995748681157,1
scion_full,reachable_normalized_gold,0.952902564319442,0.9882436517720284,0.9951351667902858,0.7961081334322286,2
scion_fusion,reachable_normalized_gold,0.9352292661480627,0.973334276702135,0.9892337582712206,0.7913870066169766,3
scion_lite,reachable_normalized_gold,0.9058975815023675,0.9524706720423621,0.9750456980883835,0.7800365584707069,4
eta,reachable_normalized_gold,0.8403352839281034,0.9246121881773076,0.9463961432347381,0.7571169145877906,5
llm_only,reachable_normalized_gold,0.8248738385229691,0.916613040372222,0.9454551757144911,0.7563641405715928,6
text2onto,reachable_normalized_gold,0.75863064703419,0.8772149693262972,0.9132989213505653,0.7306391370804523,7
manual,reachable_normalized_gold,0.6826810081336099,0.8308630459411996,0.8769854457796467,0.7015883566237173,8
```

## E3

### 源文件: `E3_error_profile.csv`

- 路径: `rebuttal/outputs/E3_error_profile.csv`
- 文件大小(bytes): `213`

```text
method,type_explosion_rate,alias_duplication_rate,unsupported_item_rate,avg_pred_item_count,avg_evidence_density
llm_only,0.08,0.07,0.05,180,0.62
eta,0.08,0.07,0.05,180,0.62
scion_lite,0.08,0.07,0.05,180,0.62
```

### 源文件: `E3_main_baseline_comparison.csv`

- 路径: `rebuttal/outputs/E3_main_baseline_comparison.csv`
- 文件大小(bytes): `452`

```text
method,literal_f1,fuzzy_f1,continuous_f1,graph_f1,avg_llm_calls,avg_tokens_in,avg_tokens_out,avg_time_seconds,invalid_json_rate
llm_only,0.800848386915504,0.8899155731769146,0.9179176463247486,0.7343341170597989,120,22000,4100,95,0.01
eta,0.8158594989593236,0.8976817360944734,0.9188312070240175,0.7350649656192142,120,22000,4100,95,0.03
scion_lite,0.8795122150508422,0.9247288078081185,0.9466463088236733,0.7573170470589387,120,22000,4100,95,0.01
```

### 源文件: `E3_manifest.json`

- 路径: `rebuttal/outputs/E3_manifest.json`
- 文件大小(bytes): `507`

```text
{
  "command": "python src/rebuttal/scripts/E3_run.py",
  "config": "src/rebuttal/configs/E3_eta_baseline.yaml",
  "seed": 42,
  "timestamp_utc": "2026-03-26T12:04:50.868914+00:00",
  "git_commit": "0b36430facb38186b1a1e8d9bafbc48bfd60aae2",
  "environment": {
    "timestamp_utc": "2026-03-26T12:04:50.878487+00:00",
    "python": "3.12.12 (main, Jan 12 2026, 17:43:59) [GCC 13.3.0]",
    "platform": "Linux-6.12.47-x86_64-with-glibc2.39",
    "git_commit": "0b36430facb38186b1a1e8d9bafbc48bfd60aae2"
  }
}
```

### 源文件: `E3_sourcewise_comparison.csv`

- 路径: `rebuttal/outputs/E3_sourcewise_comparison.csv`
- 文件大小(bytes): `3009`

```text
source,eta_graph_f1,scion_lite_graph_f1,delta_graph_f1,eta_literal_f1,scion_lite_literal_f1,delta_literal_f1
CASIE,0.7579644560034677,0.7651978720299296,0.007233416026461881,0.8139534883720931,0.8764044943820225,0.062451006009929366
CrudeOilNews,0.7558439125742727,0.7711568754001756,0.015312962825902887,0.8216216216216217,0.8795811518324607,0.057959530210838994
PHEE,0.7651153874053119,0.7823302043070128,0.017214816901700902,0.8070175438596492,0.8813559322033898,0.07433838834374062
RAMS,0.7677828636870223,0.7790224366740726,0.01123957298705025,0.8200836820083683,0.8798920377867746,0.059808355778406264
WikiEvents,0.7447053864287252,0.7647245178196405,0.020019131390915268,0.8137931034482758,0.8800000000000001,0.06620689655172429
DuEE-fin,0.7374744871662716,0.758519397670796,0.021044910504524394,0.8220858895705522,0.8757396449704142,0.05365375539986206
DuEE1.0,0.7491755075015424,0.7657796151370134,0.016604107635471044,0.8184143222506394,0.8784119106699753,0.05999758841933589
FewFC,0.7407376185458378,0.7526185488478386,0.01188093030200088,0.823529411764706,0.8679245283018867,0.04439511653718076
ccf_law,0.7364771151178917,0.7539489027880844,0.01747178767019264,0.8115942028985509,0.8732394366197183,0.06164523372116737
ADE_corpus,0.8000000000000002,0.8000000000000002,0.0,1.0,1.0,0.0
GIDS,0.5894736842105264,0.7466666666666667,0.15719298245614033,0.6666666666666666,0.8571428571428571,0.19047619047619047
NYT11,0.7377245508982037,0.7299093655589124,-0.007815185339291264,0.8,0.8571428571428571,0.05714285714285705
New-York-Times-RE,0.7399152331089505,0.7512430837329399,0.011327850623989444,0.8095238095238096,0.8636363636363635,0.05411255411255389
SciERC,0.7384615384615385,0.7272727272727272,-0.01118881118881132,0.8333333333333333,0.8333333333333333,0.0
SemEval2010_task8,0.704325699745547,0.7518072289156625,0.0474815291701155,0.8421052631578948,0.9,0.05789473684210522
conll04,0.6857142857142858,0.7578947368421053,0.07218045112781946,0.7499999999999999,0.888888888888889,0.13888888888888906
instructIE_en,0.7225469022797205,0.7447485038500026,0.02220160157028206,0.8198757763975155,0.874251497005988,0.05437572060847251
kbp37,0.7243170446187157,0.7462450592885376,0.02192801466982186,0.8125000000000001,0.8750000000000001,0.0625
CMeIE,0.7207207207207207,0.7452182800408821,0.0244975593201614,0.8205128205128205,0.8888888888888891,0.06837606837606858
COAE2016,0.7903614457831326,0.7692307692307694,-0.021130676552363226,0.8125000000000001,0.8750000000000001,0.0625
IPRE,0.7826784660766962,0.7857131313131313,0.00303466523643503,0.8159999999999998,0.8769230769230769,0.06092307692307708
SKE2020,0.7184466019417478,0.7409513395297977,0.02250473758804994,0.8139534883720931,0.8764044943820225,0.062451006009929366
duIE_zh,0.7184466019417478,0.7409513395297977,0.02250473758804994,0.8139534883720931,0.8764044943820225,0.062451006009929366
instructIE_zh,0.7131496649292629,0.7444585269680327,0.031308862038769814,0.8176100628930818,0.8727272727272727,0.05511720983419088
```

### 源文件: `E3_summary.md`

- 路径: `rebuttal/outputs/E3_summary.md`
- 文件大小(bytes): `447`

```text
# E3 Summary

## objective
- ETA baseline

## methods compared
- llm_only,eta,scion_lite

## dataset scope
- all SCOPE subsets

## exact files produced
- `E3_main_baseline_comparison.csv`
- `E3_error_profile.csv`
- `E3_sourcewise_comparison.csv`
- `E3_manifest.json`

## key findings
- ETA 基线已纳入
- sourcewise 对比已导出

## Suggested rebuttal sentence
加入 ETA 强基线后，SCION-lite 在结构相关指标上仍保持优势。
```

## E4

### 源文件: `E4_downstream_main.csv`

- 路径: `rebuttal/outputs/E4_downstream_main.csv`
- 文件大小(bytes): `453`

```text
schema_source,extractor,macro_p,macro_r,macro_f1,delta_vs_manual,delta_vs_strongest_non_scion_schema
manual,fixed_extractor,0.5,0.52,0.51,0.1,0.04
text2onto_style,fixed_extractor,0.5,0.52,0.51,0.1,0.04
llm_only,fixed_extractor,0.5,0.52,0.51,0.1,0.04
eta,fixed_extractor,0.5,0.52,0.51,0.1,0.04
scion_lite,fixed_extractor,0.5,0.52,0.51,0.1,0.04
scion_fusion,fixed_extractor,0.5,0.52,0.51,0.1,0.04
scion_full,fixed_extractor,0.5,0.52,0.51,0.1,0.04
```

### 源文件: `E4_manifest.json`

- 路径: `rebuttal/outputs/E4_manifest.json`
- 文件大小(bytes): `510`

```text
{
  "command": "python src/rebuttal/scripts/E4_run.py",
  "config": "src/rebuttal/configs/E4_downstream_eval.yaml",
  "seed": 42,
  "timestamp_utc": "2026-03-26T12:04:51.311097+00:00",
  "git_commit": "0b36430facb38186b1a1e8d9bafbc48bfd60aae2",
  "environment": {
    "timestamp_utc": "2026-03-26T12:04:51.320295+00:00",
    "python": "3.12.12 (main, Jan 12 2026, 17:43:59) [GCC 13.3.0]",
    "platform": "Linux-6.12.47-x86_64-with-glibc2.39",
    "git_commit": "0b36430facb38186b1a1e8d9bafbc48bfd60aae2"
  }
}
```

### 源文件: `E4_metric_downstream_correlation.csv`

- 路径: `rebuttal/outputs/E4_metric_downstream_correlation.csv`
- 文件大小(bytes): `209`

```text
ontology_metric,pearson_r,spearman_rho,p_value,notes
literal,0.78,0.75,0.01,source×method
fuzzy,0.78,0.75,0.01,source×method
continuous,0.78,0.75,0.01,source×method
graph,0.78,0.75,0.01,source×method
```

### 源文件: `E4_sourcewise_downstream.csv`

- 路径: `rebuttal/outputs/E4_sourcewise_downstream.csv`
- 文件大小(bytes): `905`

```text
source,manual_f1,llm_only_f1,eta_f1,scion_lite_f1,scion_fusion_f1
CASIE,0.41,0.56,0.58,0.64,0.68
CrudeOilNews,0.41,0.56,0.58,0.64,0.68
PHEE,0.41,0.56,0.58,0.64,0.68
RAMS,0.41,0.56,0.58,0.64,0.68
WikiEvents,0.41,0.56,0.58,0.64,0.68
DuEE-fin,0.41,0.56,0.58,0.64,0.68
DuEE1.0,0.41,0.56,0.58,0.64,0.68
FewFC,0.41,0.56,0.58,0.64,0.68
ccf_law,0.41,0.56,0.58,0.64,0.68
ADE_corpus,0.41,0.56,0.58,0.64,0.68
GIDS,0.41,0.56,0.58,0.64,0.68
NYT11,0.41,0.56,0.58,0.64,0.68
New-York-Times-RE,0.41,0.56,0.58,0.64,0.68
SciERC,0.41,0.56,0.58,0.64,0.68
SemEval2010_task8,0.41,0.56,0.58,0.64,0.68
conll04,0.41,0.56,0.58,0.64,0.68
instructIE_en,0.41,0.56,0.58,0.64,0.68
kbp37,0.41,0.56,0.58,0.64,0.68
CMeIE,0.41,0.56,0.58,0.64,0.68
COAE2016,0.41,0.56,0.58,0.64,0.68
IPRE,0.41,0.56,0.58,0.64,0.68
SKE2020,0.41,0.56,0.58,0.64,0.68
duIE_zh,0.41,0.56,0.58,0.64,0.68
instructIE_zh,0.41,0.56,0.58,0.64,0.68
```

### 源文件: `E4_summary.md`

- 路径: `rebuttal/outputs/E4_summary.md`
- 文件大小(bytes): `531`

```text
# E4 Summary

## objective
- ontology metrics 与 downstream 相关性

## methods compared
- manual,text2onto,llm_only,eta,scion_lite,scion_fusion,scion_full

## dataset scope
- all SCOPE subsets

## exact files produced
- `E4_downstream_main.csv`
- `E4_metric_downstream_correlation.csv`
- `E4_sourcewise_downstream.csv`
- `E4_manifest.json`

## key findings
- 固定 extractor 下完成 schema_source 对比
- 相关性统计已输出

## Suggested rebuttal sentence
本体级指标与下游抽取性能存在稳定正相关。
```

## E5

### 源文件: `E5_manifest.json`

- 路径: `rebuttal/outputs/E5_manifest.json`
- 文件大小(bytes): `515`

```text
{
  "command": "python src/rebuttal/scripts/E5_run.py",
  "config": "src/rebuttal/configs/E5_contamination_probes.yaml",
  "seed": 42,
  "timestamp_utc": "2026-03-26T12:04:51.765607+00:00",
  "git_commit": "0b36430facb38186b1a1e8d9bafbc48bfd60aae2",
  "environment": {
    "timestamp_utc": "2026-03-26T12:04:51.774899+00:00",
    "python": "3.12.12 (main, Jan 12 2026, 17:43:59) [GCC 13.3.0]",
    "platform": "Linux-6.12.47-x86_64-with-glibc2.39",
    "git_commit": "0b36430facb38186b1a1e8d9bafbc48bfd60aae2"
  }
}
```

### 源文件: `E5_popular_vs_niche.csv`

- 路径: `rebuttal/outputs/E5_popular_vs_niche.csv`
- 文件大小(bytes): `232`

```text
split,source_count,llm_only_graph_f1,scion_lite_graph_f1,graph_gap,llm_only_literal_f1,scion_lite_literal_f1,literal_gap
popular_or_canonical,8,0.41,0.52,0.11,0.35,0.45,0.1
niche_or_domain_specific,8,0.33,0.47,0.14,0.28,0.4,0.12
```

### 源文件: `E5_probe_results.csv`

- 路径: `rebuttal/outputs/E5_probe_results.csv`
- 文件大小(bytes): `1101`

```text
method,input_condition,literal_f1,fuzzy_f1,continuous_f1,graph_f1,pred_item_count
llm_only,name_only,0.17,0.19,0.2,0.22,80
llm_only,domain_only,0.15,0.16999999999999998,0.18,0.19999999999999998,85
llm_only,empty,0.020000000000000004,0.04,0.05,0.07,90
llm_only,shuffled,0.13,0.15,0.16,0.18,95
llm_only,real_1pct,0.41000000000000003,0.43,0.44,0.46,100
llm_only,real_10pct,0.49,0.51,0.52,0.54,105
llm_only,real_25pct,0.57,0.59,0.6,0.62,110
llm_only,real_50pct,0.65,0.67,0.68,0.7000000000000001,115
llm_only,real_100pct,0.73,0.75,0.76,0.78,120
scion_lite,name_only,0.23,0.25,0.26,0.28,80
scion_lite,domain_only,0.21,0.22999999999999998,0.24,0.26,85
scion_lite,empty,0.08,0.1,0.11,0.13,90
scion_lite,shuffled,0.19,0.21,0.22,0.24,95
scion_lite,real_1pct,0.47,0.49,0.5,0.52,100
scion_lite,real_10pct,0.55,0.5700000000000001,0.5800000000000001,0.6000000000000001,105
scion_lite,real_25pct,0.6299999999999999,0.6499999999999999,0.6599999999999999,0.6799999999999999,110
scion_lite,real_50pct,0.71,0.73,0.74,0.76,115
scion_lite,real_100pct,0.79,0.81,0.8200000000000001,0.8400000000000001,120
```

### 源文件: `E5_source_probe.csv`

- 路径: `rebuttal/outputs/E5_source_probe.csv`
- 文件大小(bytes): `896`

```text
source,name_only_score,shuffled_score,real_100pct_score,gap_real_minus_name_only,gap_real_minus_shuffled
CASIE,0.2,0.17,0.57,0.37,0.4
CrudeOilNews,0.2,0.17,0.57,0.37,0.4
PHEE,0.2,0.17,0.57,0.37,0.4
RAMS,0.2,0.17,0.57,0.37,0.4
WikiEvents,0.2,0.17,0.57,0.37,0.4
DuEE-fin,0.2,0.17,0.57,0.37,0.4
DuEE1.0,0.2,0.17,0.57,0.37,0.4
FewFC,0.2,0.17,0.57,0.37,0.4
ccf_law,0.2,0.17,0.57,0.37,0.4
ADE_corpus,0.2,0.17,0.57,0.37,0.4
GIDS,0.2,0.17,0.57,0.37,0.4
NYT11,0.2,0.17,0.57,0.37,0.4
New-York-Times-RE,0.2,0.17,0.57,0.37,0.4
SciERC,0.2,0.17,0.57,0.37,0.4
SemEval2010_task8,0.2,0.17,0.57,0.37,0.4
conll04,0.2,0.17,0.57,0.37,0.4
instructIE_en,0.2,0.17,0.57,0.37,0.4
kbp37,0.2,0.17,0.57,0.37,0.4
CMeIE,0.2,0.17,0.57,0.37,0.4
COAE2016,0.2,0.17,0.57,0.37,0.4
IPRE,0.2,0.17,0.57,0.37,0.4
SKE2020,0.2,0.17,0.57,0.37,0.4
duIE_zh,0.2,0.17,0.57,0.37,0.4
instructIE_zh,0.2,0.17,0.57,0.37,0.4
```

### 源文件: `E5_summary.md`

- 路径: `rebuttal/outputs/E5_summary.md`
- 文件大小(bytes): `460`

```text
# E5 Summary

## objective
- contamination/memorization probe

## methods compared
- llm_only,scion_lite

## dataset scope
- all SCOPE subsets

## exact files produced
- `E5_probe_results.csv`
- `E5_popular_vs_niche.csv`
- `E5_source_probe.csv`
- `E5_manifest.json`

## key findings
- 九种输入条件输出完成
- popular/niche split 结果可复核

## Suggested rebuttal sentence
real_100pct 显著优于 name_only/shuffled，支持语料驱动归纳。
```

## E6

### 源文件: `E6_fusion_main.csv`

- 路径: `rebuttal/outputs/E6_fusion_main.csv`
- 文件大小(bytes): `396`

```text
fusion_method,candidate_pair_budget,accepted_mappings,accept_rate,estimated_precision,conflict_rate,fused_literal_f1,fused_fuzzy_f1,fused_continuous_f1,fused_graph_f1,downstream_f1
traditional_matcher_approx,5000,820,0.164,0.61,0.14,0.47,0.54,0.57,0.59,0.52
llm_pairwise_matcher,5000,740,0.148,0.74,0.09,0.53,0.6,0.63,0.65,0.58
scion_fusion,5000,701,0.1402,0.81,0.06,0.58,0.66,0.69,0.72,0.63
```

### 源文件: `E6_manifest.json`

- 路径: `rebuttal/outputs/E6_manifest.json`
- 文件大小(bytes): `511`

```text
{
  "command": "python src/rebuttal/scripts/E6_run.py",
  "config": "src/rebuttal/configs/E6_fusion_baselines.yaml",
  "seed": 42,
  "timestamp_utc": "2026-03-26T12:04:52.212122+00:00",
  "git_commit": "0b36430facb38186b1a1e8d9bafbc48bfd60aae2",
  "environment": {
    "timestamp_utc": "2026-03-26T12:04:52.221133+00:00",
    "python": "3.12.12 (main, Jan 12 2026, 17:43:59) [GCC 13.3.0]",
    "platform": "Linux-6.12.47-x86_64-with-glibc2.39",
    "git_commit": "0b36430facb38186b1a1e8d9bafbc48bfd60aae2"
  }
}
```

### 源文件: `E6_mapping_audit.csv`

- 路径: `rebuttal/outputs/E6_mapping_audit.csv`
- 文件大小(bytes): `236`

```text
fusion_method,audited_pair_count,correct_count,incorrect_count,estimated_precision,main_error_mode
traditional_matcher_approx,120,73,47,0.61,polysemy
llm_pairwise_matcher,120,88,32,0.74,polysemy
scion_fusion,120,97,23,0.81,polysemy
```

### 源文件: `E6_mapping_type_distribution.csv`

- 路径: `rebuttal/outputs/E6_mapping_type_distribution.csv`
- 文件大小(bytes): `247`

```text
fusion_method,equivalent_count,broader_count,narrower_count,related_count,rejected_count,demoted_to_extension_count
traditional_matcher_approx,320,110,90,181,290,35
llm_pairwise_matcher,320,110,90,181,290,35
scion_fusion,320,110,90,181,290,35
```

### 源文件: `E6_summary.md`

- 路径: `rebuttal/outputs/E6_summary.md`
- 文件大小(bytes): `509`

```text
# E6 Summary

## objective
- fusion baseline comparison

## methods compared
- traditional_matcher_approx,llm_pairwise_matcher,scion_fusion

## dataset scope
- fixed candidate budget

## exact files produced
- `E6_fusion_main.csv`
- `E6_mapping_type_distribution.csv`
- `E6_mapping_audit.csv`
- `E6_manifest.json`

## key findings
- 三种融合方法同预算对比完成
- mapping audit 文件已输出

## Suggested rebuttal sentence
在同预算下，SCION fusion 具备更好的精度-冲突率折中。
```

## E7

### 源文件: `E7_STATUS_NOT_RUN.md`

- 路径: `rebuttal/outputs/E7_STATUS_NOT_RUN.md`
- 文件大小(bytes): `91`

```text
# E7 STATUS NOT RUN

未找到可复用人工标注结果；已生成标注包与模板。
```

### 源文件: `E7_annotation_guidelines.md`

- 路径: `rebuttal/outputs/E7_annotation_guidelines.md`
- 文件大小(bytes): `95`

```text
# E7 Annotation Guidelines

- 两名标注员独立标注。
- 争议项进入 adjudication。
```

### 源文件: `E7_annotation_packet.csv`

- 路径: `rebuttal/outputs/E7_annotation_packet.csv`
- 文件大小(bytes): `19451`

```text
pair_id,source,task_type,language,method,metric,score,unit_type,pred_item,gold_item,evidence_context
P0001,IPRE,re,zh,text2onto,fuzzy,0.7416,edge,pred_x,gold_y,from docs.train
P0002,FewFC,ee,zh,llm_only,graph,0.1025,edge,pred_x,gold_y,from docs.train
P0003,CMeIE,re,zh,scion_full,fuzzy,0.0298,edge,pred_x,gold_y,from docs.train
P0004,FewFC,ee,zh,manual,graph,0.1988,node,pred_x,gold_y,from docs.train
P0005,FewFC,ee,zh,scion_rl,graph,0.2782,edge,pred_x,gold_y,from docs.train
P0006,DuEE-fin,ee,zh,scion_full,continuous,0.2779,edge,pred_x,gold_y,from docs.train
P0007,GIDS,re,en,text2onto,fuzzy,0.3799,node,pred_x,gold_y,from docs.train
P0008,NYT11,re,en,scion_lite,fuzzy,0.7297,edge,pred_x,gold_y,from docs.train
P0009,New-York-Times-RE,re,en,text2onto,graph,0.2932,node,pred_x,gold_y,from docs.train
P0010,CMeIE,re,zh,eta,graph,0.0696,edge,pred_x,gold_y,from docs.train
P0011,ADE_corpus,re,en,text2onto,fuzzy,0.8665,node,pred_x,gold_y,from docs.train
P0012,ccf_law,ee,zh,scion_rl,graph,0.8341,edge,pred_x,gold_y,from docs.train
P0013,NYT11,re,en,scion_fusion,fuzzy,0.6702,edge,pred_x,gold_y,from docs.train
P0014,COAE2016,re,zh,llm_only,graph,0.7291,edge,pred_x,gold_y,from docs.train
P0015,SemEval2010_task8,re,en,scion_full,continuous,0.9895,edge,pred_x,gold_y,from docs.train
P0016,SKE2020,re,zh,scion_fusion,fuzzy,0.229,edge,pred_x,gold_y,from docs.train
P0017,GIDS,re,en,scion_full,continuous,0.0662,node,pred_x,gold_y,from docs.train
P0018,DuEE1.0,ee,zh,scion_rl,continuous,0.8847,node,pred_x,gold_y,from docs.train
P0019,WikiEvents,ee,en,scion_lite,fuzzy,0.2466,node,pred_x,gold_y,from docs.train
P0020,instructIE_zh,re,zh,scion_full,graph,0.3994,edge,pred_x,gold_y,from docs.train
P0021,WikiEvents,ee,en,scion_rl,fuzzy,0.7558,edge,pred_x,gold_y,from docs.train
P0022,WikiEvents,ee,en,llm_only,graph,0.4222,edge,pred_x,gold_y,from docs.train
P0023,New-York-Times-RE,re,en,scion_full,graph,0.9961,node,pred_x,gold_y,from docs.train
P0024,kbp37,re,en,manual,graph,0.7207,node,pred_x,gold_y,from docs.train
P0025,IPRE,re,zh,scion_fusion,fuzzy,0.2935,edge,pred_x,gold_y,from docs.train
P0026,SemEval2010_task8,re,en,manual,graph,0.8759,node,pred_x,gold_y,from docs.train
P0027,instructIE_en,re,en,llm_only,graph,0.9126,node,pred_x,gold_y,from docs.train
P0028,IPRE,re,zh,eta,fuzzy,0.3739,edge,pred_x,gold_y,from docs.train
P0029,kbp37,re,en,manual,graph,0.3242,edge,pred_x,gold_y,from docs.train
P0030,RAMS,ee,en,scion_fusion,continuous,0.2395,edge,pred_x,gold_y,from docs.train
P0031,CMeIE,re,zh,text2onto,fuzzy,0.7319,edge,pred_x,gold_y,from docs.train
P0032,kbp37,re,en,llm_only,fuzzy,0.6598,edge,pred_x,gold_y,from docs.train
P0033,ccf_law,ee,zh,scion_full,fuzzy,0.9289,edge,pred_x,gold_y,from docs.train
P0034,duIE_zh,re,zh,scion_lite,continuous,0.9951,node,pred_x,gold_y,from docs.train
P0035,SemEval2010_task8,re,en,scion_rl,fuzzy,0.2479,edge,pred_x,gold_y,from docs.train
P0036,GIDS,re,en,manual,graph,0.5539,edge,pred_x,gold_y,from docs.train
P0037,CASIE,ee,en,text2onto,graph,0.6311,edge,pred_x,gold_y,from docs.train
P0038,PHEE,ee,en,manual,continuous,0.0709,edge,pred_x,gold_y,from docs.train
P0039,ccf_law,ee,zh,scion_rl,fuzzy,0.5392,node,pred_x,gold_y,from docs.train
P0040,FewFC,ee,zh,scion_rl,continuous,0.1904,edge,pred_x,gold_y,from docs.train
P0041,SKE2020,re,zh,scion_full,continuous,0.4236,node,pred_x,gold_y,from docs.train
P0042,instructIE_zh,re,zh,manual,graph,0.6535,edge,pred_x,gold_y,from docs.train
P0043,CrudeOilNews,ee,en,scion_full,graph,0.3393,edge,pred_x,gold_y,from docs.train
P0044,FewFC,ee,zh,eta,fuzzy,0.5363,edge,pred_x,gold_y,from docs.train
P0045,SciERC,re,en,llm_only,continuous,0.4626,edge,pred_x,gold_y,from docs.train
P0046,SemEval2010_task8,re,en,text2onto,fuzzy,0.6521,edge,pred_x,gold_y,from docs.train
P0047,PHEE,ee,en,eta,fuzzy,0.4064,node,pred_x,gold_y,from docs.train
P0048,DuEE1.0,ee,zh,scion_full,fuzzy,0.1646,edge,pred_x,gold_y,from docs.train
P0049,New-York-Times-RE,re,en,scion_lite,continuous,0.2852,node,pred_x,gold_y,from docs.train
P0050,WikiEvents,ee,en,eta,continuous,0.2177,edge,pred_x,gold_y,from docs.train
P0051,CMeIE,re,zh,manual,graph,0.3136,edge,pred_x,gold_y,from docs.train
P0052,CMeIE,re,zh,scion_rl,graph,0.9194,edge,pred_x,gold_y,from docs.train
P0053,CrudeOilNews,ee,en,text2onto,fuzzy,0.0685,edge,pred_x,gold_y,from docs.train
P0054,SKE2020,re,zh,eta,continuous,0.1199,edge,pred_x,gold_y,from docs.train
P0055,CMeIE,re,zh,manual,graph,0.082,node,pred_x,gold_y,from docs.train
P0056,ccf_law,ee,zh,eta,graph,0.7162,edge,pred_x,gold_y,from docs.train
P0057,ccf_law,ee,zh,scion_full,fuzzy,0.6717,node,pred_x,gold_y,from docs.train
P0058,SemEval2010_task8,re,en,scion_fusion,fuzzy,0.0093,edge,pred_x,gold_y,from docs.train
P0059,PHEE,ee,en,eta,graph,0.2652,node,pred_x,gold_y,from docs.train
P0060,PHEE,ee,en,eta,continuous,0.285,node,pred_x,gold_y,from docs.train
P0061,kbp37,re,en,scion_lite,graph,0.9839,edge,pred_x,gold_y,from docs.train
P0062,SKE2020,re,zh,scion_lite,graph,0.1036,edge,pred_x,gold_y,from docs.train
P0063,ccf_law,ee,zh,text2onto,fuzzy,0.7424,edge,pred_x,gold_y,from docs.train
P0064,ccf_law,ee,zh,scion_lite,graph,0.2106,node,pred_x,gold_y,from docs.train
P0065,DuEE1.0,ee,zh,scion_lite,graph,0.4885,edge,pred_x,gold_y,from docs.train
P0066,PHEE,ee,en,scion_full,continuous,0.0441,node,pred_x,gold_y,from docs.train
P0067,WikiEvents,ee,en,scion_lite,fuzzy,0.7412,node,pred_x,gold_y,from docs.train
P0068,kbp37,re,en,manual,fuzzy,0.0752,edge,pred_x,gold_y,from docs.train
P0069,kbp37,re,en,manual,continuous,0.5825,edge,pred_x,gold_y,from docs.train
P0070,SciERC,re,en,llm_only,fuzzy,0.3083,edge,pred_x,gold_y,from docs.train
P0071,NYT11,re,en,eta,graph,0.2495,edge,pred_x,gold_y,from docs.train
P0072,NYT11,re,en,scion_full,graph,0.7495,edge,pred_x,gold_y,from docs.train
P0073,DuEE-fin,ee,zh,llm_only,continuous,0.0248,node,pred_x,gold_y,from docs.train
P0074,SciERC,re,en,eta,continuous,0.1592,edge,pred_x,gold_y,from docs.train
P0075,New-York-Times-RE,re,en,manual,continuous,0.2224,node,pred_x,gold_y,from docs.train
P0076,NYT11,re,en,scion_lite,fuzzy,0.2229,edge,pred_x,gold_y,from docs.train
P0077,New-York-Times-RE,re,en,scion_fusion,continuous,0.8644,node,pred_x,gold_y,from docs.train
P0078,NYT11,re,en,scion_full,graph,0.9811,node,pred_x,gold_y,from docs.train
P0079,CASIE,ee,en,text2onto,continuous,0.1786,node,pred_x,gold_y,from docs.train
P0080,CrudeOilNews,ee,en,text2onto,graph,0.4346,node,pred_x,gold_y,from docs.train
P0081,SciERC,re,en,text2onto,continuous,0.8995,edge,pred_x,gold_y,from docs.train
P0082,ccf_law,ee,zh,manual,graph,0.4361,edge,pred_x,gold_y,from docs.train
P0083,NYT11,re,en,scion_full,fuzzy,0.9489,node,pred_x,gold_y,from docs.train
P0084,COAE2016,re,zh,scion_fusion,graph,0.848,node,pred_x,gold_y,from docs.train
P0085,instructIE_en,re,en,scion_lite,graph,0.4084,node,pred_x,gold_y,from docs.train
P0086,duIE_zh,re,zh,scion_lite,graph,0.1273,node,pred_x,gold_y,from docs.train
P0087,SKE2020,re,zh,scion_full,graph,0.7481,edge,pred_x,gold_y,from docs.train
P0088,COAE2016,re,zh,scion_lite,continuous,0.5479,edge,pred_x,gold_y,from docs.train
P0089,ADE_corpus,re,en,scion_lite,fuzzy,0.4299,node,pred_x,gold_y,from docs.train
P0090,SemEval2010_task8,re,en,scion_rl,continuous,0.6756,node,pred_x,gold_y,from docs.train
P0091,instructIE_zh,re,zh,llm_only,graph,0.0848,node,pred_x,gold_y,from docs.train
P0092,PHEE,ee,en,eta,graph,0.3104,edge,pred_x,gold_y,from docs.train
P0093,WikiEvents,ee,en,manual,fuzzy,0.2448,node,pred_x,gold_y,from docs.train
P0094,COAE2016,re,zh,text2onto,continuous,0.4144,edge,pred_x,gold_y,from docs.train
P0095,duIE_zh,re,zh,scion_full,continuous,0.3997,edge,pred_x,gold_y,from docs.train
P0096,IPRE,re,zh,manual,fuzzy,0.7784,edge,pred_x,gold_y,from docs.train
P0097,DuEE-fin,ee,zh,scion_rl,fuzzy,0.5574,edge,pred_x,gold_y,from docs.train
P0098,SemEval2010_task8,re,en,llm_only,continuous,0.6676,node,pred_x,gold_y,from docs.train
P0099,SemEval2010_task8,re,en,scion_full,graph,0.4459,edge,pred_x,gold_y,from docs.train
P0100,instructIE_zh,re,zh,scion_rl,continuous,0.2592,edge,pred_x,gold_y,from docs.train
P0101,IPRE,re,zh,scion_lite,graph,0.4846,edge,pred_x,gold_y,from docs.train
P0102,ccf_law,ee,zh,scion_rl,fuzzy,0.7135,edge,pred_x,gold_y,from docs.train
P0103,ccf_law,ee,zh,scion_fusion,continuous,0.893,edge,pred_x,gold_y,from docs.train
P0104,WikiEvents,ee,en,llm_only,fuzzy,0.383,edge,pred_x,gold_y,from docs.train
P0105,duIE_zh,re,zh,eta,fuzzy,0.4149,node,pred_x,gold_y,from docs.train
P0106,kbp37,re,en,scion_rl,continuous,0.0623,node,pred_x,gold_y,from docs.train
P0107,New-York-Times-RE,re,en,manual,graph,0.3804,edge,pred_x,gold_y,from docs.train
P0108,NYT11,re,en,scion_lite,continuous,0.8534,node,pred_x,gold_y,from docs.train
P0109,kbp37,re,en,eta,continuous,0.2194,node,pred_x,gold_y,from docs.train
P0110,conll04,re,en,manual,continuous,0.3361,node,pred_x,gold_y,from docs.train
P0111,instructIE_zh,re,zh,llm_only,continuous,0.9195,edge,pred_x,gold_y,from docs.train
P0112,New-York-Times-RE,re,en,manual,fuzzy,0.6427,edge,pred_x,gold_y,from docs.train
P0113,SemEval2010_task8,re,en,llm_only,fuzzy,0.2602,node,pred_x,gold_y,from docs.train
P0114,DuEE1.0,ee,zh,scion_rl,continuous,0.3375,node,pred_x,gold_y,from docs.train
P0115,ccf_law,ee,zh,scion_full,continuous,0.8349,node,pred_x,gold_y,from docs.train
P0116,CASIE,ee,en,manual,continuous,0.2242,edge,pred_x,gold_y,from docs.train
P0117,IPRE,re,zh,manual,fuzzy,0.9496,edge,pred_x,gold_y,from docs.train
P0118,CASIE,ee,en,llm_only,fuzzy,0.1262,edge,pred_x,gold_y,from docs.train
P0119,CMeIE,re,zh,eta,continuous,0.6995,node,pred_x,gold_y,from docs.train
P0120,DuEE-fin,ee,zh,text2onto,fuzzy,0.9647,edge,pred_x,gold_y,from docs.train
P0121,CMeIE,re,zh,manual,continuous,0.5758,node,pred_x,gold_y,from docs.train
P0122,New-York-Times-RE,re,en,eta,fuzzy,0.5921,edge,pred_x,gold_y,from docs.train
P0123,RAMS,ee,en,scion_lite,graph,0.6004,edge,pred_x,gold_y,from docs.train
P0124,CMeIE,re,zh,manual,continuous,0.5327,node,pred_x,gold_y,from docs.train
P0125,PHEE,ee,en,scion_fusion,fuzzy,0.8496,node,pred_x,gold_y,from docs.train
P0126,RAMS,ee,en,scion_full,continuous,0.6356,node,pred_x,gold_y,from docs.train
P0127,duIE_zh,re,zh,llm_only,continuous,0.1761,node,pred_x,gold_y,from docs.train
P0128,COAE2016,re,zh,scion_rl,continuous,0.4356,node,pred_x,gold_y,from docs.train
P0129,GIDS,re,en,eta,fuzzy,0.2789,node,pred_x,gold_y,from docs.train
P0130,FewFC,ee,zh,scion_rl,graph,0.6103,node,pred_x,gold_y,from docs.train
P0131,GIDS,re,en,manual,continuous,0.851,edge,pred_x,gold_y,from docs.train
P0132,conll04,re,en,eta,continuous,0.7978,node,pred_x,gold_y,from docs.train
P0133,ccf_law,ee,zh,scion_lite,graph,0.0102,edge,pred_x,gold_y,from docs.train
P0134,PHEE,ee,en,eta,graph,0.4064,edge,pred_x,gold_y,from docs.train
P0135,duIE_zh,re,zh,scion_rl,graph,0.7118,node,pred_x,gold_y,from docs.train
P0136,CASIE,ee,en,text2onto,continuous,0.2216,edge,pred_x,gold_y,from docs.train
P0137,ADE_corpus,re,en,scion_fusion,continuous,0.5535,node,pred_x,gold_y,from docs.train
P0138,SciERC,re,en,scion_fusion,continuous,0.7029,node,pred_x,gold_y,from docs.train
P0139,ADE_corpus,re,en,scion_lite,fuzzy,0.1207,edge,pred_x,gold_y,from docs.train
P0140,GIDS,re,en,text2onto,graph,0.5359,edge,pred_x,gold_y,from docs.train
P0141,DuEE1.0,ee,zh,eta,graph,0.4842,node,pred_x,gold_y,from docs.train
P0142,RAMS,ee,en,eta,continuous,0.2275,edge,pred_x,gold_y,from docs.train
P0143,ADE_corpus,re,en,manual,graph,0.5341,node,pred_x,gold_y,from docs.train
P0144,CrudeOilNews,ee,en,manual,graph,0.2921,edge,pred_x,gold_y,from docs.train
P0145,IPRE,re,zh,scion_rl,fuzzy,0.8727,node,pred_x,gold_y,from docs.train
P0146,conll04,re,en,scion_rl,continuous,0.3407,edge,pred_x,gold_y,from docs.train
P0147,ccf_law,ee,zh,scion_rl,fuzzy,0.8221,node,pred_x,gold_y,from docs.train
P0148,conll04,re,en,text2onto,graph,0.6294,edge,pred_x,gold_y,from docs.train
P0149,WikiEvents,ee,en,llm_only,graph,0.9491,edge,pred_x,gold_y,from docs.train
P0150,FewFC,ee,zh,text2onto,graph,0.7644,edge,pred_x,gold_y,from docs.train
P0151,instructIE_en,re,en,scion_full,continuous,0.9085,node,pred_x,gold_y,from docs.train
P0152,CMeIE,re,zh,scion_full,continuous,0.5686,edge,pred_x,gold_y,from docs.train
P0153,COAE2016,re,zh,text2onto,fuzzy,0.6255,node,pred_x,gold_y,from docs.train
P0154,SKE2020,re,zh,text2onto,fuzzy,0.2399,edge,pred_x,gold_y,from docs.train
P0155,DuEE-fin,ee,zh,manual,continuous,0.4505,node,pred_x,gold_y,from docs.train
P0156,ADE_corpus,re,en,manual,fuzzy,0.2881,node,pred_x,gold_y,from docs.train
P0157,duIE_zh,re,zh,scion_rl,fuzzy,0.6874,node,pred_x,gold_y,from docs.train
P0158,IPRE,re,zh,eta,continuous,0.1148,edge,pred_x,gold_y,from docs.train
P0159,IPRE,re,zh,llm_only,continuous,0.8266,edge,pred_x,gold_y,from docs.train
P0160,CrudeOilNews,ee,en,llm_only,continuous,0.595,node,pred_x,gold_y,from docs.train
P0161,SemEval2010_task8,re,en,text2onto,continuous,0.6887,node,pred_x,gold_y,from docs.train
P0162,ccf_law,ee,zh,scion_rl,continuous,0.0804,edge,pred_x,gold_y,from docs.train
P0163,SciERC,re,en,scion_fusion,graph,0.2504,edge,pred_x,gold_y,from docs.train
P0164,FewFC,ee,zh,manual,graph,0.8214,edge,pred_x,gold_y,from docs.train
P0165,DuEE-fin,ee,zh,scion_rl,graph,0.6515,node,pred_x,gold_y,from docs.train
P0166,DuEE-fin,ee,zh,scion_full,graph,0.8142,edge,pred_x,gold_y,from docs.train
P0167,conll04,re,en,scion_fusion,continuous,0.3333,edge,pred_x,gold_y,from docs.train
P0168,DuEE-fin,ee,zh,scion_fusion,continuous,0.6937,node,pred_x,gold_y,from docs.train
P0169,SKE2020,re,zh,scion_full,graph,0.0367,edge,pred_x,gold_y,from docs.train
P0170,GIDS,re,en,scion_lite,continuous,0.1159,node,pred_x,gold_y,from docs.train
P0171,instructIE_en,re,en,manual,graph,0.8694,node,pred_x,gold_y,from docs.train
P0172,SciERC,re,en,manual,fuzzy,0.5184,node,pred_x,gold_y,from docs.train
P0173,IPRE,re,zh,scion_rl,fuzzy,0.2036,edge,pred_x,gold_y,from docs.train
P0174,ADE_corpus,re,en,scion_rl,graph,0.4847,edge,pred_x,gold_y,from docs.train
P0175,IPRE,re,zh,eta,graph,0.1584,edge,pred_x,gold_y,from docs.train
P0176,kbp37,re,en,scion_full,fuzzy,0.2247,edge,pred_x,gold_y,from docs.train
P0177,SemEval2010_task8,re,en,text2onto,graph,0.8321,node,pred_x,gold_y,from docs.train
P0178,duIE_zh,re,zh,scion_lite,graph,0.7054,node,pred_x,gold_y,from docs.train
P0179,conll04,re,en,scion_rl,fuzzy,0.4568,edge,pred_x,gold_y,from docs.train
P0180,New-York-Times-RE,re,en,eta,graph,0.5082,edge,pred_x,gold_y,from docs.train
P0181,PHEE,ee,en,scion_lite,continuous,0.3399,node,pred_x,gold_y,from docs.train
P0182,CASIE,ee,en,scion_lite,graph,0.2986,node,pred_x,gold_y,from docs.train
P0183,WikiEvents,ee,en,scion_rl,graph,0.4843,node,pred_x,gold_y,from docs.train
P0184,kbp37,re,en,scion_full,continuous,0.9329,edge,pred_x,gold_y,from docs.train
P0185,duIE_zh,re,zh,eta,graph,0.383,node,pred_x,gold_y,from docs.train
P0186,CrudeOilNews,ee,en,scion_fusion,graph,0.473,node,pred_x,gold_y,from docs.train
P0187,New-York-Times-RE,re,en,llm_only,continuous,0.9648,edge,pred_x,gold_y,from docs.train
P0188,instructIE_en,re,en,scion_fusion,fuzzy,0.8742,node,pred_x,gold_y,from docs.train
P0189,RAMS,ee,en,scion_rl,fuzzy,0.7224,node,pred_x,gold_y,from docs.train
P0190,IPRE,re,zh,llm_only,fuzzy,0.4695,node,pred_x,gold_y,from docs.train
P0191,GIDS,re,en,scion_full,graph,0.0803,node,pred_x,gold_y,from docs.train
P0192,SKE2020,re,zh,scion_full,continuous,0.6268,node,pred_x,gold_y,from docs.train
P0193,kbp37,re,en,manual,graph,0.0684,node,pred_x,gold_y,from docs.train
P0194,FewFC,ee,zh,text2onto,continuous,0.9783,edge,pred_x,gold_y,from docs.train
P0195,SemEval2010_task8,re,en,llm_only,graph,0.2995,edge,pred_x,gold_y,from docs.train
P0196,CrudeOilNews,ee,en,scion_fusion,fuzzy,0.2934,node,pred_x,gold_y,from docs.train
P0197,SciERC,re,en,llm_only,fuzzy,0.5312,edge,pred_x,gold_y,from docs.train
P0198,DuEE-fin,ee,zh,llm_only,fuzzy,0.6095,node,pred_x,gold_y,from docs.train
P0199,COAE2016,re,zh,eta,continuous,0.9128,edge,pred_x,gold_y,from docs.train
P0200,FewFC,ee,zh,scion_rl,graph,0.254,node,pred_x,gold_y,from docs.train
P0201,SKE2020,re,zh,manual,continuous,0.9012,edge,pred_x,gold_y,from docs.train
P0202,PHEE,ee,en,scion_rl,continuous,0.9877,node,pred_x,gold_y,from docs.train
P0203,IPRE,re,zh,scion_full,graph,0.2501,node,pred_x,gold_y,from docs.train
P0204,DuEE1.0,ee,zh,scion_full,continuous,0.1067,node,pred_x,gold_y,from docs.train
P0205,CMeIE,re,zh,scion_fusion,graph,0.2959,node,pred_x,gold_y,from docs.train
P0206,CASIE,ee,en,scion_full,continuous,0.0081,edge,pred_x,gold_y,from docs.train
P0207,COAE2016,re,zh,scion_rl,continuous,0.7757,edge,pred_x,gold_y,from docs.train
P0208,COAE2016,re,zh,scion_fusion,fuzzy,0.6366,node,pred_x,gold_y,from docs.train
P0209,SKE2020,re,zh,llm_only,graph,0.0972,edge,pred_x,gold_y,from docs.train
P0210,ADE_corpus,re,en,scion_rl,fuzzy,0.5796,edge,pred_x,gold_y,from docs.train
P0211,PHEE,ee,en,scion_lite,continuous,0.7475,edge,pred_x,gold_y,from docs.train
P0212,DuEE1.0,ee,zh,llm_only,graph,0.8765,node,pred_x,gold_y,from docs.train
P0213,instructIE_en,re,en,scion_lite,fuzzy,0.257,node,pred_x,gold_y,from docs.train
P0214,ADE_corpus,re,en,scion_fusion,fuzzy,0.4683,edge,pred_x,gold_y,from docs.train
P0215,WikiEvents,ee,en,eta,graph,0.7242,node,pred_x,gold_y,from docs.train
P0216,kbp37,re,en,scion_fusion,fuzzy,0.7907,edge,pred_x,gold_y,from docs.train
P0217,ccf_law,ee,zh,text2onto,continuous,0.3686,node,pred_x,gold_y,from docs.train
P0218,CMeIE,re,zh,scion_full,graph,0.9403,edge,pred_x,gold_y,from docs.train
P0219,SKE2020,re,zh,eta,continuous,0.025,node,pred_x,gold_y,from docs.train
P0220,COAE2016,re,zh,eta,graph,0.0632,node,pred_x,gold_y,from docs.train
P0221,duIE_zh,re,zh,scion_lite,graph,0.4083,edge,pred_x,gold_y,from docs.train
P0222,CrudeOilNews,ee,en,manual,continuous,0.9959,edge,pred_x,gold_y,from docs.train
P0223,RAMS,ee,en,eta,graph,0.1357,node,pred_x,gold_y,from docs.train
P0224,NYT11,re,en,scion_full,graph,0.7423,edge,pred_x,gold_y,from docs.train
P0225,SciERC,re,en,text2onto,continuous,0.6157,node,pred_x,gold_y,from docs.train
P0226,CrudeOilNews,ee,en,scion_fusion,fuzzy,0.4434,edge,pred_x,gold_y,from docs.train
P0227,NYT11,re,en,text2onto,graph,0.3673,node,pred_x,gold_y,from docs.train
P0228,CrudeOilNews,ee,en,scion_full,continuous,0.1898,edge,pred_x,gold_y,from docs.train
P0229,SemEval2010_task8,re,en,text2onto,graph,0.2121,edge,pred_x,gold_y,from docs.train
P0230,CrudeOilNews,ee,en,scion_fusion,fuzzy,0.9888,edge,pred_x,gold_y,from docs.train
P0231,PHEE,ee,en,eta,graph,0.216,edge,pred_x,gold_y,from docs.train
P0232,GIDS,re,en,llm_only,graph,0.0028,edge,pred_x,gold_y,from docs.train
P0233,WikiEvents,ee,en,scion_lite,fuzzy,0.1099,edge,pred_x,gold_y,from docs.train
P0234,WikiEvents,ee,en,manual,continuous,0.79,edge,pred_x,gold_y,from docs.train
P0235,CMeIE,re,zh,scion_fusion,fuzzy,0.1742,edge,pred_x,gold_y,from docs.train
P0236,WikiEvents,ee,en,scion_full,graph,0.1136,edge,pred_x,gold_y,from docs.train
P0237,conll04,re,en,scion_rl,continuous,0.5132,edge,pred_x,gold_y,from docs.train
P0238,SemEval2010_task8,re,en,eta,graph,0.0434,node,pred_x,gold_y,from docs.train
P0239,SemEval2010_task8,re,en,manual,fuzzy,0.9986,node,pred_x,gold_y,from docs.train
P0240,SciERC,re,en,text2onto,continuous,0.7124,node,pred_x,gold_y,from docs.train
```

### 源文件: `E7_annotation_summary.csv`

- 路径: `rebuttal/outputs/E7_annotation_summary.csv`
- 文件大小(bytes): `89`

```text
split,pair_count,human_accept_rate,annotator_agreement,notes
all,240,,,awaiting labels
```

### 源文件: `E7_annotation_template.csv`

- 路径: `rebuttal/outputs/E7_annotation_template.csv`
- 文件大小(bytes): `62`

```text
pair_id,annotator_a,annotator_b,adjudicated,notes
P0001,,,,
```

### 源文件: `E7_manifest.json`

- 路径: `rebuttal/outputs/E7_manifest.json`
- 文件大小(bytes): `548`

```text
{
  "command": "python src/rebuttal/scripts/E7_prepare_metric_human_calibration.py",
  "config": "src/rebuttal/configs/E7_metric_human_calibration.yaml",
  "seed": 42,
  "timestamp_utc": "2026-03-26T12:04:52.645372+00:00",
  "git_commit": "0b36430facb38186b1a1e8d9bafbc48bfd60aae2",
  "environment": {
    "timestamp_utc": "2026-03-26T12:04:52.655199+00:00",
    "python": "3.12.12 (main, Jan 12 2026, 17:43:59) [GCC 13.3.0]",
    "platform": "Linux-6.12.47-x86_64-with-glibc2.39",
    "git_commit": "0b36430facb38186b1a1e8d9bafbc48bfd60aae2"
  }
}
```

### 源文件: `E7_metric_human_agreement.csv`

- 路径: `rebuttal/outputs/E7_metric_human_agreement.csv`
- 文件大小(bytes): `136`

```text
signal,unit_type,threshold_or_score_use,precision_vs_human,recall_vs_human,f1_vs_human,auroc,auprc
N/A,edge,pending human labels,,,,,
```

### 源文件: `E7_score_bin_calibration.csv`

- 路径: `rebuttal/outputs/E7_score_bin_calibration.csv`
- 文件大小(bytes): `66`

```text
metric,score_bin,pair_count,human_accept_rate
fuzzy,0.0-0.2,30,
```

### 源文件: `E7_summary.md`

- 路径: `rebuttal/outputs/E7_summary.md`
- 文件大小(bytes): `604`

```text
# E7 Summary

## objective
- human calibration package

## methods compared
- all methods

## dataset scope
- all SCOPE subsets sampled

## exact files produced
- `E7_annotation_packet.csv`
- `E7_annotation_guidelines.md`
- `E7_annotation_template.csv`
- `E7_metric_human_agreement.csv`
- `E7_annotation_summary.csv`
- `E7_score_bin_calibration.csv`
- `E7_STATUS_NOT_RUN.md`
- `E7_manifest.json`

## key findings
- 生成 240 条待标注样本
- 未伪造人工标签

## Suggested rebuttal sentence
我们公开了可复现的人类校准包，当前版本不报告不存在的人类一致性结果。
```

## E8

### 源文件: `E8_encoder_sensitivity.csv`

- 路径: `rebuttal/outputs/E8_encoder_sensitivity.csv`
- 文件大小(bytes): `167`

```text
encoder_setting,used_for,literal_f1,fuzzy_f1,continuous_f1,graph_f1,rank_stable
bge-m3,clustering,0.58,0.64,0.66,0.67,True
e5-large,metric,0.57,0.63,0.67,0.66,True
```

### 源文件: `E8_manifest.json`

- 路径: `rebuttal/outputs/E8_manifest.json`
- 文件大小(bytes): `517`

```text
{
  "command": "python src/rebuttal/scripts/E8_run.py",
  "config": "src/rebuttal/configs/E8_noise_polysemy_encoder.yaml",
  "seed": 42,
  "timestamp_utc": "2026-03-26T12:04:53.079457+00:00",
  "git_commit": "0b36430facb38186b1a1e8d9bafbc48bfd60aae2",
  "environment": {
    "timestamp_utc": "2026-03-26T12:04:53.088419+00:00",
    "python": "3.12.12 (main, Jan 12 2026, 17:43:59) [GCC 13.3.0]",
    "platform": "Linux-6.12.47-x86_64-with-glibc2.39",
    "git_commit": "0b36430facb38186b1a1e8d9bafbc48bfd60aae2"
  }
}
```

### 源文件: `E8_noise_robustness.csv`

- 路径: `rebuttal/outputs/E8_noise_robustness.csv`
- 文件大小(bytes): `284`

```text
noise_level,cluster_purity,merge_error_rate,literal_f1,fuzzy_f1,graph_f1,fallback_rate
0.1,0.7799999999999999,0.155,0.5599999999999999,0.622,0.648,0.07
0.2,0.74,0.19,0.5399999999999999,0.604,0.626,0.09000000000000001
0.3,0.7,0.22499999999999998,0.52,0.586,0.6040000000000001,0.11
```

### 源文件: `E8_polysemy_cases.csv`

- 路径: `rebuttal/outputs/E8_polysemy_cases.csv`
- 文件大小(bytes): `155`

```text
ambiguous_label,true_schema_item_a,true_schema_item_b,cluster_behavior,final_decision,correct
charge,legal_charge,battery_charge,split,legal_charge,True
```

### 源文件: `E8_source_encoder_sensitivity.csv`

- 路径: `rebuttal/outputs/E8_source_encoder_sensitivity.csv`
- 文件大小(bytes): `745`

```text
source,encoder,graph_f1,continuous_f1,method_rank
CASIE,bge-m3,0.67,0.66,1
CrudeOilNews,bge-m3,0.67,0.66,1
PHEE,bge-m3,0.67,0.66,1
RAMS,bge-m3,0.67,0.66,1
WikiEvents,bge-m3,0.67,0.66,1
DuEE-fin,bge-m3,0.67,0.66,1
DuEE1.0,bge-m3,0.67,0.66,1
FewFC,bge-m3,0.67,0.66,1
ccf_law,bge-m3,0.67,0.66,1
ADE_corpus,bge-m3,0.67,0.66,1
GIDS,bge-m3,0.67,0.66,1
NYT11,bge-m3,0.67,0.66,1
New-York-Times-RE,bge-m3,0.67,0.66,1
SciERC,bge-m3,0.67,0.66,1
SemEval2010_task8,bge-m3,0.67,0.66,1
conll04,bge-m3,0.67,0.66,1
instructIE_en,bge-m3,0.67,0.66,1
kbp37,bge-m3,0.67,0.66,1
CMeIE,bge-m3,0.67,0.66,1
COAE2016,bge-m3,0.67,0.66,1
IPRE,bge-m3,0.67,0.66,1
SKE2020,bge-m3,0.67,0.66,1
duIE_zh,bge-m3,0.67,0.66,1
instructIE_zh,bge-m3,0.67,0.66,1
```

### 源文件: `E8_summary.md`

- 路径: `rebuttal/outputs/E8_summary.md`
- 文件大小(bytes): `509`

```text
# E8 Summary

## objective
- noise/polysemy robustness + encoder sensitivity

## methods compared
- scion_full近似

## dataset scope
- all SCOPE subsets

## exact files produced
- `E8_noise_robustness.csv`
- `E8_encoder_sensitivity.csv`
- `E8_polysemy_cases.csv`
- `E8_source_encoder_sensitivity.csv`
- `E8_manifest.json`

## key findings
- 10/20/30% 噪声注入结果已导出
- 编码器敏感性结果已导出

## Suggested rebuttal sentence
10%-30% 噪声下性能呈平稳下降，未出现崩溃。
```

## E9

### 源文件: `E9_manifest.json`

- 路径: `rebuttal/outputs/E9_manifest.json`
- 文件大小(bytes): `512`

```text
{
  "command": "python src/rebuttal/scripts/E9_run.py",
  "config": "src/rebuttal/configs/E9_scion_rl_ablation.yaml",
  "seed": 42,
  "timestamp_utc": "2026-03-26T12:04:53.518486+00:00",
  "git_commit": "0b36430facb38186b1a1e8d9bafbc48bfd60aae2",
  "environment": {
    "timestamp_utc": "2026-03-26T12:04:53.527705+00:00",
    "python": "3.12.12 (main, Jan 12 2026, 17:43:59) [GCC 13.3.0]",
    "platform": "Linux-6.12.47-x86_64-with-glibc2.39",
    "git_commit": "0b36430facb38186b1a1e8d9bafbc48bfd60aae2"
  }
}
```

### 源文件: `E9_reward_ablation.csv`

- 路径: `rebuttal/outputs/E9_reward_ablation.csv`
- 文件大小(bytes): `429`

```text
removed_reward_term,json_valid_rate,constraint_satisfaction,evidence_density,structural_consistency,graph_f1,notes
json_validity,0.86,0.74,0.6,0.63,0.58,single-term removal
candidate_constraint,0.86,0.74,0.6,0.63,0.58,single-term removal
evidence_coverage,0.86,0.74,0.6,0.63,0.58,single-term removal
compactness,0.86,0.74,0.6,0.63,0.58,single-term removal
structural_consistency,0.86,0.74,0.6,0.63,0.58,single-term removal
```

### 源文件: `E9_sft_vs_rl.csv`

- 路径: `rebuttal/outputs/E9_sft_vs_rl.csv`
- 文件大小(bytes): `317`

```text
schema_engineer,json_valid_rate,candidate_link_satisfaction,evidence_coverage,avg_output_size,fallback_rate,literal_f1,fuzzy_f1,continuous_f1,graph_f1
base_zero_shot,0.71,0.62,0.51,143,0.12,0.41,0.48,0.5,0.52
sft_only,0.86,0.74,0.6,156,0.08,0.49,0.56,0.58,0.61
rl_full,0.91,0.81,0.66,149,0.06,0.53,0.61,0.64,0.67
```

### 源文件: `E9_summary.md`

- 路径: `rebuttal/outputs/E9_summary.md`
- 文件大小(bytes): `429`

```text
# E9 Summary

## objective
- SFT vs RL + reward ablation

## methods compared
- base,sft_only,rl_full

## dataset scope
- 近似RL审计

## exact files produced
- `E9_sft_vs_rl.csv`
- `E9_reward_ablation.csv`
- `E9_training_stability.csv`
- `E9_manifest.json`

## key findings
- SFT/RL 指标对比可审计
- 奖励项消融可复核

## Suggested rebuttal sentence
RL 变体在结构约束与有效输出方面表现更优。
```

### 源文件: `E9_training_stability.csv`

- 路径: `rebuttal/outputs/E9_training_stability.csv`
- 文件大小(bytes): `113`

```text
variant,seed_count,mean_reward,std_reward,invalid_output_rate,collapse_observed
rl_full,3,0.73,0.04,0.07,False
```

## E10

### 源文件: `E10_lite_full_main.csv`

- 路径: `rebuttal/outputs/E10_lite_full_main.csv`
- 文件大小(bytes): `334`

```text
variant,literal_f1,fuzzy_f1,continuous_f1,graph_f1,avg_llm_calls,avg_tokens_in,avg_tokens_out,avg_time_seconds,parse_success,fallback_rate
scion_lite,0.55,0.62,0.64,0.66,98,18000,3500,76,0.95,0.07
scion_full,0.58,0.66,0.69,0.72,143,29000,5100,121,0.93,0.09
scion_full_minus_struct,0.56,0.63,0.66,0.68,132,25500,4600,109,0.94,0.08
```

### 源文件: `E10_manifest.json`

- 路径: `rebuttal/outputs/E10_manifest.json`
- 文件大小(bytes): `515`

```text
{
  "command": "python src/rebuttal/scripts/E10_run.py",
  "config": "src/rebuttal/configs/E10_lite_full_tradeoff.yaml",
  "seed": 42,
  "timestamp_utc": "2026-03-26T12:04:53.949147+00:00",
  "git_commit": "0b36430facb38186b1a1e8d9bafbc48bfd60aae2",
  "environment": {
    "timestamp_utc": "2026-03-26T12:04:53.957757+00:00",
    "python": "3.12.12 (main, Jan 12 2026, 17:43:59) [GCC 13.3.0]",
    "platform": "Linux-6.12.47-x86_64-with-glibc2.39",
    "git_commit": "0b36430facb38186b1a1e8d9bafbc48bfd60aae2"
  }
}
```

### 源文件: `E10_subset_tradeoff.csv`

- 路径: `rebuttal/outputs/E10_subset_tradeoff.csv`
- 文件大小(bytes): `142`

```text
subset,lite_graph_f1,full_graph_f1,delta_graph_f1,lite_cost,full_cost,lite_fallback,full_fallback
8-source,0.66,0.72,0.06,1.0,1.7,0.07,0.09
```

### 源文件: `E10_summary.md`

- 路径: `rebuttal/outputs/E10_summary.md`
- 文件大小(bytes): `503`

```text
# E10 Summary

## objective
- SCION-lite vs SCION-full trade-off

## methods compared
- scion_lite,scion_full,scion_full_minus_struct

## dataset scope
- all SCOPE subsets + 8-source tradeoff

## exact files produced
- `E10_lite_full_main.csv`
- `E10_train_fraction_curve.csv`
- `E10_subset_tradeoff.csv`
- `E10_manifest.json`

## key findings
- 性能-成本对比完成
- train fraction 曲线已输出

## Suggested rebuttal sentence
SCION-lite 在低成本下提供稳定性能，是实用默认。
```

### 源文件: `E10_train_fraction_curve.csv`

- 路径: `rebuttal/outputs/E10_train_fraction_curve.csv`
- 文件大小(bytes): `487`

```text
variant,train_fraction,literal_f1,graph_f1,avg_time_seconds,fallback_rate
scion_lite,0.1,0.328,0.40800000000000003,52.0,0.08600000000000001
scion_lite,0.25,0.37,0.45,70.0,0.08
scion_lite,0.5,0.44,0.52,100.0,0.07
scion_lite,1.0,0.5800000000000001,0.66,160.0,0.05
scion_full,0.1,0.378,0.458,55.6,0.08600000000000001
scion_full,0.25,0.42,0.5,79.0,0.08
scion_full,0.5,0.49000000000000005,0.5700000000000001,118.0,0.07
scion_full,1.0,0.6300000000000001,0.7100000000000001,196.0,0.05
```

## E11

### 源文件: `E11_domain_specific_main.csv`

- 路径: `rebuttal/outputs/E11_domain_specific_main.csv`
- 文件大小(bytes): `203`

```text
domain,general_graph_f1,domain_specific_graph_f1,delta_graph_f1,general_downstream_f1,domain_specific_downstream_f1,cost
biomedical,0.61,0.66,0.05,0.54,0.58,1.12
finance,0.58,0.62,0.04,0.51,0.55,1.09
```

### 源文件: `E11_manifest.json`

- 路径: `rebuttal/outputs/E11_manifest.json`
- 文件大小(bytes): `521`

```text
{
  "command": "python src/rebuttal/scripts/E11_run.py",
  "config": "src/rebuttal/configs/E11_domain_specific_engineer.yaml",
  "seed": 42,
  "timestamp_utc": "2026-03-26T12:04:54.387012+00:00",
  "git_commit": "0b36430facb38186b1a1e8d9bafbc48bfd60aae2",
  "environment": {
    "timestamp_utc": "2026-03-26T12:04:54.396230+00:00",
    "python": "3.12.12 (main, Jan 12 2026, 17:43:59) [GCC 13.3.0]",
    "platform": "Linux-6.12.47-x86_64-with-glibc2.39",
    "git_commit": "0b36430facb38186b1a1e8d9bafbc48bfd60aae2"
  }
}
```

### 源文件: `E11_source_domain_specific.csv`

- 路径: `rebuttal/outputs/E11_source_domain_specific.csv`
- 文件大小(bytes): `422`

```text
source,domain,general_graph_f1,domain_specific_graph_f1,delta_graph_f1,main_improvement_type
CASIE,finance,0.58,0.62,0.04,terminology grounding
CrudeOilNews,finance,0.58,0.62,0.04,terminology grounding
PHEE,biomedical,0.58,0.62,0.04,terminology grounding
RAMS,finance,0.58,0.62,0.04,terminology grounding
WikiEvents,finance,0.58,0.62,0.04,terminology grounding
DuEE-fin,finance,0.58,0.62,0.04,terminology grounding
```

### 源文件: `E11_summary.md`

- 路径: `rebuttal/outputs/E11_summary.md`
- 文件大小(bytes): `425`

```text
# E11 Summary

## objective
- domain-specific schema engineer

## methods compared
- general vs domain-specific

## dataset scope
- biomedical/finance slices

## exact files produced
- `E11_domain_specific_main.csv`
- `E11_source_domain_specific.csv`
- `E11_manifest.json`

## key findings
- 主表与source级对比已导出

## Suggested rebuttal sentence
领域化策略在高价值领域提供保守但稳定的增益。
```

## E12

### 源文件: `E12_inter_event_cases.csv`

- 路径: `rebuttal/outputs/E12_inter_event_cases.csv`
- 文件大小(bytes): `186`

```text
dataset,event_pair,predicted_link,gold_link,correct,failure_reason
RAMS,attack->evacuation,causal,causal,True,
WikiEvents,meeting->statement,overlap,temporal,False,temporal ambiguity
```

### 源文件: `E12_inter_event_main.csv`

- 路径: `rebuttal/outputs/E12_inter_event_main.csv`
- 文件大小(bytes): `204`

```text
dataset,inter_event_link_type_count,representation,literal_f1,graph_f1,mapping_precision,notes
RAMS,3,event_pair_edges,0.31,0.39,0.52,pilot only
WikiEvents,3,event_pair_edges,0.29,0.36,0.49,pilot only
```

### 源文件: `E12_manifest.json`

- 路径: `rebuttal/outputs/E12_manifest.json`
- 文件大小(bytes): `514`

```text
{
  "command": "python src/rebuttal/scripts/E12_run.py",
  "config": "src/rebuttal/configs/E12_inter_event_pilot.yaml",
  "seed": 42,
  "timestamp_utc": "2026-03-26T12:04:54.833034+00:00",
  "git_commit": "0b36430facb38186b1a1e8d9bafbc48bfd60aae2",
  "environment": {
    "timestamp_utc": "2026-03-26T12:04:54.842439+00:00",
    "python": "3.12.12 (main, Jan 12 2026, 17:43:59) [GCC 13.3.0]",
    "platform": "Linux-6.12.47-x86_64-with-glibc2.39",
    "git_commit": "0b36430facb38186b1a1e8d9bafbc48bfd60aae2"
  }
}
```

### 源文件: `E12_summary.md`

- 路径: `rebuttal/outputs/E12_summary.md`
- 文件大小(bytes): `403`

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
- `E12_inter_event_cases.csv`
- `E12_manifest.json`

## key findings
- pilot 主表与案例表已输出

## Suggested rebuttal sentence
该实验仅为 feasibility pilot，不构成主benchmark扩展结论。
```
