import numpy as np
from itertools import product
import copy


def _concatenate_sorted_list_of_integer_strings(l):
    l.sort(key=int)
    string = ''
    for i in l:
        string = string + i + "_"
    return string[:-1]


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
        self._cliques = []

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

    def _node_mindegree(self,not_current_nodes):
        mindegree =float("inf")
        node_mindegree = ""

        for key in self._nodes.keys():
            if((key in not_current_nodes) == False):
                
                key_degree = 0
                for index in self._nodes[key].neighbours:
                    if((index in not_current_nodes) == False):
                        key_degree = key_degree + 1
                # print key, key_degree
                
                if(key_degree < mindegree):
                    mindegree = key_degree
                    node_mindegree = key
        return node_mindegree

    def _connect_clique(self, clique):
        added_edges = 0
        for i in clique:
            for j in clique:
                if((i != j) and (j not in self._nodes[i].neighbours)):
                    print "Edge added : ",i,"-",j
                    self._num_edges = self._num_edges + 1
                    added_edges = added_edges + 1
                    self._nodes[i].neighbours.add(j)
                    self._nodes[j].neighbours.add(i)
        return added_edges

    def _maximal_cliques(self):
        new_cliques = []
        for i in self._cliques:
            temp_cliques = copy.deepcopy(self._cliques)
            temp_cliques.remove(i)
            flag = True
            for j in temp_cliques:
                if (i <= j): 
                    flag = False
                    break
            if (flag):
                new_cliques.append(i)
        self._cliques = new_cliques

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
        factor_key1 = _concatenate_sorted_list_of_integer_strings(list(factor_key1.split('_')))
        factor_key2 = _concatenate_sorted_list_of_integer_strings(list(factor_key2.split('_')))

        union = list(self._factors[factor_key1]._node_set.union(self._factors[factor_key2]._node_set))
        union.sort(key=int)
        union_factor_key = _concatenate_sorted_list_of_integer_strings(union)
        print union_factor_key
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
        self._factors[union_factor_key] = union_factor
        #return union_factor

    def triangulate(self):
        not_current_nodes = set()
        total_added_edges = 0
        G_tri = copy.deepcopy(self)
        for count_node in range(G_tri._num_nodes):
            node1 = G_tri._node_mindegree(not_current_nodes)
            
            current_clique = set([node1])
            for neighbour in G_tri._nodes[node1].neighbours:
                if(neighbour not in not_current_nodes):
                    current_clique.add(neighbour)

            total_added_edges = total_added_edges + G_tri._connect_clique(current_clique)
            
            not_current_nodes.add(node1)
            G_tri._cliques.append(current_clique)
            G_tri._maximal_cliques()
        print "\nNumber of Edges Added : " ,total_added_edges
        return G_tri


    def printParameters(self):
        print self._num_nodes
        print self._num_edges
        print self._nodes['1'].neighbours
        print self._factors['0_1']._node_seq
        print self._factors['0_1']._potentials
        print self._factors['1_2']._node_seq
        print self._factors['1_2']._potentials
        print "Multiplying factors..."
        self.multiply_factor('0_1', '1_2')
        print self._factors.keys()
        print self._factors['0_1_2']._node_seq
        print self._factors['0_1_2']._potentials


if __name__ == '__main__':
    G = Graph()
    G.parseGraph('TestCases/graph_1')
    G.parseFactor('TestCases/potentials_1')
    G.printParameters()
