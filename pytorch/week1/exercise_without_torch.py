import torch
from torch.utils.data import DataLoader, TensorDataset

# 1. 准备数据：生成 y = 2x + 3 + 噪声
X = torch.randn(200, 1)
noise = torch.randn(200, 1) * 0.1
Y = 2 * X + 3 + noise

# 使用 TensorDataset 和 DataLoader封装
my_dataset = TensorDataset(X, Y)
my_dataloader = DataLoader(my_dataset, batch_size=10, shuffle=True)

# 2. 初始化参数
w = torch.randn(1, requires_grad=True)
b = torch.randn(1, requires_grad=True)
lr = 0.1

# 3. 训练Epoch
for batch_x, batch_y in my_dataloader:
    # 前向传播
    y_pred = w * batch_x + b
    # 计算损失
    loss = ((y_pred - batch_y) ** 2).mean()
    # 反向传播
    loss.backward()
    # 更新参数
    with torch.no_grad():
        w -= lr * w.grad
        b -= lr * b.grad
        # 清空梯度
        w.grad.zero_()
        b.grad.zero_()

    print(f"Loss: {loss.item():.4f}, w: {w.item():.2f}, b: {b.item():.2f}")
