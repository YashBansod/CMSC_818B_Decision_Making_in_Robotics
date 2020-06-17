#!/usr/bin/env python

# ******************************************    Libraries to be imported    ****************************************** #
from __future__ import print_function
import numpy as np


# ******************************************    Class Declaration Start     ****************************************** #
class SpanningTree(object):

    def __init__(self, dist_array):
        """
        Constructor of the Class

        :param np.ndarray dist_array: A numpy array containing distance of every node from other nodes.
        """
        self._o_dist_arr = dist_array
        self._dist_arr = self._o_dist_arr.copy()
        self._open_nodes = []
        self._tree_len = None

        self.num_nodes = self._dist_arr.shape[0]
        self.graph = dict()
        for i in range(self.num_nodes):
            self.graph[i] = []

    # ******************************        Class Method Declaration        ****************************************** #
    def _compute_first_edge(self):
        min_node_1, min_node_2 = np.unravel_index(np.argmin(self._dist_arr), self._dist_arr.shape)
        self._open_nodes.extend([min_node_1, min_node_2])
        self._dist_arr[:, [min_node_1, min_node_2]] = self._dist_arr[0, 0]
        self.graph[min_node_1].append(min_node_2)
        self.graph[min_node_2].append(min_node_1)

    # ******************************        Class Method Declaration        ****************************************** #
    def compute_mst(self):
        self._compute_first_edge()
        num_o_n = len(self._open_nodes)
        while num_o_n != self.num_nodes:
            min_n_1, min_n_2 = np.unravel_index(np.argmin(self._dist_arr[self._open_nodes]), [num_o_n, self.num_nodes])
            min_n_1 = self._open_nodes[min_n_1]

            self._dist_arr[:, min_n_2] = self._dist_arr[0, 0]
            self.graph[min_n_1].append(min_n_2)
            self.graph[min_n_2].append(min_n_1)
            self._open_nodes.append(min_n_2)
            num_o_n = len(self._open_nodes)

    # ******************************        Class Method Declaration        ****************************************** #
    def get_original_dist_array(self):
        return self._o_dist_arr

    # ******************************        Class Method Declaration        ****************************************** #
    def get_tree_length(self):
        if self._tree_len is None:
            self._tree_len = 0
            graph = self.graph.copy()
            for p_node in range(self.num_nodes):
                while len(graph[p_node]) > 0:
                    n_node = graph[p_node].pop(0)
                    self._tree_len += self._o_dist_arr[p_node, n_node]
            self._tree_len = int(self._tree_len / 2)
        return self._tree_len

# ******************************************    Class Declaration End       ****************************************** #


"""
Author: Yash Bansod
UID: 116776547
E-mail: yashb@umd.edu
Organisation: University of Maryland, College Park
"""