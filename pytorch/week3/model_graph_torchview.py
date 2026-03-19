import torch
import torch.nn as nn
import torchvision.models as models
from torchvision.models import ResNet18_Weights, Weights
from torchview import draw_graph

print("=== 1. 加载预训练模型 ===")
# 加载在 ImageNet 上训练好的 ResNet18 模型
my_model = models.resnet18(weights=ResNet18_Weights.DEFAULT)

dummy_input = torch.randn(1, 3, 224, 224)

model_graph = draw_graph(my_model,
                         input_size=(1, 3, 224, 224),
                         expand_nested=True,
                         graph_name="my_resnet18",
                         directory=".",              # 保存到当前目录
                         save_graph=False            # 关键：设置为 True
                         )

model_graph.visual_graph.render(filename="resnet18_viz", format="svg")

