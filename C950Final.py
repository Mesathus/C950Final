# Author: John O'Brien
# Student ID: 001018793

from datetime import time, datetime, timedelta
from Graph import Graph, Vertex
from HashTable import PackageHashTable
from WGUPS import Package, Truck


# methods for use in the main body of the code have been inserted before the main
# to jump to the main body a find for "# region main" can be performed
# to insert the packages into the hash table, we've first created a master list
def initPackages(packageMaster):  # insert the packages into the hash table from the master list
    phTable.clear()
    for i in range(1, len(list(packageMaster)) + 1):
        p = packageMaster[str(i)]
        if p[4] == 'EOD':  # handle deadline of end of day
            p = list(packageMaster[str(i)])
            phTable.insert(Package(i, p[0], p[1], p[2], p[3], p[4], p[5], p[6]))
        else:
            tStr = p[4].split(":")  # handle other deadlines
            if tStr[1].__contains__("AM"):  # adjust for 24 hour clock
                h = int(tStr[0])
            else:
                h = int(tStr[0]) + 12
                if h == 24:
                    h = 12  # adjustment so packages from 12:00 noon to 12:59 PM don't end up as 24:00 to 24:59
            m = int(tStr[1][0:2])
            delTime = datetime(2020, 1, 1, h, m, 0)  # create a delivery deadline date time object
            phTable.insert(Package(i, p[0], p[1], p[2], p[3], delTime.strftime("%X"), p[5], p[6]))


def popHub(time):  # add packages that have arrived to the array
    packsAdded = 0
    for i in range(1, phTable.count() + 1):  # range(1, phTable.count() + 1)
        if phTable.searchID(i):
            pack = phTable.searchID(i)
            if "Delivered" not in pack.delivered and pack not in packsAtHub and pack.loaded is False and pack not in undeliveredPacks:  # check if package is loaded or delivered
                if ":" not in pack.notes:  # check for late arrivals, no : in the notes means no late arrival timestamp
                    packsAtHub.append(pack)
                    packsAdded = packsAdded + 1
                else:  # check to see if the package has arrived yet
                    tStr = pack.notes.split(':')
                    h = int(tStr[0][-2:])
                    m = int(tStr[1][0:2])
                    if "am" in tStr[1][0:].lower() and h == 12:
                        h = 0
                    if "pm" in tStr[1][0:].lower() and h != 12:
                        h += 12
                    t = datetime(2020, 1, 1, h, m)
                    if timeIsBefore(t, time):
                        # code to support address changes
                        if "wrong" in tStr[1].lower():  # search the portion of package.notes after the : in the timestamp
                            newAddress = tStr[1].split("am")[1]  # split on "am" as the second half will have the address in it
                            pack.address = newAddress
                        packsAtHub.append(pack)
                        packsAdded = packsAdded + 1
    return packsAdded  # return a count of how many packages were added


def timeIsBefore(arrTime, currTime):  # time comparison module
    h = currTime.hour - arrTime.hour
    m = (currTime.minute - arrTime.minute) / 60
    s = (currTime.second - arrTime.second) / 360
    if (h + m + s) < 0:  # return false if arrival time is after current time
        return False
    else:  # if (h + m + s) >= 0:
        return True


def getPackList(undelivered, keyList):  # build a list of package objects based on integer keys
    packList = []
    for p in undelivered:
        if p.packageID in keyList:
            packList.append(p)
    return packList


def updateTime(truckArr):  # adjust the global time based on truck internal times for late arrival packages
    currTruck = truckArr[0]
    global globalTime
    for truck in truckArr:
        if not timeIsBefore(truck.currTime, currTruck.currTime):
            currTruck = truck
    globalTime = currTruck.currTime


# region main program code
# creating global variables
distancesFile = open("WGUPS Distance Table.csv", "rt")
packagesFile = open("WGUPS Package File.csv", "rt")
graphDistance = Graph()
packageMaster = {}
vertexArray = []
truckArray = []
truck1 = Truck('truck 1', 'HUB')
truckArray.append(truck1)
truck2 = Truck('truck 2', 'HUB')
truckArray.append(truck2)
phTable = PackageHashTable()
globalTime = datetime(2020, 1, 1, 8, 0, 0)  # global timer to check for new incoming packages
menu = -1  # initialize menu option to start the while loop later

# after variable creation the data structures have to be filled
for line in distancesFile:  # create the graph adjacency list
    distanceArray = line.split(",")
    key = Vertex(distanceArray[1])  # get the location name from the file to use as our key
    distanceArray.pop(0)  # remove the address for the location before appending to the graph
    distanceArray.pop(0)  # remove the location name before appending to the graph
    vertexArray.append((key, distanceArray))
    graphDistance.adjacencyList[key] = distanceArray
for i in range(0, len(vertexArray)):  # add edges to the graph
    edgeList = list((vertexArray[i])[1:len(vertexArray)][0])
    for j in range(0, len(edgeList)):
        if edgeList[j] == "" or edgeList[j] == "/n" or edgeList[j] == "\n":
            break
        else:
            x = list(vertexArray[i])[0]
            y = list(vertexArray[j])[0]
            z = edgeList[j]
            graphDistance.addUndirectedEdge(list(vertexArray[i])[0], list(vertexArray[j])[0], float(edgeList[j]))
for line in packagesFile:  # fill the master package list
    package = line.split(",")
    packageMaster[package[0]] = package[1:len(package)]
distancesFile.close()  # file clean up
packagesFile.close()
initPackages(packageMaster)  # insert the packages into the hash table
print(str(phTable.count()) + " packages loaded to hash table.")

packsAtHub = []
undeliveredPacks = []
popHub(globalTime)  # populate the hub with packages arriving at the current global time in this case 8:00 AM
# deliver packages
for p in packsAtHub:  # load all the packages arrived at the hub into the list of undelivered packages
    if 'HUB' in p.delivered and not p.loaded and p not in undeliveredPacks:
        undeliveredPacks.append(p)

# manually load the first round of packages
# packages can be listed in any order, the algorithm sorts them
# listed here in increasing order to make which ones are being loaded more visible
truck1List = [13, 14, 15, 16, 19, 20, 21, 27, 34, 35, 39]  # grouped together 13, 14, 15, 16, 19, 20
truck2List = [4, 11, 12, 17, 18, 23, 24, 31, 36, 40]  # deadlines 1, 6, 13, 14, 15, 16, 20, 25, 29, 30, 31, 34, 37, 40
newPack = getPackList(undeliveredPacks, truck1List)
truck1.addPackageList(newPack, phTable)

newPack = getPackList(undeliveredPacks, truck2List)
truck2.addPackageList(newPack, phTable)

truck1.GreedyDeliver(graphDistance, phTable)
truck2.GreedyDeliver(graphDistance, phTable)

updateTime(truckArray)  # after each round of deliveries, update the time and repopulate with any late arrival packages
popHub(globalTime)
for p in packsAtHub:
    if 'HUB' in p.delivered and not p.loaded and p not in undeliveredPacks:
        undeliveredPacks.append(p)

# manually loading the second round of packages
truck1List = [1, 6, 22, 25, 26, 28]
truck2List = [2, 3, 5, 7, 8, 10, 29, 30, 32, 33, 37, 38]
newPack = getPackList(undeliveredPacks, truck1List)
truck1.addPackageList(newPack, phTable)

newPack = getPackList(undeliveredPacks, truck2List)
truck2.addPackageList(newPack, phTable)

truck1.GreedyDeliver(graphDistance, phTable)
truck2.GreedyDeliver(graphDistance, phTable)

updateTime(truckArray)
popHub(globalTime)
for p in packsAtHub:
    if 'HUB' in p.delivered and not p.loaded and p not in undeliveredPacks:
        undeliveredPacks.append(p)

# manually loading the final round of packages
truck1List = [9]
newPack = getPackList(undeliveredPacks, truck1List)
truck1.addPackageList(newPack, phTable)
truck1.GreedyDeliver(graphDistance, phTable)

# all packages have been delivered, but we can still check time frames because the package objects have load/deliver timestamps
# menu was initialized with our global variables at the beginning of the main code, -1 is used as a flag value any negative will work
while int(menu) < 1:
    menu = input("Choose a menu option:\n\t1. Check delivery status"
                 "\n\t2. Lookup a package\n\t3. Print delivery results\n\t4. Exit\n")
    if menu == '1':  # option 1 is to list package status in a time frame
        print("\nEnter beginning of window to check: ")
        # we ask for hours/minutes individually to avoid having to split strings
        h1 = int(input("Enter hour: "))
        m1 = int(input("Enter minute: "))
        noon1 = input("Enter AM or PM: ").upper()
        print("\nEnter end of window to check: ")
        h2 = int(input("Enter hour: "))
        m2 = int(input("Enter minute: "))
        noon2 = input("Enter AM or PM: ").upper()
        if noon1 == "AM" and h1 == 12:  # adjusting for 24 hour clock
            h1 = 0
        if noon2 == "AM" and h2 == 12:
            h2 = 0
        if noon1 == "PM" and h1 != 12:  # as above, we don't need to add twelve if the time is 12:00 noon to 12:59 PM
            h1 += 12
        if noon2 == "PM" and h2 != 12:
            h2 += 12
        startTime = datetime(2020, 1, 1, h1, m1, 0)
        endTime = datetime(2020, 1, 1, h2, m2, 0)
        for i in range(1, phTable.count() + 1):
            print(phTable.searchID(i).getStatus(startTime, endTime))  # calling getStatus fpr each package which returns a string
        menu = -1
    elif menu == '2':  # option 2 is to search package status by the id
        packID = input("\nEnter a package ID to look up: ")
        pack = phTable.searchID(int(packID))
        print(pack.info())  # calling info() to return a formatted string to print
        menu = -1
    elif menu == '3':  # option 3 is to print the delivery times of all the packages
        for i in range(1, phTable.count() + 1):
            if phTable.searchID(i).deliveryTime is not None:
                print(str(phTable.searchID(i).packageID) + " Deadline: " + phTable.searchID(i).deadline + "   Delivery Time: " +
                      phTable.searchID(i).deliveryTime.strftime("%X") + "   Load Time: " + phTable.searchID(i).loadTime.strftime("%X"))
        print("Truck 1 distance: " + str(truck1.dailyDistance) + "\n3Truck 2 distance: " + str(truck2.dailyDistance))
        print("Total distance: " + str(truck1.dailyDistance + truck2.dailyDistance))
        menu = -1
    elif menu == '4':  # exit the loop and end the program
        break   # don't set to -1 and evaluate the loop again, just exit
    else:  # if a number greater than 4 is entered, change to the flag value and prompt the menu again
        menu = -1

