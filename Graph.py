#  Graph constructs taken from zyBooks class material


class Vertex:
    def __init__(self, label, distance=0.0):
        self.label = label
        self.distance = distance


class Graph:
    def __init__(self):
        self.adjacencyList = {}
        self.edgeWeights = {}

    def addVertex(self, newVertex):
        self.adjacencyList[newVertex] = []

    def addDirectedEdge(self, fromVertex, toVertex, weight=0.0):
        self.edgeWeights[(fromVertex, toVertex)] = weight
        self.adjacencyList[fromVertex].append(toVertex)

    def addUndirectedEdge(self, vertexA, vertexB, weight=0.0):
        self.addDirectedEdge(vertexA, vertexB, weight)
        self.addDirectedEdge(vertexB, vertexA, weight)

    def getDistance(self, addr1, addr2):
        v1 = None
        v2 = None
        for x in list(self.adjacencyList.keys()):
            if v1 is not None and v2 is not None:
                break
            if addr1 in x.label:
                v1 = x
            if addr2 in x.label or x.label in addr2:
                v2 = x
        distance = self.edgeWeights[v1, v2]
        return distance
