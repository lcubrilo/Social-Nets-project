import SmallExamples, GraphVisualisation, Clusters, Coalitions, GraphOfClusters


def main(G):
    components = Clusters.BFSComponents(G)
    print("Got clusters") 
    GraphVisualisation.showComponentGraph(G, components)
    GraphVisualisation.showGraph(G, components, "Small example")
    coalitions, noncoalitions, problemEdges = Coalitions.filterComponents(components)
    
    """print("Following components: ")
    for c in components:
        print(c.nodes, c.edges)"""
    
    for coal in coalitions:
        coalitionName = GraphVisualisation.getComponentName(coal)
        print("Coalition {}: {} {}".format(coalitionName, coal.nodes, coal.edges))
    
    for nonc, prEd in zip(noncoalitions, problemEdges):
        noncoalitionName = GraphVisualisation.getComponentName(coal)
        print("Noncoalition {}: {} {}".format(noncoalitionName,  nonc.nodes, nonc.edges))
        print("\tProblematic edges: ", prEd)
    
    G2 = GraphOfClusters.create(G)
    GraphVisualisation.showGraph(G2, graphname="Components graph")

    print("Graph of clusters: {} {}".format(G2.nodes, G2.edges))


#main(SmallExamples.buildGraph())

import GenerateBigNets

G = GenerateBigNets.bigGraph(100)
GraphVisualisation.showGraph(G)

print("Main is done.")

"""
import networkx as nx
edges, edgeColors = zip(*nx.get_edge_attributes(G, 'color').items())
for (e, eC) in zip(edges, edgeColors):
    print(e, eC)"""

edges = G.edges()
colors = [G[u][v]['color'] for u,v in edges]
for e, c in zip(edges, colors):
    print(e, c)