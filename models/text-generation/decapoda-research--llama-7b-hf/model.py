import os
import transformers
from transformers import LlamaForCausalLM, GenerationConfig
from llama import LLaMATokenizer
import time


def generate(prompt: str) -> str:
    path = f"{os.path.dirname(os.path.realpath(__file__))}\\model"
    tokenizer = LLaMATokenizer.from_pretrained(path, provider="DmlExecutionProvider")

    start = time.time()
    model = LlamaForCausalLM.from_pretrained(path)
    #model.to("cpu")
    print(f"{time.time() - start} seconds to load model")

    encoded = tokenizer(prompt, return_tensors="pt", add_special_tokens=False)
    #encoded = {k: v.to("cpu") for k, v in encoded.items()}

    start = time.time()
    generated = model.generate(encoded["input_ids"], max_length=200)
    print(f"{time.time() - start} seconds to generate")
    start = time.time()
    decoded = tokenizer.decode(generated[0])
    print(f"{time.time() - start} seconds to decode")
    return decoded


if __name__ == "__main__":
    print("Started")
    print(generate("""Yo mama"""))