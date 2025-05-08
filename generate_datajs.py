import os
import json

# 定义数据集配置
datasets = [
    {
        "name": "hammer_click_pairs",
        "input_dir": "/root/autodl-tmp/RoboTwin/data/hammer_click_pairs",
        "input_prefix": "input",
        "output_prefix": "output",
        "prompt": "beat the block with the hammer"
    },
    {
        "name": "blocks_stack_pairs",
        "input_dir": "/root/autodl-tmp/RoboTwin/data/blocks_stack_pairs",
        "input_prefix": "input",
        "output_prefix": "output",
        "prompt": "stack blocks"
    },
    {
        "name": "block_handover_pairs",
        "input_dir": "/root/autodl-tmp/RoboTwin/data/block_handover_pairs",
        "input_prefix": "input",
        "output_prefix": "output",
        "prompt": "handover the blocks"
    }
]

# 输出 JSONL 文件路径
output_jsonl = "/root/autodl-tmp/RoboTwin/data/dataset.jsonl"

# 打开文件写入
with open(output_jsonl, 'w', encoding='utf-8') as f:
    for dataset in datasets:
        input_files = sorted([
            file for file in os.listdir(dataset["input_dir"])
            if file.startswith(dataset["input_prefix"]) and file.endswith(".png")
        ])
        for input_file in input_files:
            # 构建对应的输出文件名
            index = input_file.replace(dataset["input_prefix"], "").replace(".png", "")
            output_file = f"{dataset['output_prefix']}{index}.png"
            input_path = os.path.join(dataset["input_dir"], input_file)
            output_path = os.path.join(dataset["input_dir"], output_file)
            # 检查输出文件是否存在
            if not os.path.exists(output_path):
                print(f"Warning: 输出文件 {output_path} 不存在，跳过该对。")
                continue
            # 构建 JSON 对象
            json_obj = {
                "edit_prompt": dataset["prompt"],
                "input_image": input_path,
                "output_image": output_path
            }
            # 写入 JSONL 文件
            f.write(json.dumps(json_obj) + '\n')

print(f"数据集构建完成，保存为 {output_jsonl}")
