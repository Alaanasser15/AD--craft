# ✅ video_generator.py

import torch
import uuid
from diffusers import AnimateDiffPipeline, EulerDiscreteScheduler
from diffusers.utils import export_to_video
from huggingface_hub import hf_hub_download
from safetensors.torch import load_file

bases = {
    "Cartoon": "frankjoshua/toonyou_beta6",
    "Realistic": "emilianJR/epiCRealism", 
    "3d": "Lykon/DreamShaper",
    "Anime": "Yntec/mistoonAnime2"
}
step_loaded = None
base_loaded = "Realistic"
motion_loaded = None

if not torch.cuda.is_available():
    device = "cpu"
    dtype = torch.float32
else:
    device = "cuda"
    dtype = torch.float16

pipe = AnimateDiffPipeline.from_pretrained(
    bases[base_loaded],
    torch_dtype=dtype
).to(device)

pipe.scheduler = EulerDiscreteScheduler.from_config(
    pipe.scheduler.config,
    timestep_spacing="trailing",
    beta_schedule="linear"
)

def generate_video(prompt, base, motion, steps):
    global step_loaded, base_loaded, motion_loaded

    if step_loaded != steps:
        repo = "ByteDance/AnimateDiff-Lightning"
        ckpt = f"animatediff_lightning_{steps}step_diffusers.safetensors"
        pipe.unet.load_state_dict(load_file(hf_hub_download(repo, ckpt), device=device), strict=False)
        step_loaded = steps

    if base_loaded != base:
        pipe.unet.load_state_dict(torch.load(hf_hub_download(bases[base], "unet/diffusion_pytorch_model.bin"), map_location=device), strict=False)
        base_loaded = base

    if motion_loaded != motion:
        # ✅ علّقنا هذا السطر لأنه يحتاج PEFT:
        # pipe.unload_lora_weights()

        if motion:
            pipe.load_lora_weights(motion, adapter_name="motion")
            pipe.set_adapters(["motion"], [0.7])
        motion_loaded = motion

    output = pipe(prompt=prompt, guidance_scale=1.2, num_inference_steps=steps)
    name = str(uuid.uuid4()).replace("-", "")
    path = f"{name}.mp4"
    export_to_video(output.frames[0], path, fps=10)
    return path
