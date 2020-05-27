from datetime import time, datetime, timedelta


# dijkstra algorithm from zyBooks class material
def dijkstra_shortest_path(g, start_vertex):
    # Put all vertices in an unvisited queue.
    unvisited_queue = []
    for current_vertex in g.adjacency_list:
        unvisited_queue.append(current_vertex)

    # Start_vertex has a distance of 0 from itself
    start_vertex.distance = 0.0

    # One vertex is removed with each iteration; repeat until the list is
    # empty.
    while len(unvisited_queue) > 0:

        # Visit vertex with minimum distance from start_vertex
        smallest_index = 0
        for i in range(1, len(unvisited_queue)):
            if unvisited_queue[i].distance < unvisited_queue[smallest_index].distance:
                smallest_index = i
        current_vertex = unvisited_queue.pop(smallest_index)

        # Check potential path lengths from the current vertex to all neighbors.
        for adj_vertex in g.adjacency_list[current_vertex]:
            edge_weight = g.edge_weights[(current_vertex, adj_vertex)]
            alternative_path_distance = current_vertex.distance + edge_weight

            # If shorter path from start_vertex to adj_vertex is found,
            # update adj_vertex's distance and predecessor
            if alternative_path_distance < adj_vertex.distance:
                adj_vertex.distance = alternative_path_distance
                adj_vertex.pred_vertex = current_vertex


def get_shortest_path(start_vertex, end_vertex):
    # Start from end_vertex and build the path backwards.
    path = ""
    current_vertex = end_vertex
    while current_vertex is not start_vertex:
        path = " -> " + str(current_vertex.label) + path
        current_vertex = current_vertex.pred_vertex
    path = start_vertex.label + path
    return path

#  Graph constructs taken from zyBooks class material


class Vertex:
    def __init__(self, label, distance=0.0, prevVertex=None):
        self.label = label
        self.distance = distance
        self.pred_vertex = prevVertex


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


class Package:
    def __init__(self, packageID, address, city, state, zip, deadline, weight, notes=None):
        self.packageID = packageID
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.delivered = 'HUB'
        self.deliveryTime = None

    def deliver(self, deliveryTime):
        self.delivered = 'Delivered'
        self.deliveryTime = deliveryTime


class Truck:
    def __init__(self, location, speed=18, currTime=datetime(2020, 1, 1, 8, 0, 0)):
        self.packageList = {}
        self.currTime = currTime
        self.speed = speed
        self.location = location

    def addPackage(self, package):
        if len(self.packageList.items()) <= 17:
            self.packageList[package.packageID] = package
        else:
            print("Truck is fully loaded")

    def deliverPackage(self, package, distance):
        self.updateTime(distance)
        self.packageList[package.deliver(self.currTime)]
        del self.packageList[package.packageID]

    def updateTime(self, distance):
        self.currTime = self.currTime + timedelta(hours=distance/self.speed)

    def updateLoc(self, location):
        self.location = location

# TODO hash packages by delivery time to make sorting onto trucks faster?
class PackageHashTable:
    def __init__(self, capacity=10):
        self.capacity = capacity
        self.hashTable = []
        for i in range(capacity):
            self.hashTable.append([])

    def insert(self, value):
        bucket = self.packageHash(value.packageID)
        self.hashTable[bucket].append(value)

    def remove(self, value):
        bucket = self.packageHash(value.packageID)
        if key in self.hashTable[bucket]:
            self.hashTable.remove(value.packageID)

    def search(self, value):
        bucket = self.packageHash(value.packageID)
        bucketList = self.hashTable[bucket]
        if value in bucketList:
            index = bucketList.index(value)
            return bucketList[index]
        else:
            return None

    def clear(self):
        self.hashTable.clear()
        self.__init__()

    def packageHash(self, value):
        return value % 10


def initPackages(packageMaster):
    phTable.clear()
    for i in range(1, len(list(packageMaster))):
        p = packageMaster[str(i)]
        if p[4] == 'EOD':
            p = list(packageMaster[str(i)])
            phTable.insert(Package(i, p[0], p[1], p[2], p[3], p[4], p[5], p[6]))
        else:
            tStr = p[4].split(":")
            if tStr[1].__contains__("AM"):
                h = int(tStr[0])
            else:
                h = int(tStr[0]) + 12
            m = int(tStr[1][0:2])
            delTime = datetime(2020, 1, 1, h, m, 0)
            phTable.insert(Package(i, p[0], p[1], p[2], p[3], delTime.strftime("%X"), p[5], p[6]))


# TODO delivery algorithm goes here
# TODO pass in a truck, find shortest route based on packages loaded
def packageDeliver(truck):
    pass


distancesFile = open("WGUPS Distance Table.csv", "rt")
packagesFile = open("WGUPS Package File.csv", "rt")
graphDistance = Graph()
packageMaster = {}
vertexArray = []
truck1 = Truck('HUB')
truck2 = Truck('HUB')
phTable = PackageHashTable()

for line in distancesFile:
    distanceArray = line.split(",")
    key = Vertex(distanceArray[1])
    distanceArray.pop(0)
    distanceArray.pop(0)
    vertexArray.append((key, distanceArray))
    graphDistance.adjacencyList[key] = distanceArray
for i in range(0, len(vertexArray)):
    edgeList = list((vertexArray[i])[1:len(vertexArray)][0])
    for j in range(0, len(edgeList)):
        if edgeList[j] == "" or edgeList[j] == "/n" or edgeList[j] == "\n":
            break
        else:
            x=list(vertexArray[i])[0]
            y=list(vertexArray[j])[0]
            z=edgeList[j]
            graphDistance.addUndirectedEdge(list(vertexArray[i])[0], list(vertexArray[j])[0], float(edgeList[j]))
for line in packagesFile:
    package = line.split(",")
    packageMaster[package[0]] = package[1:len(package)]

currTime = datetime(2020, 1, 1, 8, 0, 0)
# TODO create menu insert interface, look-up functions
# TODO create three lists/tables 1. packages at hub 2. packages out for deliver 3. packages delivered if len(all three) == packagemaster, stop adding to 1.
menu = -1
initPackages(packageMaster)
while int(menu) < 0:
    menu = input("Choose a menu option:\n\t1. Input a new package\n\t2. Lookup a package\n\t3. Check package status\n\t4. Exit")
    if menu == '1':
        initPackages(packageMaster)
    elif menu == '2':
        pass
    elif menu == '3':
        # TODO run package delivery
        # TODO load trucks, truck1 gets time sensitive deliveries, truck2 gets anything EOD with notes
        # TODO truck1 gets EOD packages iff 3 lists have total len(packagemaster) and nothing else not-EOD needs to go out
        # TODO find a way to bind same delivery packages, some are time sensitive
        print("\nEnter beginning of window to check: ")
        h1 = input("\nEnter hours: ")
        m1 = input("\nEnter minutes: ")
        noon1 = input("Enter AM or PM: ").upper()
        print("\nEnter end of window to check: ")
        h2 = input("\nEnter hours: ")
        m2 = input("\nEnter minutes: ")
        noon2 = input("Enter AM or PM: ").upper()
        pass
    elif menu == '4':
        break
    else:
        menu = -1

# print("\n")
# print(len(list(packageMaster)))
# test = "the time is 09:05 AM"
# testArr = test.split(":")
# if testArr[1].__contains__("PM"):
#     print(int(testArr[0][-2:]) + 12)
#     print(testArr[1][0:2])
# else:
#     print(testArr[0][-2:])
#     print(testArr[1][0:2])

# rightnow = rightnow + timedelta(hours=1)
# print(rightnow.strftime("%X"))
