import torch

x_img = torch.randn(64, 128, 14, 14)
print(f"x_img shape:{x_img.shape}")

x_img = x_img.view(64, -1)
print(f"x_img shape:{x_img.shape}")
