import torch 
import torchvision
from torchvision import transforms, datasets

train = datasets.MNIST("", train = True, download = True, transform = transforms.Compose([transforms.ToTensor()]))

test = datasets.MNIST("", train = False, download = True, transform = transforms.Compose([transforms.ToTensor()]))

trainset = torch.utils.data.DataLoader(train, batch_size = 10, shuffle = True) #Batch Size: How many do you want to pass through your model each time?, 
testset = torch.utils.data.DataLoader(test, batch_size = 10, shuffle = True)

import torch.nn as nn #oop
import torch.nn.functional as F #functions

class Net(nn.Module): 
    def __init__(self): #Define fully connected layers to the neural network
        super().__init__()
        self.fc1 = nn.Linear(28*28, 64)
        self.fc2 = nn.Linear(64, 64) #Hidden Layers
        self.fc3 = nn.Linear(64, 64)
        self.fc4 = nn.Linear(64, 10)

    def forward(self, x): 
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        x = self.fc4(x)
        return F.log_softmax(x, dim = 1)


net = Net()
print(net)

X = torch.rand((28, 28))
X = X.view(1, 28*28)
output = net(X)
print(output)

import torch.optim as optim

optimizer = optim.Adam(net.parameters(), lr = 0.001) #1, everything that is adjustable in our model, Learning Rate

EPOCHS = 3 #Make Three Passes though our data

for epoch in range(EPOCHS):
    for data in trainset: 
        X, Y = data
        net.zero_grad() #Contain loss
        output = net(X.view(-1, 28*28)) #Pass Through Neural Network
        loss = F.nll_loss(output, Y)
        loss.backward() #Backward Propagation
        optimizer.step() #Adjust the weight for us
    print(loss)

correct = 0 
total = 0
with torch.no_grad():
    for data in trainset: 
        X, Y = data
        output = net(X.view(-1, 28 * 28))
        for idx, i in enumerate(output): 
            if torch.argmax(i) == Y[idx]:
                correct += 1
            total += 1
print("Accuracy: ", round(correct/total, 3))