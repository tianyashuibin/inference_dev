import torch

x = torch.tensor(1.0)
y_true = torch.tensor(3.0)

w = torch.randn(1, requires_grad=True)
print(f"初始权重 w：{w.item():.4f}")

lr = 0.1

while torch.abs(w * x - y_true) > 0.01:
    y_pred = w * x
    loss = (y_pred - y_true) ** 2
    loss.backward()
    with torch.no_grad():
        w -= lr * w.grad
        w.grad.zero_()
print(f"final y_pred: {y_pred}")
print(f"final w: {w}")
