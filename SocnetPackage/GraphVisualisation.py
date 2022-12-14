from re import X
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
def showGraph(G, components = [], title = "", AX = None, withLabels = True, fontColor = "white", showComponents = True, sourceDataFileName = "lolexd", saveDirName = "", suptitle = ""):
    from time import time
    start = time()
    plt.figure(figsize=(14,10))
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
    
    if AX == None:
        plt.suptitle(suptitle)
        plt.savefig(fname="Report/{}/{}/SocialNetwork.png".format(sourceDataFileName, saveDirName))
        plt.show()
        
    #print(time()-start, G)

# TODO check this too
import math
def showComponentGraph(components):
    #pos = nx.kamada_kawai_layout(G, seed=20)
    noComp = len(components)
    nodeColors = giveColors()
    matrixLength = math.ceil(noComp**0.5)
    #baseNumber = 110*matrixLength;
    fig, axs = plt.subplots(matrixLength, matrixLength, figsize=(14,10)); i=0
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
    #plt.show(block=True)

# TODO check if this deprecated
def showGraphAndComponents(G, components, G2, ttl):
    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.set_title(ttl[1]); ax2.set_title(ttl[2])
    fig.suptitle(ttl[0])
    showGraph(G2, AX = ax1)
    showGraph(G, components, AX = ax2)
    
    #plt.show()

def showGraphs(Graphs, subtitle, maxSize = 4, sourceDataFileName = "", graphName = ""):
    n = min(maxSize**2, len(Graphs))
    if n == 0: return
    if n == 1: showGraph(Graphs[0], title=graphName, sourceDataFileName=sourceDataFileName); return
    matrixSize = math.ceil(math.sqrt(n))

    graphs = sample(Graphs, maxSize**2) if n > maxSize**2  else Graphs
    #subtitle = "Coalition " if title[0] == "C" else "Noncoalition " 
    fig, ax = plt.subplots(matrixSize, matrixSize, figsize=(14,10))
    for i in range(matrixSize):
        for j in range(matrixSize):
            graphIndex = i*matrixSize + j
            if graphIndex >= len(graphs): break
            if graphIndex == n-1 or graphIndex == maxSize**2-1: break
            graph = graphs[graphIndex] if type(graphs) == list else graphs
            showGraph(graph, AX = ax[i, j], showComponents=False, title=subtitle + getComponentName(graph))
    
    fig.suptitle(graphName)
    plt.savefig(fname="Report/{}/{}/{}.png".format(sourceDataFileName, graphName, subtitle))

#DISTRIBUTIONS
from math import log2
from SocnetPackage.Metrics import Correlations
def showDistribution(x_axis, y_axis, metricName, graphName = "", coalitions = [], components = [], sourceDataFileName = ""):
    fig, axs = plt.subplots(2, 2, constrained_layout = True, figsize=(14,10))
    #fig.tight_layout()

    xlabels = [metricName]*3 + ["log " + metricName]
    ylabels = ["Frequency", "CCD Frequency", "log CCDF", "log CCDF"]
    titles = ["Distribution of "+metricName, "Complementary cumulative", "Linear == exp distr", "Linear == pow distr"]
    correlations = []

    ###############################    
    # nothing
    # accumulate that
    # log y of that
    # also log x of that
    def fillingAXsCoalNonc(x_axis, y_axis, color = "black", shape="o"):
        correlMsgs = []
        debugMsg = ""
        for (xl, yl, ttl, ax) in zip(xlabels, ylabels, titles, axs.flatten()):  
            if xl[:3] == "log": # Fourth step
                x_axis = [log2(e) if e>0 else 0.0 for e in x_axis]; 

            elif yl[:3] == "log": # Third step
                y_axis = [log2(e) if e>0 else 0.0 for e in y_axis]; 

            elif yl[:3] == "CCD": # Second step
                #debugMsg = str(y_axis) 
                for i in list(range(len(y_axis)-1, 0, -1)):
                    y_axis[i-1] += y_axis[i]

            # First step - just original data

            # Common part
            corrMsg, corrAmount = Correlations.correlData(x_axis, y_axis, xl+"-"+yl, False, printReport=False)
            ax.set(xlabel=xl, ylabel=yl, title=ttl+corrMsg)
            ax.scatter(x_axis, y_axis, c=color, marker=shape, s = (800)/(len(x_axis)+1))
            correlMsgs.append(corrMsg)
            #if str(corrAmount) == "nan": continue
            correlations.append(corrAmount)

        return correlMsgs
        """for (xl, yl, ttl, ax) in zip(xlabels, ylabels, titles, axs.flatten()):
            finalMessage = "Coals" + correlMsgs[0][1:] + "vs Nonc" + correlMsgs[1][1:]
            #ax.set(xlabel=xl, ylabel=yl, title=finalMessage)    wtf is this line of code???? hope to God I figure that out lmfao TODO  """

        #if yl[:3] == "CCD": print("CCD",metricName,debugMsg,y_axis)
        #print("X OSA POSLE", x_axis)
        if color == "black":
            arg = ""
        elif color == "red":
            arg = "(noncoalition)"
        else:
            arg = "(coalition)"
        Correlations.distReport(metricName, correlations, arg)
    ###############################

    # We're just doing a normal distribution
    if coalitions == [] and components == []: 
        fillingAXsCoalNonc(x_axis, y_axis)

    # We're doing a distr of 2 things together
    else:
        coalX_axis, coalY_axis = [], []
        nonCX_axis, nonCY_axis = [], []

        # Separate components into either coal or nonc
        for x, y, comp in zip(x_axis, y_axis, components):
            if comp in coalitions:
                coalX_axis.append(x); coalY_axis.append(y)
            else:
                nonCX_axis.append(x); nonCY_axis.append(y)

        # Fill within two tries/layers on same AXs
        msg1 = fillingAXsCoalNonc(coalX_axis, coalY_axis, "blue", "s")
        msg2 = fillingAXsCoalNonc(nonCX_axis, nonCY_axis, "red", "d")

        # I need correlations of both
        for ax, m1, m2 in zip(axs.flatten(), msg1, msg2):
            ax.set(title="Coals" + m1[1:] + "vs Nonc" + m2[1:])
        
    ###############################
    suptitle = "{} - {}".format(metricName.upper(), graphName)
    plt.suptitle(suptitle)
    #plt.subplots_adjust(left=0.25, right=0.8, bottom=0.2, top=0.8, wspace= 0.4, hspace=0.8)
    print("Report", sourceDataFileName, graphName, metricName, "_Distr.png")
    plt.savefig(fname="Report/{}/{}/{}_Distr.png".format(sourceDataFileName, graphName, metricName))
    #plt.show()
    plt.close()

#CORRELATIONS TODO
def showCorrelation(x_axis, y_axis, corr1, metricName1, metricName2, graphName = "", coalitions = [], components = [], sourceDataFileName = ""):
    #print("GraphVisualization.py, correlData trying to get 2 numbers {}".format(Correlations.correlData(x_axis, y_axis)))
    #corr1, corr2 = Correlations.correlData(x_axis, y_axis)
    #if min(corr1, corr2) < 0.9: 
    #    raise Exception("GraphVisualization.py finds you not worthy")
        
    fig, axs = plt.subplots(1, 1, constrained_layout = True, figsize=(14,10)) #(2, 2, constrained_layout = True)
    
    ttl = "{} & {}".format(metricName1.upper(), metricName2.upper())
    title = ttl#+Correlations.distReport(ttl, [corr1, corr1])
    axs.set(xlabel=metricName1, ylabel=metricName2, title=graphName.upper()+"-"+title)
    axs.scatter(x_axis, y_axis, s=(800)/len(x_axis))
    print("Report", sourceDataFileName, graphName, metricName1, metricName2, "_Distr.png")
    plt.savefig(fname="Report/{}/{}/{}_{}.png".format(sourceDataFileName, graphName, metricName1, metricName2))
    #plt.show()
    plt.close()