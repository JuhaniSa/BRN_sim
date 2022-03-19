from asyncio.windows_events import NULL
import numpy as np
import math
import copy
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap

import random

name = "tab10"
cmap = get_cmap(name)  # type: matplotlib.colors.ListedColormap
colors = cmap.colors  # type: list



number_of_nodes = 40
nodes = []
messages = []
area = 60
min_dist = 3
radio_range = 15
M = 3


class Node:
    def __init__(self,x,y,power) -> None:
        self.x = x
        self.y = y
        self.power = power
        self.messages = []
        self.tx_slots =[]


class Message:
    def __init__(self,hops,index,sent) -> None:
        self.sender = Node
        self.index = index
        self.hops = hops
        self.sent = sent
        self.nodes = []


def create_nodes():
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

def test_nodes():
    node1 = Node(15,15,1)
    node2 = Node(45,45,3)
    node3 = Node(30,30,2)
    #node4 = Node(35,25,4)
    node5 = Node(45,35,5)
    node6 = Node(25,25,5)
    nodes.append(node1)
    nodes.append(node2)
    nodes.append(node3)
    #nodes.append(node4)
    nodes.append(node5)
    nodes.append(node6)

def in_range(node1,node2):
    dist = (math.sqrt((node1.x-node2.x)**2+(node1.y-node2.y)**2))
    if dist<radio_range:
        return True
    else:
        return False

def dist(node1,node2):
    return (math.sqrt((node1.x-node2.x)**2+(node1.y-node2.y)**2))

def draw_arrow(tx,rx,color_index):
   offset = 0
   dx1 =(rx.x-tx.x)
   dy1 =(rx.y-tx.y)
   alpha = math.atan2(dy1,dx1)
   if alpha < 0:
       alpha += 2*math.pi

   dx =  dx1-math.cos(alpha)*offset*np.sign(rx.x-tx.x)
   dy =  dy1-math.sin(alpha)*offset*np.sign(rx.y-tx.y)
   plt.arrow(tx.x,tx.y,dx,dy,head_width = area/200,color = colors[color_index%len(colors)],length_includes_head = True)

def add_message(node,id):
    msg = Message(0,id,0)
    messages.append(msg)
    lst = []
    msg.nodes.append(lst)
    msg.nodes[0].append(node)
    node.messages.append(msg)
    node.tx_slots.append(0)

def recieve(hops,rx):
    tx_nodes = []
    final_tx_nodes = []
    rx_message = NULL
    rx_power = 0.0
    no_rx = 0
    for message in messages:
        if len(message.nodes)<= hops+1 :
            message.nodes.append([])
        power = 0.0
        for node in message.nodes[hops]:
            if in_range(node,rx):
                r = (math.sqrt((node.x-rx.x)**2+(node.y-rx.y)**2))
                if r>0:
                    if message not in rx.messages:
                        #jos vastaanottaja lähettää samanaikaisesti
                        r = (math.sqrt((node.x-rx.x)**2+(node.y-rx.y)**2))
                        if hops in rx.tx_slots:
                            if r>0:
                                circle3 = plt.Circle((rx.x,rx.y),2,fill = False,color = colors[6])
                                ax.add_patch(circle3)
                                if message in rx.messages:
                                    rx.messages.remove(message)
                                tx_nodes.clear()
                                final_tx_nodes.clear()
                                


                        #Jos vastaanottaja vastaanottaa toista viestiä
                        if hops+1 in rx.tx_slots:
                            #circle4 = plt.Circle((rx.x,rx.y),4,fill = False,color = colors[7])
                            #ax.add_patch(circle4)
                            if message in rx.messages:
                                rx.messages.remove(message)
                            tx_nodes.clear()
                            final_tx_nodes.clear()


                        else:
                            if r>0:
                                power = power + 1*1/(r**2)  
                                #tallenna    lähettäjät
                                tx_nodes.append(node)

        #Jos mahdollinen lähettäjä löytyy:   
        if power>0:              
            rx.tx_slots.append(hops+1)
            rx.messages.append(message)
            final_tx_nodes = tx_nodes
            message.nodes[hops+1].append(rx)

    for node in final_tx_nodes:
        draw_arrow(node,rx,hops)

    
            
            
            


#create nodes
create_nodes()
#test_nodes()
                


#plot nodes to area
fig,ax = plt.subplots()
for node in nodes:
    plt.scatter(node.x,node.y,color= 'k')
    #DEBUG Draw circle of minimum distance
    #circle = plt.Circle((node.x,node.y),min_dist,fill = False)
    #ax.add_patch(circle)

#plot lines reprecenting channels between nodes
add_message(nodes[0],1)
add_message(nodes[1],2)
circle1 = plt.Circle((nodes[0].x,nodes[0].y),radio_range,fill = False)
circle = plt.Circle((nodes[1].x,nodes[1].y),radio_range,fill = False)
ax.add_patch(circle1)
ax.add_patch(circle)
for i in range(0,5):
    for node in nodes:
        recieve(i,node)

for node in nodes:
    i = 0
    for message in node.messages:
        if len(node.tx_slots)>0:
            text='M:{} H:{}'.format(message.index,node.tx_slots[i])
            plt.annotate(text,(node.x+0.5,node.y+i*0.8))
        i=i+1


#draw map
plt.xlim(0,area)
plt.ylim(0,area)
plt.show()