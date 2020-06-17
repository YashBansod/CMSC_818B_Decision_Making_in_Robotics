# !/usr/bin/env python
"""
Solution for Problem 4a of the Assignment.
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
    with open('data_resources/problem4a_train.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        train_list = []
        for row in csv_reader:
            train_list.append((float(row[0]), float(row[1])))

    with open('data_resources/problem4a_test.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        test_list = []
        for row in csv_reader:
            test_list.append(float(row[0]))

    train_list.sort()
    test_list.sort()
    train_array = np.array(train_list, dtype=np.float32)
    test_array = np.array(test_list, dtype=np.float32)

    sine_kernel = gp.kernels.ExpSineSquared(length_scale=1, periodicity=1)
    model = gp.GaussianProcessRegressor(kernel=sine_kernel, alpha=0.01, n_restarts_optimizer=0)

    t_stamp_1 = time.time() if args_.debug else None
    model.fit(train_array[:, 0:1], train_array[:, 1])
    t_stamp_2 = time.time() if args_.debug else None
    params = model.kernel_.get_params()

    y_pred, std = model.predict(np.expand_dims(test_array, axis=1), return_std=True)

    if args_.debug:
        print("Time taken for GPR fitting: %f seconds" % (t_stamp_2 - t_stamp_1))
        print("Params after fitting: ", params)

        true_test_y = np.sin(3 * test_array)
        mse = np.mean(np.square(y_pred - true_test_y))
        print("Mean Square Error Value: %f" % mse)

    if args_.write:
        output = np.zeros((y_pred.shape[0], 2), dtype=np.float32)
        output[:, 0], output[:, 1] = y_pred, std
        # noinspection PyTypeChecker
        np.savetxt('data_resources/problem4a_output.csv', output, delimiter=',', fmt="%0.8f")

    if args_.display:
        fig = plt.figure(figsize=(15, 8))
        subplt = fig.subplots()
        plt.title("Gaussian Process Regression")
        plt.xlabel("x-coordinate")
        plt.ylabel("y-coordinate")

        low, high = train_array[0, 0], train_array[-1, 0]
        ref_x = np.linspace(low, high, int((high - low) * 50))
        ref_y = np.sin(3 * ref_x)

        subplt.scatter(train_array[:, 0], train_array[:, 1], marker='x', color='r', label='Train Samples')
        subplt.plot(ref_x, ref_y, color='g', linestyle='-.', linewidth=0.8, label='Reference Function')
        subplt.plot(test_array, y_pred, color='b', label='Test Prediction')

        delta = 2 * std
        upper_pred, lower_pred = y_pred + delta, y_pred - delta
        subplt.fill_between(test_array, upper_pred, lower_pred, facecolor='k', alpha=0.2)

        subplt.legend(loc='lower right', bbox_to_anchor=(1, 0.99))
        plt.tight_layout()
        plt.show(block=True)

# ******************************************        Main Program End        ****************************************** #


if __name__ == '__main__':
    try:
        argparser = argparse.ArgumentParser(description='Gaussian Process Regression on Noisy 1D Sine Wave Data')
        argparser.add_argument('-d', '--display', action='store_true', dest='display', help='display solution plot')
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