import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

print("Loading model...")
model_name = "uer/gpt2-chinese-cluecorpussmall"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
model.eval()
print("Model loaded.")

def generate_text(prompt, max_length=50):
    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    output_ids = model.generate(input_ids, max_length=max_length, do_sample=True, top_k=500, top_p=0.95, temperature=1.0)
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

# 练习：实现一个函数，输入一个文本prompt，模型根据这个prompt进行自回归生成，直到生成指定长度的文本。
def self_generation(prompt, max_length=50, top_k=50, temperature=0.7):
    print(f"输入的prompt: {prompt}")
    input_ids = tokenizer.encode(prompt, return_tensors="pt", add_special_tokens=False)
    print(f"输入的token ids: {input_ids}")
    for _ in range(max_length):
        with torch.no_grad():
            output_ids = model(input_ids)
        logits = output_ids.logits
        next_token_logits = logits[0, -1, :]
        # top_k 过滤：只保留概率最高的 top_k 个 token
        top_k_logits, top_k_indices = torch.topk(next_token_logits, top_k)
        probs = torch.softmax(top_k_logits / temperature, dim=-1)
        sampled = torch.multinomial(probs, num_samples=1).item()
        next_token_id = top_k_indices[sampled].item()
        input_ids = torch.cat([input_ids, torch.tensor([[next_token_id]])], dim=1)
    generated_text = tokenizer.decode(input_ids[0], skip_special_tokens=True)
    return generated_text
    

if __name__ == "__main__":
    prompt = "从前有个小女孩，她住在一个小村庄里。一天，她决定去森林里探险，"
    generated = generate_text(prompt)
    print("Generated text:")
    print(generated)

    forward_text("今天的天气真")

    self_generated_text = self_generation(prompt)
    print("Self-generated text:")
    print(self_generated_text)