import torch
from torch.cuda import is_available
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

# 检查设备
device = torch.device("cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu"))

# transforms.ToTensor() 会把 PIL 图像转为 Tensor，并把像素值从 0~255 归一化到 0.0~1.0
my_transform = transforms.ToTensor()

# 自动下载训练集和测试集 (第一次运行会下载数据到 ./data 文件夹)
train_data = datasets.FashionMNIST(root='./data', train=True, download=True, transform=my_transform)
test_data = datasets.FashionMNIST(root='./data', train=False, download=True, transform=my_transform)

# 封装进 DataLoader
train_loader = DataLoader(train_data, batch_size=64, shuffle=True)
test_loader = DataLoader(test_data, batch_size=64, shuffle=False)

class SimpleCNN(nn.Module):
    def __init__(self) -> None:
        super(SimpleCNN, self).__init__()
        self.layer_1 = nn.Linear(784, 1024, bias=True)
        self.relu = nn.ReLU()
        self.layer_2 = nn.Linear(1024, 10, bias=True)

    def forward(self, x):
        x = x.view(-1, 28 * 28)
        x = self.layer_1(x)
        x = self.relu(x)
        x = self.layer_2(x)

        return x

my_model = SimpleCNN().to(device)

my_criterion = nn.CrossEntropyLoss()
my_optimizer = torch.optim.Adam(my_model.parameters(), lr=0.001)

best_acc = 0.0

for epoch in range(10):
    my_model.train()
    for idx, (batch_x, batch_y) in enumerate(train_loader):
        batch_x, batch_y = batch_x.to(device), batch_y.to(device)
        my_optimizer.zero_grad()
        y_pred = my_model(batch_x)
        loss = my_criterion(y_pred, batch_y)
        loss.backward()
        my_optimizer.step()

    correct = 0
    total = 0
    my_model.eval()
    with torch.no_grad():
        for batch_x, batch_y in test_loader:
            batch_x, batch_y = batch_x.to(device), batch_y.to(device)
            my_optimizer.zero_grad()
            y_pred = my_model(batch_x)
            _, predicted = torch.max(y_pred, 1)
            total += batch_y.size(0)
            correct += (predicted == batch_y).sum().item()
    acc = 100 * correct / total
    print(f"Epoch[{epoch+1}/10], Accuracy:{acc:.2f}")

    if acc > best_acc:
        best_acc = acc
        torch.save(my_model.state_dict(), "my_model_weight.pth")

print("Training complete!")

