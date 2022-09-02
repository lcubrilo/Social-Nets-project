from re import L
import networkx as nx
import matplotlib.pyplot as plt
from math import log10
from .Correlations import correlData

def averageNodeDegree(G):
    l = len(G.edges)
    n = len(G.nodes)

    return 2*l/n

def netDensity(G):
    l, n = len(G.nodes), len(G.edges)
    maxL = n*(n-1)

    return l/maxL

def degreeOfNeighborhoodOf(G, x): #neighborhood net density
    res = []
    for node in G.neighbors(x):
        res.append(G.degree(node))
    return avg(res)

#Knn
def groupNodesByDegree(G): #defunct
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
        fig.tight_layout()
        ax[0,0].set(xlabel = "Node degree", ylabel="Frequency", title="Degree distribution " + correlData(x_axis, y_axis))
        ax[0,0].plot(x_axis, normalizedDegreeDistribution)
        return ax, x_axis, normalizedDegreeDistribution
    else:
        plt.xlabel("Node degree")
        plt.ylabel("Frequency")
        plt.title("Degree distribution" + correlData)
        plt.plot(x_axis, normalizedDegreeDistribution)
        plt.suptitle(G)
        plt.show()

def drawCCDegreeDistribution(G, testPowerExponential = False):
    ax, x, y = drawDegreeDistribution(G, thisIsSubplot=True)
    for i in reversed(range(1, len(y))):
        y[i-1] += y[i]
    
    ax[0,1].set(xlabel = "Node degree", ylabel="CCD frequency", title="Complementary cumulative" + correlData(x, y))
    ax[0,1].plot(x, y)

    if testPowerExponential:
        y = [log10(e) for e in y]
        ax[1,0].set(ylabel = "log CCDF", title="If linear: exponential distribution" + correlData(x, y))
        ax[1,0].plot(x,y)

        x = [log10(e) for e in x]
        ax[1,1].set(xlabel = "log node degree", ylabel = "log CCDF", title="If linear: power law distribution" + correlData(x, y))
        ax[1,1].plot(x,y)

    plt.suptitle("{}; Average degree: {}, Net density: {}\n".format(
        G, round(averageNodeDegree(G), 2), round(netDensity(G), 2)))


    plt.show()


def sMetric(G):
    return sum([G.degree(u)*G.degree(v) for (u, v) in G.edges])   

#Paths based metrics
def printMetrics(G):
    return "S metric: {}, Small world: {}, Net efficiency: {}, Diameter: {}, Radius: {}".format(
        round(sMetric(G), 2),
        round(smallWorldCoefficitent(G), 2),
        round(netEfficiency(G), 2),
        round(diameter(G), 2),
        round(radius(G), 2)
    )

def smallWorldCoefficitent(G):
    n = len(G.nodes); d = dict(nx.all_pairs_shortest_path_length(G))
    return sum([d[i][j] for i in range(n) for j in range(n) if i != j])/(n*n-n)

def netEfficiency(G):
    n = len(G.nodes); d = dict(nx.all_pairs_shortest_path_length(G))
    return sum([1/d[i][j] for i in range(n) for j in range(n) if i != j])/(n*n-n)

def eccentricities(G):
    n = len(G.nodes); d = dict(nx.all_pairs_shortest_path_length(G))
    return [max([d[i][j] for j in range(n)]) for i in range(n)]

def diameter(G):
    return max(eccentricities(G))

def radius(G):
    return min(eccentricities(G))



def avg(array): 
    return sum(array)/len(array)