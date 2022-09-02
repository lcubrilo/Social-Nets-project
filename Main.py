from SocnetPackage import GraphVisualisation
from SocnetPackage.DataGeneration import SmallExamples, GenerateBigNets
from SocnetPackage.BasicFunctionalities import Clusters, Coalitions, GraphOfClusters
from SocnetPackage.Metrics import Correlations, Asortativity, Degrees

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
    
"""G = SmallExamples.buildGraph()
#print(G.degree, "\n", G.edges)
Metrics.drawDegreeDistribution(G)
Metrics.drawCCDegreeDistribution(G)"""

#GraphVisualisation.showGraph(G, withLabels=True)
"""main(SmallExamples.buildGraph())
print("Main is done for small graph.")
"""

for x, clusterable in zip([30, 65, 1000, 10], [False, True, False, False]):
#clusterable = True; for x in [4000, 8000, 15000, 100000]:
    Graph = GenerateBigNets.bigGraph(x, clusterable)
    testGraph(Graph)
    Degrees.drawCCDegreeDistribution(Graph, True)   
    Asortativity.drawKNNandDeg(Graph)