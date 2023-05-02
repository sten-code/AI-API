from transformers import pipeline
import server


def generate(prompt: str, config: server.TextConfig) -> str:
    generator = pipeline("text-generation", "gpt2-medium", do_sample=config.do_sample, max_new_tokens=config.max_new_tokens)
    return generator(prompt)