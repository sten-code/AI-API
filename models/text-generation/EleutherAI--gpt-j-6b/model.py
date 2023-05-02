from transformers import AutoTokenizer, GPTJForCausalLM, set_seed
import server

def generate(prompt: str, config: server.TextConfig) -> str:
    set_seed(config.seed)
    tokenizer = AutoTokenizer.from_pretrained("./GPTJ-6B/")
    model = GPTJForCausalLM.from_pretrained(
        "./GPTJ-6B/",
        max_length=config.max_new_tokens,
        temperature=config.temp,
        do_sample=config.do_sample
    )
    encoded_input = tokenizer(prompt, return_tensors='pt')
    output = model.generate(**encoded_input)[0]
    return tokenizer.decode(output)
