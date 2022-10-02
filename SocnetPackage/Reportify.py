def handleGraphInput(G):   
    # G, comps, G2
    from .BasicFunctionalities import Clusters, Coalitions, GraphOfClusters

    comps = Clusters.BFSComponents(G)
    # TODO print a report coal, nonc, problemEdges = Coalitions.filterComponents(comps)
    G2 = GraphOfClusters.create(G)

    print("---------------------------------\nSEPARATED ORIGINAL GRAPH, COMPONENTS, GRAPH OF COMPONENTS")

    from SocnetPackage.Metrics.GraphMetrics import graphMetrics
    from SocnetPackage.Metrics.NodeMetrics import nodeMetrics
    from SocnetPackage.MetricPlots import doMetric, distributions, correlations
    from SocnetPackage.GraphVisualisation import showGraphs, showGraph


    def reportify(Inputs, metrics, optionalPreReportMetrics=None, inputName = "nemam ime", components = None):
        #Plot either 1 graph (ideally unroll with kcore) or plot a sample of 25 components
        nonlocal G, G2
        Graph = G2 if inputName == "Graph of components" else G
        # If we started with multiple things, great (so, not the original graph, or graph of components)

        if type(Inputs) == list: 
            print("---------------------------------\nInput: {}. Target: a list of components".format(inputName))
            showGraphs(Inputs, inputName)
            Graph = Inputs
            targetsOfMetric = None

        # Otherwise, tackle the one thing, and move onto multiple things
        else:
            print("---------------------------------\nINPUT: {}\nTARGET: nodes".format(inputName))
            showGraph(Inputs, components, inputName)
            # TODO DRAW GRAPH BUT WITH NODES COLORED THE INTENSITY OF METRIC M1
            print("---------------------------------\nOPTIONAL REPORT - {}: \njust single values, metrics of the {}".format(inputName, inputName))
            targetsOfMetric = list(Inputs.nodes)
            
            s = "" 
            for met, nam in optionalPreReportMetrics: # Metrics2 can only be graph-wide metrics for G or G2
                #print("Sad radimo", nam)
                s += "    - " + nam + " " + str(doMetric(Graph, None, met, nam)) + "\n"
            print(s) # Print the optional part of report
            print("We may now proceed")
            # TODO edges? I think only in corr; can't see logic in distr

        print("---------------------------------\nMAIN REPORT - {} : metrics of the targets".format(inputName))
        metricsVals = []
        metricNames = []
        for met, nam in metrics:
            val = doMetric(Graph, targetsOfMetric, met, nam)
            print("   - ", nam, val)
            metricsVals.append(val)
            metricNames.append(nam)
            
        print("---------------------------------\nMAIN REPORT - {}: distributions and correlations of those metrics".format(inputName))
        distributions(metricsVals, metricNames, inputName)
        correlations(targetsOfMetric, metricsVals, metricNames, inputName)
        # TODO: save returnvals, and pass them to distr and corr; to be efficient
        print("\n\n\n\n\n")


    #reportify(G, nodeMetrics(), graphMetrics(), inputName = "Original graph", components=comps)
    reportify(comps, graphMetrics(), inputName = "Components")
    #reportify(G2, nodeMetrics(), graphMetrics(), inputName = "Graph of components")