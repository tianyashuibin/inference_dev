import torch
import torch.nn as nn
import torchvision.models as models
from torchvision.models import ResNet18_Weights, Weights

print("=== 1. 加载预训练模型 ===")
# 加载在 ImageNet 上训练好的 ResNet18 模型
my_model = models.resnet18(weights=ResNet18_Weights.DEFAULT)

print(f"原始模型的全连接层:\n{my_model.fc}")

print("\n=== 2. 冻结特征提取器的参数 ===")
# 遍历模型所有的参数，把requires_grad设置为False
# 这样在方向传播时，就不会计算这些参数的梯度，大大节省了显存和时间
for param in my_model.parameters():
    param.requires_grad = False

print("=== 3. 替换分类头（改造为我们自己的任务）===")
# 猫狗二分类
num_classes = 2

# 获取原来全连接层的输入维度 (ResNet18 中是 512)
in_features = my_model.fc.in_features

# 重新赋值 model.fc，替换为一个新的全连接层
# 💡 注意：在 PyTorch 中，新创建的层默认 requires_grad=True
my_model.fc = nn.Linear(in_features, num_classes)

print(f"改造后的全连接层:\n{my_model.fc}")

# 检查一下哪些参数需要更新？
print("\n当前需要求导和更新的参数:")
for name, param in my_model.named_parameters():
    if param.requires_grad:
        print(name)

