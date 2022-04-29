from datetime import datetime, timedelta


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
        self.loadTime = None

    def deliver(self, deliveryTime):  # time stamping the package
        self.delivered = 'Delivered'
        self.deliveryTime = deliveryTime

    def getStatus(self, startTime, endTime):
        if timeIsBefore(self.deliveryTime, endTime):  # delivery time is before the start window
            return "Package " + str(self.packageID) + " was delivered at " + str(self.deliveryTime.strftime("%X")) + "."
        elif timeIsBefore(self.loadTime, endTime) and timeIsBefore(endTime, self.deliveryTime):  # load is before the end window, deliver is after the end window
            return "Package " + str(self.packageID) + " is en route, loaded at " + str(self.loadTime.strftime("%X")) + \
                   ".  Expected delivery time is " + str(self.deliveryTime.strftime("%X")) + "."
        else:                                                                                   # load and deliver are after the close window
            return "Package " + str(self.packageID) + " is still at the hub."

    def info(self):
        if self.delivered == 'HUB':
            status = " This package is currently at the hub."
        else:
            status = " This package was delivered at " + self.deliveryTime.strftime("%X")
        return ("\nInformation about this package: " + "\n\tPackage ID: " + str(self.packageID) +
                "\n\tAddress: " + self.address + " " + self.city + ", " + self.state + " " + self.zip + "\n\tWeight: " +
                self.weight + " lbs.\n\tDelivery deadline: " + self.deadline + "\n\tStatus: " + status + "\n")


class Truck:
    def __init__(self, name, location, speed=18, currTime=datetime(2020, 1, 1, 8, 0, 0), capacity=16):
        self.packageList = {}
        self.currTime = currTime
        self.speed = speed
        self.location = location
        self.capacity = capacity
        self.name = name.lower()
        self.dailyDistance = 0

    def addPackage(self, pack, phTable):
        if len(self.packageList.items()) <= self.capacity:
            self.packageList[pack.packageID] = pack
            phTable.load(pack)  # adjust status of the package in the hash table
            return True
        else:
            print("Truck is fully loaded")
            return False

    def addPackageList(self, packList, phTable):  # as above, but for a list of packages rather than a single
        if len(self.packageList.items()) <= self.capacity:
            if (self.capacity - len(self.packageList.items())) >= len(packList):
                for pack in packList:
                    self.packageList[pack.packageID] = pack
                    phTable.load(pack, self.currTime)
                return True
            else:
                print("Not enough room in the truck to add this group of packages.")
                return False
        else:
            print("Truck is fully loaded")
            return False

    def deliverPackage(self, pack, distance, phTable):  # updating local truck time, distance traveled and the hash table
        self.updateTime(distance)
        self.location = pack.address
        self.dailyDistance += distance
        pack.deliver(self.currTime)
        phTable.deliver(pack)

    def updateTime(self, distance):
        self.currTime = self.currTime + timedelta(hours=distance/self.speed)

    def count(self):  # count items loaded to the truck
        count = 0
        for item in list(self.packageList.values()):
            if item is not None:
                count = count + 1
        return count

    def returnHome(self, graph):  # return to the hub
        distance = graph.getDistance(self.location, 'HUB')
        self.updateTime(distance)
        self.location = 'HUB'
        self.dailyDistance += distance

    def GreedyDeliver(self, graph, phTable):
        packages = list(self.packageList.values())
        deliveryQueue = []
        for p in packages:
            deliveryQueue.append(p)
        packages.clear()
        while len(deliveryQueue) > 0:  # ensure everything gets delivered
            for p in deliveryQueue:
                if p.delivered == "Delivered":  # ensure we don't try to double deliver a package
                    break
                closest = p
                # nested loop makes this O(n^2) run time
                for i in range(0, len(deliveryQueue)):  # finding the closest address to the current location
                    d1 = float(graph.getDistance(self.location, deliveryQueue[i].address))
                    d2 = float(graph.getDistance(self.location, closest.address))
                    if d1 < d2:
                        closest = deliveryQueue[i]
                distance = graph.getDistance(self.location, closest.address)
                self.deliverPackage(closest, distance, phTable)
                deliveryQueue.remove(closest)  # remove from the delivery queue after package is delivered
        self.packageList.clear()  # clear the package list once everything is delivered so we don't get an over capacity error
        self.returnHome(graph)  # return to the hub for the next set of packages


def timeIsBefore(arrTime, currTime):  # returns True if arrival time is before current time
    h = currTime.hour - arrTime.hour
    m = (currTime.minute - arrTime.minute) / 60
    s = (currTime.second - arrTime.second) / 360
    if (h + m + s) < 0:  # return false if arrival time is after current time
        return False
    else:  # if (h + m + s) >= 0:
        return True
