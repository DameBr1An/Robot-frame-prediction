import os
import pickle
import numpy as np
from PIL import Image

def load_rgb(pkl_path):
    """读取 pkl 中 head_camera 的 rgb 图像"""
    with open(pkl_path, 'rb') as f:
        data = pickle.load(f)

    observation = data.get('observation', {})
    head_camera = observation.get('head_camera', {})
    rgb = head_camera.get('rgb', None)

    if rgb is not None and isinstance(rgb, np.ndarray):
        rgb = rgb.astype(np.uint8)
        return Image.fromarray(rgb)
    else:
        return None

def get_starting_id(output_dir):
    """统计 output 目录里最大的 inputX/outputX 编号"""
    existing_inputs = [f for f in os.listdir(output_dir) if f.startswith('input') and f.endswith('.png')]
    if not existing_inputs:
        return 0
    existing_ids = [int(f.replace('input', '').replace('.png', '')) for f in existing_inputs]
    return max(existing_ids) + 1

def convert_pkl_pairs(input_dir, output_dir, frame_gap=50):
    """从 pkl 提取图片对并保存"""
    episodes = sorted(os.listdir(input_dir))  # 保证顺序
    os.makedirs(output_dir, exist_ok=True)

    global_id = get_starting_id(output_dir)
 
    print(f"起始 global_id: {global_id}")

    count = 0  # 当前处理到第几对

    for episode in episodes:
        episode_dir = os.path.join(input_dir, episode)
        if not os.path.isdir(episode_dir):
            continue

        pkl_files = sorted([f for f in os.listdir(episode_dir) if f.endswith('.pkl')],
                           key=lambda x: int(x.replace('.pkl', '')))

        num_files = len(pkl_files)

        for i in range(num_files - frame_gap):
            if count < global_id:
                count += 1
                continue  # 无条件跳过

            pkl_file_input = pkl_files[i]
            pkl_file_output = pkl_files[i + frame_gap]

            pkl_path_input = os.path.join(episode_dir, pkl_file_input)
            pkl_path_output = os.path.join(episode_dir, pkl_file_output)

            img_input = load_rgb(pkl_path_input)
            img_output = load_rgb(pkl_path_output)

            if img_input is None or img_output is None:
                print(f"跳过无效的文件对: {pkl_file_input}, {pkl_file_output}")
                continue

            input_path = os.path.join(output_dir, f"input{count}.png")
            output_path = os.path.join(output_dir, f"output{count}.png")

            img_input.save(input_path)
            img_output.save(output_path)

            print(f"保存: {input_path}, {output_path}")

            count += 1  # 保存后增加 count

# === 配置 ===
input_dir = '/root/autodl-tmp/RoboTwin/data/blocks_stack_easy_D435_pkl'  # 输入路径
output_dir = '/root/autodl-tmp/RoboTwin/data/blocks_stack_pairs/'  # 输出路径

convert_pkl_pairs(input_dir, output_dir, frame_gap=50)
