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

    def addPackage(self, pack, phTable):
        if len(self.packageList.items()) <= self.capacity:
            self.packageList[pack.packageID] = pack
            phTable.load(pack)
            return True
        else:
            print("Truck is fully loaded")
            return False

    def addPackageList(self, packList, phTable):
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

    def deliverPackage(self, pack, distance, phTable):
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

    def getClosest(self, p, graph):  # TODO update this to a sort by next closest function
        closest = graph.getDistance(self.location, p.address)
        for item in list(self.packageList.values()):
            nextLoc = graph.getDistance(self.location, item.address)
            if nextLoc < closest and nextLoc > 0 and closest > 0:
                closest = nextLoc
        return closest

    def count(self):
        count = 0
        for item in list(self.packageList.values()):
            if item is not None:
                count = count + 1
        return count

    def sort(self, graph):
        currLocation = self.location
        sortedList = {}
        while len(self.packageList.items()) > 0:
            currBest = self.packageList[list(self.packageList)[0]]
            for index in self.packageList:
                pack = self.packageList[index]
                d1 = graph.getDistance(currLocation, pack.address)
                d2 = graph.getDistance(currBest.address, pack.address)
                if graph.getDistance(currLocation, pack.address) <= graph.getDistance(currBest.address, pack.address):
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

    def returnHome(self, graph):
        distance = graph.getDistance(self.location, 'HUB')
        self.updateTime(distance)
        self.location = 'HUB'
        self.dailyDistance += distance

    def outForDelivery(self, graph):
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
                    d1 = float(graph.getDistance(self.location, deliveryQueue[i].address))
                    d2 = float(graph.getDistance(self.location, d.address))
                    if d1 < d2:  # graphDistance.getDistance(self.location, packages[i].address) < graphDistance.getDistance(self.location, p.address):
                        closest = deliveryQueue[i]
                distance = graph.getDistance(self.location, closest.address)
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
                    d1 = float(graph.getDistance(self.location, eodQueue[i].address))
                    d2 = float(graph.getDistance(self.location, d.address))
                    if d1 < d2:  # graphDistance.getDistance(self.location, packages[i].address) < graphDistance.getDistance(self.location, p.address):
                        closest = eodQueue[i]
                distance = graph.getDistance(self.location, closest.address)
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
    def fill(self, packsAtHub, graph):
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
        self.outForDelivery(graph)


def timeIsBefore(arrTime, currTime):
    h = currTime.hour - arrTime.hour
    m = (currTime.minute - arrTime.minute) / 60
    s = (currTime.second - arrTime.second) / 360
    if (h + m + s) < 0:  # return false if arrival time is after current time
        return False
    else:  # if (h + m + s) >= 0:
        return True
