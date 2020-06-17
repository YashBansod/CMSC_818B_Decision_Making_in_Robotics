# !/usr/bin/env python

# ******************************************    Libraries to be imported    ****************************************** #
import numpy as np
import pandas as pd
import matplotlib.patches as mpatches
from matplotlib import pyplot as plt


# ******************************************    Class Declaration Start     ****************************************** #
class VisualizePolicy(object):

    def __init__(self, nn_model):
        feature = np.empty((10000, 2), dtype=np.float32)
        feature[:, 0] = np.random.uniform(-1.2, 0.6, feature.shape[0])
        feature[:, 1] = np.random.uniform(-0.07, 0.07, feature.shape[0])

        prediction = nn_model.model.predict_on_batch(feature).numpy()
        prediction = np.argmax(prediction, axis=1)

        color_series = pd.Series(prediction)
        colors = {0: 'blue', 1: 'lime', 2: 'red'}
        colors = color_series.apply(lambda x: colors[x])
        labels = ['Left', 'Right', 'Nothing']

        fig = plt.figure(5, figsize=[15, 10])
        ax = fig.gca()
        plt.set_cmap('brg')
        ax.scatter(feature[:, 0], feature[:, 1], c=color_series)
        ax.set_xlabel('Position')
        ax.set_ylabel('Velocity')
        ax.set_title('Policy')
        recs = []
        for i in range(3):
            recs.append(mpatches.Rectangle((0, 0), 1, 1, fc=sorted(colors.unique())[i]))
        plt.legend(recs, labels, loc=4, ncol=3)
        plt.grid()
        plt.tight_layout()
        fig.savefig('policy.png')
        plt.show(block=True)


# ******************************************    Class Declaration End       ****************************************** #

"""
Author: Yash Bansod
UID: 116776547
E-mail: yashb@umd.edu
Organisation: University of Maryland, College Park
"""