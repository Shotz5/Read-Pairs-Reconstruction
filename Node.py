class Node:
    def __init__(self, prefix, suffix, pair):
        self.prefix = prefix
        self.suffix = suffix
        self.pair = pair
        self.next = []
        self.prev = []
        self.visited = 0

    def __str__(self):
        return str(self.prefix) + " " + str(self.suffix)

    def addNext(self, node):
        self.next.append(node)

    def appendNext(self, list):
        self.next.extend(list)

    def removeNext(self, node):
        self.next.remove(node)

    def wipeNext(self):
        self.next = []

    def addPrev(self, node):
        self.prev.append(node)

    def getNext(self):
        return self.next
    
    def getPrev(self):
        return self.prev

    def getPrefix(self):
        return self.prefix

    def getSuffix(self):
        return self.suffix
    
    def getPair(self):
        return self.pair

    def setVisited(self):
        self.visited = 1