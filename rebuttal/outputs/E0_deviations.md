# E0 Deviations

- 缺少原生 RL 训练代码与人工标注文件，相关实验按规范生成近似结果或 STATUS_NOT_RUN。
- 软匹配/图匹配在 rebuttal 实验中使用可复现启发式近似。
- E1 reachable 由 train relations/events 重建，RE 与 EE 采用分类型 key 对齐。
- E2 mismatch cases 为代表性 source 抽样案例，避免模板化复制。
- E3 ETA 采用本地近似模拟（无在线LLM调用）。
- E4 使用可复现近似实现。
- E5 使用可复现近似实现。
- E6 使用可复现近似实现。
- E7 缺少人工标注文件，输出 STATUS_NOT_RUN 与完整准备包。
- E8 使用可复现近似实现。
- E9 使用近似 RL 结果模板，因仓库无原生可运行 RL 训练环路。
- E10 使用可复现近似实现。
- E11 使用可复现近似实现。
- E12 使用可复现近似实现。
- E1 reachable 统一 canonicalize_edge 后再取交集，并新增 untyped RE source 的 placeholder-collapsed typed reachability。
