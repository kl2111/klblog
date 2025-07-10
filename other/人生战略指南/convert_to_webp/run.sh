#!/bin/bash
# 获取脚本所在的目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# 切换到脚本所在目录
cd "$SCRIPT_DIR"

# 删除旧的虚拟环境
if [ -d "venv" ]; then
    rm -rf venv
fi

# 创建新的虚拟环境
python3 -m venv venv

# 激活新的虚拟环境
source venv/bin/activate

# 更新 pip 并安装依赖包
pip install --upgrade pip
pip install selenium webdriver-manager pillow imageio

# 打印 pip list 来确认是否安装了 webdriver-manager
pip list | grep webdriver-manager

# 运行 Python 脚本
python3 main.py