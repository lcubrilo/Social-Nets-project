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

def showGraph(G, components = [], title = "", AX = None, withLabels = True, fontColor = "white", showComponents = True):
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
            
        else: edgeColors = ["black"]; edgeWeights = [1.5]; 
        return edgeColors, edgeWeights
    def getNodeColors():
        if nx.get_node_attributes(G, 'color'):
            return [G.nodes[n]["color"] for n in G.nodes]
        else: return ["blue"]
        
    edgeColors, edgeWeights = getEdgeColorsWeights()
    nodeColors = getNodeColors()

    pos = nx.kamada_kawai_layout(G)
    if showComponents: showComponentNames(pos, components)

    if AX != None: AX.set_title(title)
    else: plt.title(title)

    nx.draw(G, 
        pos,
        edge_color=edgeColors,
        width=edgeWeights,
        node_color=nodeColors,
        with_labels=withLabels,
        font_color=fontColor,
        ax = AX)
    
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

def showGraphs(Graphs, title, maxSize = 4):
    n = min(maxSize**2, len(Graphs))
    if n == 0: return
    if n == 1: showGraph(Graphs[0], title=title); return
    matrixSize = math.ceil(math.sqrt(n))

    graphs = sample(Graphs, maxSize**2) if n > maxSize**2  else Graphs
    subtitle = "Coalition " if title[0] == "C" else "Noncoalition " 
    fig, ax = plt.subplots(matrixSize, matrixSize)
    for i in range(matrixSize):
        for j in range(matrixSize):
            graphIndex = i*matrixSize + j
            if graphIndex == n-1 or graphIndex == maxSize**2-1: break
            graph = graphs[graphIndex]
            showGraph(graph, AX = ax[i, j], showComponents=False, title=subtitle + getComponentName(graph))
    
    fig.suptitle(title)
    plt.show()