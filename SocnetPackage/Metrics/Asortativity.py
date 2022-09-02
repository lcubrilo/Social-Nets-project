import networkx as nx
from .Correlations import *
from .Degrees import degreeOfNeighborhoodOf, groupNodesByDegree
import matplotlib.pyplot as plt

def indexAsortativity(G = nx.Graph(), modified = False):
    return generalizedIndexAsortativity(G, G.degree(), G.degree(), modified)

def generalizedIndexAsortativity(G, propertyX, propertyY, modified = False):
    x, y = [], []
    for e in G.edges:
        u, v = propertyX(e[0]), propertyY(e[1])
        x.append(u, v); y.append(v, u)
    
    return Correlations.pearsonCorrelation(x, y) if not modified else Correlations.spearmanCorrelation(x, y)

#KNN
def avg(array): 
    return sum(array)/len(array)

def KNN(G, k, nodesWithDegreeK):
    return avg([degreeOfNeighborhoodOf(G, node) for node in nodesWithDegreeK])

def allKNN(G):
    k_values, KNN_values = [], []

    groupedByDegree = groupNodesByDegree(G)
    for degree in groupedByDegree:
        group = groupedByDegree[degree]
        if len(group) == 0: continue
        k_values.append(degree)
        KNN_values.append(KNN(G, degree, group))
    
    return k_values, KNN_values

#Draw
def drawKNNandDeg(G = nx.Graph()):
    fig, ax = plt.subplots(1, 2)
    fig.tight_layout()
    drawKNN(G, ax[0])
    drawDegDeg(G, ax[1])
    plt.locator_params(axis="x", integer=True)
    plt.suptitle(G)
    plt.show()

def drawKNN(G, ax):
    x, y = allKNN(G)

    ax.set(xlabel = "k degree nodes", ylabel="Degree of their neighborhood", title="Asortativity (KNN)" + correlData(x, y))
    ax.scatter(x, y)

def drawDegDeg(G, ax):
    x, y = [], []

    for e in G.edges:
        u, v = e
        u, v = G.degree(u), G.degree(v)
        x.append(u); y.append(v)
        x.append(v); y.append(u)
        

    ax.set(xlabel = "degree of node", ylabel="degree of neighbor", title="Asortativity (deg-deg)" + correlData(x, y))
    ax.scatter(x, y)


    