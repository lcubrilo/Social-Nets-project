import SmallExamples, GraphVisualisation, Clusters, Coalitions, GraphOfClusters


def main():
    G = SmallExamples.buildGraph()
    
    components = Clusters.BFSComponents(G);
    print("Got clusters") 
    GraphVisualisation.showComponentGraph(G, components)
    GraphVisualisation.showGraph(G, components)
    coalitions, noncoalitions, problemEdges = Coalitions.filterComponents(components)
    #print("Following components:\n {}\n\tCoalitions: {}\n\t Other clusters:{}".format(components, coalitions, noncoalitions))
    
    print("Following components: ")
    for c in components:
        print(c.nodes, c.edges)
    
    for coal in coalitions:
        coalitionName = GraphVisualisation.getComponentName(coal)
        print("Coalition {}: {} {}".format(coalitionName, coal.nodes, coal.edges))
    
    for nonc, prEd in zip(noncoalitions, problemEdges):
        noncoalitionName = GraphVisualisation.getComponentName(coal)
        print("Noncoalition {}: {} {}".format(noncoalitionName,  nonc.nodes, nonc.edges))
        print("\tProblematic edges: ", prEd)
    
    G2 = GraphOfClusters.create(G)
    GraphVisualisation.showGraph(G2)

    print("Graph of clusters: {} {}".format(G2.nodes, G2.edges))

print("Yo")
main()