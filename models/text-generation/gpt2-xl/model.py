from transformers import pipeline, set_seed

def generate(prompt: str, config: server.TextConfig) -> str:
    set_seed(config.seed)
    generator = pipeline("text-generation", "gpt2-xl", do_sample=config.do_sample, max_new_tokens=config.max_new_tokens)
    return generator(prompt)