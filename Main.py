import SocnetPackage
from SocnetPackage.Reportify import handleGraphInput
from SocnetPackage.DataGeneration import SmallExamples, GenerateBigNets, LoadRealNets
from pathlib import Path

Path("Report").mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    # handleGraphInput(SmallExamples.buildGraph())
    handleGraphInput(GenerateBigNets.bigNet(250, False), "bigNet")
    
    """"print("Real nets.")
    for realNet in LoadRealNets.fastLoader:
        print("Loading {}".format(realNet))
        G = LoadRealNets.getNet(realNet)
        handleGraphInput(G, realNet)"""
