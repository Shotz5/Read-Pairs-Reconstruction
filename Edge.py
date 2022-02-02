class Edge:
    def __init__(self, prev, next, pair):
        self.prev = prev
        self.next = next
        self.pair = pair
        self.visited = 0

    def getNext(self):
        return self.next

    def setVisited(self):
        self.visited = 1
    
    def getVisited(self):
        return self.visited