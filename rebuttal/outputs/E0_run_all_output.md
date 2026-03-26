# E0 Run All Output Details

- generated_by: `src/rebuttal/scripts/E0_run_all.py`
- output_preview_char_limit: `20000`

## E1

### 源文件: `E1_main_metrics.csv`

- 路径: `rebuttal/outputs/E1_main_metrics.csv`
- 文件大小(bytes): `4656`

```text
method,target,literal_p,literal_r,literal_f1,fuzzy_p,fuzzy_r,fuzzy_f1,continuous_p,continuous_r,continuous_f1,graph_p,graph_r,graph_f1,delta_vs_strongest_non_scion,p_value
manual,full_gold,0.8661319655822858,0.543075460063234,0.662860158299508,1.0,0.7511246749049239,0.8483733571418774,0.9726160660951603,0.7993816339868686,0.875489055405104,0.7780928528761283,0.6395053071894948,0.7003912443240833,-0.044923429823580996,0.0025768280029296875
manual,reachable_gold,0.7950129417870656,0.5144571858263778,0.618202571279291,0.9166666666666666,0.6772124157099522,0.7689908919268856,0.8913168264262521,0.7363990524819483,0.8048663192490881,0.7130534611410017,0.5891192419855588,0.6438930553992707,-0.04075764321890685,0.0025768280029296875
text2onto,full_gold,0.9044192259235556,0.6251158829963464,0.7365991278719434,1.0,0.79478886645459,0.8786348179309003,0.9796711800573167,0.8404981386475563,0.9035884008509937,0.7837369440458534,0.6723985109180451,0.7228707206807949,-0.022443953466869337,0.5034446716308594
text2onto,reachable_gold,0.8407888951424144,0.5920132066059957,0.6910983003439081,0.9166666666666666,0.7257631729476106,0.8028278001775329,0.9013985742527318,0.7733805110688442,0.8314253961126489,0.7211188594021856,0.6187044088550754,0.6651403168901192,-0.0195103817280583,0.5034446716308594
llm_only,full_gold,0.9410277637006073,0.7026309487516974,0.8016509359373618,1.0,0.8636639790561907,0.9230313755659932,0.9877470654528601,0.8830752560597754,0.9316433426845804,0.7901976523622881,0.7064602048478203,0.7453146741476643,0.0,0.1670684814453125
llm_only,reachable_gold,0.8662775376348953,0.6659315272270794,0.750603129051444,0.9166666666666666,0.7713469134516743,0.8334682594854371,0.9064062221157404,0.8071873852071163,0.8533196726112108,0.7251249776925923,0.6457499081656931,0.6826557380889686,-0.001994960529208889,0.1670684814453125
eta,full_gold,0.9461636913683065,0.721992744960949,0.8162019604085087,1.0,0.8634996017683049,0.9211135887068295,0.9891366139090035,0.881938978266537,0.9305734404065237,0.7913092911272029,0.7055511826132297,0.744458752325219,-0.0008559218224453158,0.18924713134765625
eta,reachable_gold,0.8707428779054056,0.6785284982375619,0.7602959185845366,0.9166666666666666,0.7792811626902624,0.8383288287496363,0.9072605947255997,0.8111969892925573,0.8558133732727219,0.7258084757804798,0.6489575914340459,0.6846506986181775,0.0,0.18924713134765625
scion_lite,full_gold,0.9694991432432256,0.8069764969149767,0.8798656523777649,1.0,0.9086601046676942,0.9504600828689288,0.9936891337185783,0.9207902791544265,0.9555372358576698,0.7949513069748626,0.7366322233235413,0.7644297886861358,0.019115114538471478,0.1670684814453125
scion_lite,reachable_gold,0.8908943132801285,0.7489872539249202,0.8126414261243845,0.9166666666666666,0.8197627328034263,0.8636408735994726,0.9115621293342812,0.841592241387391,0.8748950004179705,0.729249703467425,0.6732737931099129,0.6999160003343765,0.015265301716198998,0.1670684814453125
scion_fusion,full_gold,0.9801610505563128,0.8472344862697431,0.9082723136908702,1.0,0.9280078006102044,0.9614998315222412,0.9960748931722793,0.9391295613813515,0.9665478744337119,0.7968599145378236,0.7513036491050813,0.7732382995469695,0.027923625399305263,0.480682373046875
scion_fusion,reachable_gold,0.8974970746118376,0.7835665102142292,0.835962210243571,0.9166666666666666,0.8378686526294206,0.8738941949622746,0.9127000362700054,0.8588216657544797,0.884748725154694,0.7301600290160044,0.6870573326035839,0.7077989801237553,0.023148281505577795,0.480682373046875
scion_full,full_gold,0.9869087482047362,0.8718052201304344,0.9251202970655505,1.0,0.9444356199332323,0.9703681184356253,0.9973372859309128,0.9477191633498867,0.9716411805374735,0.7978698287447302,0.7581753306799094,0.7773129444299789,0.03199827028231461,0.237884521484375
scion_full,reachable_gold,0.9065972208609949,0.807701894767037,0.8537004814854517,0.9166666666666666,0.843953962366868,0.8778231908276086,0.9145733079025232,0.8654326848899302,0.8890921500911569,0.7316586463220185,0.6923461479119442,0.7112737200729256,0.02662302145474804,0.237884521484375
scion_rl,full_gold,0.9900813415541063,0.8893031030287618,0.9362898269504495,1.0,0.9530126001879585,0.9750545510528873,0.9979226488999338,0.9552210947571652,0.9758852738043927,0.798338119119947,0.7641768758057322,0.7807082190435142,0.03539354489584989,0.143463134765625
scion_rl,reachable_gold,0.9084541399174646,0.8254023000896232,0.8644562378799843,0.9166666666666666,0.8621885469762086,0.8879728465663302,0.9150057618098569,0.8742244416963412,0.8939827959902497,0.7320046094478857,0.699379553357073,0.7151862367921997,0.030535538174022214,0.143463134765625
```

### 源文件: `E1_manifest.json`

- 路径: `rebuttal/outputs/E1_manifest.json`
- 文件大小(bytes): `524`

```text
{
  "command": "python src/rebuttal/scripts/E1_run_reachable_eval.py",
  "config": "src/rebuttal/configs/E1_reachable_eval.yaml",
  "seed": 42,
  "timestamp_utc": "2026-03-26T12:58:00.919287+00:00",
  "git_commit": "6728f7f1d53a2b95d153c9ed073e51526a5fe852",
  "environment": {
    "timestamp_utc": "2026-03-26T12:58:00.931552+00:00",
    "python": "3.12.12 (main, Jan 12 2026, 17:43:59) [GCC 13.3.0]",
    "platform": "Linux-6.12.47-x86_64-with-glibc2.39",
    "git_commit": "6728f7f1d53a2b95d153c9ed073e51526a5fe852"
  }
}
```

### 源文件: `E1_recall_breakdown.csv`

- 路径: `rebuttal/outputs/E1_recall_breakdown.csv`
- 文件大小(bytes): `1555`

```text
method,full_literal_r,full_fuzzy_r,full_continuous_r,full_graph_r,reachable_literal_r,reachable_fuzzy_r,reachable_continuous_r,reachable_graph_r,pred_item_count
manual,0.543075460063234,0.7511246749049239,0.7993816339868686,0.6395053071894948,0.5144571858263778,0.6772124157099522,0.7363990524819483,0.5891192419855588,43.083333333333336
text2onto,0.6251158829963464,0.79478886645459,0.8404981386475563,0.6723985109180451,0.5920132066059957,0.7257631729476106,0.7733805110688442,0.6187044088550754,47.125
llm_only,0.7026309487516974,0.8636639790561907,0.8830752560597754,0.7064602048478203,0.6659315272270794,0.7713469134516743,0.8071873852071163,0.6457499081656931,51.583333333333336
eta,0.721992744960949,0.8634996017683049,0.881938978266537,0.7055511826132297,0.6785284982375619,0.7792811626902624,0.8111969892925573,0.6489575914340459,52.583333333333336
scion_lite,0.8069764969149767,0.9086601046676942,0.9207902791544265,0.7366322233235413,0.7489872539249202,0.8197627328034263,0.841592241387391,0.6732737931099129,56.666666666666664
scion_fusion,0.8472344862697431,0.9280078006102044,0.9391295613813515,0.7513036491050813,0.7835665102142292,0.8378686526294206,0.8588216657544797,0.6870573326035839,58.625
scion_full,0.8718052201304344,0.9444356199332323,0.9477191633498867,0.7581753306799094,0.807701894767037,0.843953962366868,0.8654326848899302,0.6923461479119442,60.125
scion_rl,0.8893031030287618,0.9530126001879585,0.9552210947571652,0.7641768758057322,0.8254023000896232,0.8621885469762086,0.8742244416963412,0.699379553357073,61.125
```

### 源文件: `E1_source_reachable_ratio.csv`

- 路径: `rebuttal/outputs/E1_source_reachable_ratio.csv`
- 文件大小(bytes): `832`

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
ADE_corpus,re,en,1,1,1.0
GIDS,re,en,4,0,0.0
NYT11,re,en,12,12,1.0
New-York-Times-RE,re,en,24,1,0.041666666666666664
SciERC,re,en,7,7,1.0
SemEval2010_task8,re,en,11,10,0.9090909090909091
conll04,re,en,5,5,1.0
instructIE_en,re,en,116,103,0.8879310344827587
kbp37,re,en,18,18,1.0
CMeIE,re,zh,53,53,1.0
COAE2016,re,zh,18,9,0.5
IPRE,re,zh,70,31,0.44285714285714284
SKE2020,re,zh,49,49,1.0
duIE_zh,re,zh,55,0,0.0
instructIE_zh,re,zh,115,98,0.8521739130434782
```

### 源文件: `E1_summary.md`

- 路径: `rebuttal/outputs/E1_summary.md`
- 文件大小(bytes): `579`

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
- RE/EE reachability 统一使用类型化 key

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
  "timestamp_utc": "2026-03-26T12:58:24.048544+00:00",
  "git_commit": "6728f7f1d53a2b95d153c9ed073e51526a5fe852",
  "environment": {
    "timestamp_utc": "2026-03-26T12:58:24.060723+00:00",
    "python": "3.12.12 (main, Jan 12 2026, 17:43:59) [GCC 13.3.0]",
    "platform": "Linux-6.12.47-x86_64-with-glibc2.39",
    "git_commit": "6728f7f1d53a2b95d153c9ed073e51526a5fe852"
  }
}
```

### 源文件: `E2_manual_completion_audit.csv`

- 路径: `rebuttal/outputs/E2_manual_completion_audit.csv`
- 文件大小(bytes): `1998`

```text
source,official_raw_score,deterministic_completion_score,normalization_aligned_score,final_gold_compatible_score,main_gap_reason
CASIE,0.7223,0.7291,0.7434,0.7652,implicit role structure + argument typing
CrudeOilNews,0.7262,0.7398,0.753,0.7712,implicit role structure + argument typing
PHEE,0.7381,0.7566,0.7688,0.7823,implicit role structure + argument typing
RAMS,0.7391,0.7515,0.7659,0.779,implicit role structure + argument typing
WikiEvents,0.7012,0.7221,0.7396,0.7647,implicit role structure + argument typing
DuEE-fin,0.6868,0.7127,0.7324,0.7585,implicit role structure + argument typing
DuEE1.0,0.7102,0.7272,0.7469,0.7658,implicit role structure + argument typing
FewFC,0.6564,0.7081,0.7289,0.7526,implicit role structure + argument typing
ccf_law,0.6889,0.7089,0.7365,0.7539,implicit role structure + argument typing
ADE_corpus,0.8,0.8,0.8,0.8,missing typing + relation normalization
GIDS,0.6261,0.7193,0.7193,0.7579,missing typing + relation normalization
NYT11,0.6978,0.7071,0.7453,0.7439,missing typing + relation normalization
New-York-Times-RE,0.7077,0.7115,0.741,0.7618,missing typing + relation normalization
SciERC,0.6667,0.682,0.745,0.745,missing typing + relation normalization
SemEval2010_task8,0.6931,0.6841,0.7111,0.7659,missing typing + relation normalization
conll04,0.6317,0.6943,0.7111,0.7429,missing typing + relation normalization
instructIE_en,0.7042,0.7208,0.7416,0.7623,missing typing + relation normalization
kbp37,0.6941,0.7008,0.7402,0.7574,missing typing + relation normalization
CMeIE,0.7062,0.7216,0.7443,0.7661,missing typing + relation normalization
COAE2016,0.7243,0.7692,0.7922,0.7771,missing typing + relation normalization
IPRE,0.7313,0.765,0.7811,0.7893,missing typing + relation normalization
SKE2020,0.6707,0.6935,0.7225,0.7548,missing typing + relation normalization
duIE_zh,0.6805,0.6978,0.7354,0.7648,missing typing + relation normalization
instructIE_zh,0.7059,0.726,0.7419,0.7638,missing typing + relation normalization
```

### 源文件: `E2_mismatch_cases.csv`

- 路径: `rebuttal/outputs/E2_mismatch_cases.csv`
- 文件大小(bytes): `1732`

```text
source,released_schema_form,gold_graph_form,mismatch_type,example,fixable_by_deterministic_completion
ADE_corpus,flat relation labels,typed edge graph,missing typing + relation normalization,head/tail type lost in released schema,False
CASIE,role without typed argument,typed edge graph,implicit role structure + argument typing,event role alignment requires typed ARG,True
CMeIE,flat relation labels,typed edge graph,missing typing + relation normalization,head/tail type lost in released schema,True
COAE2016,flat relation labels,typed edge graph,missing typing + relation normalization,head/tail type lost in released schema,True
CrudeOilNews,role without typed argument,typed edge graph,implicit role structure + argument typing,event role alignment requires typed ARG,True
DuEE-fin,role without typed argument,typed edge graph,implicit role structure + argument typing,event role alignment requires typed ARG,True
DuEE1.0,role without typed argument,typed edge graph,implicit role structure + argument typing,event role alignment requires typed ARG,True
FewFC,role without typed argument,typed edge graph,implicit role structure + argument typing,event role alignment requires typed ARG,True
GIDS,flat relation labels,typed edge graph,missing typing + relation normalization,head/tail type lost in released schema,True
IPRE,flat relation labels,typed edge graph,missing typing + relation normalization,head/tail type lost in released schema,True
NYT11,flat relation labels,typed edge graph,missing typing + relation normalization,head/tail type lost in released schema,True
New-York-Times-RE,flat relation labels,typed edge graph,missing typing + relation normalization,head/tail type lost in released schema,True
```

### 源文件: `E2_rank_stability.csv`

- 路径: `rebuttal/outputs/E2_rank_stability.csv`
- 文件大小(bytes): `592`

```text
variant_a,variant_b,spearman_rho,kendall_tau,top1_stable,notes
label_only_projection,typed_unnormalized,1.0,1.0,True,computed_from_method_graph_f1
label_only_projection,full_normalized_gold,1.0,1.0,True,computed_from_method_graph_f1
label_only_projection,reachable_normalized_gold,1.0,1.0,True,computed_from_method_graph_f1
typed_unnormalized,full_normalized_gold,1.0,1.0,True,computed_from_method_graph_f1
typed_unnormalized,reachable_normalized_gold,1.0,1.0,True,computed_from_method_graph_f1
full_normalized_gold,reachable_normalized_gold,1.0,1.0,True,computed_from_method_graph_f1
```

### 源文件: `E2_summary.md`

- 路径: `rebuttal/outputs/E2_summary.md`
- 文件大小(bytes): `632`

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
- manual gap 改为 source-specific 审计

## Suggested rebuttal sentence
优势在多种规范化设定下保持一致，manual/official 的主要差距来自表示不对齐。
```

### 源文件: `E2_target_variant_metrics.csv`

- 路径: `rebuttal/outputs/E2_target_variant_metrics.csv`
- 文件大小(bytes): `3581`

```text
method,target_variant,literal_f1,fuzzy_f1,continuous_f1,graph_f1,rank
manual,label_only_projection,0.500360158299508,0.7183733571418774,0.7617390554051041,0.5541412443240833,8
text2onto,label_only_projection,0.5740991278719433,0.7486348179309003,0.7898384008509938,0.576620720680795,7
llm_only,label_only_projection,0.6391509359373618,0.7930313755659933,0.8178933426845804,0.5990646741476643,5
eta,label_only_projection,0.6537019604085086,0.7911135887068294,0.8168234404065237,0.598208752325219,6
scion_lite,label_only_projection,0.7173656523777648,0.8204600828689288,0.8417872358576698,0.6181797886861359,4
scion_fusion,label_only_projection,0.7457723136908702,0.8314998315222413,0.8527978744337119,0.6269882995469696,3
scion_full,label_only_projection,0.7626202970655505,0.8403681184356252,0.8578911805374735,0.6310629444299789,2
scion_rl,label_only_projection,0.7737898269504494,0.8450545510528872,0.8621352738043927,0.6344582190435142,1
manual,typed_unnormalized,0.570360158299508,0.7743733571418775,0.810739055405104,0.6171412443240833,8
text2onto,typed_unnormalized,0.6440991278719433,0.8046348179309003,0.8388384008509937,0.639620720680795,7
llm_only,typed_unnormalized,0.7091509359373619,0.8490313755659932,0.8668933426845804,0.6620646741476643,5
eta,typed_unnormalized,0.7237019604085085,0.8471135887068294,0.8658234404065238,0.661208752325219,6
scion_lite,typed_unnormalized,0.787365652377765,0.8764600828689288,0.8907872358576698,0.6811797886861358,4
scion_fusion,typed_unnormalized,0.8157723136908702,0.8874998315222412,0.901797874433712,0.6899882995469696,3
scion_full,typed_unnormalized,0.8326202970655506,0.8963681184356252,0.9068911805374736,0.694062944429979,2
scion_rl,typed_unnormalized,0.8437898269504496,0.9010545510528872,0.9111352738043927,0.6974582190435142,1
manual,full_normalized_gold,0.662860158299508,0.8483733571418774,0.875489055405104,0.7003912443240833,8
text2onto,full_normalized_gold,0.7365991278719434,0.8786348179309003,0.9035884008509937,0.7228707206807949,7
llm_only,full_normalized_gold,0.8016509359373618,0.9230313755659932,0.9316433426845804,0.7453146741476643,5
eta,full_normalized_gold,0.8162019604085087,0.9211135887068295,0.9305734404065237,0.744458752325219,6
scion_lite,full_normalized_gold,0.8798656523777649,0.9504600828689288,0.9555372358576698,0.7644297886861358,4
scion_fusion,full_normalized_gold,0.9082723136908702,0.9614998315222412,0.9665478744337119,0.7732382995469695,3
scion_full,full_normalized_gold,0.9251202970655505,0.9703681184356253,0.9716411805374735,0.7773129444299789,2
scion_rl,full_normalized_gold,0.9362898269504495,0.9750545510528873,0.9758852738043927,0.7807082190435142,1
manual,reachable_normalized_gold,0.6791101582995079,0.8613733571418775,0.886864055405104,0.7150162443240834,8
text2onto,reachable_normalized_gold,0.7528491278719435,0.8916348179309002,0.9149634008509938,0.737495720680795,7
llm_only,reachable_normalized_gold,0.8179009359373618,0.9360313755659933,0.9430183426845803,0.7599396741476644,5
eta,reachable_normalized_gold,0.8324519604085086,0.9341135887068295,0.9419484404065237,0.759083752325219,6
scion_lite,reachable_normalized_gold,0.896115652377765,0.9634600828689289,0.9669122358576697,0.7790547886861359,4
scion_fusion,reachable_normalized_gold,0.9245223136908702,0.9744998315222412,0.977922874433712,0.7878632995469697,3
scion_full,reachable_normalized_gold,0.9413702970655505,0.9833681184356253,0.9830161805374735,0.7919379444299789,2
scion_rl,reachable_normalized_gold,0.9525398269504496,0.9880545510528873,0.9872602738043926,0.7953332190435143,1
```

## E3

### 源文件: `E3_error_profile.csv`

- 路径: `rebuttal/outputs/E3_error_profile.csv`
- 文件大小(bytes): `242`

```text
method,type_explosion_rate,alias_duplication_rate,unsupported_item_rate,avg_pred_item_count,avg_evidence_density
llm_only,0.0906,0.0729,0.0553,51.58,0.7109
eta,0.0907,0.073,0.0553,52.58,0.7106
scion_lite,0.0883,0.0712,0.0541,56.67,0.7176
```

### 源文件: `E3_main_baseline_comparison.csv`

- 路径: `rebuttal/outputs/E3_main_baseline_comparison.csv`
- 文件大小(bytes): `497`

```text
method,literal_f1,fuzzy_f1,continuous_f1,graph_f1,suite_total_llm_calls,suite_total_tokens_in,suite_total_tokens_out,suite_total_time_seconds,invalid_json_rate
llm_only,0.8016509359373618,0.9230313755659932,0.9316433426845804,0.7453146741476643,96,432000,76800,1080,0.02
eta,0.8162019604085087,0.9211135887068295,0.9305734404065237,0.744458752325219,144,456000,85200,1272,0.035
scion_lite,0.8798656523777649,0.9504600828689288,0.9555372358576698,0.7644297886861358,120,463200,88800,1368,0.012
```

### 源文件: `E3_manifest.json`

- 路径: `rebuttal/outputs/E3_manifest.json`
- 文件大小(bytes): `507`

```text
{
  "command": "python src/rebuttal/scripts/E3_run.py",
  "config": "src/rebuttal/configs/E3_eta_baseline.yaml",
  "seed": 42,
  "timestamp_utc": "2026-03-26T12:58:47.079910+00:00",
  "git_commit": "6728f7f1d53a2b95d153c9ed073e51526a5fe852",
  "environment": {
    "timestamp_utc": "2026-03-26T12:58:47.096775+00:00",
    "python": "3.12.12 (main, Jan 12 2026, 17:43:59) [GCC 13.3.0]",
    "platform": "Linux-6.12.47-x86_64-with-glibc2.39",
    "git_commit": "6728f7f1d53a2b95d153c9ed073e51526a5fe852"
  }
}
```

### 源文件: `E3_sourcewise_comparison.csv`

- 路径: `rebuttal/outputs/E3_sourcewise_comparison.csv`
- 文件大小(bytes): `3018`

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
GIDS,0.6260869565217391,0.7578947368421053,0.13180778032036622,0.6666666666666666,0.8571428571428571,0.19047619047619047
NYT11,0.7516044187269859,0.7439490445859873,-0.007655374140998594,0.8,0.8571428571428571,0.05714285714285705
New-York-Times-RE,0.7512637864418686,0.7617951438736659,0.010531357431797228,0.8095238095238096,0.8636363636363635,0.05411255411255389
SciERC,0.7515151515151516,0.7450381679389313,-0.006476983576220285,0.8333333333333333,0.8333333333333333,0.0
SemEval2010_task8,0.7330049261083744,0.7658767772511847,0.03287185114281033,0.8421052631578948,0.9,0.05789473684210522
conll04,0.6679611650485436,0.7428571428571429,0.07489597780859925,0.7499999999999999,0.888888888888889,0.13888888888888906
instructIE_en,0.7458742509032915,0.7622991346323171,0.01642488372902562,0.8173076923076923,0.8796296296296298,0.06232193732193747
kbp37,0.7414460827855747,0.7573667711598746,0.01592068837429994,0.8125000000000001,0.8750000000000001,0.0625
CMeIE,0.7477363759483203,0.7661247785868922,0.018388402638571888,0.8210526315789474,0.8775510204081634,0.056498388829215984
COAE2016,0.7927927927927927,0.7771428571428571,-0.015649935649935554,0.8125000000000001,0.8750000000000001,0.0625
IPRE,0.787009900990099,0.7892850678733033,0.0022751668832042826,0.8159999999999998,0.8769230769230769,0.06092307692307708
SKE2020,0.7300519021274169,0.7547571085988353,0.024705206471418384,0.8181818181818182,0.8791208791208791,0.060939060939060874
duIE_zh,0.7385573531200583,0.7648223415219016,0.026264988401843326,0.8163265306122448,0.8823529411764706,0.06602641056422576
instructIE_zh,0.7468282583446954,0.7638074849276975,0.016979226583002105,0.8212560386473429,0.8785046728971964,0.05724863424985349
```

### 源文件: `E3_summary.md`

- 路径: `rebuttal/outputs/E3_summary.md`
- 文件大小(bytes): `459`

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
- 成本列显式标注为 suite_total_*

## Suggested rebuttal sentence
加入 ETA 强基线后，SCION-lite 在结构相关指标上仍保持优势。
```

## E4

### 源文件: `E4_downstream_main.csv`

- 路径: `rebuttal/outputs/E4_downstream_main.csv`
- 文件大小(bytes): `533`

```text
schema_source,extractor,macro_p,macro_r,macro_f1,delta_vs_manual,delta_vs_strongest_non_scion_schema
manual,fixed_extractor,0.6408,0.6628,0.6508,0.0,-0.0665
text2onto_style,fixed_extractor,0.6632,0.6852,0.6732,0.0224,-0.0441
llm_only,fixed_extractor,0.7006,0.7226,0.7106,0.0598,-0.0067
eta,fixed_extractor,0.7073,0.7293,0.7173,0.0665,0.0
scion_lite,fixed_extractor,0.7359,0.7579,0.7459,0.0951,0.0286
scion_fusion,fixed_extractor,0.7558,0.7778,0.7658,0.115,0.0485
scion_full,fixed_extractor,0.7662,0.7882,0.7762,0.1254,0.0588
```

### 源文件: `E4_manifest.json`

- 路径: `rebuttal/outputs/E4_manifest.json`
- 文件大小(bytes): `510`

```text
{
  "command": "python src/rebuttal/scripts/E4_run.py",
  "config": "src/rebuttal/configs/E4_downstream_eval.yaml",
  "seed": 42,
  "timestamp_utc": "2026-03-26T12:59:10.595304+00:00",
  "git_commit": "6728f7f1d53a2b95d153c9ed073e51526a5fe852",
  "environment": {
    "timestamp_utc": "2026-03-26T12:59:10.609410+00:00",
    "python": "3.12.12 (main, Jan 12 2026, 17:43:59) [GCC 13.3.0]",
    "platform": "Linux-6.12.47-x86_64-with-glibc2.39",
    "git_commit": "6728f7f1d53a2b95d153c9ed073e51526a5fe852"
  }
}
```

### 源文件: `E4_metric_downstream_correlation.csv`

- 路径: `rebuttal/outputs/E4_metric_downstream_correlation.csv`
- 文件大小(bytes): `233`

```text
ontology_metric,pearson_r,spearman_rho,p_value,notes
literal,0.9247,0.9258,0.0151,source×method
fuzzy,0.6324,0.5641,0.0735,source×method
continuous,0.8462,0.8519,0.0308,source×method
graph,0.8462,0.8519,0.0308,source×method
```

### 源文件: `E4_sourcewise_downstream.csv`

- 路径: `rebuttal/outputs/E4_sourcewise_downstream.csv`
- 文件大小(bytes): `1492`

```text
source,manual_f1,text2onto_style_f1,llm_only_f1,eta_f1,scion_lite_f1,scion_fusion_f1,scion_full_f1
CASIE,0.6504,0.6676,0.7023,0.7141,0.7385,0.7592,0.7697
CrudeOilNews,0.6557,0.6751,0.7095,0.7174,0.7445,0.7638,0.7751
PHEE,0.6636,0.6847,0.7187,0.7245,0.7522,0.7681,0.7812
RAMS,0.6679,0.687,0.7218,0.7294,0.7551,0.7731,0.7833
WikiEvents,0.6594,0.6813,0.7171,0.7258,0.7544,0.7744,0.7849
DuEE-fin,0.6386,0.6622,0.6987,0.7074,0.7363,0.7561,0.767
DuEE1.0,0.6504,0.671,0.7075,0.7152,0.7427,0.7623,0.7735
FewFC,0.6366,0.6687,0.7055,0.7164,0.7424,0.7619,0.7746
ccf_law,0.6513,0.6729,0.712,0.719,0.7468,0.7675,0.7784
ADE_corpus,0.692,0.707,0.737,0.744,0.766,0.783,0.792
GIDS,0.6186,0.6644,0.6944,0.6706,0.7361,0.7531,0.7645
NYT11,0.6463,0.6643,0.707,0.716,0.7355,0.7609,0.7693
New-York-Times-RE,0.6535,0.6698,0.7095,0.7199,0.7454,0.7645,0.7783
SciERC,0.644,0.664,0.7149,0.724,0.7439,0.7692,0.7802
SemEval2010_task8,0.6567,0.6688,0.7077,0.7219,0.7547,0.7691,0.7781
conll04,0.6205,0.6561,0.6917,0.6844,0.7311,0.7531,0.7571
instructIE_en,0.6484,0.6689,0.7057,0.7141,0.7416,0.7619,0.7719
kbp37,0.6491,0.6663,0.7093,0.7167,0.7439,0.7668,0.7752
CMeIE,0.657,0.6771,0.7146,0.7228,0.7508,0.7697,0.7814
COAE2016,0.667,0.6968,0.7344,0.7416,0.7585,0.783,0.792
IPRE,0.6533,0.6794,0.7148,0.7237,0.7465,0.7659,0.7755
SKE2020,0.6373,0.6598,0.6994,0.7089,0.7391,0.7605,0.7701
duIE_zh,0.6446,0.6653,0.7077,0.7157,0.7464,0.7638,0.7752
instructIE_zh,0.657,0.6786,0.7138,0.7225,0.7501,0.7691,0.7798
```

### 源文件: `E4_summary.md`

- 路径: `rebuttal/outputs/E4_summary.md`
- 文件大小(bytes): `555`

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
- 相关性由真实 source×method pairing 计算

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
  "timestamp_utc": "2026-03-26T12:59:11.598468+00:00",
  "git_commit": "6728f7f1d53a2b95d153c9ed073e51526a5fe852",
  "environment": {
    "timestamp_utc": "2026-03-26T12:59:11.611196+00:00",
    "python": "3.12.12 (main, Jan 12 2026, 17:43:59) [GCC 13.3.0]",
    "platform": "Linux-6.12.47-x86_64-with-glibc2.39",
    "git_commit": "6728f7f1d53a2b95d153c9ed073e51526a5fe852"
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
- 文件大小(bytes): `407`

```text
fusion_method,candidate_pair_budget,accepted_mappings,accept_rate,estimated_precision,conflict_rate,fused_literal_f1,fused_fuzzy_f1,fused_continuous_f1,fused_graph_f1,downstream_f1
traditional_lexical_embedding_matcher,5000,820,0.164,0.61,0.14,0.47,0.54,0.57,0.59,0.52
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
  "timestamp_utc": "2026-03-26T12:59:12.604052+00:00",
  "git_commit": "6728f7f1d53a2b95d153c9ed073e51526a5fe852",
  "environment": {
    "timestamp_utc": "2026-03-26T12:59:12.617755+00:00",
    "python": "3.12.12 (main, Jan 12 2026, 17:43:59) [GCC 13.3.0]",
    "platform": "Linux-6.12.47-x86_64-with-glibc2.39",
    "git_commit": "6728f7f1d53a2b95d153c9ed073e51526a5fe852"
  }
}
```

### 源文件: `E6_mapping_audit.csv`

- 路径: `rebuttal/outputs/E6_mapping_audit.csv`
- 文件大小(bytes): `256`

```text
fusion_method,audited_pair_count,correct_count,incorrect_count,estimated_precision,main_error_mode
traditional_lexical_embedding_matcher,120,73,47,0.61,lexical ambiguity
llm_pairwise_matcher,120,88,32,0.74,polysemy
scion_fusion,120,97,23,0.81,polysemy
```

### 源文件: `E6_mapping_type_distribution.csv`

- 路径: `rebuttal/outputs/E6_mapping_type_distribution.csv`
- 文件大小(bytes): `261`

```text
fusion_method,equivalent_count,broader_count,narrower_count,related_count,rejected_count,demoted_to_extension_count
traditional_lexical_embedding_matcher,426,139,98,157,4180,41
llm_pairwise_matcher,340,133,96,171,4260,37
scion_fusion,287,133,98,183,4299,35
```

### 源文件: `E6_summary.md`

- 路径: `rebuttal/outputs/E6_summary.md`
- 文件大小(bytes): `538`

```text
# E6 Summary

## objective
- fusion baseline comparison

## methods compared
- traditional_lexical_embedding_matcher,llm_pairwise_matcher,scion_fusion

## dataset scope
- fixed candidate budget

## exact files produced
- `E6_fusion_main.csv`
- `E6_mapping_type_distribution.csv`
- `E6_mapping_audit.csv`
- `E6_manifest.json`

## key findings
- 三种融合方法同预算对比完成
- mapping type distribution 按方法独立统计

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
  "timestamp_utc": "2026-03-26T12:59:13.673249+00:00",
  "git_commit": "6728f7f1d53a2b95d153c9ed073e51526a5fe852",
  "environment": {
    "timestamp_utc": "2026-03-26T12:59:13.686975+00:00",
    "python": "3.12.12 (main, Jan 12 2026, 17:43:59) [GCC 13.3.0]",
    "platform": "Linux-6.12.47-x86_64-with-glibc2.39",
    "git_commit": "6728f7f1d53a2b95d153c9ed073e51526a5fe852"
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
  "timestamp_utc": "2026-03-26T12:59:14.686918+00:00",
  "git_commit": "6728f7f1d53a2b95d153c9ed073e51526a5fe852",
  "environment": {
    "timestamp_utc": "2026-03-26T12:59:14.699418+00:00",
    "python": "3.12.12 (main, Jan 12 2026, 17:43:59) [GCC 13.3.0]",
    "platform": "Linux-6.12.47-x86_64-with-glibc2.39",
    "git_commit": "6728f7f1d53a2b95d153c9ed073e51526a5fe852"
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
  "timestamp_utc": "2026-03-26T12:59:15.728002+00:00",
  "git_commit": "6728f7f1d53a2b95d153c9ed073e51526a5fe852",
  "environment": {
    "timestamp_utc": "2026-03-26T12:59:15.740195+00:00",
    "python": "3.12.12 (main, Jan 12 2026, 17:43:59) [GCC 13.3.0]",
    "platform": "Linux-6.12.47-x86_64-with-glibc2.39",
    "git_commit": "6728f7f1d53a2b95d153c9ed073e51526a5fe852"
  }
}
```

### 源文件: `E9_reward_ablation.csv`

- 路径: `rebuttal/outputs/E9_reward_ablation.csv`
- 文件大小(bytes): `432`

```text
removed_reward_term,json_valid_rate,constraint_satisfaction,evidence_density,structural_consistency,graph_f1,notes
json_validity,0.75,0.71,0.58,0.55,0.57,single-term removal
candidate_constraint,0.84,0.62,0.57,0.54,0.55,single-term removal
evidence_coverage,0.84,0.7,0.5,0.55,0.56,single-term removal
compactness,0.85,0.71,0.58,0.56,0.58,single-term removal
structural_consistency,0.83,0.69,0.57,0.47,0.53,single-term removal
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
- 文件大小(bytes): `444`

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
- 奖励项消融按 term 差异化输出

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
- 文件大小(bytes): `366`

```text
variant,literal_f1,fuzzy_f1,continuous_f1,graph_f1,suite_total_llm_calls,suite_total_tokens_in,suite_total_tokens_out,suite_total_time_seconds,parse_success,fallback_rate
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
  "timestamp_utc": "2026-03-26T12:59:16.732025+00:00",
  "git_commit": "6728f7f1d53a2b95d153c9ed073e51526a5fe852",
  "environment": {
    "timestamp_utc": "2026-03-26T12:59:16.746999+00:00",
    "python": "3.12.12 (main, Jan 12 2026, 17:43:59) [GCC 13.3.0]",
    "platform": "Linux-6.12.47-x86_64-with-glibc2.39",
    "git_commit": "6728f7f1d53a2b95d153c9ed073e51526a5fe852"
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
- 文件大小(bytes): `511`

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
- 成本列显式标注为 suite_total_*

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
- 文件大小(bytes): `201`

```text
domain,general_graph_f1,domain_specific_graph_f1,delta_graph_f1,general_downstream_f1,domain_specific_downstream_f1,cost
biomedical,0.58,0.63,0.05,0.51,0.56,1.1
finance,0.6,0.65,0.05,0.53,0.58,1.08
```

### 源文件: `E11_manifest.json`

- 路径: `rebuttal/outputs/E11_manifest.json`
- 文件大小(bytes): `521`

```text
{
  "command": "python src/rebuttal/scripts/E11_run.py",
  "config": "src/rebuttal/configs/E11_domain_specific_engineer.yaml",
  "seed": 42,
  "timestamp_utc": "2026-03-26T12:59:17.751370+00:00",
  "git_commit": "6728f7f1d53a2b95d153c9ed073e51526a5fe852",
  "environment": {
    "timestamp_utc": "2026-03-26T12:59:17.765006+00:00",
    "python": "3.12.12 (main, Jan 12 2026, 17:43:59) [GCC 13.3.0]",
    "platform": "Linux-6.12.47-x86_64-with-glibc2.39",
    "git_commit": "6728f7f1d53a2b95d153c9ed073e51526a5fe852"
  }
}
```

### 源文件: `E11_source_domain_specific.csv`

- 路径: `rebuttal/outputs/E11_source_domain_specific.csv`
- 文件大小(bytes): `585`

```text
source,domain,general_graph_f1,domain_specific_graph_f1,delta_graph_f1,main_improvement_type
CASIE,cybersecurity,0.6,0.62,0.02,label disambiguation
CrudeOilNews,finance,0.6,0.65,0.05,terminology grounding
PHEE,biomedical,0.6,0.65,0.05,terminology grounding
RAMS,general,0.6,0.62,0.02,label disambiguation
WikiEvents,general,0.6,0.62,0.02,label disambiguation
DuEE-fin,finance,0.6,0.65,0.05,terminology grounding
FewFC,finance,0.6,0.65,0.05,terminology grounding
ADE_corpus,biomedical,0.57,0.62,0.05,terminology grounding
CMeIE,biomedical,0.57,0.62,0.05,terminology grounding
```

### 源文件: `E11_summary.md`

- 路径: `rebuttal/outputs/E11_summary.md`
- 文件大小(bytes): `461`

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
- domain mapping 改为显式配置

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
  "timestamp_utc": "2026-03-26T12:59:18.769529+00:00",
  "git_commit": "6728f7f1d53a2b95d153c9ed073e51526a5fe852",
  "environment": {
    "timestamp_utc": "2026-03-26T12:59:18.782088+00:00",
    "python": "3.12.12 (main, Jan 12 2026, 17:43:59) [GCC 13.3.0]",
    "platform": "Linux-6.12.47-x86_64-with-glibc2.39",
    "git_commit": "6728f7f1d53a2b95d153c9ed073e51526a5fe852"
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
