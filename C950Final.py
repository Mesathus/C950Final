from datetime import time, datetime, timedelta
from Graph import Graph, Vertex
from HashTable import PackageHashTable
from WGUPS import Package, Truck


def initPackages(packageMaster):  # insert the packages into the hash table from the master list
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


def popHub(time):  # add packages that have arrived to the array
    packsAdded = 0
    for i in range(1, phTable.count() + 1):  # range(1, phTable.count() + 1)
        if phTable.searchID(i):
            pack = phTable.searchID(i)
            if "Delivered" not in pack.delivered and pack not in packsAtHub and pack.loaded is False and pack not in undeliveredPacks:  # check if package is loaded or delivered
                if ":" not in pack.notes:  # check for late arrivals
                    packsAtHub.append(pack)
                    packsAdded = packsAdded + 1
                else:  # check to see if the package has arrived yet
                    tStr = pack.notes.split(':')
                    h = int(tStr[0][-2:])
                    m = int(tStr[1][0:2])
                    if "pm" in tStr[1][0:].lower():
                        h += 12
                    t = datetime(2020, 1, 1, h, m)
                    if timeIsBefore(t, time):
                        packsAtHub.append(pack)
                        packsAdded = packsAdded + 1
    return packsAdded  # return a count of how many packages were added


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
            currTruck.addPackageList(groupPacks, phTable)
            currTruck.sort(graphDistance)
            for gPack in groupPacks:
                undeliveredPacks.remove(gPack)
            if len(undeliveredPacks) > 0:
                currBest[truckArr.index(currTruck)] = undeliveredPacks[0]
        #  add grouped packs if the best package is 'delivered with'
        else:
            currTruck.addPackage(currBest[truckArr.index(currTruck)], phTable)
            # p = currBest[truckArr.index(currTruck)]
            undeliveredPacks.remove(currBest[truckArr.index(currTruck)])
            if len(undeliveredPacks) > 0:
                currBest[truckArr.index(currTruck)] = undeliveredPacks[0]


def deliver(truckArr):
    for truck in truckArr:
        truck.sort(graphDistance)
    currTruck = truckArr[0]
    while not trucksEmpty(truckArr):
        for truck in truckArr:
            if timeIsBefore(truck.currTime, currTruck.currTime):  # truck.count() > currTruck.count():
                currTruck = truck
            pack = truck.packageList.pop(list(truck.packageList)[0])
            distance = graphDistance.getDistance(truck.location, pack.address)
            truck.deliverPackage(pack, distance, phTable)
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
            x = list(vertexArray[i])[0]
            y = list(vertexArray[j])[0]
            z = edgeList[j]
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
                    t.returnHome(graphDistance)
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
