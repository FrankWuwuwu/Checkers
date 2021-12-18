# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 05:04:16 2021

@author: iamga
"""

# Create CNN and train it in this script
import numpy as np
import matplotlib.pyplot as pt
import torch as tr
import math

class ConvNet(tr.nn.Module):   
    def __init__(self, inputlayer, boardsize, hid_features, kernel_size):
        super(ConvNet, self).__init__()
        C_out_conv2d_1 = boardsize - kernel_size + 1
        C_maxpool2d_1 = math.floor((C_out_conv2d_1 - kernel_size)/kernel_size) + 1
        C_out_con2d_2 = C_maxpool2d_1 - kernel_size + 1
        C_maxpool2d_2 = math.floor((C_out_con2d_2 - kernel_size)/kernel_size) + 1
        
        self.cnn_layers = tr.nn.Sequential(
            # inputlayer should always be equal to 1, and output of linear layer should =1 since we only want the utility
             
            # Change struture of CNN here: including boardsize, hid_features, kernal size
            
            # Defining a 2D convolution layer
            tr.nn.Conv2d(inputlayer, hid_features, kernel_size),
            tr.nn.BatchNorm2d(hid_features),
            tr.nn.ReLU(inplace=True),
            tr.nn.MaxPool2d(kernel_size),
            
            # Defining another 2D convolution layer
            tr.nn.Conv2d(hid_features, hid_features, kernel_size),
            tr.nn.BatchNorm2d(hid_features),
            tr.nn.ReLU(inplace=True),
            tr.nn.MaxPool2d(kernel_size),
        )
        
        # Defining Linear layer
        self.linear_layers = tr.nn.Sequential(
            tr.nn.Linear(C_maxpool2d_2**2*hid_features, hid_features * (boardsize-1)**2),
            tr.nn.Linear(hid_features * (boardsize-1)**2, 1)
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


# Trains the network on some generated data
if __name__ == "__main__":


    # Create CNN
    net = ConvNet(inputlayer=1,boardsize=8,hid_features=4,kernel_size=2)
    # in put board size and hidden features
    #net = ConvNet(size=8, hid_features=8)
    #print(net)
    # Create Optimizer
    net = net.float()
    optimizer = tr.optim.SGD(net.parameters(), lr=0.00001, momentum=0.9)

    # example/format of states and untilities  
    states = [np.random.rand(1,8,8), np.random.rand(1,8,8)]
    utilities = [0,1]
    # Convert the states and their  utilities to tensors
#    states, utilities = zip(*training_examples)
    training_batch = tr.tensor(states), tr.tensor(utilities)
    print(training_batch)

#    states, utilities = zip(*testing_examples)
    testing_batch = tr.tensor(states), tr.tensor(utilities)

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
        pt.plot()
        pt.legend(["Train","Test","Baseline"])
        pt.show()
