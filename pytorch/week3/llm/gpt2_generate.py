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

def forward_text(prompt):
    input_ids = tokenizer(prompt, return_tensors="pt", add_special_tokens=False)
    print(f"输入token:{input_ids['input_ids']}")
    print(f"input_ids: {input_ids}")
    print(f"输入token对应的文本:{tokenizer.decode(input_ids['input_ids'][0])}")
    with torch.no_grad():
        output_ids = model(**input_ids)
    print(f"模型输出内容:{output_ids}")
    logits = output_ids.logits
    print(f"前向传播结果Logits形状:{logits.shape}")
    next_token_logits = logits[0, -1, :]
    print(f"最后一个位置的预测打分形状:{next_token_logits.shape}")
    next_token_id = torch.argmax(next_token_logits).item()
    print(f"next_token_id: {next_token_id}")
    next_token_text = tokenizer.decode([next_token_id])
    print(f"根据{prompt}, 模型预测的下一个字是:{next_token_text}")
    predicted_ids = torch.argmax(logits, dim=-1)
    print(f"模型输出内容的predicted_ids:{predicted_ids}")
    print(f"模型输出内容解码之后的文本:{tokenizer.decode(predicted_ids[0], skip_special_tokens=True)}")


if __name__ == "__main__":
    prompt = "从前有个小女孩，她住在一个小村庄里。一天，她决定去森林里探险，"
    generated = generate_text(prompt)
    print("Generated text:")
    print(generated)

    forward_text("今天的天气真")
