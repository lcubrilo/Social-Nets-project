import networkx as nx

def create(G):
    result = nx.Graph()#nx.MultiGraph() #TODO reconsider

    for node in G.nodes: 
        tmpComponent = G.nodes[node]["component"]
        tmpColor = G.nodes[node]["color"]
        result.add_node(tmpComponent, color=tmpColor)
    
    for edge in G.edges():
        node1, node2 = G.nodes[edge[0]], G.nodes[edge[1]]
        comp1, comp2 = node1["component"], node2["component"]
        if comp1 != comp2:
            result.add_edge(comp1, comp2)

    return result