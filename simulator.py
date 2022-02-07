
from cProfile import label
from logging import exception
from tkinter import Y
from turtle import color, delay, update, width
import numpy
import math
import copy
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap

import random

name = "Accent"
cmap = get_cmap(name)  # type: matplotlib.colors.ListedColormap
colors = cmap.colors  # type: list



number_of_nodes = 100
nodes = []
area = 1500
min_dist = 50
radio_range = 400


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

def update(current_slot):
    for node in nodes:
        for message in node.messages:
            if message.hops < current_slot:
                transmit(node,message)

def in_range(node1,node2):
    dist = (math.sqrt((node1.x-node2.x)**2+(node1.y-node2.y)**2))
    if dist<radio_range:
        return True
    else:
        return False

def draw_arrow(tx,rx,color_index):
   offset = 2
   dist = (math.sqrt((tx.x-tx.x)**2+(tx.y-rx.y)**2))
   dx =  (rx.x-tx.x)
   dy =  (rx.y-tx.y)
   #dy = end_y-tx.y
   #dx = end_x-tx.x
   plt.arrow(tx.x,tx.y,dx,dy,head_width = area/200,color = colors[color_index%len(colors)],length_includes_head = True)

def transmit(transmitter,message):
 
    for node2 in nodes:
        if in_range(transmitter,node2):
            if len(node2.messages) == 0:
                #plt.plot([transmitter.x,node2.x],[transmitter.y,node2.y],color = colors[message.hops%len(colors)])
                #plt.plot([transmitter.x,node2.x],[transmitter.y,node2.y],color = colors[message.index])
                draw_arrow(transmitter,node2,message.hops)
                new_message=copy.copy(message)
                new_message.hops = message.hops +1
                node2.messages.append(new_message)

            if not any(obj.index == message.index for obj in node2.messages):
                #plt.plot([transmitter.x,node2.x],[transmitter.y,node2.y],color = colors[message.hops%len(colors)])
                #plt.plot([transmitter.x,node2.x],[transmitter.y,node2.y],color = colors[message.index])
                draw_arrow(transmitter,node2,message.hops)
                new_message=copy.copy(message)
                new_message.hops = message.hops +1
                node2.messages.append(new_message)


            if any(obj.index == message.index and obj.hops == message.hops+1 for obj in node2.messages):
                #plt.plot([transmitter.x,node2.x],[transmitter.y,node2.y],color = colors[message.hops%len(colors)])
                #plt.plot([transmitter.x,node2.x],[transmitter.y,node2.y],color = colors[message.index])
                draw_arrow(transmitter,node2,message.hops)
                pass



                
               


for i in range(number_of_nodes):
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
    plt.scatter(node.x,node.y,color= 'k')
    #DEBUG Draw circle of minimum distance
    #circle = plt.Circle((node.x,node.y),min_dist,fill = False)
    #ax.add_patch(circle)

#plot lines reprecenting channels between nodes
message = Message(0,0,0)
message2 = Message(1,1,0)
nodes[2].messages.append(message)
#nodes[3].messages.append(message2)
#circle1 = plt.Circle((nodes[2].x,nodes[2].y),min_dist,fill = False)
#circle2 = plt.Circle((nodes[3].x,nodes[3].y),min_dist,fill = False)
#ax.add_patch(circle1)
#ax.add_patch(circle2)
#nodes[6].messages.append(message2)
for i in range(0,3):
    update(i)
plt.xlim([0,area])
plt.ylim([0,area])
plt.show()




