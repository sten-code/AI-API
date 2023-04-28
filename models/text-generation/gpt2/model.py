from transformers import pipeline
import os
import server


def generate(prompt: str, config: server.TextConfig) -> str:
    generator = pipeline("text-generation", model=os.path.join(os.path.dirname(os.path.realpath(__file__)), "model"), do_sample=config.do_sample, max_new_tokens=config.max_new_tokens)
    return generator(prompt)