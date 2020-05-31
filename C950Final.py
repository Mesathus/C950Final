from datetime import time, datetime, timedelta


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
        for x in list(graphDistance.adjacencyList.keys()):
            if v1 is not None and v2 is not None:
                break
            if addr1 in x.label:
                v1 = x
            if addr2 in x.label or x.label in addr2:
                v2 = x
        distance = self.edgeWeights[v1, v2]
        return distance


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
    def __init__(self, name, location, speed=18, currTime=datetime(2020, 1, 1, 8, 0, 0), capacity=16):
        self.packageList = {}
        self.currTime = currTime
        self.speed = speed
        self.location = location
        self.capacity = capacity
        self.name = name
        self.dailyDistance = 0

    def addPackage(self, package):
        if len(self.packageList.items()) <= self.capacity:
            self.packageList[package.packageID] = package
        else:
            print("Truck is fully loaded")
            return False

    def deliverPackage(self, package, distance):
        self.updateTime(distance)
        self.location = package.address
        self.dailyDistance += distance
        package.delivered = "Delivered"
        package.deliveryTime = self.currTime

    def updateTime(self, distance):
        self.currTime = self.currTime + timedelta(hours=distance/self.speed)

    def updateLoc(self, location):
        self.location = location

    def getClosest(self, p):
        closest = graphDistance.getDistance(self.location, p.address)
        for x in list(self.packageList.values()):
            nextLoc = graphDistance.getDistance(self.location, x.address)
            if nextLoc < closest and nextLoc > 0 and closest > 0:
                closest = nextLoc
        return closest

    def outForDelivery(self, type):
        if type == 'Distance':
            packages = list(self.packageList.values())
            while len(packages) > 0:
                for p in packages:
                    closest = p
                    if p.delivered == "Delivered":
                        break
                    for i in range(0, len(packages)):
                        d1 = float(graphDistance.getDistance(self.location, packages[i].address))
                        d2 = float(graphDistance.getDistance(self.location, p.address))
                        if d1 < d2:  # graphDistance.getDistance(self.location, packages[i].address) < graphDistance.getDistance(self.location, p.address):
                            closest = packages[i]
                    distance = graphDistance.getDistance(self.location, closest.address)
                    self.deliverPackage(closest, distance)
                    packages.remove(closest)
            self.packageList.clear()
        elif type == 'Time':
            packages = list(self.packageList.values())
            while len(packages) > 0:
                for p in packages:
                    if p.delivered == "Delivered":
                        break
                    earliest = p
                    for i in range(0, len(packages)):
                        t1 = earliest.deadline.split(":")
                        t2 = packages[i].deadline.split(":")
                        if "pm" in earliest.notes.lower():
                            h1 = int(t1[0]) + 12
                        else:
                            h1 = int(t1[0])
                        if "pm" in packages[i].notes.lower():
                            h2 = int(t2[0]) + 12
                        else:
                            h2 = int(t2[0])
                        if timeIsBefore(datetime(2020, 1, 1, h2, int(t2[1])), datetime(2020, 1, 1, h1, int(t1[1]))):
                            earliest = packages[i]
                    distance = graphDistance.getDistance(self.location, earliest.address)
                    self.deliverPackage(earliest, distance)
                    packages.remove(earliest)
            self.packageList.clear()
            # for p in self.packageList:

        else:
            print("Please specify Distance or Time for delivery priority.")
            return False

    def fill(self, type):
        if type == 'Distance':
            for p in packsAtHub:
                if len(self.packageList.items()) < self.capacity:
                    if len(p.notes) <= 2 or self.name in p.notes:
                        if 'EOD' in p.deadline:
                            self.addPackage(p)
                else:
                    break
            for p in self.packageList.values():
                packsAtHub.remove(p)
            self.outForDelivery(type)
        elif type == 'Time':
            for p in packsAtHub:
                if len(self.packageList.items()) < self.capacity:
                    if 'EOD' not in p.deadline:
                        self.addPackage(p)
                else:
                    break
            for p in self.packageList.values():
                packsAtHub.remove(p)
            self.outForDelivery(type)
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
        if value in self.hashTable[bucket]:
            self.hashTable[bucket].remove(value)

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
        return False

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

    def countDelivered(self):
        c = 0
        for i in range(0, len(self.hashTable)):
            for j in range(0, len(self.hashTable[i])):
                if self.hashTable[i][j].delivered == "Delivered":
                    c += 1
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


def popHub():
    for i in range(1, phTable.count() + 1):  # range(1, phTable.count() + 1)
        if phTable.searchID(i):
            pack = phTable.searchID(i)
            if "Delivered" not in pack.delivered:
                if ":" not in pack.notes:
                    packsAtHub.append(pack)
                    # phTable.remove(pack)
                else:
                    tStr = pack.notes.split(':')
                    h = int(tStr[0][-2:])
                    m = int(tStr[1][0:2])
                    if "pm" in tStr[1][0:].lower():
                        h += 12
                    t = datetime(2020, 1, 1, h, m)
                    if timeIsBefore(t, globalTime):
                        packsAtHub.append(pack)
                        # phTable.remove(pack)


def timeIsBefore(arrTime, currTime):
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
truck1 = Truck('truck 1', 'HUB')
truck2 = Truck('truck 2', 'HUB')
phTable = PackageHashTable()
globalTime = datetime(2020, 1, 1, 8, 0, 0)

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
# TODO create menu insert interface, look-up functions
# TODO create three lists/tables 1. packages at hub 2. packages out for deliver 3. packages delivered if len(all three) == packagemaster, stop adding to 1.
menu = -1
initPackages(packageMaster)
print(phTable.count())
while int(menu) < 0:
    menu = input("Choose a menu option:\n\t1. Input a new package\n\t2. Lookup a package\n\t3. Check package status\n\t4. Exit")
    if menu == '1':

        menu = -1
    elif menu == '2':
        pass
    elif menu == '3':
        # TODO run package delivery
        # TODO find a way to bind same delivery packages
        packsAtHub = []
        while phTable.countDelivered() < phTable.count():
            popHub()
            truck1.fill("Distance")
            truck2.fill("Time")
            print(phTable.countDelivered())
            print(phTable.count())
            for i in range(1, phTable.count() + 1):
                if phTable.searchID(i).deliveryTime is not None:
                    print(str(phTable.searchID(i).packageID) + " Deadline: " + phTable.searchID(i).deadline + " Delivery Time: " + phTable.searchID(i).deliveryTime.strftime("%X"))

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
