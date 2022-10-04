import networkx as nx
import matplotlib.pyplot as plt
G = nx.Graph()
def loadWiki(limiter = -1):
    global G; G = nx.Graph(); i = 0
    print("Loading from original file")                    
    with open(r"SocnetPackage\DataGeneration\wiki-RfA.txt", 'r', encoding="utf8") as f:
        users = {}
        for line in f:
            tag, data = line[:3].strip(), line[4:].strip()
            if tag == "SRC": 
                if data not in users: users[data] = len(users) #giving them unique integer IDs
                u = users[data]
            elif tag == "TGT": 
                if data not in users: users[data] = len(users)
                v = users[data]
            elif tag == "VOT":
                if G.has_edge(u, v):
                    if G.edges[u, v]["color"] == "red": continue
                G.add_edge(u, v, color = "red" if data == "-1" else "green")
            else: continue

            i+=1
            if limiter != -1 and i > limiter: 
                break
            #print(line)
    
    graphToTxt(G, fastLoader["wiki"][1])
    return G  
def loadEpinions(limiter = -1):
    global G; G = nx.Graph(); i = 0
                        
    with open(r"SocnetPackage\DataGeneration\soc-sign-epinions.txt", 'r', encoding="utf8") as f:
        users = {}
        for line in f:
            if line[0] == "#": continue
            u, v, sign = line.split("	") 
            u, v, color = int(u), int(v), "red" if sign == "-1" else "green"

            if G.has_edge(u, v):
                if G.edges[u, v]["color"] == "red": continue
            G.add_edge(u, v, color = color)

            i+=1
            if limiter != -1 and i > limiter: 
                break
            #print(line)
    
    graphToTxt(G, fastLoader["epinions"][1])
    return G 
def loadSlashdot(limiter = - 1):
    global G; G = nx.Graph(); i = 0
                        
    with open(r"SocnetPackage\DataGeneration\soc-sign-Slashdot090221.txt", 'r', encoding="utf8") as f:
        users = {}
        for line in f:
            if line[0] == "#": continue
            u, v, sign = line.split("	") 
            u, v, color = int(u), int(v), "red" if sign == "-1" else "green"

            if G.has_edge(u, v):
                if G.edges[u, v]["color"] == "red": continue
            G.add_edge(u, v, color = color)

            i+=1
            if limiter != -1 and i > limiter: 
                break
            #print(line)
    
    graphToTxt(G, fastLoader["slashdot"][1])
    return G 

fastLoader = {
    "wiki": (loadWiki, "SocnetPackage\DataGeneration\wiki-RfA-simpler.txt"),
    "epinions": (loadEpinions, "SocnetPackage\DataGeneration\soc-sign-epinions-simpler.txt"),
    "slashdot": (loadSlashdot, "SocnetPackage\DataGeneration\soc-sign-Slashdot090221-simpler.txt")
}
def getNames(): return [name for name in fastLoader]

def getNet(name):
    (loadFunc, path) = fastLoader[name]
    G = txtToGraph(path)
    if G == False:
        print("Taking from original file")
        return loadFunc() #TODO: change
    else:
        return G
    print("Got net")


def graphToTxt(G, path = "SocnetPackage\DataGeneration"):
    if path == "SocnetPackage\DataGeneration":
        path += "\exported.txt"
    with open(path, 'w+', encoding="utf8") as f:
        f.write("#{}\n".format(str(G)))
        for edge in G.edges:
            f.write(str(edge)[1:-1]+", {}\n".format(G.edges[edge]["color"]))
        return True
    return False

def txtToGraph(path = "SocnetPackage\DataGeneration\exported.txt"):
    try:  
        G = nx.Graph()
        with open(path, "r", encoding="utf8") as f:
            i = 0
            for line in f:
                if line[0] == "#":
                    continue
                [u, v, color] = line[:-1].split(", ")
                G.add_edge(int(u), int(v), color = color)

                i+=1
                if i % 10000 == 1: 
                    print("{} lines of data read thus far".format(i))
            print("Got from quickload file")
            return G
    except:
        print ("Fail")
        return False

from time import time

start, timeAtFreeze= time(), 0
def printDuration(operationName = ""):
    global start, timeAtFreeze
    if timeAtFreeze > 0: unfreezeTime()
    print(operationName, "took {}".format(convertTime(time()-start)))
    start = time()
def convertTime(time): #given in seconds:
    if time < 1:
        return str(round(time*1000, 2)) + "ms"
    elif time > 60:
        return str(int(time/60)) + "min " + str(round(time%60, 2)) + "s"
    else:
        return str(round(time, 2)) + "s"

def freezeTime():
    global timeAtFreeze
    timeAtFreeze = time()
def unfreezeTime():
    global start, timeAtFreeze
    if timeAtFreeze > 0:
        start += time() - timeAtFreeze
        timeAtFreeze = 0


def showGraph(G, components = [], graphname = "graph", AX = None, withLabels = None, fontColor = "white"):
    graphname += ".dot"
    if withLabels == None:
        withLabels = type(list(G.nodes)[0])==str
    """
    edge_labels = nx.get_edge_attributes(G,'color')
    print(edge_labels)
    nx.draw_networkx_edge_labels(G, pos, edge_labels)"""

    edAt = nx.get_edge_attributes(G, 'color')
    if edAt :
        edges, edgeColors = zip(*edAt.items())
        weights = []
        for e, eC in zip(edges, edgeColors):
            weight_val = 1 if eC == "green" else 3
            G.add_edge(e[0], e[1], weight = weight_val/0.5)
            weights.append(3/weight_val)
        
    else: edgeColors = ["black"]; weights = [1.5]; 
    
    ndAt = nx.get_node_attributes(G, 'color')
    if ndAt:
        nodeColors = [G.nodes[n]["color"] for n in G.nodes]
    else:
        nodeColors = ["blue"]
    
    pos = nx.kamada_kawai_layout(G)
    #showComponentNames(pos, components)
    """ from networkx.drawing.nx_agraph import write_dot; write_dot(G,graphname)
    import os; Thread(target=lambda: os.startfile(graphname)).start()"""

    #if type(G) == type(nx.MultiGraph()):
        
        ##import pydot; (graph,) = pydot.graph_from_dot_file('multi.dot'); graph.write_png('somefile.png')
        ###from PIL import Image; Image.open('somefile.png').show()
        ####nx.draw(G, pos, edge_color=edgeColors, width=2, with_labels=True, connectionstyle="arc3,rad=0.3")
    #else:
    nx.draw(G, pos, edge_color=edgeColors, width=weights, node_color=nodeColors, with_labels=withLabels, font_color=fontColor, ax = AX)
    #nx.draw(G, pos)
    if AX == None:
        plt.show()
