from SocnetPackage import GraphVisualisation
from SocnetPackage.BasicFunctionalities import Clusters, Coalitions, GraphOfClusters
from SocnetPackage.Metrics import Asortativity, Degrees

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
#   2. the graph of components
#   3. sample of the components
from time import sleep

def assignGraphsToTasks(G, graphName):
    #Most essential functionality
    components = Clusters.BFSComponents(G)
    coalitions, noncoalitions, problemEdges = Coalitions.filterComponents(components)
    #printClusters(coalitions, noncoalitions)

    #1. Original graph 
    GraphVisualisation.showGraph(G, title=graphName, withLabels=False, showComponents=True)
    showMetrics(G, graphName)

    sleep(0.1)
    #2. Graph of components
    G2 = GraphOfClusters.create(G)
    GraphVisualisation.showGraph(G2, title=graphName + " components")
    showMetrics(G2, graphName + " components graphed")

    sleep(0.1)
    #3. Show a sample of components
    GraphVisualisation.showGraphs(coalitions, "Coalitions of " + graphName)
    GraphVisualisation.showGraphs(noncoalitions, "Noncoalition of " + graphName)
    """
    for graph in coalitions:
        showMetrics(graph)
    for graph in noncoalitions:
        showMetrics(graph)
    """
def showMetrics(G, graphName = ""):
    Degrees.drawCCDegreeDistribution(G, True, graphName)   
    Asortativity.drawKNNandDeg(G, graphName)
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
