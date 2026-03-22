import torch
from transformers import AutoModelForSequenceClassification
from peft import LoraConfig, get_peft_model, TaskType

print("=== 1. 加载原始大模型 ===")
model_name = "bert-base-chinese"
# 我们依然以分类任务为例演示，生成任务同理
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)

print("\n=== 2. 配置 LoRA 降维打击 ===")
# 设定 LoRA 的超参数
lora_config = LoraConfig(
    task_type=TaskType.SEQ_CLS, # 任务类型：序列分类 (如果是GPT生成，就选 CAUSAL_LM)
    r=8,                        # ⭐️ 核心参数：LoRA的秩，决定了小矩阵的宽度。通常设为 8, 16, 32
    lora_alpha=32,              # 缩放比例：控制 LoRA 对原模型的影响力度，通常是 r 的 2倍或4倍
    lora_dropout=0.1,           # 防过拟合的 Dropout 比例
    # target_modules=["query", "value"] # 高级用法：指定把 LoRA 挂在哪些层上（默认会自动寻找注意力层）
)

print("\n=== 3. 施加魔法：把原始模型变成 LoRA 模型 ===")
peft_model = get_peft_model(model, lora_config)

peft_model.print_trainable_parameters()

# 检验一下：现在传给优化器的，只剩下极少数的 LoRA 参数了！
# optimizer = torch.optim.AdamW(peft_model.parameters(), lr=1e-4) # LoRA 学习率通常可以设大一点
