
bigNet report
=============

# III Graph_of_components

## Visualize
  
![Indeed, image](/Report/bigNet/Graph_of_components/SocialNetwork.png)
## OPTIONAL REPORT - Graph_of_components: 
just single values, metrics of the Graph_of_components
  
    - averageNodeDegree 2.4615384615384617  
    - netDensity 0.017287234042553192  
    - sMetric 504  
    - smallWorldCoefficitent 4.17948717948718  
    - netEfficiency 0.3108347792558321  
    - diameter 9  
    - radius 5  
    - averageClusteringCoefficient 0.13333333333333333
## MAIN REPORT - Graph_of_components : metrics of the targets table


|    |   degree |   shellIndex |   eccentricity |   clusteringCoefficient |   closenessCentrality |   eigenvectorCentrality |
|---:|---------:|-------------:|---------------:|------------------------:|----------------------:|------------------------:|
|  0 |        5 |            2 |              5 |                  0      |                     0 |                  0.2006 |
|  1 |        4 |            2 |              5 |                  0      |                     1 |                  0.3287 |
|  2 |        4 |            2 |              6 |                  0.1667 |                     2 |                  0.3396 |
|  3 |        2 |            1 |              6 |                  0      |                     1 |                  0.0625 |
|  4 |        2 |            2 |              6 |                  0.5    |                     2 |                  0.1903 |
|  5 |        6 |            2 |              6 |                  0      |                     1 |                  0.1877 |
|  6 |        3 |            1 |              6 |                  0      |                     1 |                  0.0698 |
|  7 |        2 |            1 |              7 |                  0      |                     2 |                  0.0216 |
|  8 |        1 |            1 |              8 |                 -1      |                     3 |                  0.0062 |
|  9 |        4 |            2 |              6 |                  0      |                     2 |                  0.2372 |
| 10 |        5 |            2 |              6 |                  0.05   |                     2 |                  0.4234 |
| 11 |        1 |            1 |              7 |                 -1      |                     2 |                  0.0177 |
| 12 |        3 |            2 |              7 |                  0.1667 |                     3 |                  0.2903 |
| 13 |        3 |            2 |              7 |                  0.1667 |                     3 |                  0.2903 |
| 14 |        1 |            1 |              7 |                 -1      |                     2 |                  0.0533 |
| 15 |        2 |            1 |              7 |                  0      |                     2 |                  0.0217 |
| 16 |        4 |            2 |              7 |                  0      |                     3 |                  0.1054 |
| 17 |        3 |            2 |              8 |                  0      |                     4 |                  0.0473 |
| 18 |        5 |            2 |              8 |                  0.05   |                     4 |                  0.3068 |
| 19 |        1 |            1 |              9 |                 -1      |                     5 |                  0.0135 |
| 20 |        1 |            1 |              9 |                 -1      |                     5 |                  0.0872 |
| 21 |        2 |            2 |              8 |                  0      |                     4 |                  0.047  |
| 22 |        2 |            1 |              7 |                  0      |                     2 |                  0.058  |
| 23 |        1 |            1 |              8 |                 -1      |                     3 |                  0.0166 |
| 24 |        4 |            2 |              7 |                  0      |                     3 |                  0.2513 |
| 25 |        2 |            2 |              8 |                  0.5    |                     4 |                  0.1587 |
| 26 |        1 |            1 |              7 |                 -1      |                     2 |                  0.0533 |
| 27 |        1 |            1 |              7 |                 -1      |                     2 |                  0.0533 |
| 28 |        5 |            2 |              7 |                  0      |                     3 |                  0.1177 |
| 29 |        2 |            1 |              8 |                  0      |                     3 |                  0.0068 |
| 30 |        1 |            1 |              9 |                 -1      |                     4 |                  0.0019 |
| 31 |        2 |            2 |              8 |                  0.5    |                     4 |                  0.0469 |
| 32 |        2 |            2 |              8 |                  0.5    |                     4 |                  0.0469 |
| 33 |        2 |            2 |              8 |                  0.5    |                     4 |                  0.042  |
| 34 |        2 |            2 |              8 |                  0.5    |                     4 |                  0.042  |
| 35 |        2 |            1 |              8 |                  0      |                     4 |                  0.0778 |
| 36 |        1 |            1 |              9 |                 -1      |                     5 |                  0.0221 |
| 37 |        1 |            1 |              8 |                 -1      |                     4 |                  0.0335 |
| 38 |        1 |            1 |              6 |                 -1      |                     1 |                  0.0574 |
## MAIN REPORT - Graph_of_components: metric distribution plots


### Most significant correlations:
    * eccentricity-closenessCentrality(coals): 
    * eccentricity-closenessCentrality(noncoals): +0.25% likelier apower distribution (92.74%).
  
![Indeed, image](/Report/bigNet/Graph_of_components/degree_Distr.png)  
![Indeed, image](/Report/bigNet/Graph_of_components/shellIndex_Distr.png)  
![Indeed, image](/Report/bigNet/Graph_of_components/eccentricity_Distr.png)  
![Indeed, image](/Report/bigNet/Graph_of_components/clusteringCoefficient_Distr.png)  
![Indeed, image](/Report/bigNet/Graph_of_components/closenessCentrality_Distr.png)  
![Indeed, image](/Report/bigNet/Graph_of_components/eigenvectorCentrality_Distr.png)
## MAIN REPORT - Graph_of_components: metric correlations table and plots


|                       |    degree |   shellIndex |   eccentricity |   clusteringCoefficient |   closenessCentrality |   eigenvectorCentrality |
|:----------------------|----------:|-------------:|---------------:|------------------------:|----------------------:|------------------------:|
| degree                |  1        |    0.70945   |      -0.549768 |               0.549758  |            -0.353109  |                0.740698 |
| shellIndex            |  0.70945  |    1         |      -0.274584 |               0.738134  |             0.0240441 |                0.648852 |
| eccentricity          | -0.549768 |   -0.274584  |       1        |              -0.27699   |             0.924924  |               -0.546686 |
| clusteringCoefficient |  0.549758 |    0.738134  |      -0.27699  |               1         |            -0.0620868 |                0.410652 |
| closenessCentrality   | -0.353109 |    0.0240441 |       0.924924 |              -0.0620868 |             1         |               -0.287579 |
| eigenvectorCentrality |  0.740698 |    0.648852  |      -0.546686 |               0.410652  |            -0.287579  |                1        |  

Correlation table visualized:
  
![Indeed, image](/Report/bigNet/Graph_of_components/CORR_COLORMAP.png)

---

---