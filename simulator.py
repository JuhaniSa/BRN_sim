
from tkinter import Y
from turtle import color, delay, update
import numpy
import math
import copy
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap

import random

name = "Accent"
cmap = get_cmap(name)  # type: matplotlib.colors.ListedColormap
colors = cmap.colors  # type: list



number_of_nodes = 60
nodes = []
area = 1000
min_dist = 50
radio_range = 200


class Node:
    def __init__(self,x,y,power) -> None:
        self.x = x
        self.y = y
        self.power = power
        self.messages = []
        pass

class Message:
    def __init__(self,hops,index,sent) -> None:
        self.sender = Node
        self.index = index
        self.hops = hops
        self.sent = sent
        pass

def update():
    for node in nodes:
        for message in node.messages:
            if message.sent == False:
                transmit(node,message)

def in_range(node1,node2):
    dist = (math.sqrt((node1.x-node2.x)**2+(node1.y-node2.y)**2))
    if dist<radio_range:
        return True
    else:
        return False


def transmit(transmitter,message):
 
    for node2 in nodes:
        if in_range(transmitter,node2):
            for recieved_message in node2.messages:
                if message.index == recieved_message.index:
                    if message.hops == recieved_message.hops:
                        #plt.plot([transmitter.x,node2.x],[transmitter.y,node2.y],color = colors[4])
                        pass
                
                
            if len(node2.messages)==0:
                plt.plot([transmitter.x,node2.x],[transmitter.y,node2.y],color = colors[message.hops%len(colors)])
                new_message=copy.copy(message)
                new_message.hops = message.hops +1
                node2.messages.append(new_message)
                
            

#Place nodes to the area with minimum distance in between
i=0
while i < number_of_nodes:
    y = random.randint(0,area)
    x = random.randint(0,area)
    try:
        for node2 in nodes:
                dist = (math.sqrt((node2.x-x)**2+(node2.y-y)**2))
                if dist<=min_dist:
                    y = random.randint(0,area)
                    x = random.randint(0,area)
                    raise Exception
    except Exception:
        continue

    node_ = Node(x,y,i)
    nodes.append(node_)
    i += 1


#plot nodes to area
fig,ax = plt.subplots()
for node in nodes:
    plt.scatter(node.x,node.y,color=colors[0])
    #DEBUG Draw circle of minimum distance
    #circle = plt.Circle((node.x,node.y),min_dist,fill = False)
    #ax.add_patch(circle)

#plot lines reprecenting channels between nodes


message = Message(0,1,0)
message2 = Message(1,2,0)
nodes[2].messages.append(message)
circle = plt.Circle((nodes[2].x,nodes[2].y),min_dist,fill = False)
ax.add_patch(circle)
#nodes[6].messages.append(message2)
for i in range(1,5):
    update()
plt.show()




