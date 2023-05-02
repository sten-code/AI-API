from transformers import pipeline, set_seed
import server



def generate(prompt: str, config: server.TextConfig) -> str:
    set_seed(config.seed)
    generator = pipeline("text-generation", model="facebook/opt-1.3b", do_sample=config.do_sample, max_new_tokens=config.max_new_tokens, temperature=config.temp, num_return_sequences=config.numreturn)
    return generator(prompt)
