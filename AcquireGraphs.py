from SocnetPackage.DataGeneration import SmallExamples, GenerateBigNets, LoadRealNets

def acquireGraphs():
    return [LoadRealNets.getNet("wiki")]
