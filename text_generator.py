# text_generator.py
from transformers import pipeline


text_generator = pipeline("text-generation", model="gpt2")

def generate_marketing_text(prompt, max_length=100):
    result = text_generator(prompt, max_length=max_length, num_return_sequences=1)
    return result[0]["generated_text"]
