import os
import random
import shutil

# 设置源文件夹和目标文件夹路径
source_dir = '/root/autodl-tmp/RoboTwin/data/block_handover_pairs'  # 替换为你的源文件夹路径
target_dir = '/root/autodl-tmp/RoboTwin/data/block_handover_pairs_test'  # 替换为你的目标文件夹路径

# 确保目标文件夹存在
os.makedirs(target_dir, exist_ok=True)

# 获取所有以 'input' 开头且以 '.png' 结尾的文件
input_files = [f for f in os.listdir(source_dir) if f.startswith('input') and f.endswith('.png')]

# 计算要抽取的文件数量（十分之一）
sample_size = max(1, len(input_files) // 200)

# 随机抽取文件
sampled_inputs = random.sample(input_files, sample_size)

# 复制抽取的文件及其对应的输出文件到目标文件夹
for input_file in sampled_inputs:
    # 构建完整的文件路径
    input_path = os.path.join(source_dir, input_file)
    output_file = input_file.replace('input', 'output')
    output_path = os.path.join(source_dir, output_file)

    # 构建目标路径
    target_input_path = os.path.join(target_dir, input_file)
    target_output_path = os.path.join(target_dir, output_file)

    # 复制文件
    shutil.copy2(input_path, target_input_path)
    if os.path.exists(output_path):
        shutil.copy2(output_path, target_output_path)
    else:
        print(f"警告：未找到对应的输出文件 {output_file}")
