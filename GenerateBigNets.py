import networkx as nx
from random import shuffle, random, choice

"""def generateBigNets(totalNodes):
    G = nx.Graph()
    nodesAdded = 0
    components = []

    while nodesAdded < totalNodes:
        componentSize = random()
        components.append(generateComponent(componentSize, nodesAdded))
        nodesAdded += componentSize
    
    for c1 in components:
        for c2 in components:
            if c1 == c2: continue
            if random() > 0.01
    """

def connect2Components(G, c1, c2, L):
    while L > 0:
        n1, n2 = choice(c1.nodes), choice(c2.nodes)


def generateComponent(numOfNodes, startingIndex = 0):
    if numOfNodes < 2: return False
    #First add nodes, then the edges
    G = nx.Graph()
    endingIndex = startingIndex + numOfNodes
    G.add_nodes_from(range(startingIndex, endingIndex))

    #guarantees a connected graph by having ONE path thru all nodes
    #addRandomPath(G)
    #Slightly randomizes structure but still guarantees a connected graph 
    connectEmptyGraph(G)

    #start adding edges using hilberts p probability idea
    addEdgesHilbertIdea(G, numOfNodes, "green")

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

def connectEmptyGraph(G):
    if len(G.edges) > 0: return False

    connected = [list(G.nodes)[0]]

    for node in G.nodes:
        if node in connected: continue;
        G.add_edge(choice(connected), node)
        connected.append(node)
   
def addEdgesHilbertIdea(G, N, val = "", attr = "color"):
    #p*(n-1) goes from 1 to 4 => guarantees gigantic component if started with empty graph
    #p = (1+random())**2/(N-1) 
    p = 1.2*random()/(N-1) 
    maxDegree = max([G.degree(n) for n in G.nodes])

    edgesToAdd = []
    for i in range(N-1):
        for j in range(i+1, N):
            if random() < p*G.degree(j)/maxDegree:
                edgesToAdd.append((i, j))
    if val:
        G.add_edges_from(edgesToAdd, color = val)
    else:
        G.add_edges_from(edgesToAdd)
        

