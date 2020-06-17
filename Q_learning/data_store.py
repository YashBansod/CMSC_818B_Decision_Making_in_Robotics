# !/usr/bin/env python

# ******************************************    Libraries to be imported    ****************************************** #
import random
import numpy as np


# ******************************************    Class Declaration Start     ****************************************** #
class DataStore(object):

    def __init__(self, max_memory=50000):
        self._max_memory = max_memory
        self._samples = []

    # ******************************        Class Method Declaration        ****************************************** #
    def add_sample(self, sample):
        self._samples.append(sample)
        while len(self._samples) > self._max_memory:
            self._samples.pop(0)

    # ******************************        Class Method Declaration        ****************************************** #
    def sample(self, no_samples):
        if no_samples > len(self._samples):
            return np.array(random.sample(self._samples, len(self._samples)))
        else:
            return np.array(random.sample(self._samples, no_samples))


# ******************************************    Class Declaration End       ****************************************** #

"""
Author: Yash Bansod
UID: 116776547
E-mail: yashb@umd.edu
Organisation: University of Maryland, College Park
"""