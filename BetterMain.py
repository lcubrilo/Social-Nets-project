from SocnetPackage.DataGeneration import SmallExamples
import papermill as pm

name = "wiki"
pm.execute_notebook(
   'Layout3.ipynb',
   '{}.ipynb'.format(name),
   parameters=dict(netName = name)
)