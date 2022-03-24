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

plot = True

number_of_nodes = 30
nodes = []
messages = []
area = 100
min_dist = 1
radio_range = 40
M = 3

noise = 0
rx_threshold = 0
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

        node_ = Node(x,y,10)
        nodes.append(node_)
        i += 1

def test_nodes1():
    node1 = Node(15,15,1)
    node2 = Node(45,45,3)
    node3 = Node(30,30,2)
    node4 = Node(35,25,4)
    node5 = Node(45,35,5)
    node6 = Node(25,25,5)
    nodes.append(node1)
    nodes.append(node2)
    nodes.append(node3)
    nodes.append(node4)
    nodes.append(node5)
    nodes.append(node6)

def test_nodes2():
    node1 = Node(15,15,1)
    node2 = Node(35,35,3)
    node3 = Node(25,25,2)
    node4 = Node(20,20,4)
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
        circle1 = plt.Circle((node.x,node.y),0.5,fill = True)
        circle = plt.Circle((node.x,node.y),0.5,fill = True)
        ax.add_patch(circle1)
        ax.add_patch(circle)

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
                                if plot == True:
                                    circle3 = plt.Circle((rx.x,rx.y),2,fill = False,color = colors[6])
                                    ax.add_patch(circle3)
                                tx_nodes.clear()
                                final_tx_nodes.clear()
                                power = 0

                        #Jos vastaanottaja vastaanottaa toista viestiä
                        if (hops+1) in rx.tx_slots:
                            if plot == True:
                                circle4 = plt.Circle((rx.x,rx.y),4,fill = False,color = colors[7])
                                ax.add_patch(circle4)
                            tx_nodes.clear()
                            final_tx_nodes.clear()
                            rx.tx_slots.pop()
                            power = 0


                        else:
                            power = power + 1*1/(r**2)  
                            #tallenna lähettäjät
                            tx_nodes.append(node)

        #Jos mahdollinen lähettäjä löytyy:   
        if power>0:
            if len(tx_nodes)>0:
                if (hops)not in rx.tx_slots:             
                    rx.tx_slots.append(hops+1)
                    rx_message = message
                    final_tx_nodes = tx_nodes
                

    if len(final_tx_nodes)>0:
        rx_message.nodes[hops+1].append(rx)
        rx.messages.append(rx_message)
        for node in final_tx_nodes:
            draw_arrow(node,rx,hops)
   
def recieve2(hops,rx):
    tx_nodes = []
    final_tx_nodes = []
    noise = 0
    rx_power = 0.0
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
                                if plot == True:
                                    circle3 = plt.Circle((rx.x,rx.y),2,fill = False,color = colors[6])
                                    ax.add_patch(circle3)
                                tx_nodes.clear()
                                final_tx_nodes.clear()
                                

                        #Jos vastaanottaja vastaanottaa toista viestiä
                        if (hops+1) in rx.tx_slots:
                            if plot == True:
                                circle4 = plt.Circle((rx.x,rx.y),4,fill = False,color = colors[7])
                                ax.add_patch(circle4)
                            power =+ node.pwr/(r**2)  
                            #tallenna lähettäjät
                            tx_nodes.append(node)

                        else:
                            power =+ node.pwr/(r**2)  
                            #tallenna lähettäjät
                            tx_nodes.append(node)

                    else:
                        noise =+ node.pwr/(r*r)
                        
        #jos lähettäjiä                
        if len(tx_nodes)>0:
            #Jos vastaanotettava teho on suurempi kuin kohina
            if power>(noise+rx_power):       
                rx_message = message
                final_tx_nodes.clear()
                final_tx_nodes = tx_nodes.copy()
                rx_power = power
                rx.tx_slots.append(hops+1)
                tx_nodes.clear()
                power = 0
            else:

                power = 0
                tx_nodes.clear()

    if noise>rx_power:
            final_tx_nodes.clear()
            tx_nodes.clear()
            #rx.tx_slots.pop()    

    if len(final_tx_nodes)>0:
        if rx_power>noise:
            rx_message.nodes[hops+1].append(rx)
            rx.messages.append(rx_message)
            rx.tx_slots.append(hops+1)
            for node in final_tx_nodes:
                draw_arrow(node,rx,hops)

def receive3(hops,rx):
    noise = 0
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
                            power =+ node.pwr/(r*r)
                            tx_nodes.append(node)
                        if message in rx.messages:
                            noise = node.pwr/(r*r)
            #Valitaan uusi lähettäjien joukko, jos vastaanottoteho on riittävä
            if power>(noise+rx_power):
                noise = noise + rx_power
                rx_power = power
                final_tx_nodes = tx_nodes.copy()
                tx_nodes.clear()
                rx_message = message
                power = 0

      

        #Uusi vastaanotettava viesti
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
                        plt.annotate(text,(node.x+0.5,node.y+i*1.2))
                i=i+1

def add_n_messages(count,same_slot):
    if same_slot == True:
        for i in range(0,count):
            add_message(nodes[i],i,0)
    if same_slot == False:
         for i in range(0,count):
            add_message(nodes[i],i,i)            


#create nodes
#create_nodes()
#Törmäys nodessa:

#Törmäys siirtotiessä:
#test_nodes2()

nodes.clear()
messages.clear()
create_nodes()
fig,ax = plt.subplots()
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
    plt.show()
