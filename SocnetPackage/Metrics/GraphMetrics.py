import networkx as nx

def averageNodeDegree(G, trash=None):
    l = len(G.edges)
    n = len(G.nodes)
    if n < 0: return -1

    return 2*l/n

def netDensity(G, trash=None):
    l, n = len(G.nodes), len(G.edges)
    if n <= 1: return -1
    maxL = n*(n-1)

    return l/maxL

"""
# Deprecated - this will essentially be called in the new outline
def indexOfAsortativity(G, trash=None):
    x, y = distributions(G.nodes, [G.degree])
    return pearsonCorrelation(x, y)
"""

def sMetric(G, trash=None):
    return sum([G.degree(u)*G.degree(v) for (u, v) in G.edges])   
"""
#Paths based metrics
def getMetrics(G, trash=None):
    return [
        netDensity(G, trash=None),
        indexOfAsortativity,
        sMetric(G, trash=None),
        smallWorldCoefficitent(G, trash=None),
        netEfficiency(G, trash=None),
        diameter(G, trash=None),
        radius(G, trash=None),
        #TODO clustering coefficient
        #TODO  deprecate this 
    ]

def printMetrics(G, trash=None):
    return "S metric: {}, Small world: {}, Net efficiency: {}, Diameter: {}, Radius: {}".format(
        *[round(m) for m in getMetrics(G, trash=None)]
    )
"""

def smallWorldCoefficitent(G, trash=None):
    #if len(G.edges > 6000):
        #return "Nah"
    if len(G.nodes) <= 1: return -1
    summa = 0
    for line in nx.all_pairs_shortest_path_length(G):
        for v in line[1]:
            summa += line[1][v]
    return summa/(len(G.nodes)**2 - len(G.nodes))
    n = len(G.nodes); d = dict(nx.all_pairs_shortest_path_length(G, trash=None))
    sum([d[u][v] for u in G.nodes for v in G.nodes if u != v])/(n*n-n)

def netEfficiency(G, trash = None):
    if len(G.nodes) <= 1: return -1
    summa = 0
    for line in nx.all_pairs_shortest_path_length(G):
        for v in line[1]:
            if v != line[0]:
                summa += 1/line[1][v]
    return summa/(len(G.nodes)**2 - len(G.nodes))

#Technically node metric
def eccentricities(G, trash = None, n = None):
    res = {}
    for line in nx.all_pairs_shortest_path_length(G):
        max = 0
        for v in line[1]:
            if line[1][v] > max: 
                max = line[1][v]
        res[line[0]] = max
        if type(max) != int:
            raise Exception ("Brate ali kako")
    return res if not n else res[n]

def diameter(G, trash=None):
    try:
        return max(eccentricities(G, trash=None).values())
    except:
        return -1

def radius(G, trash=None):
    try:
        return min(eccentricities(G, trash=None).values())
    except:
        return -1

def averageClusteringCoefficient(G, trash=None):
    from SocnetPackage.Metrics.NodeMetrics import clusteringCoefficient
    coefs = [clusteringCoefficient(G, node) for node in G.nodes()]
    try:
        while True: coefs.remove(-1)
    finally: 
        if len(coefs) <= 0: return -1
        return sum(coefs)/len(coefs)

def graphMetrics():
    return zip([averageNodeDegree, netDensity, sMetric, smallWorldCoefficitent, netEfficiency, diameter, radius, averageClusteringCoefficient],
    ["averageNodeDegree", "netDensity", "sMetric", "smallWorldCoefficitent", "netEfficiency", 'diameter', "radius", "averageClusteringCoefficient"])

def test():
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

    return [metric(G, trash=None) for metric in graphMetrics()]

if __name__ == "__main__":
    print(test())