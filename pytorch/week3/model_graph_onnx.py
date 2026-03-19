import torch
import torch.nn as nn
import torchvision.models as models
from torchvision.models import ResNet18_Weights, Weights

print("=== 1. 加载预训练模型 ===")
# 加载在 ImageNet 上训练好的 ResNet18 模型
my_model = models.resnet18(weights=ResNet18_Weights.DEFAULT)

dummy_input = torch.randn(1, 3, 224, 224)

my_model.eval()
torch.onnx.export(
    my_model,
    (dummy_input,),
    "my_model.onnx",
    export_params=True,         # 是否导出权重参数
    opset_version=12,           # ONNX 算子版本
    input_names=['input'],      # 输入节点的名称
    output_names=['output'],    # 输出节点的名称
    dynamic_axes={'input': {0: 'batch_size'}, 'output': {0: 'batch_size'}} # 支持动态 Batch
)
