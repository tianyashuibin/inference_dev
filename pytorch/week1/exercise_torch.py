import torch
from torch.utils.data import TensorDataset, DataLoader

X = torch.randn(20, 1)
noise = torch.randn(20, 1) * 0.1
Y = 2 * X + 3 + noise

my_dataset = TensorDataset(X, Y)
my_dataloader = DataLoader(my_dataset, batch_size=10, shuffle=True)


my_model = torch.nn.Linear(1, 1, bias=True, device="cpu")
my_optimizer = torch.optim.SGD(my_model.parameters(), lr=0.1)
my_criterion = torch.nn.MSELoss()

params = list(my_model.parameters())
for epoch in range(10):
    for batch_idx, (batch_x, batch_y) in enumerate(my_dataloader):
        my_optimizer.zero_grad()
        y_pred = my_model(batch_x)
        loss = my_criterion(y_pred, batch_y)
        loss.backward()
        my_optimizer.step()
    print(f"epoch:{epoch}, my_model.parameters:{params[0].item()}, {params[1].item()}")
