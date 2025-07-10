import subprocess
import os

# 获取当前Python脚本的目录
current_directory = os.path.dirname(os.path.abspath(__file__))

# 构建Shell脚本的完整路径
script_path = os.path.join(current_directory, 'run.sh')

# 调用Shell脚本，捕获输出
print(f"Running script at {script_path}")
result = subprocess.run(['bash', script_path], text=True, capture_output=True)

# 打印Shell脚本的输出
if result.stdout:
    print("Output from script:")
    print(result.stdout)
if result.stderr:
    print("Errors from script:")
    print(result.stderr)
