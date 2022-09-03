import Tasks
from SocnetPackage.DataGeneration import SmallExamples, GenerateBigNets, LoadRealNets

Tasks.assignGraphsToTasks(LoadRealNets.getNet("epinions")); 
"""


for graph in [LoadRealNets.getNet(netName) for netName in ["wiki", "epinions"]]:
    Tasks.assignGraphsToTasks(graph)

    LoadRealNets.getNet("wiki")
    """