import SocnetPackage
from SocnetPackage.Reportify import handleGraphInput
from SocnetPackage.DataGeneration import SmallExamples

if __name__ == "__main__":
    handleGraphInput(SmallExamples.buildGraph())
