import networkx as nx
import matplotlib.pyplot as plt
from math import log10
from Correlations import correlData

def degreeOfNeighborhoodOf(G, x):
    res = []
    for node in G.neighbors(x):
        res.append(G.degree(node))
    return avg(res) if res != [] else 0

#X AXIS IN ALL DISTRIBUTIONS
def groupNodesByDegree(G):
    degreePairs = sorted(G.degree, key= lambda element:element[1])

    firstNode, itsDegree = degreePairs[0]
    currDegree = itsDegree; currGroup = []; groupedNodes = {}

    for (node, degree) in degreePairs:
        if degree == currDegree:
            currGroup.append(node)
        else:
            groupedNodes[currDegree] = currGroup
            currDegree = degree; currGroup = []
    
    return groupedNodes


#Drawing 

def drawDegreeDistribution(G, thisIsSubplot=False, debug=False):
    degrees = [G.degree[node] for node in G.nodes]
    degrees = sorted(degrees)

    minDeg, maxDeg = degrees[0], degrees[-1]
    degreeDistribution = [0]*(maxDeg - minDeg + 1)

    for deg in degrees:
        degreeDistribution[deg-minDeg] += 1
    
    if debug: print("Degrees:", degreeDistribution)

    numOfNodes = len(G.nodes)
    normalizedDegreeDistribution = [count/numOfNodes for count in degreeDistribution]
    
    x_axis = range(minDeg, maxDeg+1)
    y_axis = normalizedDegreeDistribution

    if thisIsSubplot:
        fig, ax = plt.subplots(2, 2, constrained_layout = True)
        #fig.tight_layout()
        ax[0,0].set(xlabel = "Node degree", ylabel="Frequency", title="Degree distribution " + correlData(x_axis, y_axis))
        ax[0,0].scatter(x_axis, normalizedDegreeDistribution)
        return ax, x_axis, normalizedDegreeDistribution
    else:
        plt.xlabel("Node degree")
        plt.ylabel("Frequency")
        plt.title("Degree distribution" + correlData)
        plt.scatter(x_axis, normalizedDegreeDistribution)
        plt.suptitle(G)
        plt.show()

def removeZeros(x, y):
        x=list(x); y=list(y)
        try:
            while True:
                index = x.index(0)
                x = x[:index] + x[index+1:]
                y = y[:index] + y[index+1:]
        except:
            return x, y

def drawCCDegreeDistribution(G, testPowerExponential = False, graphName = ""):
    ax, x, y = drawDegreeDistribution(G, thisIsSubplot=True)
    for i in reversed(range(1, len(y))):
        y[i-1] += y[i]
    
    ax[0,1].set(xlabel = "node degree", ylabel="CCD frequency", title="Complementary cumulative" + correlData(x, y))
    ax[0,1].scatter(x, y)

    if testPowerExponential:
        y, x = removeZeros(y,x)

        y = [log10(e) for e in y]
        ax[1,0].set(xlabel = "node degree", ylabel = "log CCDF", title="If linear: exponential distribution" + correlData(x, y))
        ax[1,0].scatter(x,y)

        x, y = removeZeros(x,y)
        x = [log10(e) for e in x if e!=0]
        ax[1,1].set(xlabel = "log node degree", ylabel = "log CCDF", title="If linear: power law distribution" + correlData(x, y))
        ax[1,1].scatter(x,y)

    import GraphMetrics
    plt.suptitle(graphName + "{}\nAverage degree: {}, Net density: {}%\n".format(
        G, round(GraphMetrics.averageNodeDegree(G), 3), round(100*GraphMetrics.netDensity(G), 3)))


    plt.show()


def avg(array): 
    return sum(array)/len(array)