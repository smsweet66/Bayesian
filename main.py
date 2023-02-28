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
            while self.probabilityMatrix[0][0] != parent:
                rowNum += 1

            parentValue = ''
            for nodeValue in nodeValues:
                if nodeValue[0] == parent:
                    parentValue = nodeValue
                    break

            columnNums = [x for x in columnNums if x == parentValue]

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
        queryString = queryString.replace('=', ':').replace('T', '1').replace('F', '0')
        nodeValues = queryString.split(',')
        unusedNodes = list(self.nodes.keys())
        for node in nodeValues:
            unusedNodes.remove(node[0])

        iterator: int = 0    # helps iterate over all valid values of nodes not specified in query
        probability = 0
        while iterator < pow(2, len(unusedNodes)):
            tempIter: int = iterator
            fullQuery = nodeValues
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


def main():
    network = BayesianNetwork("A:B,C;B:C;C:D,E;D:E;E:F;F:G;G:")
    network.addProbability('A',
                           [["A:0", .72],
                            ["A:1", .28]])

    network.addProbability('B',
                           [["A", "A:0", "A:1"],
                            ["B:0", .35, .55],
                            ["B:1", .65, .45]])

    network.addProbability("C",
                           [["B", "B:0", "B:0", "B:1", "B:1"],
                            ["A", "A:0", "A:1", "A:0", "A:0"],
                            ["C:0", .79, .86, .35, .29],
                            ["C:1", .21, .14, .65, .71]])

    network.addProbability("D",
                           [["C", "C:0", "C:1"],
                            ["D:0", .3, .49],
                            ["D:1", .7, .51]])

    network.addProbability("E",
                           [["D", "D:0", "D:0", "D:1", "D:1"],
                            ["C", "C:0", "C:1", "C:0", "C:1"],
                            ["E:0", .09, .13, .29, .6],
                            ["E:1", .91, .87, .71, .4]])

    network.addProbability("F",
                           [["E", "E:0", "E:1"],
                            ["F:0", .08, .12],
                            ["F:1", .92, .88]])

    network.addProbability("G",
                           [["F", "F:0", "F:1"],
                            ["G:0", .36, .28],
                            ["G:1", .64, .72]])

    print(network.query("C=T"))


if __name__ == '__main__':
    main()
