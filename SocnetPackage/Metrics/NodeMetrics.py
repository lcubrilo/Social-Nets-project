# Node metrics
from collections import deque
nodes = []
D, P = [[]], [[]]
eigenvectorCentralities = []

def fillMatrix(M, n):
    M = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append("Djubre")
        M.append(row)
    return M

def loadNodes(G):
    nodes = G.nodes

def calcDPMatrix(G):
    nodes = G.nodes

    n = len(nodes)
    D, P = fillMatrix(D, n), fillMatrix(P, n)
    queue = deque()
    visited = []

    for start in nodes:
        if start in visited:
            continue
        print("Again BFS")
        queue.append(start)
        visited.append(start)

        while queue:
            curr = queue.popleft()

            for x in G.neighbors(curr):
                if x not in visited:
                    visited.append(x)
                    queue.append(x)

                    D[start][x] = D[start][curr] + 1
                    if curr == start: P[start][x]
                    else: P[start][x] = P[start][curr]
                else:
                    if D[start][x] == D[start][curr] + 1:
                        P[start][x] += P[start][curr]
    
    print("D matrix:")
    for row in D:
        print(row)
    print("P matrix")
    for row in P:
        print(row)

def degree(G, node):
    return G.degree(node)

#Centralities 
def betweenness(G, z):
    nodes = G.nodes
    return sum(sigma(x,y,z)/sigma(x, y) for x in nodes for y in nodes)

def sigma(x, y, z = None):
    if P == [[]] or D == [[]]: calcDPMatrix()

    if not z: return P[x][y]
    
    if D[x][y] < D[x][z] + D[y][z]: return 0
    
    return P[x][z] * P[z][y]
    

def closeness(G, z):
    if D == [[]]: calcDPMatrix(G)
    global nodes
    return sum( [D[n][z] for n in nodes] )

def vectorLength(vector):
    return sum([x**2 for x in vector])

def eigenvector(G, node, epsilon = 0.01, maxiter = 10**6):
    if eigenvectorCentralities != []: return eigenvectorCentralities[node]

    nodes = G.nodes
    delta = epsilon; i = maxiter; n = len(nodes)
    Ce = [1 for i in range(n)]

    while delta >= epsilon and i > 0:
        i -= 1
        for n in nodes:
            curr_ce = [0 for i in range(n)]
            for neigh in G.neighbors(n):
                curr_ce[n] += Ce[neigh]
        
        l = vectorLength(curr_ce)
        curr_ce = [x/l for x in curr_ce]

        delta = sum( [abs(x1-x2) for (x1,x2) in zipped(curr_ce, Ce)] )
        Ce = [x for x in curr_ce]
        
    return Ce

def shellIndex(G, node):
    return