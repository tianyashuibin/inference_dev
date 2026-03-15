import torch

print("=== 3. 形状变换 (Reshape / View) ===")
x = torch.randn(4, 4) # 假设这是 4x4 的特征图
print(f"原始形状: {x.shape}")

# view 和 reshape 作用基本一致，用于展平张量
# -1 是一个魔法数字，意思是 "PyTorch 你自己帮我算这一维应该是多少"
# 在深度学习模型（尤其是 CNN）中，经常在卷积层转全连接层时使用 view
# 假设输入特征图形状是 [batch_size, channels, high, width] -> (64, 32, 7, 7)
# 展平（Flatten）为一维向量，传给全连接层
# flat_x = x.view(x.size(0), -1)  # 变为 (64, 1568)
x_flatten = x.view(16)
x_flatten_auto = x.view(2, -1) # 变成 2行，列数自动计算(8)
print(f"展平后的形状: {x_flatten.shape}")
print(f"自动计算维度的形状: {x_flatten_auto.shape}")

print("\n=== 4. 增加/压缩维度 (Unsqueeze / Squeeze) ===")
# 【实战场景】：你有一张图片，形状是 [Channels, Height, Width] ->[3, 224, 224]
# 但网络需要的输入总是带 Batch Size 的，即[Batch, Channels, Height, Width]
img = torch.randn(3, 224, 224)
print(f"单张图片形状: {img.shape}")

# 在第0维（最前面）增加一个维度，代表 Batch Size = 1
img_batch = img.unsqueeze(0)
print(f"增加 Batch 维度后: {img_batch.shape}") # 变成[1, 3, 224, 224]

# squeeze 会把所有维度大小为 1 的维度去掉
img_squeezed = img_batch.squeeze(0)
print(f"压缩回原来的形状: {img_squeezed.shape}")

img_batch_2 = img.unsqueeze(1)
print(f"img_batch_2 shape:{img_batch_2.shape}")
img_batch_3 = img_batch_2.squeeze(1)
print(f"img_batch_3 shape:{img_batch_3.shape}")

print("\n=== 5. 维度交换 (Transpose / Permute) ===")
# 【实战场景】：NLP 中处理文本，常需要交换 Sequence Length 和 Batch Size 维度
# 或者是将 [Batch, Channels, H, W] 转成画图库支持的 [Batch, H, W, Channels]
x_img = torch.randn(1, 3, 64, 64)
# permute 可以重新排列所有维度 (此处把 Channels 移到最后)
x_permuted = x_img.permute(0, 2, 3, 1)
print(f"Permute 后的形状: {x_permuted.shape}") # 变成 [1, 64, 64, 3]


# 无论是 transpose 还是 permute，它们返回的张量通常与原始张量 共享内存，但在内存中的存储顺序不再是连续的。
# 如果你在执行这些操作后接一个 view() 操作，PyTorch 可能会报错：
# RuntimeError: input is not contiguous
# 解决方法： 在变换维度后调用 .contiguous()。
# 推荐做法 y = x.transpose(0, 1).contiguous().view(-1)
