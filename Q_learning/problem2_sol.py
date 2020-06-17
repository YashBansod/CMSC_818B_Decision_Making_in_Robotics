# !/usr/bin/env python
"""
Solution for Problem 1 of the Assignment.
"""

# ******************************************    Libraries to be imported    ****************************************** #
from __future__ import print_function

import os
import gym
import argparse
import numpy as np

from tqdm import tqdm
from data_store import DataStore
from problem_2_support.nn_model_2 import NNModel
from problem_2_support.game_loop_2 import GameLoop
from problem_2_support.visualize_policy_2 import VisualizePolicy


# ******************************************        Main Program Start      ****************************************** #
def main(args_):

    num_episodes = 600
    env = gym.make('MountainCarContinuous-v0')
    env.seed(4)

    max_ep_reward, max_pos_val = -300, -10

    data_store = DataStore(max_memory=10000)
    nn_model = NNModel(in_size=env.observation_space.shape[0], out_size=21, batch_size=128)
    game_loop = GameLoop(data_store=data_store, nn_model=nn_model, env=env)

    reward_array = np.zeros(num_episodes, dtype=np.float32)

    if args_.test_run:
        nn_model.model.load_weights("./saved_models/unmod_reward_p_2_1.h5")
        episode_cost = game_loop.test_episode(render=args_.display)
        # VisualizePolicy(nn_model=nn_model)
        if args_.debug:
            print("\t Episode reward: %6.3f" % episode_cost)

    else:
        for i in tqdm(range(num_episodes)):
            episode_reward, max_pos, mean_cost = game_loop.train_episode(args_.display)
            reward_array[i] = episode_reward
            nn_model.write_logs(mean_cost, max_pos, episode_reward, i)

            if args_.debug:
                max_ep_reward = max(max_ep_reward, episode_reward)
                max_pos_val = max(max_pos_val, max_pos)
                if i % 10 == 0:
                    print("\t Maximum episode reward: %6.3f,  Max Position Value: %5.2f, Last Mean Cost: %8.6f"
                          % (max_ep_reward, max_pos_val, mean_cost))

        # noinspection PyTypeChecker
        np.savetxt('reward.txt', reward_array, delimiter=',')


# ******************************************        Main Program End        ****************************************** #

if __name__ == '__main__':
    try:
        argparser = argparse.ArgumentParser(description='Gaussian Process Regression on Noisy 1D Sine Wave Data')
        argparser.add_argument('-d', '--display', action='store_true', dest='display', help='display solution plot')
        argparser.add_argument('-v', '--verbose', action='store_true', dest='debug', help='print debug information')
        argparser.add_argument('-m', '--mod_reward', action='store_true', dest='mod_reward', help='modify reward')
        argparser.add_argument('-t', '--test_run', action='store_true', dest='test_run', help='test run the model')
        argparser.add_argument('-g', '--gpu', action='store_true', dest='gpu', help='use gpu for neural network')
        argparser.add_argument('-w', '--write', action='store_true', dest='write', help='write solution file')
        args = argparser.parse_args()

        if not args.gpu:
            os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
            print('\n\tRunning on CPU as per user instruction.\n')
        else:
            print('\n\tRunning on GPU as per user instruction.\n')

        main(args)

    except KeyboardInterrupt:
        print('\nProcess interrupted by user. Bye!')

"""
Author: Yash Bansod
UID: 116776547
E-mail: yashb@umd.edu
Organisation: University of Maryland, College Park
"""
