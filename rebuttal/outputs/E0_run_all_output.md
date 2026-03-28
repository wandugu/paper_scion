# E0 Run All Output Details

- generated_by: `src/rebuttal/scripts/E0_run_all.py`
- output_preview_char_limit: `20000`

## E1

### 源文件: `E1_alignment_check.json`

- 路径: `rebuttal/outputs/E1_alignment_check.json`
- 文件大小(bytes): `913`

```text
{
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
```

### 源文件: `E1_main_metrics.csv`

- 路径: `rebuttal/outputs/E1_main_metrics.csv`
- 文件大小(bytes): `6011`

```text
method,target,literal_p,literal_r,literal_f1,fuzzy_p,fuzzy_r,fuzzy_f1,continuous_p,continuous_r,continuous_f1,graph_p,graph_r,graph_f1,delta_continuous_f1_vs_strongest_non_scion,p_value,evaluator_signature,evaluator_aligned_with_submission,frozen_gold_artifact_hash,evaluation_protocol,is_proxy_result,is_approximate_result
manual,full_gold,0.7635494633643884,0.5432582768419245,0.6257505145198397,0.9971590909090909,0.8958797217122685,0.9388476784376953,0.9484141140034583,0.796207483386798,0.8638269718048392,0.96251319868504,0.7285025317345073,0.8265351437194157,-0.053904219359584116,2.38e-07,cabc45613b834dee,True,26bad3bb3f37a484,submission_aligned_scope_v1,False,False
manual,reachable_gold,0.7207218642562211,0.5612260209015031,0.6131560219498492,0.9976076555023923,0.9133877524066133,0.9465289321133348,0.938533324783198,0.7938219723046149,0.8568028605705028,0.9532458812564262,0.7616550349050274,0.8417834639452857,-0.06023106472298134,1.91e-06,cabc45613b834dee,True,26bad3bb3f37a484,submission_aligned_scope_v1,False,False
text2onto,full_gold,0.7960268222862878,0.6152867343315669,0.6866422417479979,0.9952570921985816,0.8997317115446742,0.9395379033887926,0.9557773065728098,0.8254028790844116,0.8840273951366786,0.9651979293703299,0.785463502791515,0.8638105723201357,-0.03370379602774476,2.38e-07,cabc45613b834dee,True,26bad3bb3f37a484,submission_aligned_scope_v1,False,False
text2onto,reachable_gold,0.7401014052998403,0.6382702123972221,0.6712622934042206,0.997704315886134,0.9579819549826231,0.9758985921980702,0.9424961537149198,0.8420307807553304,0.8877290073548814,0.949129622399024,0.8306750588888868,0.8820067647856569,-0.029304917938602792,1.91e-06,cabc45613b834dee,True,26bad3bb3f37a484,submission_aligned_scope_v1,False,False
llm_only,full_gold,0.8254829935079314,0.688891308395671,0.7444765316479396,0.9975247524752474,0.9516057336022433,0.972270936979351,0.9623791117205286,0.8738803247633444,0.9148153684000576,0.9669957890765218,0.8362666115412379,0.8949714501277212,-0.0029158227643657497,3.81e-06,cabc45613b834dee,True,26bad3bb3f37a484,submission_aligned_scope_v1,False,False
llm_only,reachable_gold,0.7556100628526902,0.7128360967197931,0.7213442529833399,0.9968992493963053,0.9427438926706043,0.9669418323235877,0.949471351224593,0.873928970027092,0.9086162491553001,0.9420147108647691,0.8902009817745995,0.9116388815044552,-0.008417676138184005,3.05e-05,cabc45613b834dee,True,26bad3bb3f37a484,submission_aligned_scope_v1,False,False
eta,full_gold,0.8323087821365044,0.7216971263400876,0.7669588383104345,0.9975961538461539,0.9566368446733975,0.9743882988026901,0.96104991008169,0.879967102178773,0.9177311911644234,0.9529167591999482,0.8535728118813029,0.8977800978335466,0.0,0.1250,cabc45613b834dee,True,26bad3bb3f37a484,submission_aligned_scope_v1,False,False
eta,reachable_gold,0.7634623106387083,0.7402129071682494,0.7400925234011723,0.9968272234095018,0.9645902333406348,0.9792270196207283,0.951159835675917,0.8879881882571508,0.9170339252934842,0.931223577762428,0.8978093933595034,0.9102387066761655,0.0,1.0000,cabc45613b834dee,True,26bad3bb3f37a484,submission_aligned_scope_v1,False,False
scion_lite,full_gold,0.8654318108592732,0.7948466519150839,0.822407652637775,0.9946200022652621,0.9571327725934067,0.9740688444681682,0.9678957459248211,0.9141903412907407,0.939480496863935,0.9553636342416628,0.8884192497115966,0.9175414232096145,0.021749305699511612,0.0001,cabc45613b834dee,True,26bad3bb3f37a484,submission_aligned_scope_v1,False,False
scion_lite,reachable_gold,0.7877642623654029,0.8087769715202469,0.7872729544487097,0.9964449138761066,0.9863428751285812,0.9911372102920563,0.9562349061427693,0.9239032998818101,0.9389062999156313,0.9222387018532635,0.9270113554532439,0.9207059486943892,0.021872374622147195,0.0004,cabc45613b834dee,True,26bad3bb3f37a484,submission_aligned_scope_v1,False,False
scion_fusion,full_gold,0.8747115810526225,0.8353720224882107,0.8490551299348477,0.9948942939244664,0.9723791556438105,0.9827699938116318,0.9685270478465742,0.9326039135905645,0.9496177922045589,0.954069848647352,0.9166453692110856,0.9322995244560754,0.03188660104013552,1.10e-05,cabc45613b834dee,True,26bad3bb3f37a484,submission_aligned_scope_v1,False,False
scion_fusion,reachable_gold,0.7947951747816343,0.8436617880165017,0.8084754483102206,0.9970635981665393,0.9763419313003223,0.9858753824524356,0.9582348126438794,0.9334479519490638,0.9448461273143344,0.913714348961722,0.9469080851163203,0.9262716795296254,0.02781220202085022,7.63e-05,cabc45613b834dee,True,26bad3bb3f37a484,submission_aligned_scope_v1,False,False
scion_full,full_gold,0.8858119799674379,0.8632095096118287,0.8690511023447303,0.9964181286549708,0.9919003575745194,0.9939519358469212,0.9724010728436955,0.9463435757774533,0.958754050533607,0.9541071591799458,0.9317402242411109,0.9401744598409368,0.041022859369183595,5.72e-06,cabc45613b834dee,True,26bad3bb3f37a484,submission_aligned_scope_v1,False,False
scion_full,reachable_gold,0.8052543966925327,0.8700689583633946,0.8266973455330112,0.9969651884288298,0.9745025001896771,0.9849405646660863,0.9614969673033585,0.9405198707735213,0.9500635318263547,0.909139605834164,0.953064765970202,0.9268240499186916,0.03302960653287057,3.81e-06,cabc45613b834dee,True,26bad3bb3f37a484,submission_aligned_scope_v1,False,False
scion_rl,full_gold,0.8917036323792948,0.8798110797497559,0.8805717219912302,0.9978260869565218,0.9762530873708172,0.9861202676378767,0.9721485158277838,0.9501886542916312,0.9605557889441557,0.957504188440864,0.9460464990301111,0.9492315255686905,0.042824597779732354,5.72e-06,cabc45613b834dee,True,26bad3bb3f37a484,submission_aligned_scope_v1,False,False
scion_rl,reachable_gold,0.8038244603609098,0.8930522283905421,0.836078445768678,0.9965350501881205,0.9930908925794502,0.994700702315695,0.9621454568114983,0.963276873364859,0.9621402325215517,0.9027908959562619,0.968316031162434,0.930236321029041,0.04510630722806752,1.91e-06,cabc45613b834dee,True,26bad3bb3f37a484,submission_aligned_scope_v1,False,False
```

### 源文件: `E1_manifest.json`

- 路径: `rebuttal/outputs/E1_manifest.json`
- 文件大小(bytes): `524`

```text
{
  "command": "python src/rebuttal/scripts/E1_run_reachable_eval.py",
  "config": "src/rebuttal/configs/E1_reachable_eval.yaml",
  "seed": 42,
  "timestamp_utc": "2026-03-28T10:11:45.848894+00:00",
  "git_commit": "4bd79613ab2cda309bbf7554716eb0e6ab9c99d9",
  "environment": {
    "timestamp_utc": "2026-03-28T10:11:45.856193+00:00",
    "python": "3.12.12 (main, Jan 12 2026, 17:43:59) [GCC 13.3.0]",
    "platform": "Linux-6.12.47-x86_64-with-glibc2.39",
    "git_commit": "4bd79613ab2cda309bbf7554716eb0e6ab9c99d9"
  }
}
```

### 源文件: `E1_reachability_debug_samples.csv`

- 路径: `rebuttal/outputs/E1_reachability_debug_samples.csv`
- 文件大小(bytes): `12637`

```text
source,sample_type,edge_text
CrudeOilNews,unmatched_gold_strict,EE[cause movement up gain]-role->difference
CrudeOilNews,unmatched_gold_strict,EE[cause movement up gain]-role->item
CrudeOilNews,unmatched_gold_strict,EE[cause movement up gain]-role->supplier consumer
CrudeOilNews,unmatched_gold_strict,EE[movement flat]-role->attribute
CrudeOilNews,unmatched_gold_strict,EE[movement flat]-role->final value
CrudeOilNews,unmatched_gold_strict,EE[movement flat]-role->initial reference point
CrudeOilNews,unmatched_gold_strict,EE[movement flat]-role->supplier consumer
CrudeOilNews,unmatched_gold_strict,EE[movement flat]-role->type
CrudeOilNews,unmatched_gold_strict,EE[movement up gain]-role->forecast
CrudeOilNews,unmatched_gold_strict,EE[oversupply]-role->attribute
CrudeOilNews,unmatched_gold_strict,EE[shortage]-role->final value
CrudeOilNews,unmatched_gold_strict,EE[shortage]-role->forecast
CrudeOilNews,unmatched_gold_strict,EE[shortage]-role->reference point time
RAMS,unmatched_gold_strict,EE[a person falling]-role->destination
RAMS,unmatched_gold_strict,EE[a person falling]-role->origin
RAMS,unmatched_gold_strict,EE[airstrike or missile strike]-role->instrument
RAMS,unmatched_gold_strict,EE[an artifact falling]-role->origin
RAMS,unmatched_gold_strict,EE[arson or fire setting]-role->attacker
RAMS,unmatched_gold_strict,EE[arson or fire setting]-role->instrument
RAMS,unmatched_gold_strict,EE[arson or fire setting]-role->place
RAMS,unmatched_gold_strict,EE[arson or fire setting]-role->target
RAMS,unmatched_gold_strict,EE[broadcast for requests or advice]-role->place
RAMS,unmatched_gold_strict,EE[casting a vote]-role->ballot
RAMS,unmatched_gold_strict,EE[casting a vote]-role->candidate
RAMS,unmatched_gold_strict,EE[casting a vote]-role->result
RAMS,unmatched_gold_strict,EE[casting a vote]-role->voter
RAMS,unmatched_gold_strict,EE[construction of a structure or artifact]-role->instrument
RAMS,unmatched_gold_strict,EE[conviction in a judicial process]-role->crime
RAMS,unmatched_gold_strict,EE[conviction in a judicial process]-role->defendant
RAMS,unmatched_gold_strict,EE[conviction in a judicial process]-role->judgecourt
RAMS,unmatched_gold_strict,EE[conviction in a judicial process]-role->place
RAMS,unmatched_gold_strict,EE[correspondence for negotiation]-role->place
RAMS,unmatched_gold_strict,EE[correspondence involving commands or orders]-role->place
WikiEvents,unmatched_gold_strict,EE[arresting jailing or detaining]-role->jailer
WikiEvents,unmatched_gold_strict,EE[arresting jailing or detaining]-role->place
WikiEvents,unmatched_gold_strict,EE[charging or indicting]-role->defendant
WikiEvents,unmatched_gold_strict,EE[charging or indicting]-role->prosecutor
WikiEvents,unmatched_gold_strict,EE[conducting a trial or hearing]-role->defendant
WikiEvents,unmatched_gold_strict,EE[conducting a trial or hearing]-role->judgecourt
WikiEvents,unmatched_gold_strict,EE[conducting a trial or hearing]-role->place
WikiEvents,unmatched_gold_strict,EE[contact]-role->place
WikiEvents,unmatched_gold_strict,EE[contact]-role->topic
WikiEvents,unmatched_gold_strict,EE[damage]-role->artifact
WikiEvents,unmatched_gold_strict,EE[damage]-role->damager
WikiEvents,unmatched_gold_strict,EE[damage]-role->place
WikiEvents,unmatched_gold_strict,EE[destroy]-role->artifact
WikiEvents,unmatched_gold_strict,EE[destroy]-role->destroyer
WikiEvents,unmatched_gold_strict,EE[destroy]-role->place
WikiEvents,unmatched_gold_strict,EE[disabling or defusing]-role->artifact
WikiEvents,unmatched_gold_strict,EE[disabling or defusing]-role->disabler
WikiEvents,unmatched_gold_strict,EE[dismantle]-role->artifact
WikiEvents,unmatched_gold_strict,EE[dismantle]-role->dismantler
WikiEvents,unmatched_gold_strict,EE[dismantle]-role->instrument
WikiEvents,unmatched_reachable_evidence_strict,EE[correspondence]-role->participant
GIDS,unmatched_gold_strict,RE[entity]-education degree->[entity]
GIDS,unmatched_gold_strict,RE[entity]-education institution->[entity]
GIDS,unmatched_gold_strict,RE[entity]-place of birth->[entity]
GIDS,unmatched_gold_strict,RE[entity]-place of death->[entity]
GIDS,unmatched_reachable_evidence_strict,RE[person]-education degree->[education degree]
GIDS,unmatched_reachable_evidence_strict,RE[person]-education institution->[education institution]
GIDS,unmatched_reachable_evidence_strict,RE[person]-place of birth->[place]
GIDS,unmatched_reachable_evidence_strict,RE[person]-place of death->[place]
New-York-Times-RE,unmatched_gold_strict,RE[entity]-administrative division of country->[entity]
New-York-Times-RE,unmatched_gold_strict,RE[entity]-children->[entity]
New-York-Times-RE,unmatched_gold_strict,RE[entity]-company advisors->[entity]
New-York-Times-RE,unmatched_gold_strict,RE[entity]-company founded place->[entity]
New-York-Times-RE,unmatched_gold_strict,RE[entity]-company founders->[entity]
New-York-Times-RE,unmatched_gold_strict,RE[entity]-company industry->[entity]
New-York-Times-RE,unmatched_gold_strict,RE[entity]-company major shareholders->[entity]
New-York-Times-RE,unmatched_gold_strict,RE[entity]-company shareholder among major shareholders->[entity]
New-York-Times-RE,unmatched_gold_strict,RE[entity]-country of administrative divisions->[entity]
New-York-Times-RE,unmatched_gold_strict,RE[entity]-country of capital->[entity]
New-York-Times-RE,unmatched_gold_strict,RE[entity]-ethnicity->[entity]
New-York-Times-RE,unmatched_gold_strict,RE[entity]-ethnicity of people->[entity]
New-York-Times-RE,unmatched_gold_strict,RE[entity]-geographic distribution->[entity]
New-York-Times-RE,unmatched_gold_strict,RE[entity]-nationality->[entity]
New-York-Times-RE,unmatched_gold_strict,RE[entity]-neighborhood of->[entity]
New-York-Times-RE,unmatched_gold_strict,RE[entity]-person of company->[entity]
New-York-Times-RE,unmatched_gold_strict,RE[entity]-place lived->[entity]
New-York-Times-RE,unmatched_gold_strict,RE[entity]-place of birth->[entity]
New-York-Times-RE,unmatched_gold_strict,RE[entity]-place of death->[entity]
New-York-Times-RE,unmatched_gold_strict,RE[entity]-profession->[entity]
New-York-Times-RE,unmatched_reachable_evidence_strict,RE[entity]-administrative division of country->[location]
New-York-Times-RE,unmatched_reachable_evidence_strict,RE[entity]-company founded place->[location]
New-York-Times-RE,unmatched_reachable_evidence_strict,RE[entity]-location contains->[location]
New-York-Times-RE,unmatched_reachable_evidence_strict,RE[entity]-nationality->[location]
New-York-Times-RE,unmatched_reachable_evidence_strict,RE[entity]-place lived->[location]
New-York-Times-RE,unmatched_reachable_evidence_strict,RE[entity]-place of birth->[location]
New-York-Times-RE,unmatched_reachable_evidence_strict,RE[location]-administrative division of country->[location]
New-York-Times-RE,unmatched_reachable_evidence_strict,RE[location]-administrative division of country->[organization]
New-York-Times-RE,unmatched_reachable_evidence_strict,RE[location]-company founded place->[location]
New-York-Times-RE,unmatched_reachable_evidence_strict,RE[location]-company founders->[person]
New-York-Times-RE,unmatched_reachable_evidence_strict,RE[location]-company major shareholders->[person]
New-York-Times-RE,unmatched_reachable_evidence_strict,RE[location]-company shareholder among major shareholders->[organization]
New-York-Times-RE,unmatched_reachable_evidence_strict,RE[location]-country of administrative divisions->[entity]
New-York-Times-RE,unmatched_reachable_evidence_strict,RE[location]-country of administrative divisions->[location]
New-York-Times-RE,unmatched_reachable_evidence_strict,RE[location]-country of administrative divisions->[organization]
New-York-Times-RE,unmatched_reachable_evidence_strict,RE[location]-country of administrative divisions->[person]
New-York-Times-RE,unmatched_reachable_evidence_strict,RE[location]-country of capital->[entity]
New-York-Times-RE,unmatched_reachable_evidence_strict,RE[location]-country of capital->[location]
New-York-Times-RE,unmatched_reachable_evidence_strict,RE[location]-country of capital->[organization]
New-York-Times-RE,unmatched_reachable_evidence_strict,RE[location]-country of capital->[person]
SemEval2010_task8,unmatched_gold_strict,RE[entity]-message topc->[entity]
instructIE_en,unmatched_gold_strict,RE[architectural structure]-achievement->[profession]
instructIE_en,unmatched_gold_strict,RE[geographic region]-capital->[geographic region]
instructIE_en,unmatched_gold_strict,RE[geographic region]-elevation above sea level->[measure]
instructIE_en,unmatched_gold_strict,RE[geographic region]-length->[measure]
instructIE_en,unmatched_gold_strict,RE[geographic region]-width->[measure]
instructIE_en,unmatched_gold_strict,RE[medicine]-disease transmission process->[text]
instructIE_en,unmatched_gold_strict,RE[medicine]-drug or therapy used for treatment->[medicine]
instructIE_en,unmatched_gold_strict,RE[medicine]-possible treatment->[medicine]
instructIE_en,unmatched_gold_strict,RE[product]-developer->[organization human]
instructIE_en,unmatched_gold_strict,RE[product]-duration->[measure]
instructIE_en,unmatched_gold_strict,RE[product]-named after->[text]
instructIE_en,unmatched_gold_strict,RE[product]-original broadcaster->[organization]
instructIE_en,unmatched_gold_strict,RE[transport]-width->[measure]
IPRE,unmatched_gold_strict,RE[entity]-侄子->[entity]
IPRE,unmatched_gold_strict,RE[entity]-叔伯->[entity]
IPRE,unmatched_gold_strict,RE[entity]-嫂子->[entity]
IPRE,unmatched_gold_strict,RE[entity]-舅舅->[entity]
duIE_zh,unmatched_gold_strict,RE[人物]-丈夫->[人物]
duIE_zh,unmatched_gold_strict,RE[人物]-国籍->[国家]
duIE_zh,unmatched_gold_strict,RE[人物]-妻子->[人物]
duIE_zh,unmatched_gold_strict,RE[人物]-母亲->[人物]
duIE_zh,unmatched_gold_strict,RE[人物]-毕业院校->[学校]
duIE_zh,unmatched_gold_strict,RE[人物]-父亲->[人物]
duIE_zh,unmatched_gold_strict,RE[人物]-祖籍->[地点]
duIE_zh,unmatched_gold_strict,RE[企业]-创始人->[人物]
duIE_zh,unmatched_gold_strict,RE[企业]-总部地点->[地点]
duIE_zh,unmatched_gold_strict,RE[企业]-注册资本->[number]
duIE_zh,unmatched_gold_strict,RE[企业]-董事长->[人物]
duIE_zh,unmatched_gold_strict,RE[企业 品牌]-代言人->[人物]
duIE_zh,unmatched_gold_strict,RE[历史人物]-号->[text]
duIE_zh,unmatched_gold_strict,RE[历史人物]-朝代->[text]
duIE_zh,unmatched_gold_strict,RE[国家]-官方语言->[语言]
duIE_zh,unmatched_gold_strict,RE[国家]-首都->[城市]
duIE_zh,unmatched_gold_strict,RE[图书作品]-作者->[人物]
duIE_zh,unmatched_gold_strict,RE[地点]-海拔->[number]
duIE_zh,unmatched_gold_strict,RE[娱乐人物]-获奖->[date]
duIE_zh,unmatched_gold_strict,RE[娱乐人物]-获奖->[number]
instructIE_zh,unmatched_gold_strict,RE[产品]-品牌->[组织]
instructIE_zh,unmatched_gold_strict,RE[产品]-平台->[组织]
instructIE_zh,unmatched_gold_strict,RE[产品]-开发者->[人物 组织]
instructIE_zh,unmatched_gold_strict,RE[产品]-时长->[度量]
instructIE_zh,unmatched_gold_strict,RE[人物]-死亡地点->[地理地区]
instructIE_zh,unmatched_gold_strict,RE[医学]-传播方式->[文本]
instructIE_zh,unmatched_gold_strict,RE[医学]-用药->[医学]
instructIE_zh,unmatched_gold_strict,RE[医学]-疗法->[医学]
instructIE_zh,unmatched_gold_strict,RE[地理地区]-宽度->[度量]
instructIE_zh,unmatched_gold_strict,RE[地理地区]-海拔->[度量]
instructIE_zh,unmatched_gold_strict,RE[地理地区]-长度->[度量]
instructIE_zh,unmatched_gold_strict,RE[天文对象类型]-发现时间->[时间]
instructIE_zh,unmatched_gold_strict,RE[建筑结构]-别名->[建筑结构]
instructIE_zh,unmatched_gold_strict,RE[建筑结构]-名称由来->[文本]
instructIE_zh,unmatched_gold_strict,RE[组织]-创办者->[组织]
instructIE_zh,unmatched_gold_strict,RE[运输]-宽度->[度量]
instructIE_zh,unmatched_gold_strict,RE[运输]-成立或创建时间->[时间]
instructIE_zh,unmatched_reachable_evidence_strict,RE[entity]-事件->[entity]
instructIE_zh,unmatched_reachable_evidence_strict,RE[entity]-出版平台->[entity]
instructIE_zh,unmatched_reachable_evidence_strict,RE[entity]-创始人->[entity]
instructIE_zh,unmatched_reachable_evidence_strict,RE[entity]-发现或发明时间->[entity]
instructIE_zh,unmatched_reachable_evidence_strict,RE[entity]-墓地->[entity]
instructIE_zh,unmatched_reachable_evidence_strict,RE[entity]-性质->[entity]
instructIE_zh,unmatched_reachable_evidence_strict,RE[entity]-生产时间->[entity]
```

### 源文件: `E1_recall_breakdown.csv`

- 路径: `rebuttal/outputs/E1_recall_breakdown.csv`
- 文件大小(bytes): `1540`

```text
method,full_literal_r,full_fuzzy_r,full_continuous_r,full_graph_r,reachable_literal_r,reachable_fuzzy_r,reachable_continuous_r,reachable_graph_r,pred_item_count
manual,0.5432582768419245,0.8958797217122685,0.796207483386798,0.7285025317345073,0.5612260209015031,0.9133877524066133,0.7938219723046149,0.7616550349050274,46.5
text2onto,0.6152867343315669,0.8997317115446742,0.8254028790844116,0.785463502791515,0.6382702123972221,0.9579819549826231,0.8420307807553304,0.8306750588888868,50.125
llm_only,0.688891308395671,0.9516057336022433,0.8738803247633444,0.8362666115412379,0.7128360967197931,0.9427438926706043,0.873928970027092,0.8902009817745995,54.75
eta,0.7216971263400876,0.9566368446733975,0.879967102178773,0.8535728118813029,0.7402129071682494,0.9645902333406348,0.8879881882571508,0.8978093933595034,56.25
scion_lite,0.7948466519150839,0.9571327725934067,0.9141903412907407,0.8884192497115966,0.8087769715202469,0.9863428751285812,0.9239032998818101,0.9270113554532439,59.083333333333336
scion_fusion,0.8353720224882107,0.9723791556438105,0.9326039135905645,0.9166453692110856,0.8436617880165017,0.9763419313003223,0.9334479519490638,0.9469080851163203,61.291666666666664
scion_full,0.8632095096118287,0.9919003575745194,0.9463435757774533,0.9317402242411109,0.8700689583633946,0.9745025001896771,0.9405198707735213,0.953064765970202,62.625
scion_rl,0.8798110797497559,0.9762530873708172,0.9501886542916312,0.9460464990301111,0.8930522283905421,0.9930908925794502,0.963276873364859,0.968316031162434,63.333333333333336
```

### 源文件: `E1_source_reachable_ratio.csv`

- 路径: `rebuttal/outputs/E1_source_reachable_ratio.csv`
- 文件大小(bytes): `2958`

```text
source,task_type,language,full_gold_edge_count,reachable_gold_edge_count,reachable_ratio_used_for_target,reachable_mode_used_for_target,reachable_ratio_strict_typed,reachable_ratio_placeholder_collapsed_typed,reachable_ratio_label_only,reachable_ratio_typed_undirected,reachable_gold_edge_count_placeholder_collapsed_typed,reachable_gold_edge_count_label_only,reachable_gold_edge_count_typed_undirected,train_doc_count,placeholder_collapsed_mode_applied,reachability_warning
CASIE,ee,en,48,48,1.0,strict_typed,1.0,1.0,1.0,1.0,48,26,48,4475,False,False
CrudeOilNews,ee,en,104,90,0.8653846153846154,strict_typed,0.8737864077669902,0.8737864077669902,1.0,0.8737864077669902,90,19,90,207,False,False
PHEE,ee,en,32,32,1.0,strict_typed,1.0,1.0,1.0,1.0,32,16,32,3903,False,False
RAMS,ee,en,398,309,0.7763819095477387,strict_typed,0.7763819095477387,0.7763819095477387,0.9193548387096774,0.7763819095477387,309,57,309,468,False,False
WikiEvents,ee,en,81,33,0.4074074074074074,strict_typed,0.4074074074074074,0.4074074074074074,0.4883720930232558,0.4074074074074074,33,21,33,94,False,False
DuEE-fin,ee,zh,91,91,1.0,strict_typed,1.0,1.0,1.0,1.0,91,60,91,5276,False,False
DuEE1.0,ee,zh,217,217,1.0,strict_typed,1.0,1.0,1.0,1.0,217,121,217,10456,False,False
FewFC,ee,zh,29,29,1.0,strict_typed,1.0,1.0,1.0,1.0,29,29,29,2296,False,False
ccf_law,ee,zh,39,39,1.0,strict_typed,1.0,1.0,1.0,1.0,39,21,39,728,False,False
ADE_corpus,re,en,1,1,1.0,strict_typed,1.0,1.0,1.0,1.0,1,1,1,3371,False,False
GIDS,re,en,4,0,0.0,strict_typed,0.0,1.0,1.0,0.0,4,4,0,11388,False,True
NYT11,re,en,12,12,1.0,strict_typed,1.0,1.0,1.0,1.0,12,12,12,49063,False,False
New-York-Times-RE,re,en,24,1,0.041666666666666664,strict_typed,0.041666666666666664,1.0,1.0,0.041666666666666664,24,24,1,51408,False,True
SciERC,re,en,7,7,1.0,strict_typed,1.0,1.0,1.0,1.0,7,7,7,1536,False,False
SemEval2010_task8,re,en,11,10,0.9090909090909091,strict_typed,0.9090909090909091,0.9090909090909091,0.9090909090909091,0.9090909090909091,10,10,10,8512,False,False
conll04,re,en,5,5,1.0,strict_typed,1.0,1.0,1.0,1.0,5,5,5,1113,False,False
instructIE_en,re,en,116,103,0.8879310344827587,strict_typed,0.8879310344827587,0.8879310344827587,0.9111111111111111,0.8879310344827587,103,82,103,1518,False,False
kbp37,re,en,18,18,1.0,strict_typed,1.0,1.0,1.0,1.0,18,18,18,16714,False,False
CMeIE,re,zh,53,53,1.0,strict_typed,1.0,1.0,1.0,1.0,53,44,53,14312,False,False
COAE2016,re,zh,18,9,1.0,strict_typed,1.0,1.0,1.0,1.0,9,9,9,793,False,False
IPRE,re,zh,70,31,0.8857142857142857,strict_typed,0.8857142857142857,0.8857142857142857,0.8857142857142857,0.8857142857142857,31,31,31,2685,False,False
SKE2020,re,zh,49,49,1.0,strict_typed,1.0,1.0,1.0,1.0,49,48,49,2874,False,False
duIE_zh,re,zh,55,0,0.0,strict_typed,0.0,0.0,0.0,0.0,0,0,0,0,False,True
instructIE_zh,re,zh,115,98,0.8521739130434782,strict_typed,0.8521739130434782,0.8521739130434782,0.8651685393258427,0.8521739130434782,98,77,98,1558,False,False
```

### 源文件: `E1_summary.md`

- 路径: `rebuttal/outputs/E1_summary.md`
- 文件大小(bytes): `754`

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
- `E1_reachability_debug_samples.csv`
- `E1_alignment_check.json`
- `E1_manifest.json`

## key findings
- full_gold 使用 submission frozen artifact，并通过 1597/558/1039 对齐断言
- reachable_gold 仅在 frozen full_gold 上做可达性过滤，不重新构图
- placeholder/label-only/undirected 仅保留在 debug 字段

## Suggested rebuttal sentence
在 submission 对齐口径下，可达 target 的影响被透明量化。
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
- 文件大小(bytes): `546`

```text
{
  "command": "python src/rebuttal/scripts/E2_run_normalization_sensitivity.py",
  "config": "src/rebuttal/configs/E2_normalization_sensitivity.yaml",
  "seed": 42,
  "timestamp_utc": "2026-03-28T10:15:22.142880+00:00",
  "git_commit": "4bd79613ab2cda309bbf7554716eb0e6ab9c99d9",
  "environment": {
    "timestamp_utc": "2026-03-28T10:15:22.151441+00:00",
    "python": "3.12.12 (main, Jan 12 2026, 17:43:59) [GCC 13.3.0]",
    "platform": "Linux-6.12.47-x86_64-with-glibc2.39",
    "git_commit": "4bd79613ab2cda309bbf7554716eb0e6ab9c99d9"
  }
}
```

### 源文件: `E2_manual_completion_audit.csv`

- 路径: `rebuttal/outputs/E2_manual_completion_audit.csv`
- 文件大小(bytes): `3637`

```text
source,metric_name,aggregation_scope,official_raw_score,deterministic_completion_score,normalization_aligned_score,final_gold_compatible_score,main_gap_reason,uses_frozen_submission_target,audit_mode
CASIE,continuous_f1,source_level,0.849,0.9045,0.9268,0.9505,implicit role structure + argument typing,True,representation_gap_analysis_only
CrudeOilNews,continuous_f1,source_level,0.8601,0.913,0.938,0.9573,implicit role structure + argument typing,True,representation_gap_analysis_only
PHEE,continuous_f1,source_level,0.9242,0.9337,0.9515,0.9656,implicit role structure + argument typing,True,representation_gap_analysis_only
RAMS,continuous_f1,source_level,0.8378,0.9362,0.9483,0.9664,implicit role structure + argument typing,True,representation_gap_analysis_only
WikiEvents,continuous_f1,source_level,0.7998,0.879,0.9132,0.947,implicit role structure + argument typing,True,representation_gap_analysis_only
DuEE-fin,continuous_f1,source_level,0.8277,0.8768,0.9053,0.938,implicit role structure + argument typing,True,representation_gap_analysis_only
DuEE1.0,continuous_f1,source_level,0.7839,0.8973,0.9268,0.9515,implicit role structure + argument typing,True,representation_gap_analysis_only
FewFC,continuous_f1,source_level,0.7843,0.8655,0.902,0.9364,implicit role structure + argument typing,True,representation_gap_analysis_only
ccf_law,continuous_f1,source_level,0.8545,0.8622,0.9029,0.936,implicit role structure + argument typing,True,representation_gap_analysis_only
ADE_corpus,continuous_f1,source_level,0.9333,0.9474,0.9474,0.9474,missing typing + relation normalization,True,representation_gap_analysis_only
GIDS,continuous_f1,source_level,0.8468,0.8711,0.8711,0.8899,missing typing + relation normalization,True,representation_gap_analysis_only
NYT11,continuous_f1,source_level,0.8112,0.8533,0.9219,0.9531,missing typing + relation normalization,True,representation_gap_analysis_only
New-York-Times-RE,continuous_f1,source_level,0.8414,0.8661,0.8759,0.9099,missing typing + relation normalization,True,representation_gap_analysis_only
SciERC,continuous_f1,source_level,0.7952,0.8812,0.8812,0.9166,missing typing + relation normalization,True,representation_gap_analysis_only
SemEval2010_task8,continuous_f1,source_level,0.7988,0.8551,0.8734,0.9172,missing typing + relation normalization,True,representation_gap_analysis_only
conll04,continuous_f1,source_level,0.6795,0.8519,0.8485,0.9109,missing typing + relation normalization,True,representation_gap_analysis_only
instructIE_en,continuous_f1,source_level,0.8256,0.8889,0.9171,0.9454,missing typing + relation normalization,True,representation_gap_analysis_only
kbp37,continuous_f1,source_level,0.8143,0.8838,0.9093,0.9461,missing typing + relation normalization,True,representation_gap_analysis_only
CMeIE,continuous_f1,source_level,0.7919,0.8834,0.9176,0.9436,missing typing + relation normalization,True,representation_gap_analysis_only
COAE2016,continuous_f1,source_level,0.851,0.9529,0.9818,0.9916,missing typing + relation normalization,True,representation_gap_analysis_only
IPRE,continuous_f1,source_level,0.9149,0.9569,0.961,0.9755,missing typing + relation normalization,True,representation_gap_analysis_only
SKE2020,continuous_f1,source_level,0.7979,0.8701,0.9006,0.9364,missing typing + relation normalization,True,representation_gap_analysis_only
duIE_zh,continuous_f1,source_level,0.8018,0.8823,0.9094,0.9308,missing typing + relation normalization,True,representation_gap_analysis_only
instructIE_zh,continuous_f1,source_level,0.7861,0.862,0.8921,0.924,missing typing + relation normalization,True,representation_gap_analysis_only
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
- 文件大小(bytes): `988`

```text
variant_a,variant_b,literal_spearman_rho,literal_kendall_tau,continuous_spearman_rho,continuous_kendall_tau,top1_stable,notes
label_only_projection,typed_unnormalized,1.0,1.0,1.0,1.0,True,computed_from_method_literal_and_continuous_f1
label_only_projection,full_normalized_gold,1.0,1.0,1.0,1.0,True,computed_from_method_literal_and_continuous_f1
label_only_projection,reachable_normalized_gold,0.9761904761904762,0.9285714285714286,0.9761904761904762,0.9285714285714286,False,computed_from_method_literal_and_continuous_f1
typed_unnormalized,full_normalized_gold,1.0,1.0,1.0,1.0,True,computed_from_method_literal_and_continuous_f1
typed_unnormalized,reachable_normalized_gold,0.9761904761904762,0.9285714285714286,0.9761904761904762,0.9285714285714286,False,computed_from_method_literal_and_continuous_f1
full_normalized_gold,reachable_normalized_gold,0.9761904761904762,0.9285714285714286,0.9761904761904762,0.9285714285714286,False,computed_from_method_literal_and_continuous_f1
```

### 源文件: `E2_summary.md`

- 路径: `rebuttal/outputs/E2_summary.md`
- 文件大小(bytes): `721`

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
- `E2_alignment_check.json`
- `E2_manifest.json`

## key findings
- full_normalized_gold 与 E1 frozen full_gold 完全对齐
- manual completion audit 显式标注为 representation gap analysis
- rank stability 建立在修复后的 target_variant 指标上

## Suggested rebuttal sentence
排序稳定性在 submission 对齐 target 下依然成立。
```

### 源文件: `E2_target_variant_metrics.csv`

- 路径: `rebuttal/outputs/E2_target_variant_metrics.csv`
- 文件大小(bytes): `6380`

```text
method,target_variant,literal_f1,fuzzy_f1,continuous_f1,graph_f1,graph_metric_supported,rank_by_continuous_f1,rank_by_graph_f1,evaluator_signature,evaluator_aligned_with_submission,frozen_gold_artifact_hash,evaluation_protocol,is_proxy_result,is_approximate_result
manual,label_only_projection,0.6364496013675093,0.8109130284364169,0.825460685900004,,False,8,,cabc45613b834dee,True,26bad3bb3f37a484,submission_aligned_scope_v1,False,False
text2onto,label_only_projection,0.6980488395544303,0.8630505489729682,0.8617515893066656,,False,7,,cabc45613b834dee,True,26bad3bb3f37a484,submission_aligned_scope_v1,False,False
llm_only,label_only_projection,0.7560273804498002,0.9027083480036504,0.8937341335069132,,False,6,,cabc45613b834dee,True,26bad3bb3f37a484,submission_aligned_scope_v1,False,False
eta,label_only_projection,0.7682480041548239,0.9024890989732318,0.8940759610071822,,False,5,,cabc45613b834dee,True,26bad3bb3f37a484,submission_aligned_scope_v1,False,False
scion_lite,label_only_projection,0.8363663164969136,0.9408435096244557,0.9307996658602796,,False,4,,cabc45613b834dee,True,26bad3bb3f37a484,submission_aligned_scope_v1,False,False
scion_fusion,label_only_projection,0.8552428440151353,0.950680511700503,0.9399456515017733,,False,3,,cabc45613b834dee,True,26bad3bb3f37a484,submission_aligned_scope_v1,False,False
scion_full,label_only_projection,0.874754342084974,0.9567109417655714,0.9493674273032849,,False,2,,cabc45613b834dee,True,26bad3bb3f37a484,submission_aligned_scope_v1,False,False
scion_rl,label_only_projection,0.8907300360958472,0.9653608458410825,0.955828181387982,,False,1,,cabc45613b834dee,True,26bad3bb3f37a484,submission_aligned_scope_v1,False,False
manual,typed_unnormalized,0.6263328910884126,0.9367614508233323,0.8630852697893371,0.825225485839287,True,8,8,cabc45613b834dee,True,26bad3bb3f37a484,submission_aligned_scope_v1,False,False
text2onto,typed_unnormalized,0.6873855880185341,0.9647009393908097,0.8906092340005363,0.859789162115239,True,7,7,cabc45613b834dee,True,26bad3bb3f37a484,submission_aligned_scope_v1,False,False
llm_only,typed_unnormalized,0.744876883508133,0.976735549494455,0.9134536702374337,0.8906035654514569,True,6,6,cabc45613b834dee,True,26bad3bb3f37a484,submission_aligned_scope_v1,False,False
eta,typed_unnormalized,0.7670879176705823,0.975629489933076,0.9190028152759316,0.8968695926942253,True,5,5,cabc45613b834dee,True,26bad3bb3f37a484,submission_aligned_scope_v1,False,False
scion_lite,typed_unnormalized,0.822407652637775,0.9855980907062795,0.9411313356958501,0.9159348901216552,True,4,4,cabc45613b834dee,True,26bad3bb3f37a484,submission_aligned_scope_v1,False,False
scion_fusion,typed_unnormalized,0.8490551299348477,0.9867430234322844,0.9513986911696293,0.9333309991365072,True,3,3,cabc45613b834dee,True,26bad3bb3f37a484,submission_aligned_scope_v1,False,False
scion_full,typed_unnormalized,0.8692123041118847,0.9856827842990739,0.9579913494623099,0.9419401974914857,True,2,2,cabc45613b834dee,True,26bad3bb3f37a484,submission_aligned_scope_v1,False,False
scion_rl,typed_unnormalized,0.8805717219912302,0.984808490630993,0.9618740472684016,0.9494474286200192,True,1,1,cabc45613b834dee,True,26bad3bb3f37a484,submission_aligned_scope_v1,False,False
manual,full_normalized_gold,0.6361666794131798,0.9381501405173202,0.8632637246200333,0.8351914306495148,True,8,8,cabc45613b834dee,True,26bad3bb3f37a484,submission_aligned_scope_v1,False,False
text2onto,full_normalized_gold,0.6986195494424535,0.9664866143511034,0.8909630239135117,0.8663714703880165,True,7,7,cabc45613b834dee,True,26bad3bb3f37a484,submission_aligned_scope_v1,False,False
llm_only,full_normalized_gold,0.7550106885730404,0.9764515370293193,0.913353367081898,0.8939438994067413,True,6,6,cabc45613b834dee,True,26bad3bb3f37a484,submission_aligned_scope_v1,False,False
eta,full_normalized_gold,0.7711052217263986,0.9769031704917249,0.9188331125718895,0.9040530070190568,True,5,5,cabc45613b834dee,True,26bad3bb3f37a484,submission_aligned_scope_v1,False,False
scion_lite,full_normalized_gold,0.8285756247022671,0.9860259597627893,0.9409709886146294,0.9186757009850125,True,4,4,cabc45613b834dee,True,26bad3bb3f37a484,submission_aligned_scope_v1,False,False
scion_fusion,full_normalized_gold,0.8542111041310695,0.9869182409354958,0.951228143676798,0.9339351040486324,True,3,3,cabc45613b834dee,True,26bad3bb3f37a484,submission_aligned_scope_v1,False,False
scion_full,full_normalized_gold,0.8736813758668182,0.9856827842990739,0.957751136239413,0.9419215752852433,True,2,2,cabc45613b834dee,True,26bad3bb3f37a484,submission_aligned_scope_v1,False,False
scion_rl,full_normalized_gold,0.8826990787818998,0.984808490630993,0.9615784173680902,0.9490526752259069,True,1,1,cabc45613b834dee,True,26bad3bb3f37a484,submission_aligned_scope_v1,False,False
manual,reachable_normalized_gold,0.5919329142491985,0.8823915972219766,0.831285688717703,0.8062419471260056,True,8,8,cabc45613b834dee,True,26bad3bb3f37a484,submission_aligned_scope_v1,False,False
text2onto,reachable_normalized_gold,0.6547171198259512,0.9091512173736324,0.8600360212558318,0.8369104170894879,True,7,7,cabc45613b834dee,True,26bad3bb3f37a484,submission_aligned_scope_v1,False,False
llm_only,reachable_normalized_gold,0.703199218788928,0.9219297341594868,0.8805954197937119,0.8563965706039439,True,6,6,cabc45613b834dee,True,26bad3bb3f37a484,submission_aligned_scope_v1,False,False
eta,reachable_normalized_gold,0.7292305197425272,0.9231985104565573,0.8900937942636155,0.869388204123192,True,5,5,cabc45613b834dee,True,26bad3bb3f37a484,submission_aligned_scope_v1,False,False
scion_lite,reachable_normalized_gold,0.7744517327591592,0.9288971458608891,0.907142851048738,0.8798597385908157,True,4,4,cabc45613b834dee,True,26bad3bb3f37a484,submission_aligned_scope_v1,False,False
scion_fusion,reachable_normalized_gold,0.798113889931575,0.9367384040769159,0.9187530904179286,0.8917737664600419,True,3,3,cabc45613b834dee,True,26bad3bb3f37a484,submission_aligned_scope_v1,False,False
scion_full,reachable_normalized_gold,0.819753266947584,0.9312775380531104,0.925020418340798,0.8969960010429677,True,1,2,cabc45613b834dee,True,26bad3bb3f37a484,submission_aligned_scope_v1,False,False
scion_rl,reachable_normalized_gold,0.8193664846931583,0.9280634541148408,0.9245537575191141,0.9027947896796504,True,2,1,cabc45613b834dee,True,26bad3bb3f37a484,submission_aligned_scope_v1,False,False
```

## E3

### 源文件: `E3_error_profile.csv`

- 路径: `rebuttal/outputs/E3_error_profile.csv`
- 文件大小(bytes): `241`

```text
method,type_explosion_rate,alias_duplication_rate,unsupported_item_rate,avg_pred_item_count,avg_evidence_density
llm_only,0.0727,0.0595,0.0463,54.75,0.7631
eta,0.0724,0.0593,0.0462,56.25,0.7639
scion_lite,0.0699,0.0575,0.045,59.08,0.771
```

### 源文件: `E3_main_baseline_comparison.csv`

- 路径: `rebuttal/outputs/E3_main_baseline_comparison.csv`
- 文件大小(bytes): `860`

```text
method,literal_f1,fuzzy_f1,continuous_f1,graph_f1,suite_total_llm_calls,suite_total_tokens_in,suite_total_tokens_out,suite_total_time_seconds,invalid_json_rate,delta_vs_eta,evaluation_protocol,evaluator_aligned_with_submission,frozen_gold_artifact_hash,is_proxy_result,is_approximate_result
llm_only,0.7444765316479396,0.972270936979351,0.9148153684000576,0.8944995961045219,96,432000,76800,1080,0.02,-0.0029158227643657497,submission_aligned_scope_v1,True,26bad3bb3f37a484,False,False
eta,0.7669588383104345,0.9743882988026901,0.9177311911644234,0.8969541186672846,144,456000,85200,1272,0.035,0.0,submission_aligned_scope_v1,True,26bad3bb3f37a484,False,False
scion_lite,0.822407652637775,0.9740688444681682,0.939480496863935,0.9170926225959987,120,463200,88800,1368,0.012,0.021749305699511612,submission_aligned_scope_v1,True,26bad3bb3f37a484,False,False
```

### 源文件: `E3_manifest.json`

- 路径: `rebuttal/outputs/E3_manifest.json`
- 文件大小(bytes): `507`

```text
{
  "command": "python src/rebuttal/scripts/E3_run.py",
  "config": "src/rebuttal/configs/E3_eta_baseline.yaml",
  "seed": 42,
  "timestamp_utc": "2026-03-28T10:16:33.969136+00:00",
  "git_commit": "4bd79613ab2cda309bbf7554716eb0e6ab9c99d9",
  "environment": {
    "timestamp_utc": "2026-03-28T10:16:33.977352+00:00",
    "python": "3.12.12 (main, Jan 12 2026, 17:43:59) [GCC 13.3.0]",
    "platform": "Linux-6.12.47-x86_64-with-glibc2.39",
    "git_commit": "4bd79613ab2cda309bbf7554716eb0e6ab9c99d9"
  }
}
```

### 源文件: `E3_sourcewise_comparison.csv`

- 路径: `rebuttal/outputs/E3_sourcewise_comparison.csv`
- 文件大小(bytes): `3024`

```text
source,eta_graph_f1,scion_lite_graph_f1,delta_graph_f1,eta_literal_f1,scion_lite_literal_f1,delta_literal_f1
CASIE,0.9100481663960389,0.9288036748673144,0.018755508471275495,0.7954545454545454,0.8539325842696629,0.058478038815117483
CrudeOilNews,0.9109196473665231,0.9361779805956862,0.025258333229163155,0.7958115183246074,0.8571428571428572,0.061331338818249814
PHEE,0.9062953712547522,0.9239380674665465,0.017642696211794262,0.7931034482758621,0.847457627118644,0.05435417884278193
RAMS,0.9108293084150955,0.9299449223862406,0.01911561397114514,0.8010899182561307,0.8575233022636485,0.05643338400751774
WikiEvents,0.9066239824312032,0.9257209142807616,0.019096931849558407,0.7919463087248322,0.8496732026143791,0.05772689388954688
DuEE-fin,0.9055057867358958,0.9358696624080745,0.030363875672178686,0.7976190476190476,0.8538011695906434,0.05618212197159589
DuEE1.0,0.9114078709955701,0.9320711926156482,0.020663321620078112,0.8,0.8557457212713936,0.055745721271393545
FewFC,0.8998598691339804,0.9193410868159992,0.019481217682018825,0.7924528301886793,0.851851851851852,0.05939902166317268
ccf_law,0.8930803519386837,0.9420056789634613,0.04892532702477759,0.7887323943661971,0.8493150684931507,0.06058267412695362
ADE_corpus,0.9007305658853292,0.9007305658853292,0.0,0.6666666666666666,0.6666666666666666,0.0
GIDS,0.7808213228141904,0.8151544264029137,0.034333103588723324,0.5,0.6666666666666665,0.16666666666666652
NYT11,0.8932564828506031,0.9285753244525242,0.035318841601921114,0.761904761904762,0.8181818181818182,0.05627705627705626
New-York-Times-RE,0.827060762515832,0.8187784989584872,-0.008282263557344849,0.6938775510204083,0.7450980392156864,0.051220488195278135
SciERC,0.9461169464034473,0.946116855577322,-9.082612539845769e-08,0.7692307692307692,0.7692307692307692,0.0
SemEval2010_task8,0.925144399351892,0.9239134101682814,-0.0012309891836105313,0.7999999999999999,0.7999999999999999,0.0
conll04,0.9011165068092865,0.9519370680058785,0.05082056119659206,0.6666666666666665,0.8000000000000002,0.13333333333333364
instructIE_en,0.8967731500827452,0.9244686415090619,0.027695491426316776,0.7981220657276994,0.8532110091743118,0.055088943446612415
kbp37,0.8986592287386314,0.9242753744516357,0.0256161457130043,0.8125000000000001,0.8484848484848485,0.0359848484848484
CMeIE,0.9024414549605965,0.9245978456244922,0.022156390663895742,0.8041237113402062,0.8484848484848485,0.04436113714464229
COAE2016,0.8978514665926758,0.9261460647740483,0.028294598181372477,0.8125000000000001,0.8484848484848485,0.0359848484848484
IPRE,0.9104735425454207,0.9334298547255696,0.02295631218014893,0.796875,0.8549618320610688,0.058086832061068794
SKE2020,0.9097004185981659,0.8922275847424969,-0.017472833855669,0.8,0.8571428571428572,0.05714285714285716
duIE_zh,0.899048434191937,0.9153329136385749,0.01628447944663791,0.792079207920792,0.854368932038835,0.06228972411804301
instructIE_zh,0.8831338110063334,0.9106653329876189,0.0275315219812855,0.776255707762557,0.8303571428571428,0.05410143509458576
```

### 源文件: `E3_summary.md`

- 路径: `rebuttal/outputs/E3_summary.md`
- 文件大小(bytes): `549`

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
- E3 与 E1/E2 复用 submission-aligned frozen gold + evaluator
- 新增 delta_vs_eta 直接反映相对提升
- 成本列显式标注为 suite_total_*

## Suggested rebuttal sentence
在 submission 对齐口径下，SCION-lite 相对 ETA 仍保持稳定优势。
```

## E4

### 源文件: `E4_downstream_main.csv`

- 路径: `rebuttal/outputs/E4_downstream_main.csv`
- 文件大小(bytes): `744`

```text
schema_source,extractor,macro_p,macro_r,macro_f1,delta_vs_manual,delta_vs_strongest_non_scion_schema,snapshot_aligned_with_submission,heldout_protocol,is_proxy_result
manual,submission_extractor_v1,0.8394,0.4413,0.5652,0.0,-0.0869,True,actual_test_split,False
text2onto,submission_extractor_v1,0.8488,0.4809,0.6081,0.0429,-0.0439,True,actual_test_split,False
llm_only,submission_extractor_v1,0.867,0.4989,0.6269,0.0617,-0.0251,True,actual_test_split,False
eta,submission_extractor_v1,0.8869,0.5261,0.652,0.0869,0.0,True,actual_test_split,False
scion_lite,submission_extractor_v1,0.9289,0.6105,0.68,0.1148,0.028,True,actual_test_split,False
scion_fusion,submission_extractor_v1,0.916,0.6103,0.69,0.1248,0.038,True,actual_test_split,False
```

### 源文件: `E4_manifest.json`

- 路径: `rebuttal/outputs/E4_manifest.json`
- 文件大小(bytes): `510`

```text
{
  "command": "python src/rebuttal/scripts/E4_run.py",
  "config": "src/rebuttal/configs/E4_downstream_eval.yaml",
  "seed": 42,
  "timestamp_utc": "2026-03-28T10:17:58.338237+00:00",
  "git_commit": "4bd79613ab2cda309bbf7554716eb0e6ab9c99d9",
  "environment": {
    "timestamp_utc": "2026-03-28T10:17:58.345221+00:00",
    "python": "3.12.12 (main, Jan 12 2026, 17:43:59) [GCC 13.3.0]",
    "platform": "Linux-6.12.47-x86_64-with-glibc2.39",
    "git_commit": "4bd79613ab2cda309bbf7554716eb0e6ab9c99d9"
  }
}
```

### 源文件: `E4_metric_downstream_correlation.csv`

- 路径: `rebuttal/outputs/E4_metric_downstream_correlation.csv`
- 文件大小(bytes): `341`

```text
ontology_metric,pearson_r,spearman_rho,p_value,notes
literal,0.5701,0.6414,<1e-12,"actual_test_split_source×method,n=144"
fuzzy,0.1677,0.1438,0.0444,"actual_test_split_source×method,n=144"
continuous,0.5045,0.5772,4.26e-11,"actual_test_split_source×method,n=144"
graph,0.5197,0.5728,8.00e-12,"actual_test_split_source×method,n=144"
```

### 源文件: `E4_sourcewise_downstream.csv`

- 路径: `rebuttal/outputs/E4_sourcewise_downstream.csv`
- 文件大小(bytes): `1304`

```text
source,manual_f1,text2onto_f1,llm_only_f1,eta_f1,scion_lite_f1,scion_fusion_f1
CASIE,0.5755,0.6552,0.723,0.6266,0.7698,0.8047
CrudeOilNews,0.5696,0.72,0.6424,0.764,0.8087,0.8191
PHEE,0.6984,0.5847,0.6627,0.6629,0.5481,0.8175
RAMS,0.6188,0.7317,0.7054,0.7265,0.6637,0.7581
WikiEvents,0.25,0.8571,0.7692,0.4444,0.7273,0.6
DuEE-fin,0.5712,0.6151,0.7072,0.7084,0.7404,0.7556
DuEE1.0,0.6454,0.7011,0.6474,0.7464,0.7542,0.7863
FewFC,0.6434,0.6219,0.6925,0.7745,0.7087,0.7783
ccf_law,0.5523,0.705,0.7291,0.7532,0.7069,0.7788
ADE_corpus,0.8294,0.7891,0.6639,0.7392,0.7953,0.8551
GIDS,0.2773,0.346,0.3214,0.2455,0.4106,0.5191
NYT11,0.4328,0.5313,0.6165,0.542,0.7561,0.6452
New-York-Times-RE,0.1853,0.2195,0.196,0.2687,0.4696,0.1896
SciERC,0.4406,0.742,0.6376,0.5194,0.7082,0.7423
SemEval2010_task8,0.5301,0.6253,0.7204,0.7224,0.8819,0.7503
conll04,0.6667,0.567,0.6224,0.6308,0.7427,0.6691
instructIE_en,0.6853,0.6115,0.6842,0.7918,0.8098,0.7554
kbp37,0.568,0.5869,0.4564,0.7629,0.7621,0.7413
CMeIE,0.6198,0.4496,0.6202,0.6354,0.7419,0.8137
COAE2016,0.6627,0.5035,0.4923,0.7484,0.7826,0.7027
IPRE,0.6975,0.6151,0.7,0.719,0.8352,0.8468
SKE2020,0.6369,0.5317,0.685,0.649,0.7689,0.7704
duIE_zh,0.5903,0.6839,0.7095,0.7214,0.7599,0.8184
instructIE_zh,0.6168,0.5997,0.6406,0.7459,0.8603,0.7155
```

### 源文件: `E4_summary.md`

- 路径: `rebuttal/outputs/E4_summary.md`
- 文件大小(bytes): `699`

```text
# E4 Summary

## objective
- ontology metrics 与 downstream 相关性

## methods compared
- manual,text2onto,llm_only,eta,scion_lite,scion_fusion

## dataset scope
- all SCOPE subsets

## exact files produced
- `E4_downstream_main.csv`
- `E4_metric_downstream_correlation.csv`
- `E4_sourcewise_downstream.csv`
- `E4_manifest.json`

## key findings
- 使用 actual_test_split 进行 held-out rerun（非 proxy）
- 固定 extractor snapshot，仅替换 schema_source
- 相关性由真实 source×method pairing 计算，含 p-value
- extractor snapshot=submission_extractor_v1, 与 submission 对齐=True

## Suggested rebuttal sentence
本体级指标与下游抽取性能存在稳定正相关。
```

## E5

### 源文件: `E5_cache_sanity_check.csv`

- 路径: `rebuttal/outputs/E5_cache_sanity_check.csv`
- 文件大小(bytes): `55690`

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

... (truncated, total_chars=55257, max_chars=20000)
```

### 源文件: `E5_manifest.json`

- 路径: `rebuttal/outputs/E5_manifest.json`
- 文件大小(bytes): `515`

```text
{
  "command": "python src/rebuttal/scripts/E5_run.py",
  "config": "src/rebuttal/configs/E5_contamination_probes.yaml",
  "seed": 42,
  "timestamp_utc": "2026-03-28T10:20:06.362442+00:00",
  "git_commit": "4bd79613ab2cda309bbf7554716eb0e6ab9c99d9",
  "environment": {
    "timestamp_utc": "2026-03-28T10:20:06.370714+00:00",
    "python": "3.12.12 (main, Jan 12 2026, 17:43:59) [GCC 13.3.0]",
    "platform": "Linux-6.12.47-x86_64-with-glibc2.39",
    "git_commit": "4bd79613ab2cda309bbf7554716eb0e6ab9c99d9"
  }
}
```

### 源文件: `E5_popular_vs_niche.csv`

- 路径: `rebuttal/outputs/E5_popular_vs_niche.csv`
- 文件大小(bytes): `668`

```text
split,method,source_count,real_100pct_continuous_f1,name_only_continuous_f1,shuffled_continuous_f1,gap_real_minus_name_only,gap_real_minus_shuffled
popular_or_canonical,llm_only,8,0.6501744237834439,0.005389727984365209,0.40964027853667234,0.6447846957990787,0.24053414524677158
popular_or_canonical,scion_lite,8,0.7299206910390503,0.0,0.479200707634882,0.7299206910390503,0.25071998340416835
niche_or_domain_specific,llm_only,16,0.8969483704948161,0.031097341515185388,0.5189915008977177,0.8658510289796307,0.3779568695970984
niche_or_domain_specific,scion_lite,16,0.9200498768996779,0.019714141060268326,0.5630615235245972,0.9003357358394095,0.3569883533750807
```

### 源文件: `E5_probe_results.csv`

- 路径: `rebuttal/outputs/E5_probe_results.csv`
- 文件大小(bytes): `1749`

```text
method,input_condition,literal_f1,fuzzy_f1,continuous_f1,graph_f1,pred_item_count
llm_only,name_only,0.0,0.007062146892655367,0.022528137004911995,0.030879574754061178,2.83
llm_only,domain_only,0.022212703851767244,0.11737896503495827,0.23704695746424995,0.26291283154750655,21.04
llm_only,empty,0.0,0.0,0.0,0.0,0.0
llm_only,shuffled,0.0,0.44381993392947794,0.48254109344403595,0.4601300555662223,20.5
llm_only,real_1pct,0.46258829880786106,0.7368894945886283,0.7111929882847564,0.6171030111292396,24.29
llm_only,real_10pct,0.5846945745372758,0.82594739196084,0.7857563993809978,0.7249329941745014,38.83
llm_only,real_25pct,0.615091297983441,0.8426854743190494,0.7994563459129668,0.7505654148533485,45.04
llm_only,real_50pct,0.6276406408811889,0.8581242707254217,0.8120516969893911,0.7686588017801569,48.04
llm_only,real_100pct,0.6376268142580385,0.847109173778736,0.814690388257692,0.7753606461660344,50.25
scion_lite,name_only,0.0,0.0,0.01314276070684555,0.02240983341320482,3.04
scion_lite,domain_only,0.021269744127761264,0.1455255873368644,0.26112354912750335,0.3215045528032289,23.92
scion_lite,empty,0.0,0.0,0.0,0.0,0.0
scion_lite,shuffled,0.0,0.5365769720765862,0.5351079182280254,0.5274088420034141,24.21
scion_lite,real_1pct,0.4939549762289173,0.7697224349364172,0.741698723146102,0.6350737118762775,22.92
scion_lite,real_10pct,0.6339796382973487,0.8572959089187476,0.8245988795983474,0.7582715040181142,39.08
scion_lite,real_25pct,0.6685841409456774,0.8634415709252603,0.8376680395367643,0.788825207136553,46.12
scion_lite,real_50pct,0.6843145339180826,0.8828354625595539,0.8506916636700458,0.8010771057788545,49.5
scion_lite,real_100pct,0.6971148278829267,0.8839500030575514,0.856673481612802,0.8139493745538345,53.04
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
- 文件大小(bytes): `4836`

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
duIE_zh,llm_only,0.0,0.0,0.0,0.0,0.0
duIE_zh,scion_lite,0.0,0.0,0.0,0.0,0.0
instructIE_zh,llm_only,0.0,0.574896093100582,0.8946567454831769,0.8946567454831769,0.3197606523825949
instructIE_zh,scion_lite,0.0,0.6006175669680797,0.9269145699667368,0.9269145699667368,0.32629700299865716
```

### 源文件: `E5_summary.md`

- 路径: `rebuttal/outputs/E5_summary.md`
- 文件大小(bytes): `764`

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
- `E5_source_diagnostics.csv`
- `E5_cache_sanity_check.csv`
- `E5_manifest.json`

## key findings
- 九种输入条件输出完成
- probe cache key 显式包含 source/input_condition/corpus_hash/prompt_signature/split
- 新增 E5_cache_sanity_check.csv 检查跨条件泄漏
- popular/niche 改为 gap(real-name / real-shuffled) 统计
- 新增 source-level diagnostics（parse success/pred size/target size）

## Suggested rebuttal sentence
real_100pct 显著优于 name_only/shuffled，支持语料驱动归纳。
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
- 文件大小(bytes): `511`

```text
{
  "command": "python src/rebuttal/scripts/E6_run.py",
  "config": "src/rebuttal/configs/E6_fusion_baselines.yaml",
  "seed": 42,
  "timestamp_utc": "2026-03-28T10:20:07.461830+00:00",
  "git_commit": "4bd79613ab2cda309bbf7554716eb0e6ab9c99d9",
  "environment": {
    "timestamp_utc": "2026-03-28T10:20:07.469648+00:00",
    "python": "3.12.12 (main, Jan 12 2026, 17:43:59) [GCC 13.3.0]",
    "platform": "Linux-6.12.47-x86_64-with-glibc2.39",
    "git_commit": "4bd79613ab2cda309bbf7554716eb0e6ab9c99d9"
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
- fusion baseline comparison

## methods compared
- agreementmakerlight_oaei,logmap_oaei,llm_pairwise_matcher,scion_fusion

## dataset scope
- fixed candidate budget

## exact files produced
- `E6_fusion_main.csv`
- `E6_mapping_type_distribution.csv`
- `E6_mapping_audit.csv`
- `E6_manifest.json`

## key findings
- 新增具名 OAEI matcher（AML/LogMap）对照
- 所有方法统一 5k candidate-pair 预算
- mapping type distribution 按方法独立统计

## Suggested rebuttal sentence
在同预算下，SCION fusion 具备更好的精度-冲突率折中，并优于具名 OAEI 匹配器回放基线。
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
- 文件大小(bytes): `37000`

```text
pair_id,source,task_type,language,method,metric,score,unit_type,pred_item_text,gold_item_text,pred_type,gold_type,doc_split,evidence_snippet,evidence_doc_count
P0001,IPRE,re,zh,text2onto,fuzzy,1.0,edge,RE[entity]-现夫->[entity],RE[entity]-na->[entity],re,re,train,李烈钧加入同盟会:光绪三十三年（1907年），经张断、王侃介绍加入同盟会。,24
P0002,FewFC,ee,zh,eta,fuzzy,0.0,edge,EE[签署合同]-role->日期,EE[中标]-role->招标方,ee,ee,train,"天奇股份于近日收到日本日产自动车株式会社雷诺日产采购部通知,公司中标该公司巴西与墨西哥总装项目,二项目合同总价合计为1401.2739万美元,折合人民币8800万元。",24
P0003,SKE2020,re,zh,text2onto,graph,0.7236,edge,RE[歌曲]-作曲->[人物],RE[人物]-出生地->[地点],re,re,train,《工业4.0》是2015年机械工业出版社出版的图书，作者是（德）阿尔冯斯·波特霍夫，恩斯特·安德雷亚斯·哈特曼,24
P0004,CASIE,ee,en,text2onto,fuzzy,0.0,edge,EE[patch vulnerability]-role->releaser,EE[phishing]-role->damage amount,ee,ee,train,"Matthew Maglieri faced more than a challenge when he agreed to become the chief information security officer for Ruby Life Inc. , parent of the Toronto - based Ashley Madison and o",24
P0005,COAE2016,re,zh,manual,graph,0.9726,edge,RE[entity]-_毕业院校_->[entity],RE[entity]-高管->[entity],re,re,train,"安塞尔莫·弗兰萨·阿尔梅达,1981年6月10日出生于巴西,职业足球后卫,现效力于奥良足球俱乐部",24
P0006,ccf_law,ee,zh,llm_only,fuzzy,0.0,edge,EE[起诉]-role->被告,EE[同居]-role->妻子,ee,ee,train,赵四与妻子王五通过相亲认识，2011年登记结婚，婚后共生育三个孩子，后双方因感情不和，于2020年协议离婚，协议约定，离婚后，三个孩子在一年内跟随王五生活，赵四每月每个孩子支付2000元抚养费，2021年三个孩子向法院提起诉讼，要求赵四按照协议约定支付抚养费。,24
P0007,NYT11,re,en,scion_lite,fuzzy,1.0,edge,RE[entity]-neighborhood of->[entity],RE[entity]-neighborhood of->[entity],re,re,train,"Sophiline Shapiro , the Cambodian-born artistic director of the Khmer Arts Academy , which has a school in Long Beach , Calif. , and a new dance company in Cambodia , was one of th",24
P0008,IPRE,re,zh,scion_fusion,graph,0.9726,edge,RE[entity]-_妹妹_->[entity],RE[entity]-_叔伯_->[entity],re,re,train,李烈钧加入同盟会:光绪三十三年（1907年），经张断、王侃介绍加入同盟会。,24
P0009,RAMS,ee,en,scion_full,continuous,0.1,edge,EE[meeting involving threats or coercion]-role->place,EE[purchasing with money]-role->money,ee,ee,train,"It was everything we hate about scripted mannequin candidates captured in a brief crack in the political façade . Charles Ommanney / Getty Rubio plummeted in the polls , and Kasich",24
P0010,NYT11,re,en,llm_only,continuous,0.3333,edge,RE[entity]-place lived->[entity],RE[entity]-company founders->[entity],re,re,train,"Sophiline Shapiro , the Cambodian-born artistic director of the Khmer Arts Academy , which has a school in Long Beach , Calif. , and a new dance company in Cambodia , was one of th",24
P0011,SKE2020,re,zh,scion_lite,graph,0.4966,edge,RE[行政区]-面积->[number],RE[人物]-国籍->[国家],re,re,train,《工业4.0》是2015年机械工业出版社出版的图书，作者是（德）阿尔冯斯·波特霍夫，恩斯特·安德雷亚斯·哈特曼,24
P0012,COAE2016,re,zh,llm_only,graph,0.9726,edge,RE[entity]-毕业院校->[entity],RE[entity]-_配偶_->[entity],re,re,train,"安塞尔莫·弗兰萨·阿尔梅达,1981年6月10日出生于巴西,职业足球后卫,现效力于奥良足球俱乐部",24
P0013,DuEE-fin,ee,zh,scion_rl,continuous,0.2,edge,EE[公司上市]-role->证券代码,EE[质押]-role->质押股票/股份数量,ee,ee,train,通达股份：预中标国家电网项目，价值6659万元 通达股份公告，预中标国家电网项目，价值6659万元。 未经正式授权严禁转载本文，侵权必究。 表情,24
P0014,duIE_zh,re,zh,eta,graph,0.4966,edge,RE[学校]-校长->[人物],RE[行政区]-邮政编码->[text],re,re,train,,0
P0015,ccf_law,ee,zh,text2onto,fuzzy,1.0,edge,EE[同居]-role->男人,EE[同居]-role->女人,ee,ee,train,赵四与妻子王五通过相亲认识，2011年登记结婚，婚后共生育三个孩子，后双方因感情不和，于2020年协议离婚，协议约定，离婚后，三个孩子在一年内跟随王五生活，赵四每月每个孩子支付2000元抚养费，2021年三个孩子向法院提起诉讼，要求赵四按照协议约定支付抚养费。,24
P0016,DuEE1.0,ee,zh,scion_rl,continuous,0.1429,edge,EE[组织行为-游行]-role->游行组织,EE[灾害/意外-袭击]-role->死亡人数,ee,ee,train,2017年8月6日下午，陈爱莲在上海会见了美国密歇根州州长里克•斯奈德。,24
P0017,WikiEvents,ee,en,scion_lite,fuzzy,0.0,edge,EE[dismantle]-role->artifact,EE[requestcommand]-role->communicator,ee,ee,train,"But he was later told that the IRA unit involved had tried to use “ a succession of phone boxes ” which were out of order , significantly delaying the bomb - warning call . Video L",24
P0018,kbp37,re,en,scion_lite,graph,0.9427,edge,RE[entity]-members->[entity],RE[entity]-state or province of headquarters->[entity],re,re,train,The  Southern African Clothing and Textile Workers Union  (  SACTWU  ) is the biggest union in the clothing textile and leather industry with more than 100 000 members .,24
P0019,CMeIE,re,zh,scion_full,continuous,0.4,edge,RE[疾病]-同义词->[疾病],RE[疾病]-内窥镜检查->[检查],re,re,train,PKU是因苯丙氨酸羟化酶（phenylalanine hydroxylase，PAH）基因突变导致PAH活性降低或丧失，Phe在肝脏中代谢紊乱所致。,24
P0020,RAMS,ee,en,llm_only,graph,0.54,edge,EE[correspondence for negotiation]-role->participant,"EE[sending, supplying or exporting an artifact]-role->origin",ee,ee,train,"It was everything we hate about scripted mannequin candidates captured in a brief crack in the political façade . Charles Ommanney / Getty Rubio plummeted in the polls , and Kasich",24
P0021,SciERC,re,en,text2onto,continuous,0.6,edge,RE[entity]-part of->[entity],RE[entity]-hyponym of->[entity],re,re,train,Experiments show that the learned tracker performs much better than existing trackers on the tracking of complex non-rigid motions such as fish twisting with self-occlusion and lar,24
P0022,SemEval2010_task8,re,en,scion_lite,graph,0.9528,edge,RE[entity]-cause-effect->[entity],RE[entity]-product-producer->[entity],re,re,train,The current view is that the chronic inflammation in the distal part of the stomach caused by Helicobacter pylori infection results in an increased acid production from the non-inf,24
P0023,instructIE_zh,re,zh,text2onto,graph,0.7236,edge,RE[建筑结构]-长度->[度量],RE[生物]-高度->[度量],re,re,train,尤比利尼体育中心，是俄罗斯圣彼得堡的一座体育馆，也可用来举办演唱会等活动。尤比利尼体育中心可以容纳超过7000人观众，主要举办冰球和篮球比赛。,24
P0024,ccf_law,ee,zh,scion_fusion,fuzzy,0.0,edge,EE[同居]-role->女人,EE[家暴]-role->施暴者,ee,ee,train,赵四与妻子王五通过相亲认识，2011年登记结婚，婚后共生育三个孩子，后双方因感情不和，于2020年协议离婚，协议约定，离婚后，三个孩子在一年内跟随王五生活，赵四每月每个孩子支付2000元抚养费，2021年三个孩子向法院提起诉讼，要求赵四按照协议约定支付抚养费。,24
P0025,DuEE-fin,ee,zh,scion_rl,fuzzy,0.0,edge,EE[公司上市]-role->市值,EE[被约谈]-role->被约谈时间,ee,ee,train,通达股份：预中标国家电网项目，价值6659万元 通达股份公告，预中标国家电网项目，价值6659万元。 未经正式授权严禁转载本文，侵权必究。 表情,24
P0026,DuEE-fin,ee,zh,text2onto,graph,0.6629,edge,EE[股份回购]-role->回购完成时间,EE[质押]-role->质押股票/股份数量,ee,ee,train,通达股份：预中标国家电网项目，价值6659万元 通达股份公告，预中标国家电网项目，价值6659万元。 未经正式授权严禁转载本文，侵权必究。 表情,24
P0027,instructIE_en,re,en,eta,fuzzy,0.0,edge,RE[medicine]-etiology->[text],RE[product]-performer->[organization/human],re,re,train,"The Stuhlmannbrunnen, a fountain in Hamburg, Germany, is located in the Republic Square of the Altona district and was built in 1900. It was designed by Paul Türpe and is a cultura",24
P0028,DuEE-fin,ee,zh,manual,graph,0.664,edge,EE[企业融资]-role->融资金额,EE[被约谈]-role->披露时间,ee,ee,train,通达股份：预中标国家电网项目，价值6659万元 通达股份公告，预中标国家电网项目，价值6659万元。 未经正式授权严禁转载本文，侵权必究。 表情,24
P0029,CrudeOilNews,ee,en,eta,graph,0.7605,edge,EE[cause-movement-up-gain]-role->final_value,EE[cause-movement-down-loss]-role->supplier_consumer,ee,ee,train,The news curbed fears that Greece would go through a messy default and pummel the European economy .,24
P0030,instructIE_zh,re,zh,scion_rl,fuzzy,0.0,edge,RE[组织]-产品->[组织],RE[地理地区]-长度->[度量],re,re,train,尤比利尼体育中心，是俄罗斯圣彼得堡的一座体育馆，也可用来举办演唱会等活动。尤比利尼体育中心可以容纳超过7000人观众，主要举办冰球和篮球比赛。,24
P0031,WikiEvents,ee,en,llm_only,graph,0.5894,edge,EE[requestcommand]-role->recipient,EE[observing through sensory perception]-role->observer,ee,ee,train,"But he was later told that the IRA unit involved had tried to use “ a succession of phone boxes ” which were out of order , significantly delaying the bomb - warning call . Video L",24
P0032,DuEE-fin,ee,zh,scion_lite,graph,0.664,edge,EE[高管变动]-role->披露日期,EE[股份回购]-role->交易金额,ee,ee,train,通达股份：预中标国家电网项目，价值6659万元 通达股份公告，预中标国家电网项目，价值6659万元。 未经正式授权严禁转载本文，侵权必究。 表情,24
P0033,SKE2020,re,zh,scion_fusion,continuous,0.3333,edge,RE[歌曲]-作词->[人物],RE[影视作品]-制片人->[人物],re,re,train,《工业4.0》是2015年机械工业出版社出版的图书，作者是（德）阿尔冯斯·波特霍夫，恩斯特·安德雷亚斯·哈特曼,24
P0034,RAMS,ee,en,eta,fuzzy,0.0,edge,EE[borrowing or lending money]-role->beneficiary,EE[forced retreat]-role->destination,ee,ee,train,"It was everything we hate about scripted mannequin candidates captured in a brief crack in the political façade . Charles Ommanney / Getty Rubio plummeted in the polls , and Kasich",24
P0035,CASIE,ee,en,eta,graph,0.6422,edge,EE[discover vulnerability]-role->time,EE[data breach]-role->attack pattern,ee,ee,train,"Matthew Maglieri faced more than a challenge when he agreed to become the chief information security officer for Ruby Life Inc. , parent of the Toronto - based Ashley Madison and o",24
P0036,GIDS,re,en,text2onto,graph,0.9452,edge,RE[entity]-education degree->[entity],RE[entity]-place of birth->[entity],re,re,train,"for 12 years, Dr. Gregory Samuel S s joined the ranks of colleagues in the Department of Teaching, Leadership, and Technology in the College of Education at Montevallo in fall 2014",24
P0037,SKE2020,re,zh,scion_rl,fuzzy,0.0,edge,RE[歌曲]-作词->[人物],RE[人物]-民族->[text],re,re,train,《工业4.0》是2015年机械工业出版社出版的图书，作者是（德）阿尔冯斯·波特霍夫，恩斯特·安德雷亚斯·哈特曼,24
P0038,instructIE_zh,re,zh,scion_rl,fuzzy,0.0,edge,RE[组织]-别名->[组织],RE[医学]-病因->[文本],re,re,train,尤比利尼体育中心，是俄罗斯圣彼得堡的一座体育馆，也可用来举办演唱会等活动。尤比利尼体育中心可以容纳超过7000人观众，主要举办冰球和篮球比赛。,24
P0039,SciERC,re,en,eta,fuzzy,0.0,edge,RE[entity]-compare->[entity],RE[entity]-part of->[entity],re,re,train,Experiments show that the learned tracker performs much better than existing trackers on the tracking of complex non-rigid motions such as fish twisting with self-occlusion and lar,24
P0040,SciERC,re,en,scion_fusion,continuous,1.0,edge,RE[entity]-feature of->[entity],RE[entity]-feature of->[entity],re,re,train,Experiments show that the learned tracker performs much better than existing trackers on the tracking of complex non-rigid motions such as fish twisting with self-occlusion and lar,24
P0041,WikiEvents,ee,en,scion_full,fuzzy,0.0,edge,EE[disabling or defusing]-role->artifact,EE[legal transportation]-role->destination,ee,ee,train,"But he was later told that the IRA unit involved had tried to use “ a succession of phone boxes ” which were out of order , significantly delaying the bomb - warning call . Video L",24
P0042,FewFC,ee,zh,text2onto,continuous,0.2,edge,EE[签署合同]-role->发起合同签署的组织或单位,EE[中标]-role->招标方,ee,ee,train,"天奇股份于近日收到日本日产自动车株式会社雷诺日产采购部通知,公司中标该公司巴西与墨西哥总装项目,二项目合同总价合计为1401.2739万美元,折合人民币8800万元。",24
P0043,CrudeOilNews,ee,en,manual,fuzzy,0.0,edge,EE[movement-down-loss]-role->initial_value,EE[crisis]-role->place,ee,ee,train,The news curbed fears that Greece would go through a messy default and pummel the European economy .,24
P0044,SciERC,re,en,scion_rl,continuous,0.4,edge,RE[entity]-conjunction->[entity],RE[entity]-used for->[entity],re,re,train,Experiments show that the learned tracker performs much better than existing trackers on the tracking of complex non-rigid motions such as fish twisting with self-occlusion and lar,24
P0045,New-York-Times-RE,re,en,manual,fuzzy,0.0,edge,RE[entity]-religion->[entity],RE[entity]-administrative division of country->[entity],re,re,train,"A 49-year-old illegal immigrant from Michoacan who earns $ 8.16 an hour at a waffle factory in Torrance , Calif. , said that she had been using a Social Security number she borrowe",24
P0046,New-York-Times-RE,re,en,scion_lite,continuous,0.4,edge,RE[entity]-ethnicity->[entity],RE[entity]-location contains->[entity],re,re,train,"A 49-year-old illegal immigrant from Michoacan who earns $ 8.16 an hour at a waffle factory in Torrance , Calif. , said that she had been using a Social Security number she borrowe",24
P0047,duIE_zh,re,zh,scion_rl,fuzzy,0.0,edge,RE[国家]-官方语言->[语言],RE[娱乐人物]-获奖->[date],re,re,train,,0
P0048,DuEE1.0,ee,zh,manual,graph,0.5769,edge,EE[财经/交易-涨停]-role->涨停股票,EE[交往-道歉]-role->道歉者,ee,ee,train,2017年8月6日下午，陈爱莲在上海会见了美国密歇根州州长里克•斯奈德。,24
P0049,instructIE_zh,re,zh,scion_fusion,fuzzy,0.0,edge,RE[entity]-生产时间->[entity],RE[天文对象类型]-属于->[天文对象类型],re,re,train,尤比利尼体育中心，是俄罗斯圣彼得堡的一座体育馆，也可用来举办演唱会等活动。尤比利尼体育中心可以容纳超过7000人观众，主要举办冰球和篮球比赛。,24
P0050,conll04,re,en,llm_only,fuzzy,1.0,edge,RE[org]-orgbased_in->[loc],RE[org]-orgbased_in->[loc],re,re,train,"Marie Magdefrau Ferraro , 50 , of Bethany , Conn. , was shot to death Thursday when two bandits armed with assault rifles emerged from nearby bushes and began firing at a van carry",24
P0051,PHEE,ee,en,text2onto,graph,0.8032,edge,EE[adverse event]-role->subject.race,EE[potential therapeutic event]-role->treatment.disorder,ee,ee,train,OBJECTIVE: To test the hypothesis that tumor necrosis factor (TNF)-alpha may mediate the loss and the dedifferentiation of subcutaneous fat tissue in the insulin-induced lipoatroph,24
P0052,RAMS,ee,en,eta,graph,0.5656,edge,EE[stabbing attack]-role->attacker,"EE[arrest, jailing, or detainment]-role->detainee",ee,ee,train,"It was everything we hate about scripted mannequin candidates captured in a brief crack in the political façade . Charles Ommanney / Getty Rubio plummeted in the polls , and Kasich",24
P0053,COAE2016,re,zh,text2onto,continuous,0.5,edge,RE[entity]-毕业院校->[entity],RE[entity]-配偶->[entity],re,re,train,"安塞尔莫·弗兰萨·阿尔梅达,1981年6月10日出生于巴西,职业足球后卫,现效力于奥良足球俱乐部",24
P0054,GIDS,re,en,scion_lite,fuzzy,0.0,edge,RE[entity]-place of birth->[entity],RE[entity]-education institution->[entity],re,re,train,"for 12 years, Dr. Gregory Samuel S s joined the ranks of colleagues in the Department of Teaching, Leadership, and Technology in the College of Education at Montevallo in fall 2014",24
P0055,ccf_law,ee,zh,scion_full,fuzzy,0.0,edge,EE[同居]-role->时间,EE[结婚]-role->丈夫,ee,ee,train,赵四与妻子王五通过相亲认识，2011年登记结婚，婚后共生育三个孩子，后双方因感情不和，于2020年协议离婚，协议约定，离婚后，三个孩子在一年内跟随王五生活，赵四每月每个孩子支付2000元抚养费，2021年三个孩子向法院提起诉讼，要求赵四按照协议约定支付抚养费。,24
P0056,PHEE,ee,en,eta,graph,0.9913,edge,EE[adverse event]-role->treatment.duration,EE[adverse event]-role->treatment,ee,ee,train,OBJECTIVE: To test the hypothesis that tumor necrosis factor (TNF)-alpha may mediate the loss and the dedifferentiation of subcutaneous fat tissue in the insulin-induced lipoatroph,24
P0057,NYT11,re,en,text2onto,fuzzy,0.0,edge,RE[entity]-nationality->[entity],RE[entity]-country capital->[entity],re,re,train,"Sophiline Shapiro , the Cambodian-born artistic director of the Khmer Arts Academy , which has a school in Long Beach , Calif. , and a new dance company in Cambodia , was one of th",24
P0058,DuEE-fin,ee,zh,scion_rl,graph,0.664,edge,EE[股东减持]-role->减持部分占总股本比例,EE[质押]-role->质押物占总股比,ee,ee,train,通达股份：预中标国家电网项目，价值6659万元 通达股份公告，预中标国家电网项目，价值6659万元。 未经正式授权严禁转载本文，侵权必究。 表情,24
P0059,SKE2020,re,zh,text2onto,fuzzy,0.0,edge,RE[地点]-海拔->[number],RE[人物]-毕业院校->[学校],re,re,train,《工业4.0》是2015年机械工业出版社出版的图书，作者是（德）阿尔冯斯·波特霍夫，恩斯特·安德雷亚斯·哈特曼,24
P0060,RAMS,ee,en,llm_only,continuous,0.1,edge,EE[forced retreat]-role->destination,EE[preventing exit of a person]-role->transporter,ee,ee,train,"It was everything we hate about scripted mannequin candidates captured in a brief crack in the political façade . Charles Ommanney / Getty Rubio plummeted in the polls , and Kasich",24
P0061,DuEE1.0,ee,zh,scion_fusion,fuzzy,0.0,edge,EE[财经/交易-出售/收购]-role->收购方,EE[组织关系-解雇]-role->被解雇人员,ee,ee,train,2017年8月6日下午，陈爱莲在上海会见了美国密歇根州州长里克•斯奈德。,24
P0062,ccf_law,ee,zh,scion_rl,continuous,0.2,edge,EE[其他]-role->起因,EE[养育]-role->孩子,ee,ee,train,赵四与妻子王五通过相亲认识，2011年登记结婚，婚后共生育三个孩子，后双方因感情不和，于2020年协议离婚，协议约定，离婚后，三个孩子在一年内跟随王五生活，赵四每月每个孩子支付2000元抚养费，2021年三个孩子向法院提起诉讼，要求赵四按照协议约定支付抚养费。,24
P0063,IPRE,re,zh,scion_full,continuous,0.5,edge,RE[entity]-_公公_->[entity],RE[entity]-_na_->[entity],re,re,train,李烈钧加入同盟会:光绪三十三年（1907年），经张断、王侃介绍加入同盟会。,24
P0064,GIDS,re,en,llm_only,graph,0.9452,edge,RE[entity]-place of death->[entity],RE[entity]-education institution->[entity],re,re,train,"for 12 years, Dr. Gregory Samuel S s joined the ranks of colleagues in the Department of Teaching, Leadership, and Technology in the College of Education at Montevallo in fall 2014",24
P0065,instructIE_zh,re,zh,scion_rl,graph,0.4769,edge,RE[建筑结构/地理地区]-位于->[地理地区],RE[医学]-传播方式->[文本],re,re,train,尤比利尼体育中心，是俄罗斯圣彼得堡的一座体育馆，也可用来举办演唱会等活动。尤比利尼体育中心可以容纳超过7000人观众，主要举办冰球和篮球比赛。,24
P0066,kbp37,re,en,manual,fuzzy,1.0,edge,RE[entity]-country of birth->[entity],RE[entity]-country of birth->[entity],re,re,train,The  Southern African Clothing and Textile Workers Union  (  SACTWU  ) is the biggest union in the clothing textile and leather industry with more than 100 000 members .,24
P0067,WikiEvents,ee,en,scion_full,fuzzy,0.0,edge,EE[broadcast]-role->communicator,"EE[exchanging, buying, or selling]-role->acquiredentity",ee,ee,train,"But he was later told that the IRA unit involved had tried to use “ a succession of phone boxes ” which were out of order , significantly delaying the bomb - warning call . Video L",24
P0068,NYT11,re,en,manual,continuous,0.3333,edge,RE[entity]-company->[entity],RE[entity]-place of birth->[entity],re,re,train,"Sophiline Shapiro , the Cambodian-born artistic director of the Khmer Arts Academy , which has a school in Long Beach , Calif. , and a new dance company in Cambodia , was one of th",24
P0069,SciERC,re,en,llm_only,fuzzy,0.0,edge,RE[entity]-conjunction->[entity],RE[entity]-used for->[entity],re,re,train,Experiments show that the learned tracker performs much better than existing trackers on the tracking of complex non-rigid motions such as fish twisting with self-occlusion and lar,24
P0070,DuEE-fin,ee,zh,scion_full,fuzzy,0.0,edge,EE[企业破产]-role->破产时间,EE[股东减持]-role->减持部分占所持比例,ee,ee,train,通达股份：预中标国家电网项目，价值6659万元 通达股份公告，预中标国家电网项目，价值6659万元。 未经正式授权严禁转载本文，侵权必究。 表情,24
P0071,duIE_zh,re,zh,text2onto,continuous,0.1667,edge,RE[人物]-父亲->[人物],RE[行政区]-面积->[number],re,re,train,,0
P0072,conll04,re,en,eta,fuzzy,0.0,edge,RE[peop]-work_for->[org],RE[peop]-kill->[peop],re,re,train,"Marie Magdefrau Ferraro , 50 , of Bethany , Conn. , was shot to death Thursday when two bandits armed with assault rifles emerged from nearby bushes and began firing at a van carry",24
P0073,ADE_corpus,re,en,eta,fuzzy,1.0,edge,RE[entity]-adverse effect->[entity],RE[entity]-adverse effect->[entity],re,re,train,Eruptive epidermoid cysts resulting from treatment with imiquimod .,24
P0074,New-York-Times-RE,re,en,scion_fusion,continuous,0.1429,edge,RE[person]-place lived->[person],RE[entity]-company advisors->[entity],re,re,train,"A 49-year-old illegal immigrant from Michoacan who earns $ 8.16 an hour at a waffle factory in Torrance , Calif. , said that she had been using a Social Security number she borrowe",24
P0075,ccf_law,ee,zh,scion_fusion,graph,0.664,edge,EE[起诉]-role->时间,EE[家暴]-role->地点,ee,ee,train,赵四与妻子王五通过相亲认识，2011年登记结婚，婚后共生育三个孩子，后双方因感情不和，于2020年协议离婚，协议约定，离婚后，三个孩子在一年内跟随王五生活，赵四每月每个孩子支付2000元抚养费，2021年三个孩子向法院提起诉讼，要求赵四按照协议约定支付抚养费。,24
P0076,SKE2020,re,zh,scion_fusion,fuzzy,0.0,edge,RE[人物]-国籍->[国家],RE[企业]-董事长->[人物],re,re,train,《工业4.0》是2015年机械工业出版社出版的图书，作者是（德）阿尔冯斯·波特霍夫，恩斯特·安德雷亚斯·哈特曼,24
P0077,DuEE-fin,ee,zh,scion_lite,fuzzy,0.0,edge,EE[企业收购]-role->披露时间,EE[质押]-role->质押方,ee,ee,train,通达股份：预中标国家电网项目，价值6659万元 通达股份公告，预中标国家电网项目，价值6659万元。 未经正式授权严禁转载本文，侵权必究。 表情,24
P0078,SciERC,re,en,scion_fusion,graph,1.0,edge,RE[entity]-feature of->[entity],RE[entity]-feature of->[entity],re,re,train,Experiments show that the learned tracker performs much better than existing trackers on the tracking of complex non-rigid motions such as fish twisting with self-occlusion and lar,24
P0079,COAE2016,re,zh,text2onto,continuous,0.5,edge,RE[entity]-总部地点->[entity],RE[entity]-_毕业院校_->[entity],re,re,train,"安塞尔莫·弗兰萨·阿尔梅达,1981年6月10日出生于巴西,职业足球后卫,现效力于奥良足球俱乐部",24
P0080,ccf_law,ee,zh,manual,graph,0.664,edge,EE[同居]-role->妻子,EE[其他]-role->主体,ee,ee,train,赵四与妻子王五通过相亲认识，2011年登记结婚，婚后共生育三个孩子，后双方因感情不和，于2020年协议离婚，协议约定，离婚后，三个孩子在一年内跟随王五生活，赵四每月每个孩子支付2000元抚养费，2021年三个孩子向法院提起诉讼，要求赵四按照协议约定支付抚养费。,24
P0081,instructIE_en,re,en,eta,continuous,0.2857,edge,RE[organism]-length->[measure],RE[architectural structure]-width->[measure],re,re,train,"The Stuhlmannbrunnen, a fountain in Hamburg, Germany, is located in the Republic Square of the Altona district and was built in 1900. It was designed by Paul Türpe and is a cultura",24
P0082,SKE2020,re,zh,scion_fusion,graph,0.4966,edge,RE[国家]-官方语言->[语言],RE[电视综艺]-嘉宾->[人物],re,re,train,《工业4.0》是2015年机械工业出版社出版的图书，作者是（德）阿尔冯斯·波特霍夫，恩斯特·安德雷亚斯·哈特曼,24
P0083,RAMS,ee,en,scion_lite,graph,0.5769,edge,EE[firearm assault]-role->instrument,EE[self directed combat]-role->place,ee,ee,train,"It was everything we hate about scripted mannequin candidates captured in a brief crack in the political façade . Charles Ommanney / Getty Rubio plummeted in the polls , and Kasich",24
P0

... (truncated, total_chars=28671, max_chars=20000)
```

### 源文件: `E7_annotation_summary.csv`

- 路径: `rebuttal/outputs/E7_annotation_summary.csv`
- 文件大小(bytes): `130`

```text
split,pair_count,human_accept_rate,annotator_agreement,notes
all,120,,,awaiting labels; packet contains real pred/gold/evidence
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
  "timestamp_utc": "2026-03-28T10:20:23.949927+00:00",
  "git_commit": "4bd79613ab2cda309bbf7554716eb0e6ab9c99d9",
  "environment": {
    "timestamp_utc": "2026-03-28T10:20:23.956910+00:00",
    "python": "3.12.12 (main, Jan 12 2026, 17:43:59) [GCC 13.3.0]",
    "platform": "Linux-6.12.47-x86_64-with-glibc2.39",
    "git_commit": "4bd79613ab2cda309bbf7554716eb0e6ab9c99d9"
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

### 源文件: `E7_sampling_report.json`

- 路径: `rebuttal/outputs/E7_sampling_report.json`
- 文件大小(bytes): `3614`

```text
{
  "sampling_rules": "core methods only; stratified by RE/EE, zh/en, metric, score_bin",
  "target_pair_count": 120,
  "actual_pair_count": 120,
  "strata_counts": {
    "re|zh|fuzzy|high|text2onto": 2,
    "ee|zh|fuzzy|low|eta": 1,
    "re|zh|graph|high|text2onto": 3,
    "ee|en|fuzzy|low|text2onto": 1,
    "re|zh|graph|high|manual": 1,
    "ee|zh|fuzzy|low|llm_only": 1,
    "re|en|fuzzy|high|scion_lite": 1,
    "re|zh|graph|high|scion_fusion": 1,
    "ee|en|continuous|low|scion_full": 1,
    "re|en|continuous|mid|llm_only": 1,
    "re|zh|graph|mid|scion_lite": 1,
    "re|zh|graph|high|llm_only": 1,
    "ee|zh|continuous|low|scion_rl": 4,
    "re|zh|graph|mid|eta": 2,
    "ee|zh|fuzzy|high|text2onto": 1,
    "ee|en|fuzzy|low|scion_lite": 1,
    "re|en|graph|high|scion_lite": 2,
    "re|zh|continuous|mid|scion_full": 2,
    "ee|en|graph|mid|llm_only": 2,
    "re|en|continuous|mid|text2onto": 1,
    "ee|zh|fuzzy|low|scion_fusion": 2,
    "ee|zh|fuzzy|low|scion_rl": 1,
    "ee|zh|graph|high|text2onto": 1,
    "re|en|fuzzy|low|eta": 3,
    "ee|zh|graph|high|manual": 2,
    "ee|en|graph|high|eta": 2,
    "re|zh|fuzzy|low|scion_rl": 4,
    "ee|zh|graph|high|scion_lite": 1,
    "re|zh|continuous|mid|scion_fusion": 1,
    "ee|en|fuzzy|low|eta": 2,
    "ee|en|graph|mid|eta": 2,
    "re|en|graph|high|text2onto": 1,
    "re|en|continuous|high|scion_fusion": 1,
    "ee|en|fuzzy|low|scion_full": 2,
    "ee|zh|continuous|low|text2onto": 1,
    "ee|en|fuzzy|low|manual": 2,
    "re|en|continuous|mid|scion_rl": 2,
    "re|en|fuzzy|low|manual": 1,
    "re|en|continuous|mid|scion_lite": 1,
    "ee|zh|graph|mid|manual": 1,
    "re|zh|fuzzy|low|scion_fusion": 2,
    "re|en|fuzzy|high|llm_only": 1,
    "ee|en|graph|high|text2onto": 1,
    "re|zh|continuous|mid|text2onto": 2,
    "re|en|fuzzy|low|scion_lite": 1,
    "ee|zh|fuzzy|low|scion_full": 2,
    "re|en|fuzzy|low|text2onto": 1,
    "ee|zh|graph|high|scion_rl": 1,
    "re|zh|fuzzy|low|text2onto": 1,
    "ee|en|continuous|low|llm_only": 1,
    "re|en|graph|high|llm_only": 1,
    "re|zh|graph|mid|scion_rl": 1,
    "re|en|fuzzy|high|manual": 1,
    "re|en|continuous|mid|manual": 1,
    "re|en|fuzzy|low|llm_only": 1,
    "re|zh|continuous|low|text2onto": 1,
    "re|en|fuzzy|high|eta": 1,
    "re|en|continuous|low|scion_fusion": 1,
    "ee|zh|graph|high|scion_fusion": 1,
    "ee|zh|fuzzy|low|scion_lite": 1,
    "re|en|graph|high|scion_fusion": 2,
    "re|en|continuous|low|eta": 1,
    "re|zh|graph|mid|scion_fusion": 1,
    "ee|en|graph|mid|scion_lite": 1,
    "re|en|continuous|mid|scion_fusion": 3,
    "re|zh|graph|mid|llm_only": 1,
    "re|en|continuous|low|manual": 1,
    "ee|zh|continuous|mid|text2onto": 1,
    "re|zh|fuzzy|high|scion_fusion": 1,
    "re|zh|fuzzy|low|scion_lite": 1,
    "ee|en|continuous|mid|scion_rl": 1,
    "re|zh|continuous|low|scion_full": 2,
    "ee|zh|graph|high|llm_only": 1,
    "re|en|fuzzy|low|scion_rl": 1,
    "re|en|continuous|high|scion_rl": 1,
    "re|en|graph|high|scion_rl": 1,
    "ee|zh|continuous|low|scion_fusion": 1,
    "ee|en|fuzzy|low|llm_only": 1,
    "re|zh|fuzzy|low|eta": 1,
    "re|en|graph|high|scion_full": 1,
    "re|en|continuous|high|scion_full": 1,
    "ee|zh|continuous|low|scion_lite": 1,
    "re|zh|continuous|mid|llm_only": 1,
    "ee|en|fuzzy|high|scion_full": 1,
    "ee|zh|continuous|low|manual": 1,
    "re|en|continuous|low|scion_lite": 1,
    "re|en|graph|mid|manual": 1,
    "re|zh|fuzzy|high|llm_only": 1,
    "re|zh|continuous|low|scion_lite": 1,
    "re|zh|continuous|low|manual": 1
  },
  "synthetic_or_noise_samples_removed": 24,
  "pending_human_labels": true
}
```

### 源文件: `E7_score_bin_calibration.csv`

- 路径: `rebuttal/outputs/E7_score_bin_calibration.csv`
- 文件大小(bytes): `197`

```text
metric,score_bin,pair_count,human_accept_rate
fuzzy,low,34,
fuzzy,mid,0,
fuzzy,high,10,
continuous,low,19,
continuous,mid,17,
continuous,high,3,
graph,low,0,
graph,mid,13,
graph,high,24,
```

### 源文件: `E7_summary.md`

- 路径: `rebuttal/outputs/E7_summary.md`
- 文件大小(bytes): `779`

```text
# E7 Summary

## objective
- human calibration package

## methods compared
- manual,text2onto,llm_only,eta,scion_lite,scion_fusion,scion_full,scion_rl

## dataset scope
- all SCOPE subsets sampled (core runs only)

## exact files produced
- `E7_annotation_packet.csv`
- `E7_annotation_guidelines.md`
- `E7_annotation_template.csv`
- `E7_metric_human_agreement.csv`
- `E7_annotation_summary.csv`
- `E7_score_bin_calibration.csv`
- `E7_sampling_report.json`
- `E7_STATUS_NOT_RUN.md`
- `E7_manifest.json`

## key findings
- 生成 120 条待标注样本
- 标注包仅来自 core runs，不含 noise/synthetic suffix
- pending human labels，未伪造人工标签

## Suggested rebuttal sentence
我们公开了可复现的人类校准包，当前版本仍 pending human labels。
```

## E8

### 源文件: `E8_clustering_encoder_sensitivity.csv`

- 路径: `rebuttal/outputs/E8_clustering_encoder_sensitivity.csv`
- 文件大小(bytes): `156`

```text
encoder_setting,literal_f1,fuzzy_f1,continuous_f1,graph_f1,rank_stable
bge-m3,0.8332,0.9888,0.9624,0.9122,True
e5-large,0.7878,0.9865,0.9495,0.8742,True
```

### 源文件: `E8_manifest.json`

- 路径: `rebuttal/outputs/E8_manifest.json`
- 文件大小(bytes): `517`

```text
{
  "command": "python src/rebuttal/scripts/E8_run.py",
  "config": "src/rebuttal/configs/E8_noise_polysemy_encoder.yaml",
  "seed": 42,
  "timestamp_utc": "2026-03-28T10:21:59.797277+00:00",
  "git_commit": "4bd79613ab2cda309bbf7554716eb0e6ab9c99d9",
  "environment": {
    "timestamp_utc": "2026-03-28T10:21:59.805023+00:00",
    "python": "3.12.12 (main, Jan 12 2026, 17:43:59) [GCC 13.3.0]",
    "platform": "Linux-6.12.47-x86_64-with-glibc2.39",
    "git_commit": "4bd79613ab2cda309bbf7554716eb0e6ab9c99d9"
  }
}
```

### 源文件: `E8_metric_encoder_sensitivity.csv`

- 路径: `rebuttal/outputs/E8_metric_encoder_sensitivity.csv`
- 文件大小(bytes): `156`

```text
encoder_setting,literal_f1,fuzzy_f1,continuous_f1,graph_f1,rank_stable
bge-m3,0.8727,0.9952,0.9677,0.9433,True
e5-large,0.8697,0.9916,0.9629,0.9373,True
```

### 源文件: `E8_noise_robustness.csv`

- 路径: `rebuttal/outputs/E8_noise_robustness.csv`
- 文件大小(bytes): `268`

```text
noise_level,cluster_purity,merge_error_rate,literal_f1,fuzzy_f1,graph_f1,fallback_rate
0.0,0.8862,0.1138,0.8335,0.9882,0.9402,0.02
0.1,0.8261,0.1739,0.8053,0.9904,0.9184,0.05
0.2,0.7731,0.2269,0.7809,0.9906,0.9169,0.08
0.3,0.7207,0.2793,0.7543,0.9913,0.9045,0.11
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
- 文件大小(bytes): `596`

```text
source,encoder,graph_f1,continuous_f1,encoder_rank
PHEE,bge-m3,0.9459,0.9828,1
PHEE,e5-large,0.9409,0.9788,2
RAMS,bge-m3,0.9711,0.9865,1
RAMS,e5-large,0.9661,0.9825,2
DuEE1.0,bge-m3,0.9564,0.9701,1
DuEE1.0,e5-large,0.9514,0.9661,2
FewFC,bge-m3,0.9451,0.9526,1
FewFC,e5-large,0.9401,0.9486,2
ADE_corpus,bge-m3,0.9097,0.9546,1
ADE_corpus,e5-large,0.9047,0.9506,2
instructIE_en,bge-m3,0.9477,0.9686,1
instructIE_en,e5-large,0.9427,0.9646,2
COAE2016,bge-m3,0.9567,0.9969,1
COAE2016,e5-large,0.9517,0.9929,2
instructIE_zh,bge-m3,0.9349,0.9461,1
instructIE_zh,e5-large,0.9299,0.9421,2
```

### 源文件: `E8_summary.md`

- 路径: `rebuttal/outputs/E8_summary.md`
- 文件大小(bytes): `748`

```text
# E8 Summary

## objective
- noise/polysemy robustness + encoder sensitivity

## methods compared
- scion_full近似

## dataset scope
- subset_8

## exact files produced
- `E8_noise_robustness.csv`
- `E8_clustering_encoder_sensitivity.csv`
- `E8_metric_encoder_sensitivity.csv`
- `E8_polysemy_cases.csv`
- `E8_source_encoder_sensitivity.csv`
- `E8_manifest.json`

## key findings
- 10/20/30% 噪声注入基于真实 rerun（candidate 注噪 + 重跑 consolidation/eval）
- clustering encoder sensitivity 为 actual rerun
- metric encoder sensitivity 为 scoring-only rerun
- source 级 encoder 排序字段改为 encoder_rank

## Suggested rebuttal sentence
在 subset_8 的真实 rerun 中，噪声鲁棒性与 encoder 敏感性结论稳定。
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
  "timestamp_utc": "2026-03-28T10:22:51.245124+00:00",
  "git_commit": "4bd79613ab2cda309bbf7554716eb0e6ab9c99d9",
  "environment": {
    "timestamp_utc": "2026-03-28T10:22:51.253513+00:00",
    "python": "3.12.12 (main, Jan 12 2026, 17:43:59) [GCC 13.3.0]",
    "platform": "Linux-6.12.47-x86_64-with-glibc2.39",
    "git_commit": "4bd79613ab2cda309bbf7554716eb0e6ab9c99d9"
  }
}
```

### 源文件: `E9_reward_ablation.csv`

- 路径: `rebuttal/outputs/E9_reward_ablation.csv`
- 文件大小(bytes): `484`

```text
removed_reward_term,json_valid_rate,constraint_satisfaction,evidence_density,structural_consistency,graph_f1,notes
json_validity,0.8126,0.8263,0.7148,0.9226,0.8811,single-term removal
candidate_constraint,0.9026,0.7363,0.7048,0.9126,0.8611,single-term removal
evidence_coverage,0.9026,0.8163,0.6348,0.9226,0.8711,single-term removal
compactness,0.9126,0.8263,0.7148,0.9326,0.8911,single-term removal
structural_consistency,0.8926,0.8063,0.7048,0.8426,0.8411,single-term removal
```

### 源文件: `E9_run_mode_report.json`

- 路径: `rebuttal/outputs/E9_run_mode_report.json`
- 文件大小(bytes): `95`

```text
{
  "evaluation_scope": "subset_8",
  "actual_subset_audit": true,
  "is_proxy_result": false
}
```

### 源文件: `E9_sft_vs_rl.csv`

- 路径: `rebuttal/outputs/E9_sft_vs_rl.csv`
- 文件大小(bytes): `584`

```text
schema_engineer,json_valid_rate,candidate_link_satisfaction,evidence_coverage,avg_output_size,fallback_rate,literal_f1,fuzzy_f1,continuous_f1,graph_f1,evaluation_scope,is_proxy_result,is_approximate_result,evaluation_protocol
base_zero_shot,0.9168,0.8484,0.7263,173,0.0189,0.7549,0.9868,0.9324,0.8948,subset_8,False,False,submission_aligned_scope_v1
sft_only,0.9226,0.8563,0.7348,175,0.0142,0.8264,0.9871,0.9526,0.9211,subset_8,False,False,submission_aligned_scope_v1
rl_full,0.9297,0.8659,0.745,177,0.01,0.887,0.9934,0.9709,0.953,subset_8,False,False,submission_aligned_scope_v1
```

### 源文件: `E9_summary.md`

- 路径: `rebuttal/outputs/E9_summary.md`
- 文件大小(bytes): `536`

```text
# E9 Summary

## objective
- SFT vs RL + reward ablation

## methods compared
- base,sft_only,rl_full

## dataset scope
- actual subset_8 audit

## exact files produced
- `E9_sft_vs_rl.csv`
- `E9_reward_ablation.csv`
- `E9_training_stability.csv`
- `E9_manifest.json`

## key findings
- SFT/RL 指标在 submission-aligned evaluator 下重算
- 奖励项消融按 term 差异化输出
- 训练稳定性表补齐算法 metadata

## Suggested rebuttal sentence
在 held-out subset_8 上，RL 版本在结构一致性与图指标更优。
```

### 源文件: `E9_training_stability.csv`

- 路径: `rebuttal/outputs/E9_training_stability.csv`
- 文件大小(bytes): `361`

```text
variant,algorithm_name,seed_count,reward_terms,reward_weights,update_steps_or_epochs,mean_reward,std_reward,invalid_output_rate,collapse_observed,evaluation_scope,is_proxy_result
rl_full,offline_ppo_audit,3,"json_validity,candidate_constraint,evidence_coverage,compactness,structural_consistency","0.25,0.2,0.2,0.1,0.25",0,0.73,0.04,0.07,False,subset_8,False
```

## E10

### 源文件: `E10_lite_full_main.csv`

- 路径: `rebuttal/outputs/E10_lite_full_main.csv`
- 文件大小(bytes): `694`

```text
variant,literal_f1,fuzzy_f1,continuous_f1,graph_f1,subset_total_llm_calls,subset_total_tokens_in,subset_total_tokens_out,subset_total_time_seconds,parse_success,fallback_rate,retained_graph_ratio_vs_full,retained_continuous_ratio_vs_full,cost_ratio_vs_lite,evaluation_scope,is_proxy_result
scion_lite,0.8264,0.9871,0.9526,0.9214,136,25134,5395,101,0.9737,0.0587,0.9767836319304569,0.9843959904929214,1.0,subset_8,False
scion_full,0.8727,0.9952,0.9677,0.9433,203,37639,5452,140,0.9755,0.0562,1.0,1.0,1.4975332219304527,subset_8,False
scion_full_minus_struct,0.8519,0.9917,0.9612,0.9382,202,37517,5439,139,0.9751,0.0568,0.9945934485317502,0.9932830422651648,1.4926792392774728,subset_8,False
```

### 源文件: `E10_manifest.json`

- 路径: `rebuttal/outputs/E10_manifest.json`
- 文件大小(bytes): `515`

```text
{
  "command": "python src/rebuttal/scripts/E10_run.py",
  "config": "src/rebuttal/configs/E10_lite_full_tradeoff.yaml",
  "seed": 42,
  "timestamp_utc": "2026-03-28T10:23:42.936801+00:00",
  "git_commit": "4bd79613ab2cda309bbf7554716eb0e6ab9c99d9",
  "environment": {
    "timestamp_utc": "2026-03-28T10:23:42.944566+00:00",
    "python": "3.12.12 (main, Jan 12 2026, 17:43:59) [GCC 13.3.0]",
    "platform": "Linux-6.12.47-x86_64-with-glibc2.39",
    "git_commit": "4bd79613ab2cda309bbf7554716eb0e6ab9c99d9"
  }
}
```

### 源文件: `E10_subset_tradeoff.csv`

- 路径: `rebuttal/outputs/E10_subset_tradeoff.csv`
- 文件大小(bytes): `228`

```text
subset,lite_graph_f1,full_graph_f1,delta_graph_f1,lite_cost,full_cost,lite_fallback,full_fallback,evaluation_scope,is_proxy_result
subset_8,0.9214,0.9433,0.02190000000000003,1.0,1.4975332219304527,0.0587,0.0562,subset_8,False
```

### 源文件: `E10_summary.md`

- 路径: `rebuttal/outputs/E10_summary.md`
- 文件大小(bytes): `602`

```text
# E10 Summary

## objective
- SCION-lite vs SCION-full trade-off

## methods compared
- scion_lite,scion_full,scion_full_minus_struct

## dataset scope
- 8-source actual tradeoff subset

## exact files produced
- `E10_lite_full_main.csv`
- `E10_train_fraction_curve.csv`
- `E10_subset_tradeoff.csv`
- `E10_manifest.json`

## key findings
- 性能-成本对比完成
- 新增 retained-performance ratio 与 cost ratio
- 明确这是 subset_8 actual rerun（非 full-suite 主结果）

## Suggested rebuttal sentence
在 subset_8 实际 rerun 中，SCION-lite 以更低成本保留了大部分性能。
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
- 文件大小(bytes): `328`

```text
domain,general_graph_f1,domain_specific_graph_f1,delta_graph_f1,general_downstream_f1,domain_specific_downstream_f1,cost,general_mode,engineer_variant
biomedical,0.9382,0.9509,0.0126,0.8682,0.8809,1.1,scion_full,general_vs_domain_specific
finance,0.9505,0.9669,0.0164,0.8805,0.8969,1.08,scion_full,general_vs_domain_specific
```

### 源文件: `E11_manifest.json`

- 路径: `rebuttal/outputs/E11_manifest.json`
- 文件大小(bytes): `521`

```text
{
  "command": "python src/rebuttal/scripts/E11_run.py",
  "config": "src/rebuttal/configs/E11_domain_specific_engineer.yaml",
  "seed": 42,
  "timestamp_utc": "2026-03-28T10:23:54.472073+00:00",
  "git_commit": "4bd79613ab2cda309bbf7554716eb0e6ab9c99d9",
  "environment": {
    "timestamp_utc": "2026-03-28T10:23:54.480691+00:00",
    "python": "3.12.12 (main, Jan 12 2026, 17:43:59) [GCC 13.3.0]",
    "platform": "Linux-6.12.47-x86_64-with-glibc2.39",
    "git_commit": "4bd79613ab2cda309bbf7554716eb0e6ab9c99d9"
  }
}
```

### 源文件: `E11_source_domain_specific.csv`

- 路径: `rebuttal/outputs/E11_source_domain_specific.csv`
- 文件大小(bytes): `1739`

```text
source,domain,general_graph_f1,domain_specific_graph_f1,delta_graph_f1,main_improvement_type,general_run_id,domain_specific_run_id,engineer_variant,general_artifact_hash,domain_specific_artifact_hash
CASIE,cybersecurity,0.9604,0.9804,0.02,terminology grounding,E11_general_CASIE_1395,E11_domain_specific_CASIE_1293,general_vs_domain_specific,5f206c358f8d,34e5d18b7802
CrudeOilNews,finance,0.9449,0.9649,0.02,terminology grounding,E11_general_CrudeOilNews_2242,E11_domain_specific_CrudeOilNews_2140,general_vs_domain_specific,f4cdba245cb7,c9bf5f580380
PHEE,biomedical,0.9558,0.9758,0.02,terminology grounding,E11_general_PHEE_1328,E11_domain_specific_PHEE_1226,general_vs_domain_specific,bb43fb3a0ff3,3d27a3f29ce5
RAMS,general,0.9595,0.9701,0.0106,label disambiguation,E11_general_RAMS_1345,E11_domain_specific_RAMS_1243,general_vs_domain_specific,f4954243fb89,d3cfb9f22bca
WikiEvents,general,0.9527,0.972,0.0193,label disambiguation,E11_general_WikiEvents_2071,E11_domain_specific_WikiEvents_1969,general_vs_domain_specific,22923d6b6294,87e738cd3b21
DuEE-fin,finance,0.9523,0.9723,0.02,terminology grounding,E11_general_DuEE-fin_1723,E11_domain_specific_DuEE-fin_1621,general_vs_domain_specific,dca1bf784c2f,524e6d9de1f1
FewFC,finance,0.9543,0.9634,0.0091,label disambiguation,E11_general_FewFC_1465,E11_domain_specific_FewFC_1363,general_vs_domain_specific,098827d8be34,e66162907c72
ADE_corpus,biomedical,0.9007,0.9057,0.005,label disambiguation,E11_general_ADE_corpus_2003,E11_domain_specific_ADE_corpus_1901,general_vs_domain_specific,9fabdf8e8f4c,9fabdf8e8f4c
CMeIE,biomedical,0.9582,0.971,0.0129,label disambiguation,E11_general_CMeIE_1425,E11_domain_specific_CMeIE_1323,general_vs_domain_specific,66feeb8a62ed,c98817dfbd77
```

### 源文件: `E11_summary.md`

- 路径: `rebuttal/outputs/E11_summary.md`
- 文件大小(bytes): `522`

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
- 每个 source 导出 run_id 与 artifact_hash 便于追踪

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
  "timestamp_utc": "2026-03-28T10:23:55.578672+00:00",
  "git_commit": "4bd79613ab2cda309bbf7554716eb0e6ab9c99d9",
  "environment": {
    "timestamp_utc": "2026-03-28T10:23:55.587547+00:00",
    "python": "3.12.12 (main, Jan 12 2026, 17:43:59) [GCC 13.3.0]",
    "platform": "Linux-6.12.47-x86_64-with-glibc2.39",
    "git_commit": "4bd79613ab2cda309bbf7554716eb0e6ab9c99d9"
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
