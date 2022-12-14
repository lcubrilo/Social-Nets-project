import networkx as nx
from collections import deque
from ..ComponentNamesColors import iterateThruComponentNames, giveColors
from random import choice

#Dobijanje klastera (komponenti dobijene uklanjanjem negativnih grana)
def checkForNegative(G, cluster):
    for node1 in cluster.nodes:
        for node2 in cluster.nodes:
            if G.has_edge(node1, node2):
                if G.edges[node1, node2]["color"] == "red":
                    cluster.add_edge(node1, node2, color="red")

problemEdges = []
nonc = []
coal = []
def BFSComponents(G, legitimateLinksFunction = None):
    nx.set_node_attributes(G, None, "component")
    visited = []
    components = []
    componentName = "A"
    def BFSComponent(node, compName):
        global problemEdges, nonc
        comp = nx.Graph()
        queue = deque()
        thisComponentsColor = choice(list(giveColors()))

        def pushNode(x):
            comp.add_node(x, component = compName, color = thisComponentsColor)
            G.nodes[x]["component"] = compName
            G.nodes[x]["color"] = thisComponentsColor
            visited.append(x)
            queue.append(x)
        def onlyPositiveNeighbors(x):
            positiveNeighbors = []
            for neighbor in G.neighbors(x):
                if G.edges[x, neighbor]["color"] == "green":
                    positiveNeighbors.append(neighbor)
            return positiveNeighbors
        pushNode(node)

        while queue:
            curr = queue.popleft()

            for neighbor in G.neighbors(curr):
                if G.edges[curr, neighbor]["color"] == "green" :
                    comp.add_edge(curr, neighbor, color = "green")

                elif G.nodes[neighbor]["component"] == comp:
                    comp.add_edge(curr, neighbor, color = "red")
                    problemEdges.append(curr, neighbor)
                    nonc.append(comp)
                    continue;
                else: continue;

                if neighbor not in visited:
                    pushNode(neighbor)

        return comp
  
    #G = nx.Graph()
    for node in G:
        if node not in visited:
            # ????????? TODO
            components.append(BFSComponent(node, componentName))
            componentName = iterateThruComponentNames(componentName)

    for component in components:
        if component not in nonc:
            coal.append(component)

    return coal, nonc, problemEdges

    