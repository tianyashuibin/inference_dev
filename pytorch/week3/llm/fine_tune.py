import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

model_name = "bert-base-chinese"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)
# 1. 准备数据
texts = ["我喜欢这个产品！", "这个服务太差了。"]
labels = [1, 0]  # 1: 正面, 0:

# 2. 数据预处理
inputs = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
labels = torch.tensor(labels)

print("=== 模型微调前 ===")
print(f"输入 ID(input_ids):\n{inputs['input_ids']}")
print(f"注意力掩码(attention_mask):\n{inputs['attention_mask']}")
outputs = model(**inputs)
print(f"输出 logits:\n{outputs.logits}")
predicted_classes = torch.argmax(outputs.logits, dim=-1)
print(f"预测类别: {predicted_classes.tolist()}")

# 3. 定义损失函数和优化器
criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-5)
# 4. 训练模型
model.train()
for epoch in range(10):  # 训练10个epoch
    optimizer.zero_grad()
    outputs = model(**inputs)
    loss = criterion(outputs.logits, labels)
    loss.backward()
    optimizer.step()
    print(f"Epoch {epoch+1}, Loss: {loss.item():.4f}")
# 5. 模型评估
model.eval()
with torch.no_grad():
    outputs = model(**inputs)
    predicted_classes = torch.argmax(outputs.logits, dim=-1)
    print(f"预测类别: {predicted_classes.tolist()}")
