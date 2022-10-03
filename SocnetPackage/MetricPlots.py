from cmath import nan
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
def distributions(metricsVals, metricNames = "", thingName = "", coalitions = [], components = [], fileName = ""): 
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
        valFreq = {}
        # We are going through every value of that metric
        for metVal in metricVals:
            if metVal not in valFreq: valFreq[metVal] = 0
            valFreq[metVal]+=1
        
        x = []; y = []
        for key in sorted(valFreq.keys()):
            x.append(key); y.append(valFreq[key])

        #showDistribution(x, y, metricNam, thingName, coalitions, components, fileName)
    
    return# values, frequency

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
def shorterMetricNames(metricNames):
    if metricNames[0] == "averageDegree":
        return ["avgDeg", "dens", "sMetr", "smlwrldC", "effic", "diam", "rad", "avgClusC"]
    else:
        return ["deg", "shell", "eccent", "clustCoef", "btwnes", "clsnes", "eigen"]
    """return {                 
        "averageNodeDegree":"avgDeg", 
        "netDensity":"dens", 
        "sMetric":"sMetr", 
        "smallWorldCoefficitent":"smlwrldC", 
        "netEfficiency":"effic", 
        "diameter":"diam", 
        "radius":"rad", 
        "averageClusteringCoefficient":"avgClusC"
    }"""
def correlations(Thing, metricsVals, MetricNames, graphName="", coalitions = [], components = [], sourceInputFileNAme = ""):
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
    shortMetricNames = shorterMetricNames(MetricNames)
    import pandas as pd; from IPython.display import display
    df = pd.DataFrame({name:[round(val, 4) for val in vals] for name, vals in zip(MetricNames, metricsVals)})
    display(df.to_markdown())
    
    print("--------------")
    corrMat = df.corr()
    corrMat2 = df.corr("spearman")
    for axis1 in corrMat:
        if type(axis1) == str: continue
        for axis2 in axis1:
            axis2 = round(axis2, 4)
    #corrMat.columns = shortMetricNames
    display(corrMat.to_markdown())

    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1,1)
    plotX, plotY, sizes, colors = [], [], [], []
    for i, nam1 in enumerate(MetricNames):
        for j, nam2 in enumerate(MetricNames):
            currCorr = corrMat[nam1][nam2]
            if str(currCorr) != "nan":
                if currCorr < -0.8: color = "red"
                elif currCorr < -0.5: color = "purple"
                elif currCorr > 0.8: color = "green"
                elif currCorr > 0.5: color = "olive"
                else: color = "blue"
                plotX.append(nam1); plotY.append(nam2); sizes.append(20+(30*abs(currCorr))**2); colors.append(color if i!=j else "darkgreen")
            else:  plotX.append(nam1); plotY.append(nam2); sizes.append(20); colors.append("black")
            plt.text((i*1.015+0.35)/len(MetricNames), (j*1.015+0.35)/len(MetricNames), str(round(currCorr*100, 2))+"%", transform=ax.transAxes)
            if i>=j: continue
            if currCorr > 0.8:
                #showCorrelation(df[MetricNames[i], df[nam2]])
                #showCorrelation(df[MetricNames[i]], df[nam2], currCorr, nam1, nam2, graphName, sourceInputFileNAme)
                print(Correlations.distReport("{}-{}".format(nam1, nam2), [currCorr, corrMat2[nam1][nam2]]))
            #else:
                #print("{}&{} combo was fruitless.".format(nam1, nam2))
    
    ax.set(title = "Red and green strong correlations, purple and olive medium, blue weak, black empty")
    ax.scatter(plotX, plotY, sizes, colors, alpha = 0.8)
    fig.suptitle("(DIS)/(A)/(NON)SORTATIVITY (more green, red, blue respectively): Correlation between metrics for "+graphName)
    plt.savefig(fname="Report/{}/{}/CORR_COLORMAP.png".format(sourceInputFileNAme, graphName))
    #TODO
    #plt.show()
    return df.to_markdown(), corrMat.to_markdown()