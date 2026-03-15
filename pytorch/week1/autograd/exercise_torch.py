import torch
import torch.optim as optim

x = torch.tensor([[1.0]])
y_true = torch.tensor([[3.0]])

model = torch.nn.Linear(1, 1, bias=False)
optimizer = optim.SGD(model.parameters(), lr=0.1)
criterion = torch.nn.MSELoss()

for epoch in range(30):
    # 梯度清零
    optimizer.zero_grad()
    # 前向传播 + 计算损失
    y_pred = model(x)
    loss = criterion(y_pred, y_true)
    # 反向传播：计算梯度
    loss.backward()
    # 更新参数：执行 w = w - lr * grad
    optimizer.step()
    print(f"epoch {epoch + 1}: loss={loss.item():.4f}, w={model.weight.item():.4f}")

print(f"\n最终预测值: {model(x).item():.4f}")
