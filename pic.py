from PIL import Image
import os

input_dir = "/root/autodl-tmp/RoboTwin/data/hammer_click_pairs_ori"
output_dir = "/root/autodl-tmp/RoboTwin/data/hammer_click_pairs"
os.makedirs(output_dir, exist_ok=True)

for filename in os.listdir(input_dir):
    if filename.endswith(".png"):
        img = Image.open(os.path.join(input_dir, filename))
        img = img.resize((256, 256))
        img.save(os.path.join(output_dir, filename))
