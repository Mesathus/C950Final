from datetime import time, datetime, timedelta


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
        self.packageList[package.deliveryTime(self.currTime)]
        del self.packageList[package.packageID]

    def updateTime(self, distance):
        self.currTime = self.currTime + timedelta(hours=distance/self.speed)

    def updateLoc(self, location):
        self.location = location

    def outForDelivery(self, type):
        if type == 'Distance':
            pass
        elif type == 'Time':
            pass
        else:
            print("Please specify Distance or Time for delivery priority.")
            return False

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

    def searchID(self, value):
        bucket = self.packageHash(value)
        bucketList = self.hashTable[bucket]
        for i in range(0, len(bucketList)):
            if bucketList[i].packageID == value:
                return bucketList[i]
        return None

    def clear(self):
        self.hashTable.clear()
        self.__init__()

    def packageHash(self, value):
        return value % 10

    def count(self):
        c = 0
        for i in range(0, len(self.hashTable)):
            c += len(self.hashTable[i])
        return c


def initPackages(packageMaster):
    phTable.clear()
    for i in range(1, len(list(packageMaster)) + 1):
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


def timeIsBefore(currTime, arrTime):
    h = currTime.hour - arrTime.hour
    m = (currTime.minute - arrTime.minute) / 60
    s = (currTime.second - arrTime.second) / 360
    if (h + m + s) < 0:  #return false if arrival time is after current time
        return False
    else:  # if (h + m + s) >= 0:
        return True

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
print(phTable.count())
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
