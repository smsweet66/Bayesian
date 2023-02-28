# class that represents one node in a bayesian network
# contains the node's children, parents, and probability table
class Node:
    def __init__(self, name: str, children: str):
        self.probabilityMatrix = None
        self.name = name
        if children != '':
            self.children = children.split(',')
        else:
            self.children = []

        self.parents = []

    def query(self, nodeValues: [str]):
        columnNums = range(1, len(self.probabilityMatrix[0]))   # creates an array of all column numbers
        for parent in self.parents:
            rowNum = 0
            while self.probabilityMatrix[rowNum][0] != parent:
                rowNum += 1

            parentValue = ''
            for nodeValue in nodeValues:
                if nodeValue[0] == parent:
                    parentValue = nodeValue
                    break

            columnNums = [x for x in columnNums if self.probabilityMatrix[rowNum][x] == parentValue]

        value = ''
        for nodeValue in nodeValues:
            if nodeValue[0] == self.name:
                value = nodeValue
                break

        rowNum = len(self.parents)
        while self.probabilityMatrix[rowNum][0] != value:
            rowNum += 1

        return self.probabilityMatrix[rowNum][columnNums[0]]

    # returns a string representation of the node
    def __str__(self):
        return f'{self.children}:{self.parents}\n'


# class that represents a bayesian network
# contains several nodes and the probability of
# a certain outcome of a node given its parent nodes
class BayesianNetwork:
    def __init__(self, networkString: str):
        self.nodes = dict()
        nodeStrings = networkString.split(';')

        # generates the dictionary of nodes and sets the children
        for nodeString in nodeStrings:
            nodeInfo = nodeString.split(':')
            self.nodes[nodeInfo[0]] = Node(nodeInfo[0], nodeInfo[1])

        # sets the parents of each node
        for node in self.nodes:
            for child in self.nodes[node].children:
                self.nodes[child].parents.append(node)

    # adds a probability table to a given node
    def addProbability(self, node: str, probabilityMatrix):
        self.nodes[node].probabilityMatrix = probabilityMatrix

    def query(self, queryString: str):
        nodeValues = []
        unusedNodes = list(self.nodes.keys())
        if queryString != '':
            queryString = queryString.replace('=', ':')
            nodeValues = queryString.split(',')
        for i in range(len(nodeValues)):
            if nodeValues[i][2] == 'T':
                nodeValues[i] = nodeValues[i][:2] + '1'
            else:
                nodeValues[i] = nodeValues[i][:2] + '0'

            unusedNodes.remove(nodeValues[i][0])

        iterator: int = 0    # helps iterate over all valid values of nodes not specified in query
        probability = 0
        while iterator < pow(2, len(unusedNodes)):
            tempIter: int = iterator
            fullQuery = nodeValues.copy()
            for node in unusedNodes:
                fullQuery.append(node + f':{int(tempIter % 2)}')
                tempIter /= 2

            tempProb = 1
            for node in self.nodes:
                tempProb *= self.nodes[node].query(fullQuery)

            probability += tempProb
            iterator += 1

        return probability

    # outputs the network as a string
    def __str__(self):
        output = ''
        for node in self.nodes:
            output += f'{node}:{self.nodes[node]}'

        return output