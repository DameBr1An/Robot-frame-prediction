from diffusers import StableDiffusionInstructPix2PixPipeline
import torch

model_id = "timbrooks/instruct-pix2pix"
pipe = StableDiffusionInstructPix2PixPipeline.from_pretrained(
    model_id, torch_dtype=torch.float16
)

# 保存到本地文件夹
pipe.save_pretrained("instruct-pix2pix-local")
