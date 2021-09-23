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
        self.loaded = False
        self.deliveryTime = None

    def deliver(self, deliveryTime):
        self.delivered = 'Delivered'
        self.deliveryTime = deliveryTime
        #undeliveredPacks.remove(self)


class Truck:
    def __init__(self, name, location, speed=18, currTime=datetime(2020, 1, 1, 8, 0, 0), capacity=16):
        self.packageList = {}
        self.currTime = currTime
        self.speed = speed
        self.location = location
        self.capacity = capacity
        self.name = name.lower()
        self.dailyDistance = 0

    def addPackage(self, pack):
        if len(self.packageList.items()) <= self.capacity:
            self.packageList[pack.packageID] = pack
            phTable.load(pack)
            return True
        else:
            print("Truck is fully loaded")
            return False

    def addPackageList(self, packList):
        if len(self.packageList.items()) <= self.capacity:
            if (self.capacity - len(self.packageList.items())) >= len(packList):
                for pack in packList:
                    self.packageList[pack.packageID] = pack
                    phTable.load(pack)
                return True
            else:
                print("Not enough room in the truck to add this group of packages.")
                return False
        else:
            print("Truck is fully loaded")
            return False

    def deliverPackage(self, pack, distance):
        self.updateTime(distance)
        self.location = pack.address
        self.dailyDistance += distance
        pack.deliver(self.currTime)
        phTable.deliver(pack)
        #package.delivered = "Delivered"
        #package.deliveryTime = self.currTime

    def updateTime(self, distance):
        self.currTime = self.currTime + timedelta(hours=distance/self.speed)

    def updateLoc(self, location):
        self.location = location

    def getClosest(self, p):  # TODO update this to a sort by next closest function
        closest = graphDistance.getDistance(self.location, p.address)
        for item in list(self.packageList.values()):
            nextLoc = graphDistance.getDistance(self.location, item.address)
            if nextLoc < closest and nextLoc > 0 and closest > 0:
                closest = nextLoc
        return closest

    def count(self):
        count = 0
        for item in list(self.packageList.values()):
            if item is not None:
                count = count + 1
        return count

    def sort(self):
        currLocation = self.location
        sortedList = {}
        while len(self.packageList.items()) > 0:
            currBest = self.packageList[list(self.packageList)[0]]
            for index in self.packageList:
                pack = self.packageList[index]
                d1 = graphDistance.getDistance(currLocation, pack.address)
                d2 = graphDistance.getDistance(currBest.address, pack.address)
                if graphDistance.getDistance(currLocation, pack.address) <= graphDistance.getDistance(currBest.address, pack.address):
                    currBest = pack
            sortedList[currBest.packageID] = currBest
            currLocation = currBest.address
            self.packageList.pop(currBest.packageID)
        self.packageList = sortedList
    # def outForDelivery(self, type):
    #     if type == 'Distance':
    #         packages = list(self.packageList.values())
    #         while len(packages) > 0:
    #             for p in packages:
    #                 closest = p
    #                 if p.delivered == "Delivered":
    #                     break
    #                 for i in range(0, len(packages)):
    #                     d1 = float(graphDistance.getDistance(self.location, packages[i].address))
    #                     d2 = float(graphDistance.getDistance(self.location, p.address))
    #                     if d1 < d2:  # graphDistance.getDistance(self.location, packages[i].address) < graphDistance.getDistance(self.location, p.address):
    #                         closest = packages[i]
    #                 distance = graphDistance.getDistance(self.location, closest.address)
    #                 self.deliverPackage(closest, distance)
    #                 packages.remove(closest)
    #         self.packageList.clear()
    #     elif type == 'Time':
    #         packages = list(self.packageList.values())
    #         deliveryQueue = []
    #         while len(packages) > 0:
    #             for p in packages:
    #                 if p.delivered == "Delivered":
    #                     break
    #                 earliest = p
    #                 for i in range(0, len(packages)):
    #                     if 'EOD' in earliest.deadline or 'EOD' in packages[i].deadline:
    #                         continue
    #                     t1 = earliest.deadline.split(":")
    #                     t2 = packages[i].deadline.split(":")
    #                     if "pm" in earliest.notes.lower():
    #                         h1 = int(t1[0]) + 12
    #                     else:
    #                         h1 = int(t1[0])
    #                     if "pm" in packages[i].notes.lower():
    #                         h2 = int(t2[0]) + 12
    #                     else:
    #                         h2 = int(t2[0])
    #                     if timeIsBefore(datetime(2020, 1, 1, h2, int(t2[1])), datetime(2020, 1, 1, h1, int(t1[1]))):
    #                         earliest = packages[i]
    #                 distance = graphDistance.getDistance(self.location, earliest.address)
    #                 if len(deliveryQueue) == 0 or deliveryQueue[0].deadline == earliest.deadline:
    #                     deliveryQueue.append(earliest)
    #                     packages.remove(earliest)
    #             while len(deliveryQueue) > 0:
    #                 for d in deliveryQueue:
    #                     if d.delivered == "Delivered":
    #                         break
    #                     closest = d
    #                     for i in range(0, len(deliveryQueue)):
    #                         d1 = float(graphDistance.getDistance(self.location, deliveryQueue[i].address))
    #                         d2 = float(graphDistance.getDistance(self.location, d.address))
    #                         if d1 < d2:  # graphDistance.getDistance(self.location, packages[i].address) < graphDistance.getDistance(self.location, p.address):
    #                             closest = deliveryQueue[i]
    #                     distance = graphDistance.getDistance(self.location, closest.address)
    #                     self.deliverPackage(closest, distance)
    #                     deliveryQueue.remove(closest)
    #                     # self.deliverPackage(earliest, distance)
    #                     # packages.remove(earliest)
    #         if len(deliveryQueue) == 0 and len(packages) > 0:
    #             self.outForDelivery("Distance")
    #         self.packageList.clear()
    #         # for p in self.packageList:
    #     else:
    #         print("Please specify Distance or Time for delivery priority.")
    #         return False
    #     self.dailyDistance += graphDistance.getDistance(self.location, 'HUB')
    #     self.location = 'HUB'

    def returnHome(self):
        distance = graphDistance.getDistance(self.location, 'HUB')
        self.updateTime(distance)
        self.location = 'HUB'
        self.dailyDistance += distance

    def outForDelivery(self):
        packages = list(self.packageList.values())
        deliveryQueue = []
        eodQueue = []
        while len(packages) > 0:
            for p in packages:
                if p.delivered == "Delivered":
                    break
                earliest = p
                second = False
                for i in range(0, len(packages)):
                    # if 'EOD' in earliest.deadline:
                    #     eodQueue.append(earliest)
                    # if 'EOD' in packages[i].deadline:
                    #     break
                    if 'EOD' not in earliest.deadline and 'EOD' not in packages[i].deadline:
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
                        for j in range(0, len(packages)):
                            if str(t2[0] + ":" + t2[1] + ":" + t2[2]) in packages[j].deadline:
                                second = True
                            else:
                                second = False
                                break
                if len(deliveryQueue) == 0 or deliveryQueue[0].deadline == earliest.deadline:
                    if 'EOD' not in earliest.deadline:
                        deliveryQueue.append(earliest)
                        packages.remove(earliest)
                if second and deliveryQueue[0].deadline not in earliest.deadline:
                    deliveryQueue.append(earliest)
                    packages.remove(earliest)
                if 'EOD' in earliest.deadline:
                    eodQueue.append(earliest)
                    packages.remove(earliest)
        while len(deliveryQueue) > 0:
            for d in deliveryQueue:
                if d.delivered == "Delivered":
                    break
                closest = d
                for i in range(0, len(deliveryQueue)):
                    d1 = float(graphDistance.getDistance(self.location, deliveryQueue[i].address))
                    d2 = float(graphDistance.getDistance(self.location, d.address))
                    if d1 < d2:  # graphDistance.getDistance(self.location, packages[i].address) < graphDistance.getDistance(self.location, p.address):
                        closest = deliveryQueue[i]
                distance = graphDistance.getDistance(self.location, closest.address)
                self.deliverPackage(closest, distance)
                deliveryQueue.remove(closest)
                # self.deliverPackage(earliest, distance)
                # packages.remove(earliest)
        while len(eodQueue) > 0:
            for d in eodQueue:
                if d.delivered == "Delivered":
                    break
                closest = d
                for i in range(0, len(eodQueue)):
                    d1 = float(graphDistance.getDistance(self.location, eodQueue[i].address))
                    d2 = float(graphDistance.getDistance(self.location, d.address))
                    if d1 < d2:  # graphDistance.getDistance(self.location, packages[i].address) < graphDistance.getDistance(self.location, p.address):
                        closest = eodQueue[i]
                distance = graphDistance.getDistance(self.location, closest.address)
                self.deliverPackage(closest, distance)
                eodQueue.remove(closest)
        self.packageList.clear()

    # def fill(self, type):
    #     if type == 'Distance':
    #         for p in packsAtHub:
    #             if len(self.packageList.items()) < self.capacity:
    #                 if len(p.notes) <= 2 or self.name in p.notes:
    #                     if 'EOD' in p.deadline:
    #                         self.addPackage(p)
    #             else:
    #                 break
    #         for p in self.packageList.values():
    #             packsAtHub.remove(p)
    #         self.outForDelivery(type)
    #     elif type == 'Time':
    #         for p in packsAtHub:
    #             if len(self.packageList.items()) < self.capacity:
    #                 if 'EOD' not in p.deadline:
    #                     self.addPackage(p)
    #             else:
    #                 break
    #         for p in packsAtHub:
    #             if len(self.packageList.items()) < self.capacity:
    #                 if self.name in p.notes:
    #                     self.addPackage(p)
    #         for p in self.packageList.values():
    #             packsAtHub.remove(p)
    #         self.outForDelivery(type)
    #     else:
    #         print("Please specify Distance or Time for delivery priority.")
    #         return False
# TODO update fill function to add packages based on shortest distance
    def fill(self):
        for p in packsAtHub:
            if len(self.packageList.items()) < 6:
                if 'EOD' not in p.deadline:
                    self.addPackage(p)
        for p in packsAtHub:
            if len(self.packageList.items()) < self.capacity:
                if len(p.notes) <= 2 or self.name in p.notes or ":" in p.notes:
                    if 'EOD' in p.deadline:
                        self.addPackage(p)
            else:
                break
        for p in self.packageList.values():
            packsAtHub.remove(p)
        self.outForDelivery()


# TODO hash packages by delivery time to make sorting onto trucks faster?
class PackageHashTable:
    def __init__(self, capacity=10):
        self.capacity = capacity
        self.hashTable = []
        for item in range(capacity):
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
        for item in range(0, len(bucketList)):
            if bucketList[item].packageID == value:
                return bucketList[item]
        return False

    def clear(self):
        self.hashTable.clear()
        self.__init__()

    def packageHash(self, value):
        return value % 10

    def count(self):
        c = 0
        for item in range(0, len(self.hashTable)):
            c += len(self.hashTable[item])
        return c

    def countDelivered(self):
        c = 0
        for item in range(0, len(self.hashTable)):
            for jtem in range(0, len(self.hashTable[item])):
                if self.hashTable[item][jtem].delivered == "Delivered":
                    c += 1
        return c

    def deliver(self, pack):
        toUpdate = self.searchID(pack.packageID)
        toUpdate.delivered = 'Delivered'

    def load(self, pack):
        toUpdate = self.searchID(pack.packageID)
        toUpdate.loaded = True


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


def popHub(time):
    packsAdded = 0
    for i in range(1, phTable.count() + 1):  # range(1, phTable.count() + 1)
        if phTable.searchID(i):
            pack = phTable.searchID(i)
            if "Delivered" not in pack.delivered and pack not in packsAtHub and pack.loaded is False and pack not in undeliveredPacks:
                if ":" not in pack.notes:
                    packsAtHub.append(pack)
                    packsAdded = packsAdded + 1
                else:
                    tStr = pack.notes.split(':')
                    h = int(tStr[0][-2:])
                    m = int(tStr[1][0:2])
                    if "pm" in tStr[1][0:].lower():
                        h += 12
                    t = datetime(2020, 1, 1, h, m)
                    if timeIsBefore(t, time):
                        packsAtHub.append(pack)
                        packsAdded = packsAdded + 1
    return packsAdded

def sortHub():
    phTable.clear()
    eodHub = []
    timeHub = []
    nextPack = None
    val = len(pm)
    for i in range(0, len(pm)):
        p = pm[i][1]
        if 'EOD' in pm[i][1][4]:
            eodHub.append(Package(i + 1, p[0], p[1], p[2], p[3], p[4], p[5], p[6]))
        else:
            timeHub.append(Package(i + 1, p[0], p[1], p[2], p[3], p[4], p[5], p[6]))
    for p in eodHub:
        phTable.insert(p)
    for p in timeHub:
        tStr = p.deadline.split(":")
        if tStr[1].__contains__("AM"):
            h = int(tStr[0])
        else:
            h = int(tStr[0]) + 12
        m = int(tStr[1][0:2])
        delTime = datetime(2020, 1, 1, h, m, 0)
        p.deadline = delTime.strftime("%X")
        phTable.insert(p)
    print(phTable.count())


def timeIsBefore(arrTime, currTime):
    h = currTime.hour - arrTime.hour
    m = (currTime.minute - arrTime.minute) / 60
    s = (currTime.second - arrTime.second) / 360
    if (h + m + s) < 0:  # return false if arrival time is after current time
        return False
    else:  # if (h + m + s) >= 0:
        return True


def trucksFull(truckArr):
    for truck in truckArr:
        if truck.count() < truck.capacity:
            return False
    return True


def trucksEmpty(truckArr):
    for truck in truckArr:
        if truck.count() > 0:
            return False
    return True


def findPackage(packID):
    for pack in undeliveredPacks:
        if pack.packageID == int(packID):
            return pack
    return None


def grouping():
    groupedPacks = []
    packsToAdd = []
    for pack in undeliveredPacks:
        if "delivered with" in pack.notes.lower():
            groupedPacks.append(pack)
    for pack in groupedPacks:
        if "delivered with" in pack.notes.lower():
            notesList = pack.notes.lower().split()
            for val in notesList:
                val = val.replace('\"', '')
                if val.isdigit():
                    toAdd = findPackage(val)
                    packsToAdd.append(toAdd)
    groupedPacks.extend(set(packsToAdd))
    return groupedPacks


def deadlineCount():
    count = 0
    for pack in undeliveredPacks:
        if 'EOD' not in pack.deadline:
            count = count + 1
    return count


def fill(truckArr):
    currentPosition = []  # position list for truck array
    currBest = []  # current best distance for each truck
    currTruck = truckArr[0]
    groupPacks = grouping()
    for truck in truckArr:
        currentPosition.append(truck.location)
        currBest.append(undeliveredPacks[0])
    while len(undeliveredPacks) > 0 and not trucksFull(truckArr):
        deadlineLeft = deadlineCount()
        for truck in truckArr:
            currBest[truckArr.index(truck)] = undeliveredPacks[0]
        for pack in undeliveredPacks:
            for truck in truckArr:  # rather than alternating trucks choose truck with lowest package count
                if truck.count() < currTruck.count():
                    currTruck = truck
            if 'EOD' not in pack.deadline:
                if 'truck' not in pack.notes.lower():  # have to cycle trucks if this is false
                    if graphDistance.getDistance(currentPosition[truckArr.index(currTruck)], pack.address) <= graphDistance.getDistance(currentPosition[truckArr.index(currTruck)], currBest[truckArr.index(currTruck)].address):
                        currentPosition[truckArr.index(currTruck)] = pack.address
                        currBest[truckArr.index(currTruck)] = pack
                    else:
                        continue
                elif currTruck.name in pack.notes.lower():
                    if graphDistance.getDistance(currentPosition[truckArr.index(currTruck)], pack.address) <= graphDistance.getDistance(currentPosition[truckArr.index(currTruck)], currBest[truckArr.index(currTruck)].address):
                        currentPosition[truckArr.index(currTruck)] = pack.address
                        currBest[truckArr.index(currTruck)] = pack
                    else:
                        continue
            elif deadlineLeft == 0:
                if 'truck' not in pack.notes.lower():  # have to cycle trucks if this is false
                    if graphDistance.getDistance(currentPosition[truckArr.index(currTruck)], pack.address) <= graphDistance.getDistance(currentPosition[truckArr.index(currTruck)], currBest[truckArr.index(currTruck)].address):
                        currentPosition[truckArr.index(currTruck)] = pack.address
                        currBest[truckArr.index(currTruck)] = pack
                    else:
                        continue
                elif currTruck.name in pack.notes.lower():
                    if graphDistance.getDistance(currentPosition[truckArr.index(currTruck)], pack.address) <= graphDistance.getDistance(currentPosition[truckArr.index(currTruck)], currBest[truckArr.index(currTruck)].address):
                        currentPosition[truckArr.index(currTruck)] = pack.address
                        currBest[truckArr.index(currTruck)] = pack
                    else:
                        continue
        if 'delivered with' in currBest[truckArr.index(currTruck)].notes.lower():
            currTruck.addPackageList(groupPacks)
            currTruck.sort()
            for gPack in groupPacks:
                undeliveredPacks.remove(gPack)
            if len(undeliveredPacks) > 0:
                currBest[truckArr.index(currTruck)] = undeliveredPacks[0]
        #  add grouped packs if the best package is 'delivered with'
        else:
            currTruck.addPackage(currBest[truckArr.index(currTruck)])
            # p = currBest[truckArr.index(currTruck)]
            undeliveredPacks.remove(currBest[truckArr.index(currTruck)])
            if len(undeliveredPacks) > 0:
                currBest[truckArr.index(currTruck)] = undeliveredPacks[0]


def deliver(truckArr):
    for truck in truckArr:
        truck.sort()
    currTruck = truckArr[0]
    while not trucksEmpty(truckArr):
        for truck in truckArr:
            if timeIsBefore(truck.currTime, currTruck.currTime):  # truck.count() > currTruck.count():
                currTruck = truck
            pack = truck.packageList.pop(list(truck.packageList)[0])
            distance = graphDistance.getDistance(truck.location, pack.address)
            truck.deliverPackage(pack, distance)
            updateTime(truckArr)
            count = popHub(globalTime)  # update hub see if packages with deadlines arrive
            if count > 0:
                undeliveredCount = deadlineCount()  # count packages with deadlines to see if a truck needs to go back to the hub
                if undeliveredCount > 0:
                    closestTruck = currTruck
                    for truckToHub in truckArr:
                        if truckToHub.count() == truckToHub.capacity:
                            continue
                        elif graphDistance.getDistance(truckToHub.location, 'HUB') < graphDistance.getDistance(closestTruck.location, 'HUB'):
                            closestTruck = truckToHub
                    closestTruck.returnHome()
                    fill(closestTruck)
                    closestTruck.sort()

    # for truck in truckArr:
    #     truck.returnHome()


def updateTime(truckArr):
    currTruck = truckArr[0]
    global globalTime
    for truck in truckArr:
        if not timeIsBefore(truck.currTime, currTruck.currTime):
            currTruck = truck
    globalTime = currTruck.currTime


distancesFile = open("WGUPS Distance Table.csv", "rt")
packagesFile = open("WGUPS Package File.csv", "rt")
graphDistance = Graph()
packageMaster = {}
pm = []  # TODO replace packageMaster with pm
vertexArray = []
truckArray = []
truck1 = Truck('truck 1', 'HUB')
truckArray.append(truck1)
truck2 = Truck('truck 2', 'HUB')
truckArray.append(truck2)
phTable = PackageHashTable()
# global globalTime
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
    pm.append((int(package[0]), package[1:len(package)]))
distancesFile.close()
packagesFile.close()
# print(pm[0][0])
# print(pm[0][1])
# print(pm[0][1][0])
# for i in range(0, len(pm)):
#     print(pm[i][1][4])
# TODO create menu insert interface, look-up functions
menu = -1
sortHub()
initPackages(packageMaster)
print(phTable.count())
while int(menu) < 1:
    #  menu = input("Choose a menu option:\n\t1. Input a new package\n\t2. Lookup a package\n\t3. Check delivery status\n\t4. Exit")
    menu = '3'
    if menu == '1':

        menu = -1
    elif menu == '2':
        pass
    elif menu == '3':
        packsAtHub = []
        undeliveredPacks = []
        while phTable.countDelivered() < phTable.count():
            popHub(globalTime)
            # sortHub()
            for p in packsAtHub:
                if 'HUB' in p.delivered and not p.loaded and p not in undeliveredPacks:
                    undeliveredPacks.append(p)

            # fillType = "Time"
            # for i in range(0, len(packsAtHub)):
            #     if 'EOD' not in packsAtHub[i].deadline:
            #         fillType = "Time"
            #         break
            #     else:
            #         fillType = "Distance"

            fill(truckArray)
            deliver(truckArray)
            if phTable.countDelivered() < phTable.count():
                for t in truckArray:
                    t.returnHome()
            #truck1.fill()
            #truck2.fill()
            # if timeIsBefore(truck1.currTime, truck2.currTime):
            #     globalTime = truck2.currTime
            # else:
            #     globalTime = truck1.currTime
            print(phTable.countDelivered())
            print(phTable.count())
            for i in range(1, phTable.count() + 1):
                if phTable.searchID(i).deliveryTime is not None:
                    print(str(phTable.searchID(i).packageID) + " Deadline: " + phTable.searchID(i).deadline + " Delivery Time: " + phTable.searchID(i).deliveryTime.strftime("%X"))
            print("Truck 1 distance: " + str(truck1.dailyDistance) + " Truck 2 distance: " + str(truck2.dailyDistance))
            print("Total distance: " + str(truck1.dailyDistance + truck2.dailyDistance))

        print("\nEnter beginning of window to check: ")
        h1 = input("Enter hours: ")
        m1 = input("Enter minutes: ")
        noon1 = input("Enter AM or PM: ").upper()
        print("\nEnter end of window to check: ")
        h2 = input("Enter hours: ")
        m2 = input("Enter minutes: ")
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
