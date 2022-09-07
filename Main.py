from Tasks import assignGraphsToTasks
from SocnetPackage.DataGeneration import SmallExamples, GenerateBigNets, LoadRealNets

#Let's get nets
allNets = {}

testCategories = []

testCategories.append("small")
#testCategories.append("big")
testCategories.append("real")


if "small" in testCategories:
    #Only one
    print("Will test small handcrafted examples: ")
    allNets["small"] = SmallExamples.buildGraph()

if "big" in testCategories:
    examplePairs = zip([500, 120, 1000, 300], [False, True, False, True])
    print("Will test the following big random nets [nodeCount, clusterable]:", examplePairs)
    for i, (nodeCount, clusterable) in enumerate(examplePairs):
        allNets["big{}".format(i)] = GenerateBigNets.bigNet(nodeCount, clusterable)

if "real" in testCategories:
    realNets = ["wiki", "epinions", "slashdot"]#LoadRealNets.getNames()
    
    print("Will test real nets [netName]:", realNets)
    for netName in realNets:
        allNets[netName] = LoadRealNets.getNet(netName) 

import papermill as pm

for graphName in allNets:
    #print("\tTesting " + graphName)
    #assignGraphsToTasks(, graphName)
    pm.execute_notebook(
        'Layout3.ipynb',
        '{}.ipynb'.format(graphName),
        parameters=dict(G=allNets[graphName])
    )


