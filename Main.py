from Tasks import assignGraphsToTasks
from SocnetPackage.DataGeneration import SmallExamples, GenerateBigNets, LoadRealNets

#Let's get nets
allNets = []

testCategories = []

#testCategories.append("small")
#testCategories.append("big")
testCategories.append("real")


if "small" in testCategories:
    #Only one
    print("Testing small handcrafted examples: ")
    allNets  += [SmallExamples.buildGraph()]; 

if "big" in testCategories:
    examplePairs = zip([500, 120, 1000, 300], [False, True, False, True])
    print("Testing the following big random nets [nodeCount, clusterable]:", examplePairs)
    allNets += [GenerateBigNets.bigNet(nodeCount, clusterable) for nodeCount, clusterable in examplePairs]

if "real" in testCategories:
    realNets = ["wiki"]#LoadRealNets.getNames()
    
    print("Testing real nets [netName]:", realNets)
    allNets += [LoadRealNets.getNet(netName) for netName in realNets]

for graph in allNets:
    assignGraphsToTasks(graph)
