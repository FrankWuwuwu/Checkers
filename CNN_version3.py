# Create CNN and train it in this script
## Shuangding Zhu's configuration
import numpy as np
import matplotlib.pyplot as pt
import torch as tr
import math
from data_generator import *
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

class ConvNet(tr.nn.Module):   
    def __init__(self, inputlayer, boardsize, hid_features, kernel_size):
        super(ConvNet, self).__init__()
        C_out_conv2d_1 = boardsize - kernel_size + 1
        C_maxpool2d_1 = math.floor((C_out_conv2d_1 - kernel_size)/kernel_size) + 1
        
        self.cnn_layers = tr.nn.Sequential(
            # inputlayer should always be equal to 1, and output of linear layer should =1 since we only want the utility
             
            # Change struture of CNN here: including boardsize, hid_features, kernal size
            
            # Defining a 2D convolution layer
            tr.nn.Conv2d(inputlayer, hid_features, kernel_size),
            tr.nn.BatchNorm2d(hid_features),
            tr.nn.ReLU(inplace=True),
            tr.nn.MaxPool2d(kernel_size),
            
        )
        
        # Defining Linear layer
        self.linear_layers = tr.nn.Sequential(
            tr.nn.LazyLinear(1),
        )

    # Defining the forward pass    
    def forward(self, x):
        x = self.cnn_layers(x)
        x = x.view(x.size(0), -1)
        x = self.linear_layers(x)
        return x

# Calculates the error on a batch of training examples
def batch_error(net, batch):
    states, utilities = batch
    u = utilities.reshape(-1,1).float()
    y = net(states.float())
    # Meam square error
    e = tr.sum((y - u)**2) / utilities.shape[0]
    return e

def get_baseline_error(batch):
    states, utilities = batch
    u = utilities.reshape(-1,1).float()
    e = tr.sum((0 - u)**2) / utilities.shape[0]
    return e


# Trains the network on some generated data
if __name__ == "__main__":


    # Create CNN
    net = ConvNet(inputlayer=1,boardsize=10,hid_features=4,kernel_size=2)
    # in put board size and hidden features
    #net = ConvNet(size=8, hid_features=8)
    #print(net)
    # Create Optimizer
    net = net.float()
    optimizer = tr.optim.SGD(net.parameters(), lr=0.00001, momentum=0.9)

    # get test dataset
    state_list, utilitie_list = get_traing_data()
    states=[]
    for item in state_list:
        states.append(item.reshape(1,10,10))
    states=np.array(states)
    utilities=np.array(utilitie_list)
    
    # Convert the states and their  utilities to tensors
#    states, utilities = zip(*training_examples)
    print(len(utilities),"training data.",len(utilities)/2, "as training data and rest for testing.")
    slicer=int(len(utilities)/2)
    training_batch = tr.tensor(states[:slicer]), tr.tensor(utilities[:slicer])
    print(training_batch)

    # testing_batch = tr.tensor(states), tr.tensor(utilities)
    testing_batch = tr.tensor(states[slicer:]), tr.tensor(utilities[slicer:])
    
    baseline_error=get_baseline_error(testing_batch)

    # Run the gradient descent iterations
    curves = [], []
    for epoch in range(500):
    
        # zero out the gradients for the next backward pass
        optimizer.zero_grad()


        # batch version (fast)

        e = batch_error(net, training_batch)
        e.backward()
        training_error = e.item()

        with tr.no_grad():
            e = batch_error(net, testing_batch)
            testing_error = e.item()

        # take the next optimization step
        optimizer.step()    
        
        # print/save training progress
        if epoch % 1000 == 0:
            print("%d: %f, %f" % (epoch, training_error, testing_error))
        curves[0].append(training_error)
        curves[1].append(testing_error)
        
    # visualize learning curves on train/test data
    pt.plot(curves[0], 'b-')
    pt.plot(curves[1], 'r-')
    #pt.plot([0, len(curves[1])], [baseline_error, baseline_error], 'g-')
    pt.plot()
    pt.legend(["Train","Test","Baseline"])
        
    pt.savefig('CNN3.jpg')
    pt.show()
    tr.save(net.state_dict(),'model/CNN3.pkl')


