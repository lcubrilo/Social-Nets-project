import SocnetPackage
from SocnetPackage.Reportify import handleGraphInput
from SocnetPackage.DataGeneration import SmallExamples, GenerateBigNets

if __name__ == "__main__":
    handleGraphInput(SmallExamples.buildGraph())
    #handleGraphInput(GenerateBigNets.bigNet(250))
