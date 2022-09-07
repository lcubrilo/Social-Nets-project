import networkx as nx

def sMetric(G):
    return sum([G.degree(u)*G.degree(v) for (u, v) in G.edges])   

#Paths based metrics
def getMetrics(G):
    return [
        sMetric(G),
        smallWorldCoefficitent(G),
        netEfficiency(G),
        diameter(G),
        radius(G),
        #TODO clustering coefficient
        #TODO   
    ]

def printMetrics(G):
    return "S metric: {}, Small world: {}, Net efficiency: {}, Diameter: {}, Radius: {}".format(
        *[round(m) for m in getMetrics(G)]
    )


def smallWorldCoefficitent(G):
    #if len(G.edges > 6000):
        #return "Nah"
    summa = 0
    for line in nx.all_pairs_shortest_path_length(G):
        for v in line[1]:
            summa += line[1][v]
    return summa/(len(G.nodes)**2 - len(G.nodes))
    n = len(G.nodes); d = dict(nx.all_pairs_shortest_path_length(G))
    sum([d[u][v] for u in G.nodes for v in G.nodes if u != v])/(n*n-n)

def netEfficiency(G):
    summa = 0
    for line in nx.all_pairs_shortest_path_length(G):
        for v in line[1]:
            if v != line[0]:
                summa += 1/line[1][v]
    return summa/(len(G.nodes)**2 - len(G.nodes))
    n = len(G.nodes); d = dict(nx.all_pairs_shortest_path_length(G))
    return sum([1/d[u][v] for u in G.nodes for v in G.nodes if u != v])/(n*n-n)

#Technically node metric
def eccentricities(G):
    res = []
    for line in nx.all_pairs_shortest_path_length(G):
        max = 0
        for v in line[1]:
            if line[1][v] > max: 
                max = line[1][v]
        res.append(max)
    return res
    return summa/(len(G.nodes)**2 - len(G.nodes))
    n = len(G.nodes); d = dict(nx.all_pairs_shortest_path_length(G))
    return [max([d[u][v] for u in G.nodes for v in G.nodes])]

def diameter(G):
    return max(eccentricities(G))

def radius(G):
    return min(eccentricities(G))
