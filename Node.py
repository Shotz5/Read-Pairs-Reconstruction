class Node:
    def __init__(self, prefix, suffix, pair):
        self.prefix = prefix
        self.suffix = suffix
        self.outEdge = []
        self.inEdge = []
        self.pairMap = dict()
        self.pair = pair
        self.visited = 0

    def __str__(self):
        return str(self.prefix) + " " + str(self.suffix)

    def addOutEdge(self, node):
        self.outEdge.append(node)

    def appendOutEdge(self, list):
        self.outEdge.extend(list)

    def removeOutEdge(self, edge):
        self.outEdge.remove(edge)

    def addInEdge(self, node):
        self.inEdge.append(node)

    def appendInEdge(self, list):
        self.inEdge.extend(list)

    def removeInEdge(self, edge):
        self.inEdge.remove(edge)

    def getOutEdge(self):
        return self.outEdge

    def getInEdge(self):
        return self.inEdge

    def incrementVisited(self):
        self.visited += 1

    def getVisited(self):
        return self.visited

    def setVisited(self):
        self.visited = 1

    def wipeOutEdges(self):
        self.outEdge = []

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

    def getPair(self, node):
        return self.pairMap[node]

    def getPair(self):
        return self.pair