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

    def search(self, value):  # search the table by package object
        bucket = self.packageHash(value.packageID)
        bucketList = self.hashTable[bucket]
        if value in bucketList:
            index = bucketList.index(value)
            return bucketList[index]
        else:
            return None

    def searchID(self, value):  # search the table by integer package id
        bucket = self.packageHash(value)
        bucketList = self.hashTable[bucket]
        for item in range(0, len(bucketList)):
            if bucketList[item].packageID == value:
                return bucketList[item]
        return False

    def clear(self):
        self.hashTable.clear()
        self.__init__()

    def packageHash(self, value):  # hash function to sort into buckets
        return value % 10

    def count(self):  # count the number of items in the hash table
        c = 0
        for item in range(0, len(self.hashTable)):
            c += len(self.hashTable[item])
        return c

    def countDelivered(self):  # return a count of how many packages have Delivered status
        c = 0
        for item in range(0, len(self.hashTable)):
            for jtem in range(0, len(self.hashTable[item])):
                if self.hashTable[item][jtem].delivered == "Delivered":
                    c += 1
        return c

    def deliver(self, pack):  # update method
        toUpdate = self.searchID(pack.packageID)
        toUpdate.delivered = 'Delivered'

    def load(self, pack, loadTime):  # update method
        toUpdate = self.searchID(pack.packageID)
        toUpdate.loaded = True
        toUpdate.loadTime = loadTime
