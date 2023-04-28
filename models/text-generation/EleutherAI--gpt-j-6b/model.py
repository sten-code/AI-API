from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import os
#import server


def generate(prompt: str) -> str:
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "model")
    tokenizer = AutoTokenizer.from_pretrained(path)
    model = AutoModelForCausalLM.from_pretrained(path)
    generator = pipeline("text-generation", model=model, tokenizer=tokenizer, do_sample=True, max_new_tokens=200)
    return generator(prompt)

if __name__ == "__main__":
    print("Started")
    response = generate("""Yo mama""")
    print(response)