import SmallExamples, GraphVisualisation, Clusters, Coalitions

def main():
    G = SmallExamples.buildGraph()
    
    components = Clusters.BFSComponents(G);
    print("Got clusters") 
    GraphVisualisation.showComponentGraph(G, components)
    GraphVisualisation.showGraph(G)
    coalitions, noncoalitions, problemEdges = Coalitions.filterComponents(components)
    #print("Following components:\n {}\n\tCoalitions: {}\n\t Other clusters:{}".format(components, coalitions, noncoalitions))
    
    print("Following components: ")
    for c in components:
        print(c.nodes, c.edges)
    
    for coal in coalitions:
        coalitionName = coal.nodes[list(coal.nodes)[0]]["component"]
        print("Coalition {}: {} {}".format(coalitionName, coal.nodes, coal.edges))
    
    for nonc, prEd in zip(noncoalitions, problemEdges):
        noncoalitionName = nonc.nodes[list(nonc.nodes)[0]]["component"]
        print("Noncoalition {}: {} {}".format(noncoalitionName,  nonc.nodes, nonc.edges))
        print("\tProblematic edges: ", prEd)

print("Yo")
main()