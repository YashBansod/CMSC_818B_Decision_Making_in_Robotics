# !/usr/bin/env python

# ******************************************    Libraries to be imported    ****************************************** #
import tensorflow as tf


# ******************************************    Class Declaration Start     ****************************************** #
class NNModel(object):

    def __init__(self, in_size, out_size, batch_size=256):

        self.batch_size = batch_size

        self.model = tf.keras.Sequential([
            tf.keras.layers.Dense(200, input_shape=(in_size,)),
            tf.keras.layers.LeakyReLU(alpha=0.01),
            tf.keras.layers.Dense(200),
            tf.keras.layers.LeakyReLU(alpha=0.01),
            # tf.keras.layers.Dense(200),
            # tf.keras.layers.LeakyReLU(alpha=0.01),
            # tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(out_size)
        ])

        self.model.compile(optimizer='adam', loss='mean_squared_error')

        self.writer = None

        # log_dir = ".\\logs\\fit\\" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        # self.tb_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir)

    # ******************************        Class Method Declaration        ****************************************** #
    def write_logs(self, mean_cost, max_pos, episode_reward, step):
        if self.writer is None:
            # noinspection PyUnresolvedReferences
            self.writer = tf.summary.create_file_writer(".\\saved_logs\\logs_2\\")

        with self.writer.as_default():
            tf.summary.scalar('ep_mean_cost', mean_cost, step=step)
            tf.summary.scalar('ep_max_pos', max_pos, step=step)
            tf.summary.scalar('ep_reward', episode_reward, step=step)
            self.writer.flush()


# ******************************************    Class Declaration End       ****************************************** #

"""
Author: Yash Bansod
UID: 116776547
E-mail: yashb@umd.edu
Organisation: University of Maryland, College Park
"""
