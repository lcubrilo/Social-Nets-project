# -*- coding: utf-8 -*-
"""
Created on Mon Aug 29 17:24:43 2022

@author: Lenovo
"""
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
import random
import math

def giveColors():
    sampleColors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 
    'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan']
    random.shuffle(sampleColors)
    return iter(sampleColors)

#Dobijanje klastera (komponenti dobijene uklanjanjem negativnih grana)
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
    for node in G.nodes:
        if node not in visited:
            components.append(BFSComponent(node))

    return components

    
#Dobijanje koalicija (klaster nema negativne veze)

def main2():
    G = nx.Graph()
    G.add_nodes_from(range(10))
    x = [2, 4, 7, 3, 1, 8, 3, 5]; y = [3, 6, 1, 5, 4, 2, 5, 1]
    for od, do in zip(x, y):
        G.add_edge(od, do)
        #pos = nx.spring_layout(G, seed=69)  # Seed for reproducible layout
    nx.draw(G)
    plt.show()

def main():
    def buildGraph():
        G = nx.Graph()
        G.add_nodes_from(range(10))
        G.add_edge(1, 2, color="green")
        G.add_edge(3, 2, color="green")
        G.add_edge(4, 5, color="green")
        G.add_edge(1, 5, color="red")
        G.add_edge(4, 2, color="red")
        G.add_edge(2, 6, color="red")
        G.add_edge(6, 7, color="green")
        G.add_edge(7, 8, color="green")
        G.add_edge(6, 8, color="green")
        G.add_edge(3, 9, color="green")
        
        return G
    def showGraph():
        pos = nx.spring_layout(G, seed=50)
        """
        edge_labels = nx.get_edge_attributes(G,'color')
        print(edge_labels)
        nx.draw_networkx_edge_labels(G, pos, edge_labels)"""
    
        edges, edgeColors = zip(*nx.get_edge_attributes(G, 'color').items())
        nx.draw(G, pos, edge_color=edgeColors, width=2, with_labels=True)
        #nx.draw(G, pos)
        plt.show()
    def showComponentGraph():
        pos = nx.spring_layout(G, seed=20)
        noComp = len(components)
        nodeColors = []
        baseNumber = 110*min(9, math.ceil(noComp**0.5)); i=1
        for c in components:
            print(c.nodes, c.edges)
            pos = nx.spring_layout(c, seed=random.randint(5, 31415))
            plt.subplot(baseNumber+i); i+=1 
            if not nodeColors: nodeColors = giveColors()
            edgeinfo = nx.get_edge_attributes(c, 'color').items()
            if edgeinfo:
                edges, edgeColors = zip(*edgeinfo)
            else: edgeColors = "black"
            nx.draw(c, pos, node_color = next(nodeColors), edge_color=edgeColors, width=2, with_labels=True)
        plt.show()
    G = buildGraph()
    
    components = BFSComponents(G); 
    showComponentGraph()
    showGraph()
main()