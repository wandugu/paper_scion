#!/bin/bash
# backend/run.sh

# === 解析你传入的命令 ===
if [[ "$1" != "python" || -z "$2" ]]; then
    echo "用法: ./run.sh python path/to/your_script.py"
    exit 1
fi

# 去掉 .py 后缀
script="${2%.py}"

# 替换路径分隔符 / 为 .，得到模块路径
module_path="${script//\//.}"

# 执行 python -m module
shift 2
echo ">> 执行: python -m $module_path $@"
python -m "$module_path" "$@"

