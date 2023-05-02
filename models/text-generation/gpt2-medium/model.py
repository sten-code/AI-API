from transformers import GPT2Tokenizer, GPT2LMHeadModel, set_seed
import server


def generate(prompt: str, config: server.TextConfig) -> str:
    set_seed(config.seed)
    model = GPT2LMHeadModel.from_pretrained('gpt2-medium',
        max_length=config.max_new_tokens,
        temperature=config.temp,
        do_sample=config.do_sample,
        num_return_sequences=config.numreturn
    )
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2-medium')
    encoded_input = tokenizer(prompt, return_tensors='pt')
    output = model.generate(**encoded_input)[0]
    return tokenizer.decode(output)