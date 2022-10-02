from SocnetPackage.GraphVisualisation import showDistribution, showCorrelation
import networkx as nx
# Doing plots for any metric: 1. distribution pots and 2. correlation plots 
# (I obviously need a list of inputs for both)

def doMetric(Graph, targetsOfMetric, metric, metricName): 
    if targetsOfMetric != None:
        if type(targetsOfMetric) == list:
            return [metric(Graph, target) for target in targetsOfMetric]
    elif type(Graph) == list:
        return [metric(G) for G in Graph]
    else: #Got just one (should happen only in the optional pre-report)
        return metric(Graph, targetsOfMetric)

# See distribution for a metric; List input is called "things"
# x-axis: metricVals = doMetric(things)
# y-axis: count(mV); mV € metricVals
def distributions(metricsVals, metricNames = "", thingName = ""): 
    """ 
   DEPRECATED: just give me values, don't make me calc them
   #If input not a list make it a list
    if type(sfgsgdgdeafgdegdfg) != list: 
        rtghrrthtntt = sfgsgdgdeafgdegdfg.nodes if type(sfgsgdgdeafgdegdfg) == type(nx.Graph()) else sfgsgdgdeafgdegdfg
    else: # This means we got components/coalitions/clusters w/e
        rtghrrthtntt = sfgsgdgdeafgdegdfg
    
    # X AXIS
    # If no values given, calc them
    if not metricsVals:
        metricsVals = [doMetric(rtghrrthtntt, metric, metricName) for metric, metricName in metrics]
    # If they're given, it has to make sense - match the no of maetrics
    elif not metrics:
        metricsVals = metricsVals
    elif len(metricsVals) != len(metrics): 
        metricsVals = [doMetric(rtghrrthtntt, metric, metricName) for metric, metricName in metrics]"""
    # Y AXIS
    # We are going through every metric
    print("\n I DISTRIBUTIONS")
    for metricVals, metricNam in zip(metricsVals, metricNames):
        # We have to discretize with continuous data
        def discretizeIfContinuous(arrayOfWhatShouldBeDiscrete):
            for el in arrayOfWhatShouldBeDiscrete:
                if type(el) == float:
                    return [int(10*val) for val in metricVals]
                elif type(el) == int:
                    continue
                else: raise Exception("Must be numerical data") 
            return arrayOfWhatShouldBeDiscrete
                    
        metricVals = discretizeIfContinuous(metricVals)
        # Counting-sort-esque stuff to get y axis
        x = list(range(min(metricVals), max(metricVals)+1))
        y = [0]*len(x)
        # We are going through every value of that metric
        for metDat in metricVals:
            y[metDat]+=1

        #TODO doublecheck I actually DID USE ALL4: THE DISTR, CUM DIST, LOGLOG THING
        showDistribution(x, y, metricNam, thingName)
    
    return x, y

from SocnetPackage.Metrics import Correlations

# For a metric1, run it through all things1 and get metric1Vals
# x-axis: metric1Vals
# For a metric2, run it through all things2 and get metric2Vals
# y-axis: metric2Vals
# 
# Note: the common connecting logic of the two axes (AKA what are things1 and things2) can be two things:
#
#   1. those metrics are being run for the exact same node. (things1 == things2)
#       Eg - if a node has high betwennees centrality, how likely will it ALSO BE OF high eigen centrality
#
#   2. those metrics are being run for two neighbors (things1 != things2 && (t1, t2) € G.edges())
#       Eg - if a node has a betwennees centrality, how likely will likely will it BE CONNECTED TO high eigen centrality

def correlations(Thing, metricsVals, metricNames, graphName=""):
    """
    DEPRECATED
    # If input not a list, make it a list
    if type(Thing) != list: 
        things = Thing.nodes
        #for edge in Thing.edges: # TODO: Why edges???? Maybe makes sense as a parallel thing to nodes; smth like correlations(edges, metrics); correlations(nodes, metrics) but cannot be mixed like  this
            #things.append(edge[0], edge[1])
    else:
        things = Thing"""
    print("\n II CORRELATIONS")
    for i, (x, nam1) in enumerate(zip(metricsVals, metricNames)):
        for j, (y, nam2) in enumerate(zip(metricsVals, metricNames)):
            if i >= j: continue;
            relevance = abs(Correlations.pearsonCorrelation(x,y))
            # I thought spearman was more reasonable, test below points otherwise? TODO
            #print("Outside conditional sees     ", round(relevance, 2))
            if relevance >= 0.3: # or len(metricsVals) < 10:
                showCorrelation(x,y, nam1, nam2, graphName)