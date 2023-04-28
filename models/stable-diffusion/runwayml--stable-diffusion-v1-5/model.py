from diffusers import StableDiffusionOnnxPipeline
import torch
import os
import time
import server
import base64
from io import BytesIO


def generate(prompt: str, config: server.TextConfig) -> str:
    path = f"{os.path.dirname(os.path.realpath(__file__))}\\model"
    pipe = StableDiffusionOnnxPipeline.from_pretrained(path, provider="DmlExecutionProvider", torch_dtype=torch.float16)
    generator = torch.Generator()
    seed = generator.seed()
    generator = generator.manual_seed(seed)
    image = pipe(prompt, 512, 512, config.num_inference_steps, config.guidance_scale).images[0]

    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue())
