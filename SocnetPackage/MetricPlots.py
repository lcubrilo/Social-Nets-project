from cmath import nan
from SocnetPackage.GraphVisualisation import showDistribution, showCorrelation
import networkx as nx
# Doing plots for any metric: 1. distribution pots and 2. correlation plots 
# (I obviously need a list of inputs for both)

def doMetric(Graph, targetsOfMetric, metric, metricName): 
    print("Doing {} on {}".format(metricName, str(Graph)))
    if targetsOfMetric != None:
        if type(targetsOfMetric) == list:
            retVal = []
            for target in targetsOfMetric:
                retVal.append(metric(Graph, target))
            print("Done.")
            return retVal

    elif type(Graph) == list:
        print("Done.")
        return [metric(G) for G in Graph]

    else: #Got just one (should happen only in the optional pre-report)
        retVal = metric(Graph, targetsOfMetric)
        if type(retVal) != str or retVal != None:
            print("Done.")
            return retVal
        print("Hjustone.")


def distributions(metricsVals, metricNames = "", thingName = "", coalitions = [], components = [], fileName = ""): 
    """ # See distribution for a metric; List input is called "things"
    ## x-axis: metricVals = doMetric(things)
    ## y-axis: count(mV); mV € metricVals"""
    
    # Y AXIS
    # We are going through every metric
    print("\n I DISTRIBUTIONS")
    for metricVals, metricNam in zip(metricsVals, metricNames):
        print("{} started".format(metricNam))
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
            if metVal not in valFreq: 
                valFreq[metVal] = 0
            valFreq[metVal]+=1
        
        x = []; y = []
        for key in sorted(valFreq.keys()):
            x.append(key); y.append(valFreq[key])

        showDistribution(x, y, metricNam, thingName, coalitions, components, fileName)
    
    return# values, frequency

from SocnetPackage.Metrics import Correlations

# For a metric1, run it through all things1 and get metric1Vals
# x-axis: metric1Vals
# For a metric2, run it through all things2 and get metric2Vals
# y-axis: metric2Vals
# 
# Note: the common connecting logic of the two axes (AKA what are things1 and things2) can be two things:
#
#   1. those metrics are being run for the exact same node. (things1 == things2) implemented
#       Eg - if a node has high betwennees centrality, how likely will it ALSO BE OF high eigen centrality
#
#   2. those metrics are being run for two neighbors (things1 != things2 && (t1, t2) € G.edges()) TODO
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
def correlations(Thing, metricsVals, MetricNames, graphName="", coalitions = [], components = [], sourceInputFileName = ""):
    print("\n II CORRELATIONS")
    shortMetricNames = shorterMetricNames(MetricNames)
    import pandas as pd; from IPython.display import display
    df = pd.DataFrame({name:[round(val, 4) for val in vals] for name, vals in zip(MetricNames, metricsVals)})
    display(df.to_markdown())
    
    print("--------------")
    corrMat1 = df.corr()
    corrMat2 = df.corr("spearman")
    for axis1 in corrMat1:
        if type(axis1) == str: continue
        for axis2 in axis1:
            axis2 = round(axis2, 4)
    #corrMat.columns = shortMetricNames
    display(corrMat1.to_markdown())

    textForTheReport = "### Most significant correlations:\n"
    for i, nam1 in enumerate(MetricNames):
        for j, nam2 in enumerate(MetricNames):
            currCorr = corrMat1[nam1][nam2]
            if i>=j: continue
            if corrMat1[nam1][nam2] > 0.8 or corrMat2[nam1][nam2] > 0.8:
                showCorrelation(df[MetricNames[i]], df[nam2], currCorr, nam1, nam2, graphName, sourceDataFileName=sourceInputFileName)
                textForTheReport += Correlations.distReport("{}-{}".format(nam1, nam2), [currCorr, corrMat2[nam1][nam2]]) + "\n"
            #else:
                #print("{}&{} combo was fruitless.".format(nam1, nam2))
      
    #TODO
    #plt.show()
    graphOfAllCorrelations((corrMat1, corrMat2), MetricNames, graphName, sourceInputFileName)
    return df.to_markdown(), corrMat1.to_markdown(), textForTheReport

def graphOfAllCorrelations(corrMat, MetricNames, graphName="", sourceInputFileName = ""):
    import matplotlib.pyplot as plt
    corrMat1, corrMat2 = corrMat
    fig, ax = plt.subplots(1, 1, figsize=(14,10))
    plotX, plotY, sizes, colors = [], [], [], []
    ax.axline([0, 0], [1, 1], color = 'darkgreen')
    for i, nam1 in enumerate(MetricNames):
        for j, nam2 in enumerate(MetricNames):
            if i>=j: continue;
            offset = 0
            for corr in corrMat:
                # Prepare data for scatter
                plotX.append(MetricNames.index(nam1)+offset)
                plotY.append(MetricNames.index(nam2)+offset)
                sizes.append(20+(65*abs(corr[nam1][nam2]))**2)
                colors.append(determineColor(corr[nam1][nam2]))

                # Write actual labels/vals/text on top
                scaleX = 1.24; scaleY = 1.06; move = 0.35
                posX = (i*scaleX + move) / len(MetricNames)
                posY = (j*scaleY + move) / len(MetricNames)
                bothCorr = "{:.0%}, {:.0%}".format(corrMat1[nam1][nam2], corrMat2[nam1][nam2])
                plt.text(posX, posY, bothCorr, transform=ax.transAxes)
                offset += 0.15

    plt.text(0.8, 0.1,"Pearson downleft, Spearman upright\nRed and green strong correlations\nPurple and olive medium\nblue weak, black empty", transform=ax.transAxes, horizontalalignment='right')
    #ax.set(title = "Red and green strong correlations, purple and olive medium, blue weak, black empty")
    ax.scatter(plotX, plotY, sizes, colors, alpha = 0.7)
    fig.suptitle("(DIS)/(A)/(NON)SORTATIVITY (more green, red, blue respectively): Correlation between metrics for "+graphName)

    labels = []; labels.append(""); 
    for mn in MetricNames: labels.append(mn)
    ax.set_xticklabels(labels); ax.set_yticklabels(labels)

    plt.savefig(fname="Report/{}/{}/CORR_COLORMAP.png".format(sourceInputFileName, graphName))
    plt.show(); plt.close();

def determineColor(correlationStrength):
    # Probably NaN
    if correlationStrength == 0: return "black" 

    # Impossible, kinda hide urself
    if abs(correlationStrength) > 1: return "white" 

    # As intense as it gets
    if correlationStrength == 1: return "darkgreen"
    if correlationStrength == -1: return "darkred"

    # Shades
    if correlationStrength < -0.8: return "red"
    elif correlationStrength < -0.5: return "purple"
    elif correlationStrength > 0.8: return "green"
    elif correlationStrength > 0.5: return "olive"

    # Not too interesting
    else: return "blue"
