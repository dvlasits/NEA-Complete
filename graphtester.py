class Stack:
    def __init__(self):
        self.myStack = []

    def push(self,item):
        self.myStack.append(item)

    def pop(self):
        return self.myStack.pop(-1)

class Tree:
    #This is the graph class
    def __init__(self):
        self.nodes = []

    def isCyclicSpecific(self,node,vis,stack):
        vis[node] = True
        stack[node] = True
        for neighbour in node.connectedToForwards():
            if not vis[neighbour]:
                if self.isCyclicSpecific(neighbour,vis,stack):
                    return True
            elif stack[neighbour]:
                return True
        stack[node] = False
        return False
    def isCyclic(self):
        vis = {node:False for node in self.nodes}
        stack = {node:False for node in self.nodes}
        for node in self.nodes:
            if not vis[node]:
                if self.isCyclicSpecific(node,vis,stack):
                    return True
        return False



    def cyclomComplex(self,start):
        numPaths = 0
        done1 = 0
        for edge in start.edges:
            if edge.node2 != start:
                done1 = 1
                numPaths += self.cyclomComplex(edge.node2)
        if done1 == 0:
            numPaths += 1
        return numPaths



    def save(self,saveLocation,Database):
        #This function used to convert graph to networkX graph so that it can be saved
        #as a graphml file
        DG = nx.DiGraph()
        #double loop through node and children
        for node in self.nodes:
            for child in node.connectedTo():
                edge = node.getEdge(child)
                if edge.node1 == node:
                    #weighted edge added and weight of node put as text under name so that it can be viewed in the GUI
                    DG.add_weighted_edges_from([(node.getName() + '\n' + str(node.weight),child.getName() + '\n' + str(child.weight),edge.weight)])
        Database.saveGraph(DG,"ReducedDynamicFuncInteracting",saveLocation)
        #nx.write_graphml(DG,saveLocation + "/ReducedDynamicFuncInteracting.graphml")

    def createNode(self,node,weight):
        #node createc with a certain weight
        self.nodes.append(Node(node,weight))

    def createPath(self,node1,weight1,node2,weight2,edgeWeight):
        #weighted edge creation nodes also created if
        #they dont exist
        if not self.inTree(node1):
            self.nodes.append(Node(node1,weight1))
        if not self.inTree(node2):
            self.nodes.append(Node(node2,weight2))
        self.createEdge(node1,node2,edgeWeight)

    def createEdge(self,node1,node2,edge):
        #Edge class created between two nodes with its weight
        node1 = self.getNode(node1)
        node2 = self.getNode(node2)
        edge = Edge(node1,node2,edge)
        node1.addEdge(edge)
        node2.addEdge(edge)

    def inTree(self,nodeN):
        #Check if a node is in a tree and either returning
        #True or False
        for node in self.nodes:
            if node.getName() == nodeN:
                return True
        return False

    def getNode(self,nodeN):
        #Node object based on name is found and returned
        for node in self.nodes:
            if node.getName() == nodeN:
                return node

    def reduceOnce(self):
        #One pair that can be reduced is found reduced and then function finishes
        #If no pair found True is returned to show that graph is fully reduced

        #Double loop through nodes and their children
        for node in self.nodes:
            for child in node.connectedTo():
                #Check to see both node,child have 2 or less nodes
                #which is a requirement for compressing
                if node.numChildren() <= 2 and child.numChildren() <= 2:
                    #If they both only have one node they can always be combines
                    #irrespective of the direction
                    if node.numChildren() == 1 and child.numChildren() == 1:
                        #Combine function of the two nodes and then exit with False
                        #as other pair could still exist
                        self.combine(node,child)
                        return False
                    #if node has one, of course if child has then this will be checked later on in the loop
                    #at this point if node has 1 child then the child must have 2
                    if node.numChildren() == 1:
                        #OtherEdge and connectorEdge located of the child
                        for edge in child.edges:
                            if node in edge.nodes and child in edge.nodes:
                                connectorEdge = edge
                            else:
                                otherEdge = edge

                        #Check to see direction is in one way as described in the NEA writeup
                        if otherEdge.node2 == child and connectorEdge.node2 == node or otherEdge.node1 == child and connectorEdge.node1 == node:
                              #Combined
                              self.combine(node,child)
                              return False
                    #Final scenario if they both have 2
                    if node.numChildren() == 2 and child.numChildren() == 2:
                        #otherEdge and connectorEdge must be located for both node and child
                        for edge in child.edges:
                            if node in edge.nodes and child in edge.nodes:
                                connectorEdge = edge
                            else:
                                otherEdge = edge
                        for edge in node.edges:
                            if node in edge.nodes and child in edge.nodes:
                                connectorEdge2 = edge
                            else:
                                otherEdge2 = edge
                        #check if direction all in the same way
                        if otherEdge.node2 == child and connectorEdge.node2 == node and otherEdge2.node1 == node or otherEdge.node1 == child and connectorEdge.node1 == node and otherEdge2.node2 == node:
                            self.combine(node,child)
                            return False

        #If got to here no pairs found so graph fully reduced
        return True

    def reduce(self):
        #Function to reduce works by repeatedly calling reduceOnce()
        #until it returns True showing graph fully reduced
        while not self.reduceOnce():
            #any edges that now dont have nodes on both sides becuase
            #one side has been combined are deleted
            for node in self.nodes:
                node.removeEdgesWasted(self.nodes)

    def combine(self,node1,node2):
        #Function to combine two nodes as they have been found combinable


        #first two nodes are removed from the nodes array
        self.nodes.remove(node1)
        self.nodes.remove(node2)
        #name of new node created by putting a ',' in between the two names
        newName = node1.getName() + "," + node2.getName()
        #combined node created
        self.createNode(newName,node1.weight+node2.weight)
        combinedNode = self.getNode(newName)
        #edge in original node1 that combines node1 with node2 is removed
        #this also happens with node2
        for edge in node1.edges:
            if node2 in edge.nodes:
                node1.edges.remove(edge)
        for edge in node2.edges:
            if node1 in edge.nodes:
                node2.edges.remove(edge)
        #edges in node1 and node2 updated so that instead of pointing to node1
        #or node2 they point to the combined node
        for edge in node1.edges:
            if edge.node1 == node1:
                edge.node1 = combinedNode
                edge.nodes[0] = combinedNode
            if edge.node2 == node1:
                edge.node2 = combinedNode
                edge.nodes[1] = combinedNode
        for edge in node2.edges:
            if edge.node1 == node2:
                edge.node1 = combinedNode
                edge.nodes[0] = combinedNode
            if edge.node2 == node2:
                edge.node2 = combinedNode
                edge.nodes[1] = combinedNode
        #the edges of the combined nodes are now just the edges of node1 and node2
        combinedNode.edges = node1.edges + node2.edges
        #for all other nodes if they pointed to node1 or node2 now need to point to the
        # combined node
        for node in self.nodes:
            node.refresh(node1,node2,combinedNode)



    def __repr__(self):
        #for debugging if graph printed it should print a list of the nodes
        return str(self.nodes)







class Edge:
    #Edge class which houses the weight and the two nodes it connects
    def __init__(self,node1,node2,edge):
        self.weight = edge
        self.node1 = node1
        self.node2 = node2
        self.nodes = [node1,node2]

    def refresh(self,node1,node2,combinedNode):
        #if nodes being combined this replaces the pointer to node1 or node2 with the combined
        #node
        if self.node1 == node1 or self.node1 == node2:
            self.node1 == combinedNode
            self.nodes[0] = combinedNode
        if self.node2 == node1 or self.node2 == node2:
            self.node2 = combinedNode
            self.nodes[1] = combinedNode

    def otherNode(self,nodeGot):
        #if want to know from one node where it points to this returns
        #the other node
        if nodeGot == self.node1:
            return self.node2
        return self.node1

    def __repr__(self):
        #for debugging prints the first node and the second node and then the weight
        return f"{self.node1.getName()} to {self.node2.getName()} with weight {self.weight}"

class Node:
    def __init__(self,name,weight):
        self.name = name
        self.weight = weight
        self.edges = []

    def refresh(self,node1,node2,combinedNode):
        #looks at all edges and if node1 or node2 in edges
        #replaces them with the combinedNode
        for edge in self.edges:
            edge.refresh(node1,node2,combinedNode)


    def getEdge(self,node):
        #Find a certain edge connecting to a certain node
        for edge in self.edges:
            if node in edge.nodes:
                return edge

    def removeEdgesWasted(self,nodes):
        #removes an edge if now no longer connects to valid node
        edgesToRemove = []
        for edge in self.edges:
            if edge.node1 not in nodes or edge.node2 not in nodes:
                edgesToRemove.append(edge)
        for edge in edgesToRemove:
            self.edges.remove(edge)


    def addEdge(self,edge):
        #adds an edge to its array of edges
        self.edges.append(edge)

    def getName(self):
        #function to encapsulate self.name
        return self.name

    def connectedTo(self):
        #returns all children node connecting to
        children = []
        for edge in self.edges:
            children.append(edge.otherNode(self))
        return children

    def connectedToForwards(self):
        #returns all children node connecting to
        children = []
        for edge in self.edges:
            if edge.node1 == self:
                children.append(edge.otherNode(self))
        return children

    def numChildren(self):
        #each edge connects to a child and therefore length of
        #edges is the number of children
        return len(self.edges)

    def __repr__(self):
        #for debugging to print the node it first prints the name
        #then the weight and then a list of its edges
        return f"Name : {self.name} Weight : {self.weight} Edges : {self.edges}"



mytree = Tree()
mytree.createPath("Module",0,"Main",0,0)
mytree.createPath("Main",0,"s1",0,0)
mytree.createPath("Main",0,"s2",0,0)
mytree.createPath("s2",0,"s1",0,0)
mytree.createPath("s2",0,"s3",0,0)
mytree.createPath("s1",0,"s3",0,0)
mytree.createPath("s1",0,"s4",0,0)

start = mytree.getNode("Module")
print(mytree.isCyclic())
#print(mytree.cyclomComplex(start))
