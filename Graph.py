import numpy as np
from itertools import product


def _concatenate_sorted_list_of_integer_strings(l):
    l.sort(key=int)
    string = ''
    for i in l:
        string = string + i
    return string


def _diff_list(a, b):
    b = set(b)
    return [aa for aa in a if aa not in b]


def _mask_node_list(union_factor_list, factor_list):
    mask = []
    for i in union_factor_list:
        if i in factor_list:
            mask.append(True)
        else:
            mask.append(False)
    return mask


def _masked_tuple(union_factor_index, mask):
    factor_index = []
    for i in range(len(mask)):
        if mask[i]:
            factor_index.append(union_factor_index[i])
    return tuple(factor_index)


class Graph:

    def __init__(self):
        self._num_nodes = 0
        self._num_edges = 0
        self._nodes = {}
        self._factors = {}

    class Node:
        def __init__(self, index, cardinality):
            self.index = index
            self.cardinality = cardinality
            self.neighbours = set()

    class Factor:
        def __init__(self, node_list):
            self._node_seq = node_list
            self._node_set = set(node_list)
            self._cardinality_seq = []
            self._cardinality_product = 1            

    def parseGraph(self, fileName):
        line_no = 1
        with open(fileName) as f:
            for line in f:
                line = line[:-1]
                if line_no == 1:
                    self._num_nodes = int(line)

                elif line_no == 2:
                    self._num_edges = int(line)

                # cardinality
                elif line_no > 2 and line_no <= 2 + self._num_nodes:
                    line = line.split()
                    self._nodes[line[0]] = self.Node(line[0], int(line[1]))

                elif line_no > 2 + self._num_nodes and line_no <= 2 + self._num_nodes + self._num_edges:
                    node1, node2 = line.split()
                    self._nodes[node1].neighbours.add(node2)
                    self._nodes[node2].neighbours.add(node1)
                line_no = line_no + 1

    def parseFactor(self, fileName):
        with open(fileName) as f:
            for line in f:
                line = line[:-1]
                line = line.split()
                if line[0] == '#':
                    key = _concatenate_sorted_list_of_integer_strings(line[1:])
                    self._factors[key] = self.Factor(line[1:])
                    for i in self._factors[key]._node_seq:
                        card = self._nodes[i].cardinality
                        self._factors[key]._cardinality_seq.append(card)
                        self._factors[key]._cardinality_product *= card
                    self._factors[key]._potentials = np.zeros(tuple(self._factors[key]._cardinality_seq))
                else:
                    index = tuple(np.asarray(line[:-1]).astype(int))
                    self._factors[key]._potentials[index] = float(line[-1])

    def multiply_factor(self, factor_key1, factor_key2):
        factor_key1 = _concatenate_sorted_list_of_integer_strings(list(factor_key1))
        factor_key2 = _concatenate_sorted_list_of_integer_strings(list(factor_key2))

        union = list(self._factors[factor_key1]._node_set.union(self._factors[factor_key2]._node_set))
        union.sort(key=int)
        union_factor_cardinality_seq = []
        union_indices = []

        for i in union:
            union_indices.append(range(self._nodes[i].cardinality))
            union_factor_cardinality_seq.append(self._nodes[i].cardinality)

        union_factor_potentials = np.zeros(tuple(union_factor_cardinality_seq))

        mask1 = _mask_node_list(union, self._factors[factor_key1]._node_seq)
        mask2 = _mask_node_list(union, self._factors[factor_key2]._node_seq)
        for index in product(*union_indices):
            union_factor_potentials[index] = (self._factors[factor_key1]._potentials[_masked_tuple(index, mask1)] *
                                              self._factors[factor_key2]._potentials[_masked_tuple(index, mask2)])

        union_factor = self.Factor(union)
        union_factor._potentials = union_factor_potentials
        union_factor._cardinality_seq = union_factor_cardinality_seq
        return union_factor

    def printParameters(self):
        print self._num_nodes
        print self._num_edges
        print self._nodes['1'].neighbours
        print self._factors['01']._node_seq
        print self._factors['01']._potentials
        print self._factors['12']._node_seq
        print self._factors['12']._potentials
        factor = self.multiply_factor('01', '12')
        print factor._node_seq
        print factor._potentials


if __name__ == '__main__':
    G = Graph()
    G.parseGraph('samplegraph.txt')
    G.parseFactor('potentials.txt')
    G.printParameters()
