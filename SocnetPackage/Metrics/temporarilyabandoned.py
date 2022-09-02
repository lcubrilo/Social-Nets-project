def nodesWithDegree(G, k):
    original, array = sorted(G.degree), sorted(G.degree)
    
    if k < array[0][1] or k > array[-1][1]: return False

    #Binary search to find ANY k degree node
    while True:
        if len(array) <= 1: #Somehow failed?
            return []

        i = len(array)//2

        if array[i][1] < k: 
            array = array[i:]
        elif array[i][1] > k:
            array = array[:i]
        else:
            break
    
    #From there linear search to find ALL k degree nodes 
    left, right = i, i
    spreadLeft, spreadRight = True, True
    while spreadLeft or spreadRight:
        if(original[left][1] != original[right][1]):
            if(original[left][1] < original[i][1]): left +=1; spreadLeft = False
            if(original[right][1] > original[i][1]): right -=1; spreadRight = False
            break

        if spreadLeft: left -=1
        if spreadRight: right +=1
    
    res = [original[index][0] for index in range(left, right+1)]
    return res
#if not nodesWithDegreeK: nodesWithDegreeK = nodesWithDegree(k)

def degreeOfNeighborhoodOf(G, x):
    res = []
    for node in G.neighbors(x):
        res.append(G.degree(node))
    return avg(res)

def avg(array): 
    return sum(array)/len(array)

def KNN(G, k, nodesWithDegreeK):
    return avg([degreeOfNeighborhoodOf(G, node) for node in nodesWithDegreeK])

import networkx as nx
G = nx.Graph()
G.add_nodes_from(range(10))
G.add_edge(1, 2, color="green")
G.add_edge(3, 2, color="green")
G.add_edge(4, 5, color="green")
G.add_edge(1, 5, color="red")
G.add_edge(4, 2, color="red")
G.add_edge(2, 6, color="red")
G.add_edge(6, 7, color="green")
G.add_edge(7, 8, color="green")
G.add_edge(6, 8, color="green")
G.add_edge(3, 9, color="green")
G.add_edge(2, 9, color="red")
    
print(KNN(G, 2, [5,4,8,7,3,9,1]))

###Deprecated stuff from main_old, hopefully soon remove
def testGraph(G):
    components = Clusters.BFSComponents(G)
    print("Got clusters") 
    #GraphVisualisation.showComponentGraph(components)
    #GraphVisualisation.showGraph(G, components, "Small example")
    coalitions, noncoalitions, problemEdges = Coalitions.filterComponents(components)
    
    """print("Following components: ")
    for c in components:
        print(c.nodes, c.edges)"""
    
    
    
    G2 = GraphOfClusters.create(G)
    #GraphVisualisation.showGraph(G2, graphname="Components graph")
    #print("Graph of clusters: {} {}".format(G2.nodes, G2.edges))

    

    Degrees.drawCCDegreeDistribution(G, True)   
    Asortativity.drawKNNandDeg(Graph)
    #print(Degrees.printMetrics(Graph))

    
"""G = SmallExamples.buildGraph()
#print(G.degree, "\n", G.edges)
Metrics.drawDegreeDistribution(G)
Metrics.drawCCDegreeDistribution(G)"""

#GraphVisualisation.showGraph(G, withLabels=True)
"""main(SmallExamples.buildGraph())
print("Main is done for small graph.")
"""
"""
for x, clusterable in zip([30, 65, 1000, 10], [False, True, False, False]):
#clusterable = True; for x in [4000, 8000, 15000, 100000]:
    Graph = GenerateBigNets.bigGraph(x, clusterable)
    testGraph(Graph)"""
    
    