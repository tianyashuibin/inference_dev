import torch
from torch.utils.data import Dataset, DataLoader

print(f"=== 1. 构建自定义 Dataset ===")

class MyDummyDataset(Dataset):
    def __init__(self, num_samples=1000) -> None:
        super().__init__()
        # 在实际项目中，这里通常是读取图片路径列表，或者读取 CSV 文件
        # 为了演示，我们直接生成一些模拟数据：1000个样本，每个样本10个特征
        self.features = torch.randn(num_samples, 10)
        # 模拟标签：0 或 1 二分类
        self.labels = torch.randint(0, 2, (num_samples, ))

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        x = self.features[idx]
        y = self.labels[idx]
        return x, y

my_dataset = MyDummyDataset(num_samples=100)
print(f"数据集总大小:{len(my_dataset)}")

# 测试一下能不能拿到第 0 个样本
sample_x, sample_y = my_dataset[0]
print(f"第 0 个样本的特征形状: {sample_x.shape}")
print(f"第 0 个样本的标签: {sample_y}")

print(f"\n=== 2. 使用DataLoader 批量加载数据 ===")
# num_workers: 开启多少个线程来加载数据
train_loader = DataLoader(dataset=my_dataset,
                          batch_size=16,
                          shuffle=True,
                          num_workers=0)

print(f"开始模拟训练时的分批次提取：")
for batch_idx, (batch_features, batch_labels) in enumerate(train_loader):
    print(f"批次 {batch_idx}:")
    print(f" 特征形状(Batch X): {batch_features.shape}")
    print(f" 标签形状(Batch Y): {batch_labels.shape}")

    if batch_idx == 2:
        break;


