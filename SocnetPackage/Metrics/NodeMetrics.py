# Node metrics
import networkx as nx

nodes = {}
D, P = {}, {}

# Use BFS to fill D and P used for between and closeness
def calcDPMatrix(G):
    global D, P
    nodes = G.nodes

    n = len(nodes)
    
    def fillMatrix(M, nodes):
        M = {}
        for n1 in nodes:
            n1 = n1
            M[n1] = {}
            for n2 in nodes:
                M[n1][n2] = 0
        return M
    D, P = fillMatrix(D, G.nodes()), fillMatrix(P, G.nodes())
    from collections import deque; queue = deque()
    visited = []

    for start in nodes:
        if start in visited:
            continue
        #print("Again BFS")
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
    
    #print("D matrix:")
    #for row in D:
    #    print(row)
    #print("P matrix")
    #for row in P:
    #    print(row)

#Centralities 
# 
# 1. Betweenness Centrality
def betweennessCentrality(G, z):
    global nodes
    nodes = G.nodes
    if z == None:
        return [betweennessCentrality(G, nod) for nod in nodes]

    # Sigma gets values from D and P
    def sigma(x, y, z = None): 
        if P == {} or D == {}: 
            calcDPMatrix(G)
        if not z: return P[x][y]

        # Use inequality of triangles
        if D[x][y] < D[x][z] + D[y][z]:
            return 0
        else:
            return P[x][z] * P[z][y]

    return sum(sigma(x,y,z)/sigma(x, y) for x in nodes for y in nodes if sigma(x,y)!=0)
  
# 2. Closeness Centrality
def closenessCentrality(G, z):
    if D == {}: calcDPMatrix(G)
    global nodes
    nodes = G.nodes
    if z == None:
        return [closenessCentrality(G, nod) for nod in nodes]
    return sum( [D[n][z] for n in nodes] )

# 3. Eigenvector Centrality
eigenvectorCentralities = {}
def eigenvectorCentrality(G, node, epsilon = 0.01, maxiter = 10**6):
    # A little trick if we've already calculated this
    global eigenvectorCentralities
    if eigenvectorCentralities != {}: return eigenvectorCentralities[node]

    nodes = G.nodes
    delta = epsilon; old_delta = 2*delta; i = maxiter
    Ce = {n:1 for n in nodes}# Start with everybody being equal
    curr_ce = {n:0 for n in nodes}

    while abs(old_delta-delta)/delta >= epsilon and delta >= epsilon and i > 0:
        i -= 1
        if i%1000 == 0:
            print(delta)
        
        # In this iteration, get values for every node
        for n in nodes:
            # Sum up vals from neighbors
            curr_ce[n] = 0
            for neigh in G.neighbors(n):
                curr_ce[n] += Ce[neigh]
        
        def length(v): return sum([v[x]**2 for x in v])**0.5 # Pythagora's for length
        def normalize(v): l = length(v); return {x:v[x]/l for x in v} if l!= 0 else {1} # Divide by length
        curr_ce = normalize(curr_ce)

        # Compute distance of this and previous iteration
        old_delta = delta
        delta = sum( [abs(curr_ce[x1]-Ce[x2]) for (x1,x2) in zip(curr_ce, Ce)] )

        # Move over one spot
        Ce = {x:curr_ce[x] for x in curr_ce}

    # print(Ce)
    eigenvectorCentralities = Ce; 
    return eigenvectorCentralities[node]

shellValues = {}
def shellIndex(G, node):
    global shellValues
    if shellValues != {}:
        return shellValues[node]

    nodes = G.nodes()
    currnodes = nodes # Constantly shrinking amount of nodes interesting to us
    res = {n:0 for n in nodes} # AFAIK every node does have shell index 0; only by each successive iteration do they actually prove their shell index to be higher by one
    k = 0 # Will be iterating k values as far as possible
    # Peel k by k the shells until the very core when no one remains
    while len(currnodes) > 0:
        k += 1
        currnodes = nx.k_core(G, k).nodes()
        # These guys survived this level, mark this
        for nodes in currnodes:
            res[nodes] += 1

    # Everybody's gone as far as they can, that's it
    shellValues = res
    return shellValues[node]

    
def clusteringCoefficient(G, node):        
    hisNeighbors = G.neighbors(node)
    num = G.degree(node)
    if num < 2: return -1

    # What portion of em are connected?
    maximumNumberOfConnections = num*(num-1)
    actualNumberOfConnections = 0

    for neig1 in hisNeighbors:
        for neig2 in hisNeighbors:
            if (neig1, neig2) in G.edges():
                actualNumberOfConnections += 1
    
    return actualNumberOfConnections/maximumNumberOfConnections

def degree(G, node): 
    return G.degree(node)

# Even though it's a node metric, it has to be calculated graph-wide
# Let's do that only once and store the value
eccentricitiesValues = {}    
def eccentricity(G, node): 
    # Get the graphwide vals
    global eccentricitiesValues
    if len(eccentricitiesValues) != len(G.nodes()):
        from SocnetPackage.Metrics.GraphMetrics import eccentricities; 
        eccentricitiesValues = eccentricities(G)

    return eccentricitiesValues[node]

def nodeMetrics():
    global D, P, eccentricitiesValues, eigenvectorCentralities, nodes, shellValues
    D = {}; P = {}; eccentricitiesValues = {}; eigenvectorCentralities = {}; nodes = {}; shellValues = {}
    return zip([degree, shellIndex, eccentricity, clusteringCoefficient, closenessCentrality, eigenvectorCentrality],
    ["degree", "shellIndex", "eccentricity", "clusteringCoefficient", "closenessCentrality", "eigenvectorCentrality"])

def test():
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

    print("degree")
    for node in G.nodes:
        print(degree(G, node))

    print("shellIndex")
    for node in G.nodes:
        print(shellIndex(G, node))

    print("eccentricity")
    for node in G.nodes:
        print(eccentricity(G, node))

    print("clusteringCoefficient")
    for node in G.nodes:
        print(clusteringCoefficient(G, node))

    print("betweenness")
    for node in G.nodes:
        print(betweennessCentrality(G, node))

    print("closeness")
    for node in G.nodes:
        print(closenessCentrality(G, node))

    print("eigenvector")
    for node in G.nodes:
        print(eigenvectorCentrality(G, node))

if __name__ == "__main__":
    test()