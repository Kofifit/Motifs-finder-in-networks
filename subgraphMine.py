import numpy
import numpy as np
import pandas as pd
import collections
import itertools


def subgraphGenerator(n):
    # This function get an integer (n) as the input
    # This function gives back all the fully-connected sub-graphs of the size n.

    ## Get all possible edges ##

    # Define a list of the vertices
    nodes = np.arange(0, n)

    # Define list to store all possible edges
    edgeAll = np.zeros((n ** 2 - n, 2), dtype=int)

    # Loop to find all possible edges
    index = 0
    for e1 in range(0, n):
        for e2 in range(0, n):
            if e1 != e2:
                edgeAll[index, 0] = e1
                edgeAll[index, 1] = e2
                index += 1

    ## Find all possible edge combinations that contain all vertices

    # Define counter for loop
    counter = 0

    # Define an empty list for the combinations
    combo = list()

    # Define an empty list for the number of edges for each sub-graph
    edgeNum = list()

    # For loop to get all combinations
    for conNum in range(n - 1, n ** 2 - n + 1):

        # Get all possible combinations with itertools package
        currentCombo = list(itertools.combinations(list(range(0, n ** 2 - n)), conNum))

        # Loop to find if each combination has all the vertices
        for c in currentCombo:
            lst = np.unique(np.concatenate((edgeAll[[tuple(c)]]), axis=0))

            # If not, the combination is removed from the list
            if not np.array_equal(lst, nodes):
                currentCombo.remove(c)

        # Add current list of combinations to the general list of combinations
        combo.extend(currentCombo)
        edgeNum.extend(np.repeat(conNum, len(currentCombo)))

    return combo, edgeNum, edgeAll


def motifGeneratorMine(n):
    combo, _, edgeAll = subgraphGenerator(n)

    # Create new list to store motifs
    output = list()

    # Find sub-graphs that are exactly the same and merge them
    for sub in combo:
        subG = collections.defaultdict(list)  # Dictionary for current sub-graph

        # Loop for adding the count of 'in' and 'out' for each node
        for e in sub:
            edge = edgeAll[e]  # Get the nodes of the current edge
            subG[edge[0]].append('out')
            subG[edge[1]].append('in')

        # Loop to sort the values in the dictionary
        for value in subG.values():
            value.sort()

        # Check if current sub-graph is already in output list
        ans = True
        if output:  # Check if output is not empty
            for d in output:  # Loop through sub-graphs in output
                fnd = list()
                for v in d.values():  # Check if they match current sub-graph
                    fnd.append(v in subG.values())
                if all(fnd):
                    ans = False
                    break

        # Add current sub-graph to output list, if not found
        if ans:
            output.append(subG)

    return output


def networkCombosMine(n, network):
    # This function gets two inputs - a network (a list of lists) and a node number (an integer)
    # It returns a table with the possible motifs, the number of times they appeared in the given network
    # and the locations where they appeared
    # The algorithm used to find the motifs and their locations in the network is my own algorithm

    edgeNum = np.arange(n - 1, n ** 2 - n + 1)  # Vector of possible number of edges
    edgeNetNum = len(network)  # Find number of edges in the network
    combo = []  # Define an empty list for the combinations

    for num in edgeNum:
        currentCombo = list(itertools.combinations(list(range(0, edgeNetNum)), num))

        # Loop to find if each combination has exactly n nodes
        for c in currentCombo:
            lst = np.unique(np.concatenate((network[[tuple(c)]]), axis=0))
            nodeNum = len(lst)

            # If not, the combination is removed from the list
            if not np.array_equal(nodeNum, n):
                currentCombo.remove(c)

        combo.extend(currentCombo)

    # Run subgraphFinder to get all sub-graphs with n nodes
    motifs = motifGeneratorMine(n)

    # Define output dataframe
    output = pd.DataFrame(columns=['Motif', 'Counter', 'Locations'])

    # Add motifs to Motif column in df
    output['Motif'] = motifs

    # Add zeros to Counter column in df
    output['Counter'] = 0

    #  Create dictionaries for sub-graphs and match them with motifs
    for sub in combo:
        subG = collections.defaultdict(list)  # Dictionary for current sub-graph
        outputSG = list()  # Save the sub-graph's edges to a list

        # Loop for adding the count of 'in' and 'out' for each node
        for e in sub:
            outputSG.append(network[e])
            edge = network[e]  # Get the nodes of the current edge
            subG[edge[0]].append('out')
            subG[edge[1]].append('in')

        # Loop to sort the values in the dictionary
        for value in subG.values():
            value.sort()

        # Match sub-graph to motif
        for m in motifs:  # Loop through sub-graphs in output
            fnd = list()
            for v in m.values():  # Check if they match current sub-graph
                fnd.append(v in subG.values())

            # If sub-graph is matching motif, add the sub-graph to the dataframe and update the counter
            if all(fnd):
                output.loc[output['Motif'] == m, 'Counter'] += 1  # Add to counter
                # Add to Locations
                break


def uniqueNodes(graph):

    # This functions get a graph as a list of lists
    # It returns the unique edges in the order they appeared in the graph
    # For example: graph = [[1,0][0,2]] --> the function returns [1,0,2]

    vector = []
    for edge in graph: vector.extend(edge)

    output = []
    for node in vector:
        if node not in output or not output:
            output.append(node)

    return output

print(len(motifGeneratorMine(3)))