from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import os
#import server


def generate(prompt: str) -> str:
 
    tokenizer = AutoTokenizer.from_pretrained(facebook/opt-1.3b)
    model = AutoModelForCausalLM.from_pretrained(facebook/opt-1.3b)
    generator = pipeline("text-generation", model=model, tokenizer=tokenizer, do_sample=True, max_new_tokens=200)
    return generator(prompt)

