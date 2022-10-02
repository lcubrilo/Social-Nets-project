from random import random

def myCommunity(node, communities):
    # Given a disjoint community list, return membership
    n = len(communities)
    for i in range(n):
        if node >= communities[i][0]:
            return i - 1
    
import networkx as nx
def SBM(n, r, pGreen, pRed, pRandomness = False):
    # Normalize values (btw if pGreen>pRed - assortative)
    pGreen, pRed = pGreen/max(pGreen,pRed), pRed/max(pGreen, pRed)

    # Get a disjoint division of n nodes into r communities
    m = [random()*1000 for i in range(r)]
    summa = sum(m)
    m = [e/summa for e in m]

    # Create communities of nodes according to the given community lengths
    index = 0
    communities = []
    for i in range(r):
        start, end = index, index + round(m[i]*n)
        communities.append(list(range(start, end)))
    
    # Populate the edge probability matrix
    P = [0]*r
    P = P*r
    for i in range(r):
        for j in range(r):
            P[i][j] = pGreen if i == j else pRed
    
    # Place the data into graph
    G = nx.Graph()
    for n1 in range(n):
        for n2 in range(n):
            c1 = myCommunity(n1, communities)
            c2 = myCommunity(n2, communities)
            edgeColor = "green" if c1==c2 else "red"
            if random() < P[c1][c2]:
                G.add_edge(c1, c2, color = edgeColor)
    
    # We now have a graph filled with coalitions
    return G
