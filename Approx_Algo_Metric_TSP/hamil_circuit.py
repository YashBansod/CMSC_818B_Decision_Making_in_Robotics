#!/usr/bin/env python

# ******************************************    Libraries to be imported    ****************************************** #
from __future__ import print_function
import numpy as np
from copy import deepcopy
from span_tree import SpanningTree


# ******************************************    Class Declaration Start     ****************************************** #
class HamiltonianCircuit(object):

    def __init__(self, mst, coord_array):
        """
        Constructor of the Class

        :param SpanningTree mst: An instance of the class SpanningTree. Instance should have the mst already computed.
        :param np.ndarray coord_array: A numpy array containing the coordinates of the nodes.
        """
        self.num_nodes = mst.num_nodes
        self.visit_check = np.zeros(self.num_nodes, dtype=np.bool)
        self.edge_list = []
        self._circuit_length = None
        self._route_list = None
        self._mst_graph = deepcopy(mst.graph)
        self._coord_arr = coord_array.copy()
        self._o_dist_arr = mst.get_original_dist_array()
        self._stack = []

    # ******************************        Class Method Declaration        ****************************************** #
    def _compute_first_edge(self):
        p_node = np.random.randint(0, self.num_nodes)
        n_node = self._mst_graph[p_node].pop(0)
        self._stack.extend([p_node, n_node])

        self.edge_list.append(np.array([p_node, n_node]))
        self.visit_check[[p_node, n_node]] = True

    # ******************************        Class Method Declaration        ****************************************** #
    def compute_2_approx_hmlt_circuit(self, seed=20):
        """
        :param int seed: (Optional) Integer specifying the seed for controlled randomization.
        """
        np.random.seed(seed)
        self._compute_first_edge()
        while True:
            p_node = self._stack[-1]
            try:
                n_node = self._mst_graph[p_node].pop(0)
                while self.visit_check[n_node]:
                    n_node = self._mst_graph[p_node].pop(0)
                self._stack.append(n_node)
                self.edge_list.append(np.array([self.edge_list[-1][1], n_node]))
                self.visit_check[n_node] = True
            except IndexError:
                if len(self._stack) > 1:
                    self._stack.pop(-1)
                else:
                    break

    # ******************************        Class Method Declaration        ****************************************** #
    def untangle_circuit(self, num_passes=1):
        """
        :param int num_passes: (Optional) Integer specifying the number of passes the algorithm should make to to
                                untangle the circuit.
        """
        num_edges = len(self.edge_list)
        num_edges_m2 = num_edges - 2
        edge_array = np.array(self.edge_list)

        for i in range(num_passes):
            edge_1_ind = 0
            while edge_1_ind < num_edges_m2:
                for edge_2_ind in range(edge_1_ind + 2, num_edges):
                    if self._do_intersect(edge_array[edge_1_ind], edge_array[edge_2_ind]):
                        edge_1_p_2 = edge_array[edge_1_ind, 1]
                        edge_array[edge_1_ind, 1] = edge_array[edge_2_ind, 0]
                        edge_array[edge_2_ind, 0] = edge_1_p_2
                        edge_array[edge_1_ind + 1: edge_2_ind] = np.flip(edge_array[edge_1_ind + 1: edge_2_ind])
                edge_1_ind += 1
        self.edge_list = list(edge_array)

    # ******************************        Class Method Declaration        ****************************************** #
    def _orientation(self, p_1, p_2, p_3):
        """
        :param int p_1: Index of point 1 in the coordinate array.
        :param int p_2: Index of point 2 in the coordinate array.
        :param int p_3: Index of point 3 in the coordinate array.
        :return: Boolean representing if the points connect clockwise or counter-clockwise.
        :rtype: bool
        """
        p = self._coord_arr[p_1]
        q = self._coord_arr[p_2]
        r = self._coord_arr[p_3]
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        return 1 if val > 0 else 0

    # ******************************        Class Method Declaration        ****************************************** #
    def _do_intersect(self, edge_1, edge_2):
        """
        :param tuple edge_1: A tuple / list / nd-array containing the nodes in the edge 1.
        :param tuple edge_2: A tuple / list / nd-array containing the nodes in the edge 2.
        :return: A boolean denoting if the edges intersect.
        :rtype: bool
        """
        p_1, n_1 = edge_1
        p_2, n_2 = edge_2

        o1 = self._orientation(p_1, n_1, p_2)
        o2 = self._orientation(p_1, n_1, n_2)
        o3 = self._orientation(p_2, n_2, p_1)
        o4 = self._orientation(p_2, n_2, n_1)

        return True if o1 != o2 and o3 != o4 else False

    # ******************************        Class Method Declaration        ****************************************** #
    def get_circuit_length(self):
        if self._circuit_length is None:
            self._circuit_length = 0
            for i in range(self.num_nodes - 1):
                self._circuit_length += self._o_dist_arr[self.edge_list[i][0], self.edge_list[i][1]]
            self._circuit_length += self._o_dist_arr[self.edge_list[-1][1], self.edge_list[0][0]]
        return self._circuit_length

    # ******************************        Class Method Declaration        ****************************************** #
    def get_route_list(self):
        if self._route_list is None:
            self._route_list = []
            for index in range(len(self.edge_list)):
                self._route_list.append(self.edge_list[index][0])
            self._route_list.append(self.edge_list[-1][1])
        return self._route_list

# ******************************************    Class Declaration End       ****************************************** #


"""
Author: Yash Bansod
UID: 116776547
E-mail: yashb@umd.edu
Organisation: University of Maryland, College Park
"""