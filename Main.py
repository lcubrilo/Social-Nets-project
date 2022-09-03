import AcquireGraphs, Tasks

graphs = AcquireGraphs.acquireGraphs()
for graph in graphs:
    Tasks.assignGraphsToTasks(graph)