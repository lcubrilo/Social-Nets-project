import networkx as nx
from random import shuffle, random, choice
from numpy.random import poisson
from ComponentNamesColors import iterateThruComponentNames

#import GraphVisualisation

def bigGraph(numOfNodes):
    nodesMade = 0
    components = []
    currCompName = "A"

    while nodesMade < numOfNodes:
        compSize = poisson(6)+1
        generated = generateComponent(compSize, nodesMade, name = currCompName)
        if not generated:
            continue
        components.append(generated)
        iterateThruComponentNames(currCompName)
        nodesMade += compSize
    
    """for c in components:
        print(c.nodes)
"""
    #GraphVisualisation.showComponentGraph(components)
    graphOfComponents = generateGraphOfComponents(components)
    #GraphVisualisation.showGraph(graphOfComponents)
    return graphOfComponents2BigGraph(graphOfComponents, components)

def graphOfComponents2BigGraph(g, components):
    BigGraph = nx.Graph()
    for c in components:
        BigGraph.add_edges_from(c.edges, color = "green")

    print("Converting it to big graph")
    for edge in g.edges:
        c1, c2 = edge[0], edge[1]
        connect2Components(BigGraph, c1, c2, int(random()*4)+1)
    
    print("Got big graph")
    return BigGraph

def generateGraphOfComponents(components):
    G = nx.Graph()
    G.add_nodes_from(components)

    print("Got graph of components")
    return generateComponent(2, startingGraph=G)

def connect2Components(G, c1, c2, L):
    lstNds1, lstNds2 = list(c1.nodes), list(c2.nodes)
    while L > 0:
        n1, n2 = choice(lstNds1), choice(lstNds2)
        G.add_edge(n1, n2, color = "red")
        L -= 1

def generateComponent(numOfNodes, startingIndex = 0, startingGraph = None, name = None):
    #First add nodes, then the edges
    if not startingGraph:
        G = nx.Graph()
        endingIndex = startingIndex + numOfNodes
        if name:
            G.add_nodes_from(range(startingIndex, endingIndex), component = name)
        else:
            G.add_nodes_from(range(startingIndex, endingIndex))
    else:
        G = startingGraph

    color = "green" if startingGraph == None else "red"
    #guarantees a connected graph by having ONE path thru all nodes
    #addRandomPath(G)
    #Slightly randomizes structure but still guarantees a connected graph 
    connectEmptyGraph(G, color)

    #start adding edges using hilberts p probability idea
    
    addEdgesHilbertIdea(G, color)

    #print("Made component, starting from", startingIndex)
    return G

def addRandomPath(G):
    randomPathOrder = list(G.nodes)
    shuffle(randomPathOrder) 
    prev_node = randomPathOrder[0]

    for node in randomPathOrder:
        if node == prev_node: continue #don't make a self connection for the first node
        G.add_edge(prev_node, node)
        prev_node = node
    
    return G

def connectEmptyGraph(G, val):
    if len(G.edges) > 0: return False

    connected = [list(G.nodes)[0]]

    for node in G.nodes:
        if node in connected: continue;
        G.add_edge(choice(connected), node, color = val)
        connected.append(node)
   
def addEdgesHilbertIdea(G, val = "", attr = "color"):
    #p*(n-1) goes from 1 to 4 => guarantees gigantic component if started with empty graph
    #p = (1+random())**2/(N-1) 
    listOfNodes = list(G.nodes)
    N = len(listOfNodes)
    p = random()/(N-1) if N > 1 else random()
    coef = 2 if val == "green" else 0.9
    p*= coef

    maxDegree = max([G.degree(n) for n in G.nodes])

    edgesToAdd = []
    for i in range(N-1):
        for j in range(i+1, N):
            if random() < p*G.degree[listOfNodes[j]]/maxDegree:
                edgesToAdd.append((listOfNodes[i], listOfNodes[j]))
    if val != "":
        G.add_edges_from(edgesToAdd, color = val)
    else:
        G.add_edges_from(edgesToAdd)
        

