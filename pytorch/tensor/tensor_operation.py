import torch

print("=== 1. 张量创建 ===")
# 1. 从python列表直接创建
data = [[1, 2], [3, 4]]
x_data = torch.tensor(data)
print(f"从列表创建:\n{x_data}")

# 2. 模拟神经网络的权重或输入（标准正态分布）
# 常用于模拟：BatchSize=2, Channels=3, Height=4, Width=4 的图像数据
x_rand = torch.randn(2, 3, 4, 4)
print(f"\n随机张量的形状:{x_rand.shape}")

# 3. 创建全0或者全1的张量（常用于生成Mask或特定形状的Bias）
x_zeros = torch.zeros(2, 2)
print(f"\n全0张量:\n{x_zeros}")
x_ones = torch.ones(2, 2)
print(f"\n全1张量:\n{x_ones}")

print("\n=== 2. 张量的三大核心属性 ===")
x_tensor = torch.randn(3, 4)
print(f"形状（shape）:{x_tensor.shape}")
print(f"数据类型（Dtype）:{x_tensor.dtype}")
print(f"所在设备（Device）:{x_tensor.device}")

if torch.backends.mps.is_available():
    print(f"当前设备支持mps")
    device = torch.device("mps")
    x_tensor = x_tensor.to(device)
    print(f"所在设备（Device）:{x_tensor.device}")
    print(f"Current device: {device}")
else:
    print(f"当前设备不支持mps")

