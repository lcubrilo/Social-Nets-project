from SocnetPackage import GraphVisualisation
from SocnetPackage.DataGeneration import SmallExamples, GenerateBigNets
from SocnetPackage.BasicFunctionalities import Clusters, Coalitions, GraphOfClusters
from SocnetPackage.Metrics import Correlations, Asortativity, Degrees

def printClusters(coalitions, noncoalitions, problemEdges):
    for coal in coalitions:
        coalitionName = GraphVisualisation.getComponentName(coal)
        print("Coalition {}: {} {}".format(coalitionName, coal.nodes, coal.edges))
    
    for nonc, prEd in zip(noncoalitions, problemEdges):
        noncoalitionName = GraphVisualisation.getComponentName(coal)
        print("Noncoalition {}: {} {}".format(noncoalitionName,  nonc.nodes, nonc.edges))
        print("\tProblematic edges: ", prEd)

#Titles/texts to be shown for thing_1 and thing_2
def getTitles(G, numComp, numCoal, areWeClusterable):
    yesNoMsg = "truly" if areWeClusterable else "not"
    ttl ="What you are currently seeing is " + yesNoMsg + " a clusterable " + str(G)

    ttl1 = Degrees.printMetrics(G)

    percentage = round(100*numCoal/numComp, 2)
    ttl2 = "{} clusters, {} coalitions ({}%).".format(numComp, numCoal, percentage)
    
    return [ttl, ttl2, ttl1]
    
# Tasks: 
#   1. ANALYZE some graphs (metrics)
#   2. SHOW some graphs

# Do the tasks on "some" graphs? Which graphs?

# Well, given 1 graph - do the tasks on these three graphs
#   1. the original graph itself
#   3. each of the components
#   2. the graph of components

def assignGraphsToTasks(G):
    #1. Original graph 
    #GraphVisualization.showGraph(G)
    showMetrics(G)

    #3. Each of the components
    components = Clusters.BFSComponents(G)
    coalitions, noncoalitions, problemEdges = Coalitions.filterComponents(components)
    #printClusters(coalitions, noncoalitions)
    G2 = GraphOfClusters.create(G)

    #2. Graph of components
    GraphVisualisation.showGraph(G2)
    showMetrics(G2)

    #Show a sample of components
    GraphVisualisation.showGraphs(coalitions)
    GraphVisualisation.showGraphs(noncoalitions)
    """
    for graph in coalitions:
        showMetrics(graph)
    for graph in noncoalitions:
        showMetrics(graph)
    """
def showMetrics(G):
    Degrees.drawCCDegreeDistribution(G, True)   
    Asortativity.drawKNNandDeg(G)
    #TODO: x-axis deg; y-axis [3 centralities + shell index]
    #smth like Centrality.moreAsortativityGraphs(G)

# Okay, that's cool. 
# ...
# You said "Given 1 graph"? Where is it? Which graphs are we given?

# We are given the following:
#   1. Small handmade graph [so far, only one]
#   2. Big (randomly) generated graph [however many we wish]
#   3. Real-life graphs (that is networks); specifically signed undirected social networks)
#       [there are 3 of them, Epinions, Wikipedia, Slashdot]        

############################
