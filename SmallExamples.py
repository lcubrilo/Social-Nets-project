import networkx as nx

def buildGraph():
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
    
    return G