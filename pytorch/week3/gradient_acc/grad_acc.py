import torch
import torch.nn as nn
import torch.optim as optim

print("=== 演示：工业级省显存训练循环 ===")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = nn.Linear(10, 2).to(device)
optimizer = optim.Adam(model.parameters(), lr=0.001)
criterion = nn.CrossEntropyLoss()

dummy_inputs = torch.randn(8, 10).to(device)
dummy_labels = torch.randint(0, 2, (8,)).to(device)

# 1. 梯度累加步数：假设真实 batch_size=8，我们希望模拟 batch_size=32
accumulation_steps = 4

model.train()
optimizer.zero_grad()  # 初始化梯度

# 模拟有 12 个 Batch 的训练过程
for i in range(1, 13):
    outputs = model(dummy_inputs)
    loss = criterion(outputs, dummy_labels) / accumulation_steps  # 注意要除以累加步数
    loss.backward()  # 反向传播，梯度会累加到 model.parameters().grad 中
    print(f"Step {i} 跑完，梯度已累加，当前还没更新参数！")

    # 只有当积累了足够的步数，或者到了最后一个 batch 时，才更新参数
    if i % accumulation_steps == 0:
        optimizer.step()  # 更新参数
        optimizer.zero_grad()  # 清空梯度，为下一轮累加做准备
        print(f"Step {i} 参数已更新，梯度已清零！")
