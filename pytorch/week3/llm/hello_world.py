import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

print("=== 1. Tokenizer(文本->向量）===")
model_name = "bert-base-chinese"
tokenizer = AutoTokenizer.from_pretrained(model_name)

text = "我超级喜欢学习pytorch和LLM"
inputs = tokenizer(text, return_tensors="pt")

print("Tokenizer 输出的结果是一个字典，包含:")
print(f"输入 ID(input_ids):\n{inputs['input_ids']}")
print(f"张量形状：{inputs['input_ids'].shape}")
print(f"注意力掩码(attention_mask):\n{inputs['attention_mask']}")

print("\n=== 2. 加载预训练模型(本质就是nn.Module) ===")
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)

print(f"这是一个Pytorch模型吗 {isinstance(model, torch.nn.Module)}")

print("\n=== 3. 前向传播 ===")
model.eval()
with torch.no_grad():
    outputs = model(**inputs)

logits = outputs.logits
print(f"模型输出的预测得分(Logits):{logits}")
print(f"Logits 形状: {logits.shape}")

predicted_class = torch.argmax(logits, dim=-1).item()
print(f"模型预测的类别是: {predicted_class}")

