from diffusers import StableDiffusionPipeline
import torch
import os
import time
import server
import base64
from io import BytesIO


def generate(prompt: str, config: server.TextConfig) -> str:
    pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16).to("cuda")

    image = pipe(prompt, 512, 512, config.num_inference_steps, config.guidance_scale).images[0]

    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")
