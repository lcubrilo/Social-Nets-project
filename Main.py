import SmallExamples, GraphVisualisation, Clusters, Coalitions, GraphOfClusters


def testGraph(G):
    components = Clusters.BFSComponents(G)
    print("Got clusters") 
    #GraphVisualisation.showComponentGraph(components)
    #GraphVisualisation.showGraph(G, components, "Small example")
    coalitions, noncoalitions, problemEdges = Coalitions.filterComponents(components)
    
    """print("Following components: ")
    for c in components:
        print(c.nodes, c.edges)"""
    
    for coal in coalitions:
        coalitionName = GraphVisualisation.getComponentName(coal)
        #print("Coalition {}: {} {}".format(coalitionName, coal.nodes, coal.edges))
    
    for nonc, prEd in zip(noncoalitions, problemEdges):
        noncoalitionName = GraphVisualisation.getComponentName(coal)
        print("Noncoalition {}: {} {}".format(noncoalitionName,  nonc.nodes, nonc.edges))
        print("\tProblematic edges: ", prEd)
    
    G2 = GraphOfClusters.create(G)
    #GraphVisualisation.showGraph(G2, graphname="Components graph")
    #print("Graph of clusters: {} {}".format(G2.nodes, G2.edges))

    ttl1 = "{} nodes, {} edges.".format(len(G.nodes), len(G.edges))
    numComp, numCoal = len(components), len(coalitions)
    ttl2 = "{} clusters, {} coalitions ({}%).".format(numComp, numCoal, round(100*numCoal/numComp, 2))
    areWeClusterable = ("truly" if len(problemEdges) == 0 else "not")
    ttl ="What you are currently seeing is " + areWeClusterable + " a clusterable graph."
    GraphVisualisation.showGraphAndComponents(G, components, G2, [ttl, ttl1, ttl2])
    


"""main(SmallExamples.buildGraph())
print("Main is done for small graph.")
"""
import GenerateBigNets

for x, clusterable in zip([30, 65, 1000, 10], [False, True, False, False]):
    testGraph(GenerateBigNets.bigGraph(x, clusterable))