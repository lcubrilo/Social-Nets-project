import SmallExamples, GraphVisualisation, Clusters, Coalitions

def main():
    G = SmallExamples.buildGraph()
    
    components = Clusters.BFSComponents(G); 
    GraphVisualisation.showComponentGraph(G, components)
    GraphVisualisation.showGraph(G)
    coalitions, noncoalitions = Coalitions.filterComponents(components)
    #print("Following components:\n {}\n\tCoalitions: {}\n\t Other clusters:{}".format(components, coalitions, noncoalitions))
    
    print("Following components: ")
    for c in components:
        print(c.nodes, c.edges)
    
    print("Coalitions:")
    for coal in coalitions:
        print("\t", coal.nodes, coal.edges)
    
    print("Noncoalitions:")
    for nonc in noncoalitions:
        print("\t", nonc[0].nodes, nonc[0].edges)
        print("\tProblematic edges: ", nonc[1])

main()