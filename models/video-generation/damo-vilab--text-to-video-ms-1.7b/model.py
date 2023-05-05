import torch, server, cv2, os, time, base64
from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
from typing import List
import numpy as np

from transformers import set_seed
from moviepy.editor import *


def generate(prompt: str, config: server.VideoConfig) -> str:
    set_seed(config.seed)
    pipe = DiffusionPipeline.from_pretrained("damo-vilab/text-to-video-ms-1.7b", torch_dtype=torch.float16, variant="fp16")
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
    pipe.enable_model_cpu_offload()
    video_frames = pipe(prompt, num_inference_steps=config.num_inference_steps, num_frames=config.num_frames).frames
    video_path = export_to_video(video_frames=video_frames, fps=config.fps)
    return video_path

def export_to_video(video_frames: List[np.ndarray], fps: int) -> str:
    name = round(time.time())
    output_video_path = f"./website/src/video's/{name}.mp4"
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    h, w, c = video_frames[0].shape
    video_writer = cv2.VideoWriter(output_video_path, fourcc, fps=fps, frameSize=(w, h))
    for i in range(len(video_frames)):
        img = cv2.cvtColor(video_frames[i], cv2.COLOR_RGB2BGR)
        video_writer.write(img)
    video_writer.release()
    # Convert to MP4 with H.264 and AAC codecs
    video_clip = VideoFileClip(output_video_path)
    video_clip.write_videofile(output_video_path.replace(".mp4", "_converted.mp4"), codec="libx264", audio_codec="aac")
    video_clip.close()

    # Delete the original file
    os.remove(output_video_path)
    new_path =output_video_path.replace(".mp4", "_converted.mp4")

    with open(new_path, 'rb') as file:
        video_bytes = file.read()
        video_base64 = base64.b64encode(video_bytes).decode('utf-8')
        
    os.remove(new_path)
    return video_base64
