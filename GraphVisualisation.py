import networkx as nx
import matplotlib.pyplot as plt
from statistics import mean
from threading import Thread
from ComponentNamesColors import giveColors

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

def showGraph(G, components = [], graphname = "graph", AX = None):
    graphname += ".dot"
    
    """
    edge_labels = nx.get_edge_attributes(G,'color')
    print(edge_labels)
    nx.draw_networkx_edge_labels(G, pos, edge_labels)"""

    edAt = nx.get_edge_attributes(G, 'color')
    if edAt :
        edges, edgeColors = zip(*edAt.items())
        weights = []
        for e, eC in zip(edges, edgeColors):
            weight_val = 1 if eC == "green" else 3
            G.add_edge(e[0], e[1], weight = weight_val/0.5)
            weights.append(3/weight_val)
        
    else: edgeColors = ["black"]; weights = [1.5]; 
    
    nodeColors = [G.nodes[n]["color"] for n in G.nodes]
    
    pos = nx.kamada_kawai_layout(G)
    showComponentNames(pos, components)
    """ from networkx.drawing.nx_agraph import write_dot; write_dot(G,graphname)
    import os; Thread(target=lambda: os.startfile(graphname)).start()"""

    #if type(G) == type(nx.MultiGraph()):
        
        ##import pydot; (graph,) = pydot.graph_from_dot_file('multi.dot'); graph.write_png('somefile.png')
        ###from PIL import Image; Image.open('somefile.png').show()
        ####nx.draw(G, pos, edge_color=edgeColors, width=2, with_labels=True, connectionstyle="arc3,rad=0.3")
    #else:
    nx.draw(G, pos, edge_color=edgeColors, width=weights, node_color=nodeColors, with_labels=type(list(G.nodes)[0])==str, font_color='white', ax = AX)
    #nx.draw(G, pos)
    if AX == None:
        plt.show()

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

def showGraphAndComponents(G, components, G2):
    fig, (ax1, ax2) = plt.subplots(1, 2)
    showGraph(G2, AX = ax1)
    showGraph(G, components, AX = ax2)
    
    plt.show()
