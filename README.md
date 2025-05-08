# first you need to download RoboTwin from github
# prepare enviroment
vim ~/.bashrc

source /root/miniconda3/etc/profile.d/conda.sh

conda activate base

conda create -n RoboTwin python=3.10.0
conda activate RoboTwin


pip install jupyter d2l
conda install ipykernel

ipython kernel install --user --name=RoboTwin

# VPN(if need)：
source /etc/network_turbo 
unset http_proxy && unset https_proxy
# (or you can choose ) : 
export HF_ENDPOINT=https://hf-mirror.com


# install requirements
pip install torch==2.2.1 torchvision==0.17.1 torchaudio==2.2.1 --index-url https://download.pytorch.org/whl/cu121


sudo apt update

sudo apt install libvulkan1 mesa-vulkan-drivers vulkan-tools


pip install packaging==24.0
# Install flash-attn
pip install flash-attn --no-build-isolation


pip install sapien==3.0.0b1 scipy==1.10.1 mplib==0.1.1 gymnasium==0.29.1 trimesh==4.4.3 open3d==0.18.0 imageio==2.34.2 pydantic zarr openai huggingface_hub==0.25.0


Then, install pytorch3d:
```
cd third_party/pytorch3d_simplified && pip install -e . && cd ../..
```

## 2. Download Assert
```
python ./script/download_asset.py
unzip aloha_urdf.zip && unzip main_models.zip
```

## 3. Modify `mplib` Library Code
### 3.1 Remove `convex=True`
You can use `pip show mplib` to find where the `mplib` installed.
```
# mplib.planner (mplib/planner.py) line 71
# remove `convex=True`

### 3.2 Remove `or collide`
```
# mplib.planner (mplib/planner.py) line 848
# remove `or collide`
# Install other prequisites
pip install -r requirements.txt

requirements.txt

packaging==24.0
wandb==0.17.0
deepspeed==0.14.2   
accelerate==0.30.1
diffusers==0.27.2
timm==1.0.3
transformers==4.41.0
sentencepiece==0.2.0
h5py==3.11.0
opencv-python==4.9.0.80
imgaug==0.4.0

# test 
sudo apt-get update && sudo apt-get install -y xvfb x11-utils
Xvfb :99 -screen 0 1024x768x16 &  # 在后台启动虚拟显示器（显示号 99，分辨率 1024x768）
export DISPLAY=:99  # 指定当前终端会话使用虚拟显示器
# if cant find arx5.......urdf(python ./script/download_asset.py
unzip aloha_urdf.zip && unzip main_models.zip)

## 3. Modify `mplib` Library Code
### 3.1 Remove `convex=True`
You can use `pip show mplib` to find where the `mplib` installed.
```
# mplib.planner (mplib/planner.py) line 71
# remove `convex=True`

self.robot = ArticulatedModel(
            urdf,
            srdf,
            [0, 0, -9.81],
            user_link_names,
            user_joint_names,
            convex=True,
            verbose=False,
        )
=> 
self.robot = ArticulatedModel(
            urdf,
            srdf,
            [0, 0, -9.81],
            user_link_names,
            user_joint_names,
            # convex=True,
            verbose=False,
        )
```

### 3.2 Remove `or collide`
```
# mplib.planner (mplib/planner.py) line 848
# remove `or collide`

if np.linalg.norm(delta_twist) < 1e-4 or collide or not within_joint_limit:
                return {"status": "screw plan failed"}
=>
if np.linalg.norm(delta_twist) < 1e-4 or not within_joint_limit:
                return {"status": "screw plan failed"}
```



python script/test_render.py
# the ouput should be : render ok

# run 
bash run_task.sh block_hammer_beat 0

bash run_task.sh blocks_stack_easy 0

bash run_task.sh block_handover 0

# extract png(replace the path to your png in convert.py)
python path/to/convert.py 

# download the model instruct_p2p
python path/to/dl.py 

# resize the picture to 256*256 
python path/to/pic.py

# split train test dataset
python path/to/train_test_sp.py

# generate data.jsonl to load the data 
python path/to/generate_datajs.py

# finetune the model (replace the your own path)

export DATASET_ID="/root/autodl-tmp/instruct-pix2pix-main/roboframe.py"
export OUTPUT_DIR="/root/autodl-tmp/Finetuned_p2p"

accelerate launch --mixed_precision="fp16" finetune_instruct_pix2pix.py --pretrained_model_name_or_path=$MODEL_ID --dataset_name=$DATASET_ID --original_image_column="input_image" --edit_prompt_column="instruction" --edited_image_column="ground_truth_image" --resolution=256 --random_flip --train_batch_size=2 --gradient_accumulation_steps=4 --gradient_checkpointing --max_train_steps=15000 --checkpointing_steps=5000 --checkpoints_total_limit=1 --learning_rate=5e-05 --lr_warmup_steps=0 --mixed_precision=fp16 --seed=42 --output_dir="output_set"

# inference 
# run the code in the inference.ipynb to inference 

# evaluate
# run the code in the evaluate.ipynb