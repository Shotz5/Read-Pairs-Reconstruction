class Node:
    def __init__(self, prefix, suffix, pair):
        self.prefix = prefix
        self.suffix = suffix
        self.next = []
        self.prev = []
        self.pairMap = dict()
        self.visited = dict()
        self.pair = pair

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

    def addPair(self, node, pair):
        self.pairMap[node] = pair

    def addPairMap(self, map):
        self.pairMap.update(map)
    
    def getPairMap(self):
        return self.pairMap

    def getPairFromMap(self, node):
        return self.pairMap[node]

    def getPair(self):
        return self.pair

    def wipePairMap(self):
        self.pairMap = dict()

    def getVisitedMap(self):
        return self.visited
    
    def addVisited(self, node):
        self.visited[node] = 0

    def addVisitedMap(self, map):
        self.visited.update(map)
        
    def setVisited(self, node):
        self.visited[node] = 1

    def isVisited(self, node):
        return self.visited[node]

    def wipeVisited(self):
        self.visited = dict()

    def changeNext(self, old, new):
        for i in range(len(self.next)):
            if (self.next[i] == old):
                self.next[i] = new
            else:
                print("errr")

    def changeVisited(self, old, new):
        self.visited.pop(old)
        self.visited[new] = 0

    def changePairMap(self, old, new):
        key = self.pairMap.pop(old)
        self.pairMap[new] = key
    