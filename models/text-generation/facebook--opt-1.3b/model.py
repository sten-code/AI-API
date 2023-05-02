from transformers import pipeline, set_seed
import os
import server

set_seed(config.seed)

def generate(prompt: str, config: server.TextConfig) -> str:
    generator = pipeline("text-generation", model="facebook/opt-1.3b", do_sample=config.do_sample, max_new_tokens=config.max_new_tokens, temperature=config.temp)
    return generator(prompt)
