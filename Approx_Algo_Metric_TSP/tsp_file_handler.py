#!/usr/bin/env python

# ******************************************    Libraries to be imported    ****************************************** #
from __future__ import print_function
import tsplib95 as tsp


# ******************************************    Class Declaration Start     ****************************************** #
class TspFileHandler(object):

    def __init__(self, problem_path):
        """
        Constructor of the Class

        :param str problem_path: A string containing the absolute path of the problem ".tsp" file
        """
        assert problem_path is not None, "You must give a valid path of the problem \".tsp\" file."
        self.inp_abs_path = problem_path.replace("\\", "/")
        self.inp_file_name = self.inp_abs_path.split('/')[-1]
        self.out_file_name = self.inp_file_name.split('.')[0] + ".out.tour"
        self.out_abs_path = self.inp_abs_path[:self.inp_abs_path.find(self.inp_file_name)] + self.out_file_name
        self._problem = None
        self._solution = None
        self._solution_text = None
        self._solution_header = self._create_solution_header()

    # ******************************        Class Method Declaration        ****************************************** #
    def _create_solution_header(self):
        header = "NAME : " + self.out_file_name + '\n'
        header += "COMMENT : Tour for " + self.inp_file_name + " (Length {0})" + '\n'
        header += "TYPE : TOUR" + '\n'
        header += "DIMENSION : {1}" + '\n'
        header += "TOUR_SECTION" + '\n'
        return header

    # ******************************        Class Method Declaration        ****************************************** #
    @staticmethod
    def _create_tour_section_text(edge_list):
        """
        :param list edge_list: A list containing the edges in the circuit
        :return: A string containing the tour section text
        :rtype: str
        """
        tour_section = ""
        for edge in edge_list:
            tour_section += str(edge[0]) + '\n'
        tour_section += str(edge_list[-1][1]) + '\n'
        return tour_section

    # ******************************        Class Method Declaration        ****************************************** #
    def get_solution_text(self, tour_len, num_nodes, edge_list):
        """
        :param int tour_len: An integer value denoting the tour length
        :param int num_nodes: An integer value denoting the number of nodes in the tour i.e. the tour dimension
        :param list edge_list: A list containing the edges in the circuit
        :return: A string containing the solution file text
        :rtype: str
        """
        if self._solution_text is None:
            header = self._solution_header.format(tour_len, num_nodes)
            tour_section = self._create_tour_section_text(edge_list)
            solution_footer = "-1\nEOF\n"
            self._solution_text = header + tour_section + solution_footer
        return self._solution_text

    # ******************************        Class Method Declaration        ****************************************** #
    def load_problem(self):
        if self._problem is None:
            self._problem = tsp.load_problem(self.inp_abs_path)
        return self._problem

    # ******************************        Class Method Declaration        ****************************************** #
    def load_solution(self, path=None):
        """
        :param str path: (Optional) Path of solution file. If solution not in directory containing problem file.
        :return: A solution object.
        :rtype: tsp.models.Solution
        """
        load_path = self.out_abs_path if path is None else path
        if self._solution is None:
            self._solution = tsp.load_solution(load_path)
        return self._solution

    # ******************************        Class Method Declaration        ****************************************** #
    def write_solution_file(self, tour_len, num_nodes, edge_list):
        """
        :param int tour_len: An integer value denoting the tour length
        :param int num_nodes: An integer value denoting the number of nodes in the tour i.e. the tour dimension
        :param list edge_list: A list containing the edges in the circuit
        """
        solution_text = self.get_solution_text(tour_len, num_nodes, edge_list)
        with open(self.out_abs_path, "w") as solution_file:
            solution_file.write(solution_text)

# ******************************************    Class Declaration End       ****************************************** #


"""
Author: Yash Bansod
UID: 116776547
E-mail: yashb@umd.edu
Organisation: University of Maryland, College Park
"""