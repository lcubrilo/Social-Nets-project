import networkx as nx
import matplotlib.pyplot as plt
from statistics import mean
from threading import Thread

def getComponentName(component):
    return component.nodes[list(component.nodes)[0]]["component"]

def showComponentName(pos, component):
    positions = [pos[node] for node in component.nodes]
    x, y = [p[0] for p in positions], [p[1] for p in positions]
    plt.text(mean(x), mean(y), getComponentName(component))

def showComponentNames(pos, components):
    if not components: return
    if type(components) == list:
        for c in components:
            showComponentName(pos, c)
    else: showComponentName(pos, components)

def showGraph(G, components = [], graphname = "graph"):
    graphname += ".dot"
    pos = nx.spring_layout(G, seed=50)
    """
    edge_labels = nx.get_edge_attributes(G,'color')
    print(edge_labels)
    nx.draw_networkx_edge_labels(G, pos, edge_labels)"""

    showComponentNames(pos, components)          

    edAt = nx.get_edge_attributes(G, 'color')
    if edAt :
        edges, edgeColors = zip(*edAt.items())
    else: edgeColors = ["black"]

    """ from networkx.drawing.nx_agraph import write_dot; write_dot(G,graphname)
    import os; Thread(target=lambda: os.startfile(graphname)).start()"""

    #if type(G) == type(nx.MultiGraph()):
        
        ##import pydot; (graph,) = pydot.graph_from_dot_file('multi.dot'); graph.write_png('somefile.png')
        ###from PIL import Image; Image.open('somefile.png').show()
        ####nx.draw(G, pos, edge_color=edgeColors, width=2, with_labels=True, connectionstyle="arc3,rad=0.3")
    #else:
    nx.draw(G, pos, edge_color=edgeColors, width=2, with_labels=True)
    #nx.draw(G, pos)
    plt.show()

import math
import random
def showComponentGraph(components):
    #pos = nx.spring_layout(G, seed=20)
    noComp = len(components)
    nodeColors = giveColors()
    matrixLength = math.ceil(noComp**0.5)
    #baseNumber = 110*matrixLength;
    fig, axs = plt.subplots(matrixLength, matrixLength); i=0
    for c in components:
        #print(c.nodes, c.edges)
        
        #plt.subplot(baseNumber + i%matrixLength + 1); i+=1 
        nodeColor = next(nodeColors, None)
        if not nodeColor: nodeColors = giveColors()
        edgeinfo = nx.get_edge_attributes(c, 'color').items()
        if edgeinfo:
            edges, edgeColors = zip(*edgeinfo)
        else: edgeColors = "black"
        pos = nx.spring_layout(c, seed=random.randint(5, 31415))
        nx.draw(c, pos, node_color = nodeColor, edge_color=edgeColors, width=2, with_labels=True, ax = axs[i//matrixLength, i%matrixLength]); i+=1
        showComponentNames(pos, c)
    plt.show(block=True)

def giveColors():
    sampleColors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 
    'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan']
    random.shuffle(sampleColors)
    return iter(sampleColors)