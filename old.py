import SmallExamples, GraphVisualisation, Clusters

def main():
    G = SmallExamples.buildGraph()
    
    components = Clusters.BFSComponents(G); 
    GraphVisualisation.showComponentGraph(G, components)
    GraphVisualisation.showGraph(G)

main()