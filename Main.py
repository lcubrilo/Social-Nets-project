import SocnetPackage
from SocnetPackage.Reportify import handleGraphInput
from SocnetPackage.DataGeneration import SmallExamples, GenerateBigNets
from pathlib import Path

Path("Report").mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    #handleGraphInput(SmallExamples.buildGraph())
    handleGraphInput(GenerateBigNets.bigNet(50), "bigNet")
