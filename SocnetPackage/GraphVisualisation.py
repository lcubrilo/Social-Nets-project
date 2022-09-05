import networkx as nx
import matplotlib.pyplot as plt
from statistics import mean
from threading import Thread
from .ComponentNamesColors import giveColors
from random import sample

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

def showGraph(G, components = [], title = "", AX = None, withLabels = None, fontColor = "white"):
    from time import time
    start = time()
    if title == "": title = str(G)

    def getEdgeColorsWeights():
        edAt = nx.get_edge_attributes(G, 'color')
        if edAt :
            edges, edgeColors = zip(*edAt.items())
            edgeWeights = []
            for e, eC in zip(edges, edgeColors):
                weight_val = 1 if eC == "green" else 3
                G.add_edge(e[0], e[1], weight = weight_val/0.5)
                edgeWeights.append(3/weight_val)
            
        else: edgeColors = ["black"]; weights = [1.5]; 
        return edgeColors, edgeWeights
    def nodeColors():
        ndAt = nx.get_node_attributes(G, 'color')
        if ndAt:
            nodeColors = [G.nodes[n]["color"] for n in G.nodes]
        else:
            nodeColors = ["blue"]
            return nodeColors()
    edgeColors, edgeWeights, nodeColors = getEdgeColorsWeights(), nodeColors()

    pos = nx.kamada_kawai_layout(G)
    showComponentNames(pos, components)
    nx.draw(G, pos, edge_color=edgeColors, width=edgeWeights, node_color=nodeColors, with_labels=withLabels, font_color=fontColor, title=title, ax = AX)
    
    if AX == None:plt.show()
    #print(time()-start, G)

import math
def showComponentGraph(components):
    #pos = nx.kamada_kawai_layout(G, seed=20)
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
        pos = nx.kamada_kawai_layout(c)
        AX = axs[i//matrixLength, i%matrixLength] if matrixLength > 1 else axs
        nx.draw(c, pos, node_color = nodeColor, edge_color=edgeColors, width=2, with_labels=True, ax = AX); i+=1
        showComponentNames(pos, c)
    plt.show(block=True)

def showGraphAndComponents(G, components, G2, ttl):
    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.set_title(ttl[1]); ax2.set_title(ttl[2])
    fig.suptitle(ttl[0])
    showGraph(G2, AX = ax1)
    showGraph(G, components, AX = ax2)
    
    plt.show()

def showGraphs(Graphs):
    n = min(36, len(Graphs))
    matrixSize = math.ceil(math.sqrt(n))

    graphs = sample(Graphs, 36) if n == 36  else Graphs

    fig, ax = plt.subplots(n,n)
    for i in range(matrixSize):
        for j in range(matrixSize):
            showGraph(graphs[i*matrixSize + j], ax[i][j])

    plt.show()