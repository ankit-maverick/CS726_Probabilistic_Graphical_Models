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
        self._JTree = None

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
            self._potentials = None

    class JunctionTree:
        def __init__(self):
            self._Nodes = []
            self._nodeList = []
            self._factorList = []
            self._edgeList = []
            self._messageList = []

    class JT_Node:
        def __init__(self):
            self._neighbours = []
            self._clique = set([])

    def _nodeMindegree(self, not_current_nodes):
        mindegree =float("inf")
        nodeMindegree = ""

        for key in self._nodes.keys():
            if((key in not_current_nodes) == False):
                
                key_degree = 0
                for index in self._nodes[key].neighbours:
                    if((index in not_current_nodes) == False):
                        key_degree = key_degree + 1
                # print key, key_degree
                
                if(key_degree < mindegree):
                    mindegree = key_degree
                    nodeMindegree = key
        return nodeMindegree

    def _connectClique(self, clique):
        added_edges = 0
        for i in clique:
            for j in clique:
                if((i != j) and (j not in self._nodes[i].neighbours)):
                    print "-- Edge added : ",i,"-",j
                    self._num_edges = self._num_edges + 1
                    added_edges = added_edges + 1
                    self._nodes[i].neighbours.add(j)
                    self._nodes[j].neighbours.add(i)
        return added_edges

    def _maximalClique(self):
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

    def _maximalEdge(self, crossing_edges):
        max_edge = (0,(0,0,set([])))
        for edge1 in crossing_edges:
            if(edge1[1][1] > max_edge[1][1]):
                max_edge = edge1;
        return max_edge

    def _multiply_factors_for_clique_node(self, node_list):
        clique_node_factor = self.Factor([])
        pair_node_list = []
        print "Entering _multiply_factors_for_clique_node...."
        print node_list
        for i in range(len(node_list)):
            for j in range(i + 1, len(node_list)):
                pair = [node_list[i], node_list[j]]
                pair_node_list.append(pair)
                if _concatenate_sorted_list_of_integer_strings(pair) not in self._factors:
                    intermediate_factor = self.Factor(pair)
                    intermediate_factor._potentials = np.ones((self._nodes[pair[0]].cardinality, self._nodes[pair[1]].cardinality))
                    self._factors[_concatenate_sorted_list_of_integer_strings(pair)] = intermediate_factor

        for node in node_list:
            if node in self._factors:
                clique_node_factor = self.multiply_factor([node], clique_node_factor._node_seq)

        for pair in pair_node_list:
            clique_node_factor = self.multiply_factor(pair, clique_node_factor._node_seq)

        self._factors[_concatenate_sorted_list_of_integer_strings(node_list)] = clique_node_factor

        return clique_node_factor
        #for pair in pair_node_list:
        #    if _concatenate_sorted_list_of_integer_strings(pair) in self._factors and (pair[0] not in clique_node_factor._node_set or pair[1] not in clique_node_factor._node_set):
        #        clique_node_factor = self.multiply_factor(pair, clique_node_factor._node_seq)


    def junctionTree(self):
        # Generate Graph with Maximal Cliques as Nodes and edge weight
        # between them as number of common Variables between them
        clique_graph = []
        clique_nodes = self._cliques
        for i in clique_nodes:
            connection_list =[]
            for j in clique_nodes:
                if (i != j):
                    intersect = len(i.intersection(j))
                    if(intersect > 0):
                        connection_list.append((clique_nodes.index(j),intersect,j))
            clique_graph.append(connection_list)

        # Prim's Algorithm
        n = len(clique_nodes)
        V = [0]
        E = []
        print "\nNumber of Clique Nodes : ",n
        print "Number of Clique Nodes : ",n-1,"\n"

        self._JTree = self.JunctionTree()
        for node in clique_nodes:
            node_list = list(node)
            self._JTree._factorList.append(self._multiply_factors_for_clique_node(node_list))

        for count_node in range(n):
            E.append([])
        for count_node in range(n-1):
            crossing_edges =[]
            for node1 in V:
                for edge1 in clique_graph[node1] :

                    if(edge1[0] not in V):
                        # node2 = node1
                        crossing_edges.append((node1,edge1))

            (node2,max_edge) = self._maximalEdge(crossing_edges)
            print "max :" ,max_edge 

            V.append(max_edge[0])
            E[node2].append((max_edge[0], max_edge[1], self.marginalize_factor(list(clique_nodes[node2]), list(clique_nodes[node2] - (clique_nodes[node2].intersection(clique_nodes[max_edge[0]]))))))
            E[max_edge[0]].append((node2, max_edge[1], self.marginalize_factor(list(clique_nodes[max_edge[0]]), list(clique_nodes[max_edge[0]] - (clique_nodes[max_edge[0]].intersection(clique_nodes[node2]))))))

        # Store JuntionTree in self._JTree
        
        for node1 in clique_nodes:
            jt_node = self.JT_Node()
            jt_node._clique = node1
            self._JTree._Nodes.append(jt_node)

        for jt_node in self._JTree._Nodes:
            jt_node._neighbours = []
            
            for e in E[clique_nodes.index(jt_node._clique)]:
                jt_node._neighbours.append((self._JTree._Nodes[e[0]],e[1]))

        self._JTree._edgeList = E
        self._JTree._nodeList = clique_nodes

        # Calculate & Print Largest Clique
        largest_clique = set([])
        for i in self._JTree._nodeList:
            if (len(i) > len(largest_clique)):
                largest_clique = i

        print "Largest Clique : ",largest_clique, "\n"
        
        # Calculate Separatir Nodes
        for e in self._JTree._edgeList:
            for i in e:
                print "Cliques : ", self._JTree._nodeList[self._JTree._edgeList.index(e)]," & ", self._JTree._nodeList[i[0]], "  |   Separation Variables : ", self._JTree._nodeList[self._JTree._edgeList.index(e)].intersection(self._JTree._nodeList[i[0]])

    def sum_query(self, node_list):
        node_list = set(node_list)
        for i in range(len(self._JTree._nodeList)):
            if node_list <= self._JTree._nodeList[i]:
                clique_index = i
                break
        print " Clique index : " + str(clique_index)

        MPA_tree = copy.deepcopy(self)
        for k in range(len(MPA_tree._JTree._edgeList) - 1):
            for i in range(len(MPA_tree._JTree._edgeList)):
                if len(MPA_tree._JTree._edgeList[i]) == 1 and clique_index != i:
                    dest_clique_index = MPA_tree._JTree._edgeList[i][0][0]
                    print "To be eliminated : "
                    print MPA_tree._JTree._nodeList[i]
                    message_factor = MPA_tree._JTree._edgeList[i][0][2]
                    print "message_factor._node_seq"
                    print message_factor._node_seq
                    print "MPA_tree._JTree._factorList[dest_clique_index]._node_seq"
                    print MPA_tree._JTree._factorList[dest_clique_index]._node_seq
                    print self._factors.keys()
                    MPA_tree._JTree._factorList[dest_clique_index] = self.multiply_factor(message_factor._node_seq, MPA_tree._JTree._factorList[dest_clique_index]._node_seq)
                    # removing nodes and edges.
                    MPA_tree._JTree._nodeList[i] = None
                    MPA_tree._JTree._factorList[i] = None
                    MPA_tree._JTree._edgeList[i] = []
                    for j in range(len(MPA_tree._JTree._edgeList[dest_clique_index])):
                        if MPA_tree._JTree._edgeList[dest_clique_index][j][0] == i:
                            MPA_tree._JTree._edgeList[dest_clique_index].remove(MPA_tree._JTree._edgeList[dest_clique_index][j])
                            break
                    break
        for m in MPA_tree._JTree._factorList:
            if m is not None:
                out_factor = m
                if len(out_factor._node_seq) > len(node_list):
                    result_factor = self.marginalize_factor(out_factor._node_seq, list(set(out_factor._node_seq) - set(node_list)))

        probability = result_factor._potentials / np.sum(result_factor._potentials)
        return probability

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

    def multiply_factor(self, factor_node_list1, factor_node_list2):
        if factor_node_list1 == []:
            union_factor = self._factors[_concatenate_sorted_list_of_integer_strings(factor_node_list2)]
            return union_factor

        if factor_node_list2 == []:
            union_factor = self._factors[_concatenate_sorted_list_of_integer_strings(factor_node_list1)]
            return union_factor

        factor_key1 = _concatenate_sorted_list_of_integer_strings(factor_node_list1)
        factor_key2 = _concatenate_sorted_list_of_integer_strings(factor_node_list2)

        union = list(self._factors[factor_key1]._node_set.union(self._factors[factor_key2]._node_set))
        union.sort(key=int)
        union_factor_key = _concatenate_sorted_list_of_integer_strings(union)
        union_factor_cardinality_seq = []
        union_indices = []

        for i in union:
            union_indices.append(range(self._nodes[i].cardinality))
            union_factor_cardinality_seq.append(self._nodes[i].cardinality)

        union_factor_potentials = np.zeros(tuple(union_factor_cardinality_seq))

        print "union_factor_potentials.shape..."
        print union_factor_potentials.shape
        mask1 = _mask_node_list(union, self._factors[factor_key1]._node_seq)
        mask2 = _mask_node_list(union, self._factors[factor_key2]._node_seq)
        print "Multiplying factors...."
        print union
        print mask1
        print mask2
        for index in product(*union_indices):
            try:
                union_factor_potentials[index] = (self._factors[factor_key1]._potentials[_masked_tuple(index, mask1)] *
                                                  self._factors[factor_key2]._potentials[_masked_tuple(index, mask2)])
            except IndexError:
                print "IndexError...."
                print index
                print factor_key1
                print self._factors[factor_key1]._potentials.shape
                print _masked_tuple(index, mask1)
                print factor_key2
                print self._factors[factor_key2]._potentials.shape
                print _masked_tuple(index, mask2)

        union_factor = self.Factor(union)
        union_factor._potentials = union_factor_potentials
        union_factor._cardinality_seq = union_factor_cardinality_seq
        self._factors[union_factor_key] = union_factor
        return union_factor

    def marginalize_factor(self, factor_node_list, elimination_variables):
        factor_key = _concatenate_sorted_list_of_integer_strings(factor_node_list)
        factor_node_list.sort(key=int)
        elimination_variables.sort(key=int)
        print "marginalize_factor...."
        print factor_node_list
        print elimination_variables
        remaining_variables = list(set(factor_node_list) - set(elimination_variables))
        output_factor = self.Factor(remaining_variables)
        sum_axes = []
        for i in elimination_variables:
            sum_axes.append(factor_node_list.index(i))
        print "sum_axes"
        print sum_axes
        print "factor_key"
        print factor_key
        output_factor._potentials = np.sum(self._factors[factor_key]._potentials, tuple(sum_axes))
        print "self._factors[factor_key]._potentials"
        print self._factors[factor_key]._potentials
        print "output_factor._potentials.shape"
        print output_factor._potentials.shape
        self._factors[_concatenate_sorted_list_of_integer_strings(remaining_variables)] = output_factor
        return output_factor

    def triangulate(self):
        not_current_nodes = set()
        total_added_edges = 0
        G_tri = copy.deepcopy(self)
        for count_node in range(G_tri._num_nodes):
            node1 = G_tri._nodeMindegree(not_current_nodes)
            
            current_clique = set([node1])
            for neighbour in G_tri._nodes[node1].neighbours:
                if(neighbour not in not_current_nodes):
                    current_clique.add(neighbour)

            print "MinDegree Node :", node1
            total_added_edges = total_added_edges + G_tri._connectClique(current_clique)
            
            not_current_nodes.add(node1)
            G_tri._cliques.append(current_clique)
            G_tri._maximalClique()
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
        # self.multiply_factor(['2','7'], ['6','7'])
        # #print self._factors.keys()
        # print self._factors['2_6_7']._node_seq
        # print self._factors['2_6_7']._potentials
        # print "Multiplying factors..."
        # self.multiply_factor(['6','7'], ['6','2'])
        # print self._factors['2_6_7']._node_seq
        # print self._factors['2_6_7']._potentials
        # print "Multiplying factors..."
        # self.multiply_factor(['2','6'], ['7','2'])
        # print self._factors.keys()
        # print self._factors['2_6_7']._node_seq
        # print self._factors['2_6_7']._potentials


if __name__ == '__main__':
    G = Graph()
    G.parseGraph('TestCases/graph_1')
    G.parseFactor('TestCases/potentials_1')
    G.printParameters()
