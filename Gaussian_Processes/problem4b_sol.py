# !/usr/bin/env python
"""
Solution for Problem 4b of the Assignment.
"""
# ******************************************    Libraries to be imported    ****************************************** #
from __future__ import print_function

import csv
import time
import argparse
import numpy as np
from matplotlib import pyplot as plt
from sklearn import gaussian_process as gp


# ******************************************        Main Program Start      ****************************************** #
def main(args_):
    with open('data_resources/problem4b_train.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        train_list = []
        for row in csv_reader:
            train_list.append((float(row[0]), float(row[1]), float(row[2]), float(row[3]), float(row[4])))

    with open('data_resources/problem4b_test.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        test_list = []
        for row in csv_reader:
            test_list.append((float(row[0]), float(row[1]), float(row[2]), float(row[3])))

    with open('data_resources/problem4b_sol.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        sol_list = []
        for row in csv_reader:
            sol_list.append(float(row[0]))

    train_array = np.array(train_list, dtype=np.float32)
    del train_list

    test_array = np.array(test_list, dtype=np.float32)
    del test_list

    sol_array = np.array(sol_list, dtype=np.float32)
    del sol_list

    if args_.display:
        plt.figure(figsize=(18, 7))

        plt.subplot(2, 2, 1)
        plt.xlabel("temperature")
        plt.ylabel("energy output")
        plt.scatter(train_array[:, 0], train_array[:, 4], marker='+')

        plt.subplot(2, 2, 2)
        plt.xlabel("ambient pressure")
        plt.ylabel("energy output")
        plt.scatter(train_array[:, 1], train_array[:, 4], marker='+')

        plt.subplot(2, 2, 3)
        plt.xlabel("relative humidity")
        plt.ylabel("energy output")
        plt.scatter(train_array[:, 2], train_array[:, 4], marker='+')

        plt.subplot(2, 2, 4)
        plt.xlabel("exhaust vaccum")
        plt.ylabel("energy output")
        plt.scatter(train_array[:, 3], train_array[:, 4], marker='+')

        plt.tight_layout()
        plt.show(block=True)

    rq_kernel = gp.kernels.RationalQuadratic(length_scale=0.005, alpha=0.03)
    model = gp.GaussianProcessRegressor(kernel=rq_kernel, alpha=0.001, n_restarts_optimizer=0, optimizer=None)

    t_stamp_1 = time.time() if args_.debug else None
    model.fit(train_array[:, 0:4], train_array[:, 4])
    t_stamp_2 = time.time() if args_.debug else None
    params = model.kernel_.get_params()

    y_pred, std = model.predict(test_array, return_std=True)

    if args_.debug:
        print("Time taken for GPR fitting: %f seconds" % (t_stamp_2 - t_stamp_1))
        print("Params after fitting: ", params)
        mse = np.mean(np.square(y_pred - sol_array))
        print("Mean Square Error Value: %f" % mse)

    if args_.write:
        output = np.zeros((y_pred.shape[0], 2), dtype=np.float32)
        output[:, 0], output[:, 1] = y_pred, std
        # noinspection PyTypeChecker
        np.savetxt('data_resources/problem4b_output.csv', output, delimiter=',', fmt="%0.4f")


# ******************************************        Main Program End        ****************************************** #
if __name__ == '__main__':
    try:
        argparser = argparse.ArgumentParser(description='GP Regression on Combined Cycle Power Plant Data Set')
        argparser.add_argument('-d', '--display', action='store_true', dest='display', help='display dataset plot')
        argparser.add_argument('-v', '--verbose', action='store_true', dest='debug', help='print debug information')
        argparser.add_argument('-w', '--write', action='store_true', dest='write', help='write solution file')
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