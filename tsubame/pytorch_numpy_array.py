a = torch.rand(1,2,3,4)
print(a.transpose(0,3).transpose(1,2).size())
print(a.permute(3,2,1,0).size())
squeeze(x)

x = np.ones((1, 2, 3))
>>> np.transpose(x, (1, 0, 2)).shape
(2, 1, 3)
np.squeeze(x)
