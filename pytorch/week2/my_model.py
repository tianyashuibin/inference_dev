import torch
import torch.nn as nn

print("=== 1. 模型切换演示 ===")

my_model = nn.Sequential(
    nn.Linear(10, 20),
    nn.Dropout(p=0.5),
    nn.Linear(20, 1)
)

dummy_x = torch.randn(1, 10)

# 训练模式，默认模式
my_model.train()
out_train1 = my_model(dummy_x)
out_train2 = my_model(dummy_x)
print(f"训练模式输出1: {out_train1.item():.4f}")
print(f"训练模式输出2: {out_train2.item():.4f}")

# 评估模式
my_model.eval()
with torch.no_grad():
    out_eval1 = my_model(dummy_x)
    out_eval2 = my_model(dummy_x)
print(f"评估模式输出1: {out_eval1.item():.4f}")
print(f"评估模式输出2: {out_eval2.item():.4f}")

import os

print("=== 2. 模型的保存和加载 ===")
print("模型的 state_dict 字典包含:")
for param_tensor in my_model.state_dict():
    print(param_tensor, "\t", my_model.state_dict()[param_tensor].size())

# 保存模型权重（通常以 .pt\.pth 为后缀）
save_path = "my_model_weight.pth"
torch.save(my_model.state_dict(), save_path)
print(f"模型已经保存到了:{save_path}")

# 3. 加载模型权重
# 第一步：必须先初始化一个结构一样的“空模型”
loaded_model = my_model

loaded_model.load_state_dict(torch.load(save_path, weights_only=True))
loaded_model.eval()
print("模型参数加载成功")


