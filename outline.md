# General outline suggestion

* load locations from file -> dict
* load packages from file -> dict
* load graph from file -> graph class
* solve for best route (branch and bound)
  * generate candidate solutions (routes) -> list of paths
    * distribute packages to trucks
    * apply truck constraints and delayed package constraints
    * generate paths using greedy NN algo.
  * for each candidate
    * calculate total distance
    * verify delivery constraintes
    * If valid and better than previous solution, set as current best
  * Print best solution

## Useful structures

```python
class Delivery:
    location: int
    package: [int]
    time: int # epoch
    dist: int

class Solution:
    truck1_path: list(Delivery)
    truck1_total_dist: int
    truck2_path: list(Delivery)
    truck2_total_dist: int
```
