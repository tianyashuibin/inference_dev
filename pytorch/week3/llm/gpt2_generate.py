import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

print("Loading model...")
model_name = "uer/gpt2-chinese-cluecorpussmall"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
print("Model loaded.")

def generate_text(prompt, max_length=50):
    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    output_ids = model.generate(input_ids, max_length=max_length, do_sample=True, top_k=50, top_p=0.95, temperature=0.7)
    generated_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return generated_text

if __name__ == "__main__":
    prompt = "从前有个小女孩，她住在一个小村庄里。一天，她决定去森林里探险，"
    generated = generate_text(prompt)
    print("Generated text:")
    print(generated)
