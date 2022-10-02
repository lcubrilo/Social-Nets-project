import networkx as nx
import matplotlib.pyplot as plt
from statistics import mean
from threading import Thread

# from SocnetPackage.MetricPlots import correlations was this here for a reason?
from .ComponentNamesColors import giveColors
from random import sample

# Component names hovering above in graph drawing
def getComponentName(component):
    return component.nodes[list(component.nodes)[0]]["component"]

def showComponentName(pos, component):
    positions = [pos[node] for node in component.nodes]
    x_axis, y_axis = [p[0] for p in positions], [p[1] for p in positions]
    plt.text(mean(x_axis), mean(y_axis), getComponentName(component))

def showComponentNames(pos, components):
    if not components: 
        return
    if type(components) == list: # TODO: why this if??
        for c in components:
            showComponentName(pos, c)
    else: showComponentName(pos, components)

# TODO check if this still makes sense
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

# TODO check this too
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

# TODO check if this deprecated
def showGraphAndComponents(G, components, G2, ttl):
    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.set_title(ttl[1]); ax2.set_title(ttl[2])
    fig.suptitle(ttl[0])
    showGraph(G2, AX = ax1)
    showGraph(G, components, AX = ax2)
    
    plt.show()

# TODO check if ok, bad or deprecated
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
            graph = graphs[graphIndex] if type(graphs) == list else graphs
            showGraph(graph, AX = ax[i, j], showComponents=False, title=subtitle + getComponentName(graph))
    
    fig.suptitle(title)
    plt.show()

#DISTRIBUTIONS
from math import log2
from SocnetPackage.Metrics import Correlations
def showDistribution(x_axis, y_axis, metricName, graphName = ""):
    fig, axs = plt.subplots(2, 2, constrained_layout = True)
    #fig.tight_layout()

    xlabels = [metricName]*3 + ["log " + metricName]
    ylabels = ["Frequency", "CCD Frequency", "log CCDF", "log CCDF"]
    titles = ["Distribution of "+metricName, "Complementary cumulative", "Linear == exp distr", "Linear == pow distr"]
    correlations = []
    # nothing
    # accumulate that
    # log y of that
    # also log x of that
    for (xl, yl, ttl, ax) in zip(xlabels, ylabels, titles, axs.flatten()):
        if yl[:3] == "log" and xl[:3] != "log": y_axis = [log2(e) if e>0 else 0.0 for e in y_axis]
        if xl[:3] == "log": x_axis = [log2(e) if e > 0 else 0.0 for e in x_axis]
        if yl[:3] == "CCD": 
            n = len(y_axis)
            for i in list(range(n-1, 0, -1)):
                y_axis[i-1] += y_axis[i]
            #print("Odradio CCD")
        corrMsg, corrAmount = Correlations.correlData(x_axis, y_axis, "-", False, printReport=False)
        correlations.append(corrAmount)
        ax.set(xlabel=xl, ylabel=yl, title=ttl+corrMsg)
        ax.scatter(x_axis, y_axis)

    Correlations.distReport(metricName, correlations)

    suptitle = "{} - {}".format(metricName.upper(), graphName)
    plt.suptitle(suptitle)
    #plt.subplots_adjust(left=0.25, right=0.8, bottom=0.2, top=0.8, wspace= 0.4, hspace=0.8)
    plt.savefig(suptitle+'.pdf')
    plt.show()

#CORRELATIONS TODO
def showCorrelation(x_axis, y_axis, metricName1, metricName2, graphName = ""):
    fig, axs = plt.subplots(1, 1, constrained_layout = True) #(2, 2, constrained_layout = True)
    
    ttl = "{} - {} & {}".format(graphName.upper(), metricName1.upper(), metricName2.upper())
    axs.set(xlabel=metricName1, ylabel=metricName2, title=ttl+Correlations.correlData(x_axis, y_axis, ttl, False))
    axs.scatter(x_axis, y_axis)
    plt.show()