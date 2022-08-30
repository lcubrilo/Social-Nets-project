from tabnanny import check
import networkx as nx
from collections import deque

#Dobijanje klastera (komponenti dobijene uklanjanjem negativnih grana)
def checkForNegative(G, cluster):
    for node1 in cluster.nodes:
        for node2 in cluster.nodes:
            if G.has_edge(node1, node2):
                if G.edges[node1, node2]["color"] == "red":
                    cluster.add_edge(node1, node2, color="red")

def BFSComponents(G):
    visited = []
    components = []

    def BFSComponent(node):
        comp = nx.Graph()
        queue = deque()

        def pushNode(x):
            comp.add_node(x)
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

            for neighbor in onlyPositiveNeighbors(curr): #TODO: not all neighbors, just positive ones
                comp.add_edge(curr, neighbor, color = "green")
                if neighbor not in visited:
                    pushNode(neighbor)

        return comp
  
    #G = nx.Graph()
    for node in G:
        if node not in visited:
            components.append(BFSComponent(node))

    for component in components:
        checkForNegative(G, component)

    return components

    