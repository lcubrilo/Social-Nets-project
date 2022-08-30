import networkx as nx
import matplotlib.pyplot as plt

def showGraph(G):
    pos = nx.spring_layout(G, seed=50)
    """
    edge_labels = nx.get_edge_attributes(G,'color')
    print(edge_labels)
    nx.draw_networkx_edge_labels(G, pos, edge_labels)"""

    edges, edgeColors = zip(*nx.get_edge_attributes(G, 'color').items())
    nx.draw(G, pos, edge_color=edgeColors, width=2, with_labels=True)
    #nx.draw(G, pos)
    plt.show()

import math
import random
def showComponentGraph(G, components):
    pos = nx.spring_layout(G, seed=20)
    noComp = len(components)
    nodeColors = []
    baseNumber = 110*min(9, math.ceil(noComp**0.5)); i=1
    for c in components:
        #print(c.nodes, c.edges)
        pos = nx.spring_layout(c, seed=random.randint(5, 31415))
        plt.subplot(baseNumber+i); i+=1 
        if not nodeColors: nodeColors = giveColors()
        edgeinfo = nx.get_edge_attributes(c, 'color').items()
        if edgeinfo:
            edges, edgeColors = zip(*edgeinfo)
        else: edgeColors = "black"
        nx.draw(c, pos, node_color = next(nodeColors), edge_color=edgeColors, width=2, with_labels=True)
    plt.show()

def giveColors():
    sampleColors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 
    'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan']
    random.shuffle(sampleColors)
    return iter(sampleColors)