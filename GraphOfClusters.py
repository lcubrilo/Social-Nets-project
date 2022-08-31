import networkx as nx

def create(G):
    result = nx.MultiGraph()

    for node in G.nodes: 
        tmpComponent = G.nodes[node]["component"]
        result.add_node(tmpComponent)
    
    for edge in G.edges():
        node1, node2 = G.nodes[edge[0]], G.nodes[edge[1]]
        comp1, comp2 = node1["component"], node2["component"]
        if comp1 != comp2:
            result.add_edge(comp1, comp2)

    return result