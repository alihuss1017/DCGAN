import torch
import torch.nn as nn
import torch.optim as optim

def trainDiscriminator(D, G, optimD, data, device):

    criterion = nn.BCELoss()
    D.zero_grad()
    realOutput = D(data.to(device)).view(-1)
    realLoss = criterion(realOutput, torch.ones_like(realOutput).to(device))
    realLoss.backward()

    noise = torch.randn(64, 100, 1, 1).to(device)
    fakeOutput = D(G(noise).detach()).view(-1)
    fakeLoss = criterion(fakeOutput,  torch.zeros_like(fakeOutput, dtype = torch.float).to(device))

    fakeLoss.backward()
    optimD.step()
    loss = fakeLoss + realLoss
    return loss, realOutput, fakeOutput

def trainGenerator(D, G, optimG, data, device):
    criterion = nn.BCELoss()
    G.zero_grad()
    noise = torch.randn(64, 100, 1, 1).to(device)
    output = D(G(noise)).view(-1)
    loss = criterion(output, torch.ones_like(output))
    loss.backward()

    optimG.step()
    return loss