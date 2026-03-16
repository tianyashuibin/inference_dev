import torch
import torch.nn as nn

print(f"=== 1. 搭建多层感知机（MLP）===")

class MyModel(nn.Module):
    def __init__(self):
        super(MyModel, self).__init__()

        # nn.Linear 就是全连接层，内部包含权重和偏置
        # 假设输入是10维，隐藏层是32维，输出是1维（比如房价预测）
        self.layer1 = nn.Linear(in_features=10, out_features=32)
        self.relu = nn.ReLU()
        self.layer2 = nn.Linear(in_features=32, out_features=1)

    def forward(self, x):
        x = self.layer1(x)
        x = self.relu(x)
        x = self.layer2(x)
        return x

model = MyModel()
print(model)

dummy_input = torch.randn(5, 10)
output = model(dummy_input)
print(f"\n输入形状:{dummy_input.shape}")
print(f"输出形状:{output.shape}")


