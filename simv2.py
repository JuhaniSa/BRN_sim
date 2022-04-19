import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap

import random

name = "tab10"
cmap = get_cmap(name)  # type: matplotlib.colors.ListedColormap
colors = cmap.colors  # type: list

plot = True
#cooperation = True

number_of_nodes = 50
nodes = []
messages = []
area = 10000
min_dist = 100
radio_range = 3000
rx_threshold = 2e-7
M = 3

class Node:
    def __init__(self,x,y,pwr) -> None:
        self.x = x
        self.y = y
        self.pwr = pwr
        self.messages = []
        self.tx_slots =[]

class Message:
    def __init__(self,hops,index,sent) -> None:
        self.sender = Node
        self.index = index
        self.hops = hops
        self.sent = sent
        self.nodes = []

def create_nodes(num):
    for i in range(num):
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

        node_ = Node(x,y,15)
        nodes.append(node_)
        i += 1

def test_nodes1():
    node1 = Node(1500,1500,1)
    node2 = Node(4500,4500,3)
    node3 = Node(3000,3000,2)
    node4 = Node(3500,2500,4)
    node5 = Node(4500,3500,5)
    node6 = Node(2500,2500,5)
    nodes.append(node1)
    nodes.append(node2)
    nodes.append(node3)
    nodes.append(node4)
    nodes.append(node5)
    nodes.append(node6)

def test_nodes2():
    node1 = Node(1500,1500,1)
    node2 = Node(3500,3500,3)
    node3 = Node(2500,2500,2)
    node4 = Node(20,2000,4)
    #node5 = Node(45,35,5)
    #node6 = Node(25,25,5)
    nodes.append(node1)
    nodes.append(node2)
    nodes.append(node3)
    nodes.append(node4)
    #nodes.append(node5)
    #nodes.append(node6)

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
   if plot == True:
        plt.arrow(tx.x,tx.y,dx,dy,head_width = area/200,color = colors[color_index%len(colors)],length_includes_head = True)

def add_message(node,id,slot):
    msg = Message(0,id,0)
    messages.append(msg)
    while len(msg.nodes)<slot+1:
        lst = []
        msg.nodes.append(lst)
    msg.nodes[slot].append(node)
    node.messages.append(msg)
    node.tx_slots.append(slot)
    if plot == True:
        circle1 = plt.Circle((node.x,node.y),area/90,fill = True)
        circle = plt.Circle((node.x,node.y),area/90,fill = True)
        ax.add_patch(circle1)
        ax.add_patch(circle)

def receive3(hops,rx):
    noise = rx_threshold
    rx_power = 0.0
    rx_message = 0
    final_tx_nodes = []
    #Tarkasta, ettei vastaanottaja lähetä samainaikaisesti
    if hops not in rx.tx_slots:
        for message in messages:
            tx_nodes = []
            if len(message.nodes)<= hops+1 :
                message.nodes.append([])
            power = 0.0
            for node in message.nodes[hops]:
                if in_range(node,rx):
                    r = (math.sqrt((node.x-rx.x)**2+(node.y-rx.y)**2))
                    if r>0:
                        if message not in rx.messages:
                                power =+ node.pwr/(4*math.pi*(r*r))
                                tx_nodes.append(node)
                        if message in rx.messages:
                            noise = node.pwr/(4*math.pi*(r*r))
    

            #Valitaan uusi lähettäjien joukko, jos vastaanottoteho on riittävä
            if power>(noise+rx_power):
                noise = noise + rx_power
                rx_power = power
                final_tx_nodes = tx_nodes.copy()
                tx_nodes.clear()
                rx_message = message
                power = 0

        if(rx_power<noise):    
            final_tx_nodes.clear()

    if len(final_tx_nodes)>0:
        if rx_power>noise:
            rx_message.nodes[hops+1].append(rx)
            rx.messages.append(rx_message)
            rx.tx_slots.append(hops+1)
            for node in final_tx_nodes:
                draw_arrow(node,rx,hops)

        

def add_info():
    if plot == True:
        for node in nodes:
            i = 0
            for message in node.messages:
                if len(node.tx_slots)>0:
                    if len(node.tx_slots)>i:
                        text='M:{} H:{}'.format(message.index,node.tx_slots[i])
                        plt.annotate(text,(node.x+0.5,node.y+i*area/70))
                i=i+1

def add_n_messages(count,same_slot):
    if same_slot == True:
        for i in range(0,count):
            add_message(nodes[i],i,0)
    if same_slot == False:
         for i in range(0,count):
            add_message(nodes[i],i,i)            

def calculate_recieved(n_messages,nodes):
    received = 0
    for node in nodes:
        received = received + len(node.tx_slots)
    return received/(n_messages*len(nodes))

def random_test():
    create_nodes()
    for node in nodes:
        if plot == True:
            plt.scatter(node.x,node.y,color= 'k')
    add_n_messages(2,True)
    for i in range(0,20):
                for node in nodes:
                    receive3(i,node)
    add_info()
    if plot == True:
        plt.xlim(0,area)
        plt.ylim(0,area)

def scatter_nodes():
    for node in nodes:
        if plot == True:
            plt.scatter(node.x,node.y,color= 'k')

def received():
    res = []
    for j in range(1,20):
        for i in range(0,10):
            nodes.clear()
            messages.clear()
            create_nodes()
            scatter_nodes()
            add_n_messages(j,False)
            for i in range(0,20):
                for node in nodes:
                    receive3(i,node,True)

            res1 = calculate_recieved(j,nodes)
            res.append(res1)
            add_info()
            if plot == True:
                plt.xlim(0,area)
                plt.ylim(0,area)
                plt.show()
    plt.bar(range(len(res)),res)
    plt.show()


fig,ax = plt.subplots()
create_nodes(number_of_nodes)
scatter_nodes()
add_message(nodes[1],0,0)
for i in range(0,10):
    for node in nodes:
        receive3(i,node)
add_info()
if plot == True:
    plt.xlim(0,area)
    plt.ylim(0,area)
    plt.show()
print(calculate_recieved(1,nodes))
