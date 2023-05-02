from transformers import pipeline, set_seed
import server


def generate(prompt: str, config: server.TextConfig) -> str:
    set_seed(config.seed)
    generator = pipeline("text-generation", "gpt2", do_sample=config.do_sample, max_new_tokens=config.max_new_tokens)
    return generator(prompt)