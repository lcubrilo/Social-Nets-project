def filterComponents(clusters):
    coalitions, wannabes = [], []
    for c in clusters:
        status = isCoalition(c)
        if status[0]:
            coalitions.append(c)
        else:
            wannabes.append((c, status[1]))
    return coalitions, wannabes

import networkx as nx
def isCoalition(cluster):
    problematicEdges = []
    for n1, n2, color in cluster.edges.data("color"):
        if color == "red":
            problematicEdges.append((n1, n2))
    
    if problematicEdges == []:
        return True, []
    else:
        return False, problematicEdges
    """for e in cluster.edges():
        if e['color'] == 'red':
            return False
    return True"""
                
