# Show me the distributions/correlations of node metrics

# For x axis
def groupNodesByVal(nodeValPairs):
    nodeValPairs = sorted(nodeValPairs, key= lambda pair:pair[1])

    firstNode, itsVal = nodeValPairs[0]
    currVal = itsVal; currGroup = []; groupedNodes = {}

    for (node, val) in nodeValPairs:
        if val == currVal:
            currGroup.append(node)
        else:
            groupedNodes[currVal] = currGroup
            currVal = val; currGroup = []
    
    #{val:[nodes with that val]}
    return groupedNodes

def groupNodesByMetric(allNodes, metric1):
    vals1 = [metric1(node) for node in allNodes]
    return groupNodesByVal(zip(allNodes, vals1))

# For y axis - distributions
def frequencyOfGroup(group, whole):
    return len(group)/len(whole)

def distribution(allNodes, metric1):
    #How common is it for a node to have a certain metric value?
    groups = groupNodesByMetric(allNodes, metric1)
    
    x, y = [], []
    for val in groups:
        x.append(val)
        y.append(frequencyOfGroup(groups[val], allNodes))

    return x, y

# For y axis - correlations
def avgValsOfNodes(nodes, metric2):
    vals2 = [metric2(node) for node in nodes]
    return sum(vals2)/len(vals2)

def comparison(allNodes, metric1, metric2):
    #If a node usually has a certain metric1 value, what metric2 value does it have on average?
    groups = groupNodesByMetric(allNodes, metric1)
    
    x, y = [], []
    for val in groups:
        x.append(val) 
        y.append(avgValsOfNodes(groups[val], metric2))

    return x, y
