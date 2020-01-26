class Tree:
    def __init__(self):
        self.nodes = []

    def createNode(self,node,weight):
        self.nodes.append(Node(node,weight))

    def createPath(self,node1,weight1,node2,weight2,edgeWeight):
        if not self.inTree(node1):
            self.nodes.append(Node(node1,weight1))
        if not self.inTree(node2):
            self.nodes.append(Node(node2,weight2))
        self.createEdge(node1,node2,edgeWeight)

    def createEdge(self,node1,node2,edge):
        node1 = self.getNode(node1)
        node2 = self.getNode(node2)
        edge = Edge(node1,node2,edge)
        node1.addEdge(edge)
        node2.addEdge(edge)

    def inTree(self,nodeN):

        for node in self.nodes:
            if node.getName() == nodeN:
                return True
        return False

    def getNode(self,nodeN):
        for node in self.nodes:
            if node.getName() == nodeN:
                return node

class Edge:
    def __init__(self,node1,node2,edge):
        self.weight = edge
        self.node1 = node1
        self.node2 = node2

    def __repr__(self):
        return f"{self.node1.getName()} to {self.node2.getName()} with weight {self.weight}"

class Node:
    def __init__(self,name,weight):
        self.name = name
        self.weight = weight
        self.edges = []

    def addEdge(self,edge):
        self.edges.append(edge)

    def getName(self):
        return self.name

    def __repr__(self):
        return f"Name : {self.name} Weight : {self.weight} Edges : {self.edges}"

myTree = Tree()
myTree.createNode("hello",10)
myTree.createPath("hello",10,"Goodbye",50,100)
myTree.createPath("Goodbye",50,"Terence",300,1000)
print(myTree.nodes)
