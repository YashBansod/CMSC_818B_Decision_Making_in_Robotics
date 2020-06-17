#!/usr/bin/env python

# ******************************************    Libraries to be imported    ****************************************** #
from __future__ import print_function
import numpy as np
from copy import deepcopy
from matplotlib import pyplot as plt
from utils import coord_array_from_node_dict


# ******************************************    Class Declaration Start     ****************************************** #
class TspPlotter(object):

    def __init__(self, node_dict):
        """
        Constructor of the Class

        :param dict node_dict: An ordered dictionary containing the indices and the coordinates of the nodes.
        """
        self.nodes = deepcopy(node_dict)
        self.node_coord = coord_array_from_node_dict(self.nodes)
        self.plt = plt
        self.fig, self.subplt = None, None
        self.node_plt, self.start_node_plt, self.last_node_plt = None, None, None
        self.path_plt = None

    # ******************************        Class Method Declaration        ****************************************** #
    def plot_nodes(self, route_indices=None):
        """
        :param np.ndarray route_indices: (Optional) A numpy array containing the indices of the nodes in the route.
        """
        self.plot_setup()

        if route_indices is None:
            self.node_plt = self.subplt.scatter(self.node_coord[:, 0], self.node_coord[:, 1],
                                                marker='o', color='c', label='Nodes')
        else:
            r_l = np.array(route_indices)
            r_l -= np.min(r_l)

            if self.node_plt is not None:
                self.node_plt.remove()

            self.start_node_plt = self.subplt.scatter(self.node_coord[r_l[0], 0], self.node_coord[r_l[0], 1],
                                                      marker='+', color='g', label='Start Node')
            self.node_plt = self.subplt.scatter(self.node_coord[r_l[1:-1], 0], self.node_coord[r_l[1:-1], 1],
                                                marker='o', color='c', label='Nodes')
            self.last_node_plt = self.subplt.scatter(self.node_coord[r_l[-1], 0], self.node_coord[r_l[-1], 1],
                                                     marker='x', color='r', label='Last Node')

        self.subplt.legend(loc='lower right', bbox_to_anchor=(1, 0.99))

    # ******************************        Class Method Declaration        ****************************************** #
    def plot_path(self, route_indices):
        """
        :param np.ndarray route_indices: A numpy array containing the indices of the nodes in the route.
        """
        self.plot_nodes(route_indices)
        route_list = np.array(route_indices)
        route_list -= np.min(route_list)

        self.path_plt = self.subplt.plot(self.node_coord[route_list, 0], self.node_coord[route_list, 1], "--",
                                         linewidth=0.5, color='b', label='Path')
        self.subplt.legend(loc='lower right', bbox_to_anchor=(1, 0.95))

    # ******************************        Class Method Declaration        ****************************************** #
    def plot_setup(self):
        self.fig = plt.figure(figsize=(6, 6)) if self.fig is None else self.fig
        self.subplt = self.fig.subplots() if self.subplt is None else self.subplt
        plt.xlabel("x-coordinate")
        plt.ylabel("y-coordinate")

        axes = plt.gca()
        min_coord_val, max_coord_val = np.min(self.node_coord), np.max(self.node_coord)
        buffer = (max_coord_val - min_coord_val) // 10 + 1
        axes.set_xlim([min_coord_val - buffer, max_coord_val + buffer])
        axes.set_ylim([min_coord_val - buffer, max_coord_val + buffer])


# ******************************************    Class Declaration End       ****************************************** #


"""
Author: Yash Bansod
UID: 116776547
E-mail: yashb@umd.edu
Organisation: University of Maryland, College Park
"""
