#!/usr/bin/env python

# ******************************************    Libraries to be imported    ****************************************** #
from __future__ import print_function
import numpy as np


# ******************************************    Func Declaration Start      ****************************************** #
def coord_array_from_node_dict(node_dict):
    """
    :param dict node_dict: An ordered dictionary containing the indices and the coordinates of the nodes.
    :return: A numpy array containing the coordinates.
    :rtype: np.ndarray
    """
    num_nodes = len(node_dict)
    coord_dim = len(node_dict[1])
    node_coord = np.zeros((num_nodes, coord_dim), dtype=np.int32)
    key_list = list(node_dict.keys())

    for key_ in key_list:
        node_coord[key_ - 1] = node_dict[key_]

    return node_coord

# ******************************************    Func Declaration End        ****************************************** #


# ******************************************    Func Declaration Start      ****************************************** #
def dist_array_from_coord_array(coord_array, fill_val=6000000, sqrt=False, naive=True):
    """
    :param np.ndarray coord_array: A numpy array containing the coordinates of the nodes
    :param int fill_val: A fill value to use for self distance of node.
    :param bool sqrt: A boolean denoting if the square root operation is done to compute distance.
    :param bool naive: A boolean to select between naive and specially handcrafted algorithm for computing distance.
                        Set this as False if number of coordinates more than 600 (recommended).
    :return: A numpy array containing distance of every node from other nodes.
    :rtype: np.ndarray
    """
    num_coord = coord_array.shape[0]
    if naive:
        x_mat = np.repeat([coord_array[:, 0]], num_coord, axis=0)
        y_mat = np.repeat([coord_array[:, 1]], num_coord, axis=0)
        delta_x = np.square(x_mat - x_mat.T)
        delta_y = np.square(y_mat - y_mat.T)
        if sqrt:
            dist_array = np.int32(np.sqrt(delta_x + delta_y) + 0.5)
        else:
            dist_array = delta_x + delta_y

        np.fill_diagonal(dist_array, fill_val)

    else:
        dist_array = np.empty((num_coord, num_coord), dtype=np.int32)
        np.fill_diagonal(dist_array, fill_val)

        if sqrt:
            for i in range(num_coord - 1):
                delta_x = np.square(coord_array[i + 1:, 0] - coord_array[i, 0])
                delta_y = np.square(coord_array[i + 1:, 1] - coord_array[i, 1])
                dist_array[i, i + 1:] = np.int32(np.sqrt(delta_x + delta_y) + 0.5)
                dist_array[i + 1:, i] = dist_array[i, i + 1:]

        else:
            for i in range(num_coord - 1):
                delta_x = np.square(coord_array[i + 1:, 0] - coord_array[i, 0])
                delta_y = np.square(coord_array[i + 1:, 1] - coord_array[i, 1])
                dist_array[i, i + 1:] = delta_x + delta_y
                dist_array[i + 1:, i] = dist_array[i, i + 1:]

    return dist_array

# ******************************************    Func Declaration End        ****************************************** #


# ******************************************    Func Declaration Start      ****************************************** #
def random_nodes_generator(num_nodes, seed=20):
    """
    :param int num_nodes: An Integer denoting the number of nodes
    :param int seed: (Optional) Integer specifying the seed for controlled randomization.
    :return: A dictionary containing the coordinates.
    :rtype: dict
    """
    np.random.seed(seed)
    max_coord_val = num_nodes
    num_coord_grid = max_coord_val * max_coord_val
    index = np.arange(max_coord_val * max_coord_val)
    np.random.shuffle(index)
    random_slice_start = np.random.randint(0, num_coord_grid - num_nodes)
    coord_index = index[random_slice_start:random_slice_start + num_nodes]
    x_array = np.arange(max_coord_val).repeat(max_coord_val)
    y_array = np.tile(np.arange(max_coord_val), max_coord_val)
    node_coord = np.empty((num_nodes, 2), dtype=np.int32)
    node_coord[:, 0] = x_array[coord_index]
    node_coord[:, 1] = y_array[coord_index]

    node_dict = {}
    for i in range(num_nodes):
        node_dict[i] = (x_array[coord_index[i]], y_array[coord_index[i]])
    return node_dict

# ******************************************    Func Declaration End        ****************************************** #


"""
Author: Yash Bansod
UID: 116776547
E-mail: yashb@umd.edu
Organisation: University of Maryland, College Park
"""