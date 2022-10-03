from pathlib import Path
from statistics import correlation
from mdutils.mdutils import MdUtils
from .BasicFunctionalities import Clusters, Coalitions, GraphOfClusters
from SocnetPackage.Metrics.GraphMetrics import graphMetrics
from SocnetPackage.Metrics.NodeMetrics import nodeMetrics
from SocnetPackage.MetricPlots import doMetric, distributions, correlations
from SocnetPackage.GraphVisualisation import showGraphs, showGraph


G, G2, mdFile, comps, coal, nonc, dataSourceName = None, None, None, None, None, None, None

def shortenNam(nam):
    opt1 = ["averageNodeDegree", "netDensity", "sMetric", "smallWorldCoefficitent", "netEfficiency", 'diameter', "radius", "averageClusteringCoefficient"]
    sol1 = ["avgDeg", "dens", "sMet", "smlWrld", "effic", "diam", "rad", "avgClus"]
    if nam in opt1:
        return sol1[opt1.index(nam)]
    
    opt2 = ["degree", "shellIndex", "eccentricity", "clusteringCoefficient", "closenessCentrality", "eigenvectorCentrality"]
    sol2 = ["deg", "shell", "eccen", "clust", "closn", "eigen"]
    if nam in opt2:
        return sol2[opt1.index(nam)]

    return "Unknown metric name, can't shorten."

# Helper function for doing subreports for: Graph, Clusters, Graph of Clusters
def subreport(Inputs, metrics, optionalPreReportMetrics=None, inputName = "nemam ime", components = None, romanNumeral = ""):
    global G, G2, dataSourceName, comps, coal, nonc, mdFile
    mdFile = MdUtils(file_name="Report/{}/{}".format(dataSourceName, inputName), title="{} report".format(dataSourceName))
    Graph = G2 if inputName == "Graph_of_components" else G # Clear up which graph
    
    # Create header for this subreport
    mdFile.new_header(level=1, title=romanNumeral + " " + inputName)
    mdFile.new_header(level=2, title="Visualize")

    #region If we started with multiple things, great (so, not the original graph, or graph of components)
    if type(Inputs) == list: 
        # print("---------------------------------\nInput: {}. Target: a list of components".format(inputName))
        showGraphs(coal, "Coalitions", sourceDataFileName=dataSourceName, graphName=inputName)
        showGraphs(nonc, "Noncoalitions", sourceDataFileName=dataSourceName, graphName=inputName)

        Graph = Inputs
        targetsOfMetric = None

        mdFile.new_line(mdFile.new_inline_image(text="Coalitions", path="/Report/{}/{}/Coalitions.png".format(dataSourceName, inputName)))
        mdFile.new_line(mdFile.new_inline_image(text="Noncoalitions", path="/Report/{}/{}/Noncoalitions.png".format(dataSourceName, inputName)))
        
    #endregion

    #region Otherwise, tackle the one thing (optional), and move onto multiple things
    else:
        #print("---------------------------------\nINPUT: {}\nTARGET: nodes".format(inputName))
        # TODO: unroll with kcore for huge SocNets, we dont have to see unrelevant guys and it showcases exp/pow growth
        # TODO DRAW GRAPH BUT WITH NODES COLORED THE INTENSITY OF METRIC
        #print("---------------------------------\nOPTIONAL REPORT - {}: \njust single values, metrics of the {}".format(inputName, inputName))
        targetsOfMetric = list(Inputs.nodes())
        mdFile.new_line(mdFile.new_inline_image(text="Indeed, image", path="/Report/{}/{}/SocialNetwork.png".format(dataSourceName, inputName)))
        
        mdFile.new_header(level=2, title="OPTIONAL REPORT - {}: \njust single values, metrics of the {}".format(inputName, inputName))
        lines = "" 
        for met, nam in optionalPreReportMetrics: # Metrics2 can only be graph-wide metrics for G or G2
            #print("Sad radimo", nam)
            metVal = doMetric(Graph, None, met, nam)
            if nam == "netEfficiency":
                print("Ustavljaj")
            if type(metVal) == str:
                print("Zasto exceptions ne rade svoj posao")
            stringLine = "    - " + nam + " " + str(metVal)
            if metVal > 1 or metVal < -1:
                numRepres = "{}".format(round(metVal, 2))
            else:
                numRepres = "{:.2%}".format(metVal) 
            graphLine = "{}:{}; ".format(shortenNam(nam), numRepres)
            mdFile.new_line(stringLine)
            lines += graphLine

        showGraph(Inputs, components, lines, withLabels= (inputName != "Original_graph"), sourceDataFileName = dataSourceName, saveDirName= inputName, suptitle=inputName)
        # mdFile.new_paragraph(lines) # Print the optional part of report
        # print("We may now proceed")
        # TODO edges? I think only in corr; can't see logic in distr
    #endregion
    
    #region Get important data
    
    # Metric data
    metricsVals = []
    metricNames = []
    for met, nam in metrics:
        val = doMetric(Graph, targetsOfMetric, met, nam)
        print("   * {} {}".format(nam, val if len(val) < 10 else "{} values...".format(len(val))))
        metricsVals.append(val)
        metricNames.append(nam)

    # Distribution and correlation data
    distributions(metricsVals, metricNames, inputName, coal, comps, dataSourceName)
    metricTable, corrTable, reportThisText = correlations(targetsOfMetric, metricsVals, metricNames, inputName, coal, comps, dataSourceName)
    #endregion
    
    #region Write them in the same order in the report
    mdFile.new_header(level=2, title="MAIN REPORT - {} : metrics of the targets table".format(inputName))
    mdFile.new_paragraph(metricTable) 


    mdFile.new_header(level=2, title="MAIN REPORT - {}: metric distribution plots".format(inputName))
    mdFile.new_paragraph(reportThisText) 
    for plottedMetric in metricNames:
        mdFile.new_line(mdFile.new_inline_image(text="Indeed, image", path="/Report/{}/{}/{}_Distr.png".format(dataSourceName, inputName, plottedMetric)))


    mdFile.new_header(level=2, title="MAIN REPORT - {}: metric correlations table and plots".format(inputName))
    mdFile.new_paragraph(corrTable) 
    mdFile.new_line("\nCorrelation table visualized:\n")
    mdFile.new_line(mdFile.new_inline_image(text="Indeed, image", path="/Report/{}/{}/CORR_COLORMAP.png".format(dataSourceName, inputName)))

    for metricName1 in metricNames:
        for metricName2 in metricNames:
            path = "/Report/{}/{}/{}_{}.png".format(dataSourceName, inputName, metricName1, metricName2); import os
            if os.path.exists(path):
                mdFile.new_line(mdFile.new_inline_image(text="Indeed, image", path=path))
    
    #endregion End this subreport
    
    mdFile.new_paragraph("---\n\n---") 
    mdFile.create_md_file()

# Msin gunvyion when give a graph loaded from file or elsewhere
def handleGraphInput(G1, dataSourceName1):
    global G, G2, mdFile, comps, coal, nonc, dataSourceName
    G = G1; dataSourceName = dataSourceName1

    #region Report initialize
    # Make Report folder
    Path("Report", dataSourceName).mkdir(parents=True, exist_ok=True)

    # Make three subfolders
    threeThingsToReport = ["Original_graph", "Components", "Graph_of_components"]
    for subfolder in threeThingsToReport:
        Path("Report", dataSourceName, subfolder).mkdir(parents=True, exist_ok=True)

    # Create MarkDown report file
    mdFile = MdUtils(file_name="Report"+dataSourceName, title="{} report".format(dataSourceName))
    mdFile.new_header(level=1, title=dataSourceName) 
    #endregion

    #region Get new separate data
    # Clusterize
    coal, nonc, problemEdges = Clusters.BFSComponents(G)
    comps = coal + nonc
    G2 = GraphOfClusters.create(G)

    # By clusterizing, we've set up three branches
    mdFile.new_paragraph("CLUSTERIZATION INTO -> ")
    mdFile.new_table_of_contents(table_title='Contents', depth=2)
    
    # Write clusterization status in the report
    if problemEdges != []:
        mdFile.new_header(level=2, title="This graph is not clusterable.")
        mdFile.new_header(level=2, title="The following edges are the preventing this: {}".format(problemEdges))
    else: mdFile.new_header(level=2, title="This graph is clusterable!")
    mdFile.new_header(level=2, title="There are {} components/clusters. {} coalitions and {} noncoalitions".format(len(comps),len(coal), len(nonc)))
    #endregion

    # Branch off
    subreport(G, nodeMetrics(), graphMetrics(), inputName = threeThingsToReport[0], components=comps, romanNumeral="I")
    subreport(comps, graphMetrics(), inputName = threeThingsToReport[1], romanNumeral="II")
    subreport(G2, nodeMetrics(), graphMetrics(), inputName = threeThingsToReport[2], romanNumeral="III")
    
    # Finalize report
    #mdFile.create_md_file()