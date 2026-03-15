import torch

print(f"=== 1. 基础自动求导 ===")
x = torch.tensor([2.0])
w = torch.tensor([3.0], requires_grad=True)
b = torch.tensor([1.0], requires_grad=True)

y = w * x + b
print(f"前向计算结果 y: {y.item()}")

y.backward()

print(f"w 的梯度(dy/dw): {w.grad.item()}")
print(f"b 的梯度(dy/db): {b.grad.item()}")

# 梯度默认是累加的，不是覆盖的，所以第二次迭代的时候需要把梯度清零
# 下面的这部分没有清零，可以看看结果
y2 = w * x + b
y2.backward()

print(f"第二次backward之后，w的梯度变成了:{w.grad.item()}")

# 正确的做法：每次方向传播前，手动清零梯度
w.grad.zero_()
b.grad.zero_()
print(f"清零后 w 的梯度:{w.grad.item()}")

print(f"=== 3. 禁用梯度计算 ===")
with torch.no_grad():
    y_test = w * x + b
    print(f"y_test 是否需要求导? {y_test.requires_grad}")

y_detached = y.detach()
print(f"y_detached 是否需要求导? {y_detached.requires_grad}")
