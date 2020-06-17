#!/usr/bin/env python
"""
Solution for the second part of Question 1 of the Assignment. (Random instances)
"""
# ******************************************    Libraries to be imported    ****************************************** #
from __future__ import print_function

import time
import argparse
from utils import coord_array_from_node_dict, dist_array_from_coord_array, random_nodes_generator
from span_tree import SpanningTree
from hamil_circuit import HamiltonianCircuit
from tsp_plotter import TspPlotter


# ******************************************        Main Program Start      ****************************************** #
def main(args_):
    nodes_dict = random_nodes_generator(num_nodes=100, seed=50)
    coord_array = coord_array_from_node_dict(nodes_dict)

    naive_dist_compute = False if coord_array.shape[0] > 600 else True
    sqrt = True if args_.debug else False
    t_stamp_1 = time.time() if args_.debug else None
    dist_array = dist_array_from_coord_array(coord_array, fill_val=8000000, sqrt=sqrt, naive=naive_dist_compute)

    t_stamp_2 = time.time() if args_.debug else None
    mst = SpanningTree(dist_array)
    mst.compute_mst()

    t_stamp_3 = time.time() if args_.debug else None
    hmlt_circuit = HamiltonianCircuit(mst, coord_array)
    hmlt_circuit.compute_2_approx_hmlt_circuit(seed=50)
    if args_.untangle:
        hmlt_circuit.untangle_circuit()

    t_stamp_4 = time.time() if args_.debug else None
    if args_.debug:
        tree_len = mst.get_tree_length()
        circuit_len = hmlt_circuit.get_circuit_length()

        if args_.debug:
            print("MST_Length %d" % tree_len)
            print("Hamiltonian_Circuit_Length %d" % circuit_len)
            print("Distance_Computation %fs" % (t_stamp_2 - t_stamp_1))
            print("MST_Computation %fs" % (t_stamp_3 - t_stamp_2))
            print("Hamiltonian_Circuit_Computation %fs" % (t_stamp_4 - t_stamp_3))
            print("Total_TSP_Computation %fs" % (t_stamp_4 - t_stamp_1))

        if args_.display:
            plotter = TspPlotter(nodes_dict)
            plotter.plot_path(hmlt_circuit.get_route_list())
            plotter.plt.show(block=True)

# ******************************************        Main Program End        ****************************************** #


if __name__ == '__main__':
    try:
        argparser = argparse.ArgumentParser(description='2-Approximation TSP Solver')
        argparser.add_argument('-d', '--display', action='store_true', dest='display', help='display TSP plots')
        argparser.add_argument('-u', '--untangle', action='store_true', dest='untangle', help='run untangle heuristic')
        argparser.add_argument('-v', '--verbose', action='store_true', dest='debug', help='print debug information')
        args = argparser.parse_args()

        main(args)
    except KeyboardInterrupt:
        print('\nProcess interrupted by user. Bye!')

"""
Author: Yash Bansod
UID: 116776547
E-mail: yashb@umd.edu
Organisation: University of Maryland, College Park
"""